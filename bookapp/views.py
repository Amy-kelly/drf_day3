from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bookapp.models import Book
from .serializers import BookModelSerializer,BookModelDeSerializer,BookModelSerializerV2

class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("pk")
        if book_id:
            book_obj = Book.objects.filter(pk=book_id).first()
            book_ser = BookModelSerializer(book_obj).data
            return Response({
                "status":status.HTTP_200_OK,
                "msg":"查询单个图书成功",
                "results":book_ser
            })
        else:
            book_list = Book.objects.all()
            book_list_ser = BookModelSerializer(book_list,many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "msg": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self,request,*args,**kwargs):
        book_data = request.data
        book_ser = BookModelDeSerializer(data=book_data)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            "status":status.HTTP_200_OK,
            "msg":"添加图书成功",
            "results":BookModelSerializer(book_obj).data
        })

class BookAPIViewV2(APIView):
    #查询单个，查询所有图书信息
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("pk")
        if book_id:
            book_obj = Book.objects.filter(pk=book_id,is_delete=False)
            book_ser = BookModelSerializerV2(book_obj).data
            return Response({
                "status":status.HTTP_200_OK,
                "msg":"查询单个图书信息",
                "results":book_ser
            })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list,many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "msg": "查询所有图书信息",
                "results": book_list_ser
            })
    #添加单个，添加多个图书信息
    def post(self,request,*args,**kwargs):
        book_data = request.data
        if isinstance(book_data,dict):
            many = False
        elif isinstance(book_data,list):
            many = True
        else:
            return Response({
                "status":status.HTTP_304_NOT_MODIFIED,
                "msg":"参数格式有误"
            })
        book_obj = BookModelSerializerV2(data=book_data,many=many)
        book_obj.is_valid(raise_exception=True)
        book_ser = book_obj.save()
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "添加成功",
            "result":BookModelSerializerV2(book_ser,many=many).data
        })
    #单删，多删
    def delete(self,request,*args,**kwargs):
        book_id = kwargs.get("pk")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        if Book.objects.filter(pk__in=ids,is_delete=False).update(is_delete=True):
            return Response({
                "status":status.HTTP_200_OK,
                "msg":"删除成功"
            })
        return Response({
            "status":status.HTTP_400_BAD_REQUEST,
            "msg":"删除失败或图书不存在"
        })
    #单整体改
    def put(self,request,*args,**kwargs):
        book_id = kwargs.get("pk")
        book_data = request.data
        book_obj = Book.objects.filter(pk=book_id,is_delete=False).first()
        book_ser = BookModelSerializerV2(data=book_data,instance=book_obj)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status":status.HTTP_200_OK,
            "msg":"修改成功",
            "results":BookModelSerializerV2(book_obj).data
        })
    #单局部改
    def patch(self,request,*args,**kwargs):
        book_id = kwargs.get("pk")
        book_data = request.data
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": "该图书不存在",
            })
        book_ser = BookModelSerializerV2(data=book_data,instance=book_obj,partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "修改成功",
            "results": BookModelSerializerV2(book_obj).data
        })



