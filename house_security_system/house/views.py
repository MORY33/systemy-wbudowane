from django.db import transaction
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


# Your code that interacts with the database
# Create your views here.
class TestView(APIView):
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data)
        return Response(request.data)

    def get(self, request):
        print(request.user)
        print(request.user.__dict__)
        return Response("Hello authenticated user")
