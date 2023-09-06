from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class User(AbstractUser):
    pass

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): # pragma: no cover
    if created and instance.is_superuser:
        UserPlaylist.objects.create(user=instance, name=instance.username+"'s Playlist", creationDate=timezone.now())

class RecoverUser(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insertionDate = models.DateTimeField()

class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    artist = models.CharField(max_length=150)
    image = models.ImageField(upload_to ='capstone/albumImages/')

class Song(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    albumId = models.ForeignKey(Album, on_delete=models.CASCADE)
    audioFile = models.FileField(upload_to = 'capstone/audioFiles/')
    likes = models.BigIntegerField(default=0)

class UserPlaylist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField()
    profileImage = models.ImageField(upload_to = 'capstone/profileImages/', default="capstone/profileImages/NoImage.jpg")
    lastSongPlayedId = models.BigIntegerField(default=0)
    lastSongPlayedSeconds = models.IntegerField(default=0)
    repeat = models.BooleanField(default=True)
    shuffle = models.BooleanField(default=False)
    volume = models.IntegerField(default=50)

class PlaylistSong(models.Model):
    id = models.BigAutoField(primary_key=True)
    songId = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlistId = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE)
    playingOrder = models.IntegerField()
    liked = models.BooleanField(default=False)

class FriendRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    userRequestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userRequestor')
    userAcceptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userAcceptor')
    insertionDate = models.DateTimeField()
    accepted = models.SmallIntegerField()