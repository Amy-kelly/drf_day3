from django.db import models

# Create your models here.
from drf_day3 import settings


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Press(BaseModel):
    press_name = models.CharField(max_length=64)
    pic = models.ImageField(upload_to="pic",default="pic/1.jpg")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "drf_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name

    def get_pic(self):
        return "%s%s%s" % ("http://127.0.0.1:8000",settings.MEDIA_URL,str(self.pic))

class Author(BaseModel):
    author_name = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        db_table = "drf_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name="detail")
    class Meta:
        db_table = "drf_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name

class Book(BaseModel):
    book_name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    pic = models.ImageField(upload_to="pic",default="pic/1.jpg")
    publish = models.ForeignKey(to="Press",on_delete=models.CASCADE,db_constraint=False,related_name="books")
    authors = models.ManyToManyField(to="Author",db_constraint=False,related_name="books")
    class Meta:
        db_table = "drf_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name
    #自定义字段，作为类属性
    @property
    def publish_name(self):
        return self.publish.press_name

    @property
    def author_info(self):
        return self.authors.values("author_name","age","detail__phone")

    def publish_address(self):
        return self.publish.address

    def get_pic(self):
        return "%s%s%s" % ("http://127.0.0.1:8000",settings.MEDIA_URL,str(self.pic))