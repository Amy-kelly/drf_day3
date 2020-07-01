from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.response import Response
from utils.response import APIResponse
from bookapp.models import Book
from .models import User
from .serializers import BookModelSerializer,UserModelSerializer
from rest_framework import generics, status
from rest_framework import viewsets
# Create your views here.
class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    queryset = Book.objects.filter(is_delete=False).all()
    serializer_class = BookModelSerializer
    def get(self,request,*args,**kwargs):
        if kwargs.get("pk"):
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

class UserGenericViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_delete=False)
    serializer_class = UserModelSerializer

    def register(self,request,*args,**kwargs):
        response = self.create(request,*args,**kwargs)
        if response:
            return APIResponse(status.HTTP_200_OK,"注册成功",results=response.data)
        return APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "注册失败")

    def login(self,request,*args,**kwargs):
        username = request.data.get("username")
        pwd = request.data.get("password")
        user_obj = User.objects.filter(username=username,password=pwd).first()
        if user_obj:
            return APIResponse(status.HTTP_200_OK,"登陆成功",results=UserModelSerializer(user_obj).data)
        return APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,"登陆失败")




