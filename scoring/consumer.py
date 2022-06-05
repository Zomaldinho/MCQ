import sys
import os
import django

sys.path.append('../mcq')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcq.settings')
django.setup()
import pickle
from kafka import KafkaConsumer
from django.db.models import F
from api.models.scores import Scores

while True:   
    consumer = KafkaConsumer('mcq', 
        bootstrap_servers=['127.0.0.1:9092'], 
        api_version=(0, 10) 
        # ,consumer_timeout_ms=1000
    )

    for message in consumer:
        deserialized_data = pickle.loads(message.value)
        print(deserialized_data)
        student_id = deserialized_data.get('student_id')
        topic_id = deserialized_data.get('topic_id')
        is_correct_answer = deserialized_data.get('is_correct_answer')
        score = Scores.objects.get_or_create(student_id=student_id, topic_id=topic_id, defaults={'score': 0})
        if is_correct_answer:
           Scores.objects.filter(student=student_id, topic=topic_id).update(score=F('score')+1) 
