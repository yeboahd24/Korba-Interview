from rest_framework import permissions, status, generics
from rest_framework.response import Response
import requests

from .serializers import TodoSerializer, UserSerializer

from .models import TodoList
from django.contrib.auth.models import User


CREATE_ENDPOINT = 'https://jsonplaceholder.typicode.com/posts'
LIST_ENDPOINT = 'https://jsonplaceholder.typicode.com/posts'
UPDATE_ENDPOINT = 'https://jsonplaceholder.typicode.com/posts/{}'
DELETE_ENDPOINT = 'https://jsonplaceholder.typicode.com/posts/{}'


class TodoListCreateView(generics.CreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(userid=self.request.user.id)
        # serializer.save(userid=1)

        # get the title of the request
        title = serializer.validated_data['title']
        # get the body of the request
        body = serializer.validated_data['body']
        # get the userid of the request
        userid = self.request.user.id
        # userid = 1
        # create a new todo to CREATE_ENDPOINT
        response = requests.post(CREATE_ENDPOINT, data={
            'title': title,
            'body': body,
            'userid': userid
        })

        # if the response is not 201
        if response.status_code != 201:
            # return the response
            return response

        # get the response data
        data = response.json()
        # create a new todo
        todo = TodoList.objects.create(
            title=data['title'],
            body=data['body'],
            userid=userid
        )
        # return the todo
        return todo
        




class TodoListView(generics.ListAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # get all the todos
        todos = TodoList.objects.all()
        # create a serializer for the todos
        serializer = TodoSerializer(todos, many=True)
        # return the serializer data
        response = requests.get(LIST_ENDPOINT)
        print(response.json())
        return Response(serializer.data, status=status.HTTP_200_OK)



class TodoUpdateView(generics.UpdateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        # get the todo
        todo = TodoList.objects.get(id=pk)
        # create a serializer for the todo
        serializer = TodoSerializer(todo, data=request.data)
        # if the serializer is valid
        if serializer.is_valid():
            # save the serializer
            serializer.save()
            # return the serializer data
            response = requests.put(UPDATE_ENDPOINT.format(pk), data={
                'title': serializer.validated_data['title'],
                'body': serializer.validated_data['body'],
                'userid': serializer.validated_data['userid']
            })
            print(response.json())
            return Response(serializer.data, status=status.HTTP_200_OK)
        # return the serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoDeleteView(generics.DestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        # get the todo
        todo = TodoList.objects.get(id=pk)
        # delete the todo
        todo.delete()
        # return the response
        # return Response(status=status.HTTP_204_NO_CONTENT)
        response = requests.delete(DELETE_ENDPOINT.format(pk))
        print(response.json())
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()