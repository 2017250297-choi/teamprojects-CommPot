
#api/posts/{id} urls
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='post'),
    path('api/posts/<int:id>',views.posting_detail,name = 'detail-posting'),
    path('api/posts/delete/<int:id>',views.delete_posting,name = 'delete-posting'),
    path('api/posts/comment/<int:id>',views.write_comment,name = 'write-comment'),
    path('api/posts/comment/delete/<int:id>',views.delete_comment,name = 'delete-comment'),
]