from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PersonSerializer
from .models import Person, Status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .exceptions import UserAlreadyDeleted
from utils.kafka_utils import KProducer

# Create your views here.

producer = KProducer()


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def list(self, request):
        all_users = self.queryset.exclude(status=Status.deleted())
        serializer = PersonSerializer(all_users, many=True)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            user_obj = self.get_object()
            if user_obj.status == Status.deleted():
                raise UserAlreadyDeleted({"message : User All ready deleted"})
        except Person.DoesNotExist:
            return Response({"message : User Does Not Exists"})
        except UserAlreadyDeleted as e:
            return Response({"message : User already soft deleted"})
        print(user_obj)
        user_obj.status = Status.deleted()
        user_obj.save()
        return Response({"message": "user is soft deleted"})

    @action(detail=False, methods=["GET"], url_path="deleted-users")
    def deleted_users(self, request):
        deleted_users = self.queryset.filter(status=Status.deleted())
        serializer = self.serializer_class(deleted_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("sending data to kafka topic also...")
            producer.produce("TutorialTopic", serializer.data)
        return Response({"message : user is created and details sent to kafka topic"})
