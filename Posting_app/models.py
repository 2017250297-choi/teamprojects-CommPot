
# tweet/models.py
from django.db import models

from User_app.models import UserModel


# Create your models here.


class Posting(models.Model):
    class Meta:
        db_table = "posting"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,verbose_name='글 제목')
    content = models.CharField(max_length=10000000,verbose_name='글 내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostingComment(models.Model):
    class Meta:
        db_table = "comment"
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
