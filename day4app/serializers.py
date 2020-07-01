from rest_framework import serializers, exceptions

from bookapp.models import Book
from day4app.models import User


class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(instance) #要修改的对象实例
        print(validated_data) #接收的数据
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance
#book类的序列化器
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","publish","authors","pic")
        list_serializer_class = BookListSerializer
        #通过校验规则指定哪些是参与序列化，哪些是参与反序列化的，如果没有指定，则都参与
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 2,
                "max_length": 8,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名不能低于2个字符",
                    "max_length": "图书名不能超过8个字符"
                }
            },
            #write_only:只参与反序列化的字段
            "publish":{
                "write_only":True
            },
            "authors":{
                "write_only":True
            },
            #read_only：只参与序列化的字段
            "pic":{
                "read_only":True
            }
        }

        # 局部钩子
        def validate_book_name(self, value):
            if "1" in value:
                raise exceptions.ValidationError("图书名不符合规范")
            return value

        # 全局钩子
        def validate(self, attrs):
            price = attrs.get("price", 0)
            if price > 100:
                raise exceptions.ValidationError("图书价格过高，请重新定价")
            return attrs

#user类的序列化器
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "phone", "gender")
        # 通过校验规则指定哪些是参与序列化，哪些是参与反序列化的，如果没有指定，则都参与
        extra_kwargs = {
            "username": {
                "required": True,
                "min_length": 2,
                "max_length": 8,
                "error_messages": {
                    "required": "用户名是必填的",
                    "min_length": "用户名不能低于2个字符",
                    "max_length": "用户名不能超过8个字符"
                }
            },
            # write_only:只参与反序列化的字段
            "phone": {
                "write_only": True
            },
            "gender": {
                "write_only": True
            },
            # # read_only：只参与序列化的字段
            # "password": {
            #     "read_only": True
            # }
        }

        # 局部钩子
        def validate_username(self, value):
            if "1" in value:
                raise exceptions.ValidationError("用户名不符合规范")
            return value

        # 全局钩子
        # def validate(self, attrs):
        #     price = attrs.get("price", 0)
        #     if price > 100:
        #         raise exceptions.ValidationError("图书价格过高，请重新定价")
        #     return attrs

