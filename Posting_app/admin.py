from django.contrib import admin


from .models import Posting, PostingComment, PostingImage
# Register your models here.
admin.site.register(PostingComment)
admin.site.register(Posting)

admin.site.register(PostingImage)
