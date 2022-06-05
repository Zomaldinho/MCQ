from rest_framework import viewsets, exceptions, response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from api.models.scores import Scores
from api.serializers import ScoresSerializer


class ScoresViewSet(viewsets.GenericViewSet):
    queryset = Scores.objects.all()
    serializer_class = ScoresSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(method='get', manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, 'student id', type=openapi.TYPE_INTEGER),
        openapi.Parameter('topic_id', openapi.IN_QUERY, 'topic id', type=openapi.TYPE_INTEGER),
        ])
    @action(detail=False, methods=['GET'], url_path='student', url_name='student')
    def get_student_score_in_topic(self, request, *args, **kwargs):
        try:
            result = Scores.objects.get(student_id=request.query_params.get(
                'student_id'), topic_id=request.query_params.get('topic_id'))
        except Scores.DoesNotExist:
            raise exceptions.NotFound()
        serializer = ScoresSerializer(instance=result)
        return response.Response(serializer.data)

    @swagger_auto_schema(method='get', manual_parameters=[
        openapi.Parameter('topic_id', openapi.IN_QUERY, 'topic id', type=openapi.TYPE_INTEGER),
        ])
    @action(detail=False, methods=['GET'], url_path='average/topic', url_name='average/topic')
    def get_average_score_of_topic(self, request, *args, **kwargs):
        try:
            result = Scores.objects.filter(
                topic_id=request.query_params.get('topic_id'))
            total_score = 0
            for score in result:
                total_score += score.score
        except Scores.DoesNotExist:
            raise exceptions.NotFound
        return response.Response({"average_score": total_score / len(result)})

    @swagger_auto_schema(method='get', manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, 'student id', type=openapi.TYPE_INTEGER),
        ])
    @action(detail=False, methods=['GET'], url_path='average/student', url_name='average/student')
    def get_average_score_of_student(self, request, *args, **kwargs):
        try:
            result = Scores.objects.filter(
                student_id=request.query_params.get('student_id'))
            total_score = 0
            for score in result:
                total_score += score.score
        except Scores.DoesNotExist:
            raise exceptions.NotFound
        return response.Response({"average_score": total_score / len(result)})

    @swagger_auto_schema(method='get', manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, 'student id', type=openapi.TYPE_INTEGER),
        ])
    @action(detail=False, methods=['GET'], url_path='max/topic', url_name='max/topic')
    def get_max_score_of_topic(self, request, *args, **kwargs):
        try:
            result = Scores.objects.filter(
                topic_id=request.query_params.get('topic_id')).order_by('score').last()
        except Scores.DoesNotExist:
            raise exceptions.NotFound
        return response.Response({"max_score": result.score})
