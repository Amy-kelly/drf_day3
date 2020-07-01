from rest_framework import serializers, exceptions
from bookapp.models import Book,Press

#序列化器嵌套：主表嵌套在从表
class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name","get_pic","address")

#序列化器
class BookModelSerializer(serializers.ModelSerializer):
    #与图书表中的外键字段保持一致
    publish = PressModelSerializer()
    class Meta:
        model = Book
        #查询指定字段
        # fields = ("book_name","price","publish_name","author_info","publish_address")
        fields = ("book_name","price","publish","author_info","get_pic")

        #查询所有字段
        # fields = "__all__"
        #指定哪些字段不展示
        # exclude = ("is_delete","create_time","status")
        #指定查询深度（关联表）(上面三个任意一个字段的展示方式+深度查询)
        # depth = 1

        #自定义字段:可以和serializer一样（不推荐）
                 # 推荐在model类中使用

#反序列化器
class BookModelDeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","publish","authors")

    #添加校验规则
    extra_kwargs = {
        "book_name":{
            "required":True,
            "min_length":2,
            "max_length":8,
            "error_messages":{
                "required":"图书名是必填的",
                "min_length":"图书名不能低于2个字符",
                "max_length":"图书名不能超过8个字符"
            }
        },
        "price":{
            "max_digits":5,
            "decimal_places":2
        }
    }
    #局部钩子
    def validate_book_name(self,value):
        if "1" in value:
            raise exceptions.ValidationError("图书名不符合规范")
        return value

    #全局钩子
    def validate(self, attrs):
        price = attrs.get("price",0)
        if price > 100:
            raise exceptions.ValidationError("图书价格过高，请重新定价")
        return attrs


class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(instance) #要修改的对象实例
        print(validated_data) #接收的数据
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

#序列化器反序列化器整合
class BookModelSerializerV2(serializers.ModelSerializer):
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

