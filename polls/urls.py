from django.urls import path

from .views import *

app_name = 'polls'
urlpatterns = [
    path("nickname/", CustomerCV.as_view(), name="nickname"),
    path("<int:nickname_id>/cate/", CateLV.as_view(), name="cate"),
    path("<int:nickname_id>/cate/<int:pk>/", MenuDV.as_view(), name="menu"),
    path("result/", ResultDV.as_view(), name="result"),
    path("<int:nickname_id>/cate/<int:pk>/choosing/", choose, name="choosing"),


]