from django.urls import path

from day4app import views

urlpatterns = [
    path("books/",views.BookGenericAPIView.as_view()),
    path("books/<str:pk>/",views.BookGenericAPIView.as_view()),
    path("list/", views.BookListAPIView.as_view()),
    path("list/<str:pk>/", views.BookListAPIView.as_view()),
    path("login/", views.UserGenericViewSet.as_view({"post":"login"})),
    path("register/", views.UserGenericViewSet.as_view({"post":"register"})),
    path("set/<str:pk>/", views.UserGenericViewSet.as_view({"post":"login"})),
]