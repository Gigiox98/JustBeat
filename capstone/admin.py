from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.UserPlaylist)
admin.site.register(models.Album)
admin.site.register(models.PlaylistSong)
admin.site.register(models.Song)
admin.site.register(models.FriendRequest)
