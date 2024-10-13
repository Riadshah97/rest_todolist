from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.
class TodoListCreate(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetail(APIView):
    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
