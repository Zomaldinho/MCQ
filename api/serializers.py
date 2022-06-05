from dataclasses import fields
from rest_framework import serializers
from api.models.questions import Questions
from api.models.students import Students
from api.models.topics import Topics
from api.models.choices import Choices
from api.models.scores import Scores

class ChoicesSerializer(serializers.ModelSerializer):
    is_answer = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Choices
        fields = '__all__'
  
class QuestionChoicesSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True)
    class Meta:
        model = Questions
        fields = '__all__'
  
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
        
class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'
              
class ScoresSerializer(serializers.ModelSerializer):
    student = StudentsSerializer()
    topic = TopicSerializer()
    class Meta:
        model = Scores
        fields = '__all__'