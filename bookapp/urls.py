from django.urls import path

from bookapp import views

urlpatterns = [
    path("books/",views.BookAPIView.as_view()),
    path("books/<str:pk>/",views.BookAPIView.as_view()),
    path("books_v2/",views.BookAPIViewV2.as_view()),
    path("books_v2/<str:pk>/",views.BookAPIViewV2.as_view()),

]