from django.contrib import admin

from .models import Post, Group, Comment, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author') 
    search_fields = ('text',) 
    list_filter = ('pub_date',) 
    empty_value_display = '-пусто-'

class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'text', 'author', 'created')
    search_fields = ('post', 'author')
    list_filter = ('post',)
    empty_value_display = '-пусто-'

class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'

admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)