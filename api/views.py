from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from kafka import KafkaProducer
import pickle
from operator import attrgetter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication

from api.models.choices import Choices
from .models.topics import Topics
from .models.students import Students
from .models.questions import Questions
from .serializers import TopicSerializer, StudentsSerializer, QuestionSerializer, QuestionChoicesSerializer, ChoicesSerializer


class TopicsViewSet(ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


class StudentsViewSet(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


class QuestionsViewSet(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionChoicesSerializer

    def create(self, request, *args, **kwargs):
        questionSerializer = QuestionSerializer(data=request.data)
        questionSerializer.is_valid(raise_exception=True)
        question = questionSerializer.save()
        for choice in request.data.get('choices'):
            choice['question'] = question.id
            choicesSerializer = ChoicesSerializer(data=choice)
            choicesSerializer.is_valid(raise_exception=True)
            choicesSerializer.save()

        headers = self.get_success_headers(questionSerializer.data)
        return Response(questionSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        for choice in request.data.get('choices'):
            choiceInstance = Choices.objects.get(pk=choice.get('id'))
            choiceSerializer = ChoicesSerializer(choiceInstance, choice, partial=partial)
            choiceSerializer.is_valid(raise_exception=True)
            self.perform_update(choiceSerializer)
        instance = self.get_object()
        print(instance)
        questionSerializer = QuestionSerializer(instance, data=request.data, partial=partial)
        questionSerializer.is_valid(raise_exception=True)
        self.perform_update(questionSerializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(questionSerializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='student phone number'),
            'topic': openapi.Schema(type=openapi.TYPE_STRING, description='topic name'),
        }))
@api_view(['POST'])
def enroll_topic(request, *args, **kwargs):
    get_object_or_404(Students, phone_number=request.data.get('phone_number'))
    topic = get_object_or_404(Topics, name=request.data.get('topic'))
    questions = Questions.objects.filter(topic=topic.id)
    serializer = QuestionChoicesSerializer("json", questions, many=True)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='question id'),
            'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='student id'),
            'topic_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='topic id'),
            'choice_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='choice id'),
        }))
@api_view(['POST'])
def evaluate_answers(request, *args, **kwargs):
    question_id, student_id, topic_id, choice_id = attrgetter(
        'question_id', 'student_id', 'topic_id', 'choice_id')(request.data)
    choice = Choices.objects.get(
        pk=choice_id) if choice_id is not None else None
    is_correct_answer = choice.is_answer if choice_id is not None else False
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
    data = {"question_id": question_id, "student_id": student_id,
            "topic_id": topic_id, "is_correct_answer": is_correct_answer}
    data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    producer.send('mcq', data)
    return Response({"message": "answer evaluated successfully"})
