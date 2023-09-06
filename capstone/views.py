import io
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.core.files.images import ImageFile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Lower
from .models import User, RecoverUser, UserPlaylist, Album, Song, PlaylistSong, FriendRequest
from .functionUtilities import sendRecoverEmail
import json, random
import re, base64
from django.conf import settings
import os.path

alphabetAndNumbers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
passwordPattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

def view_404(request, exception=None): # pragma: no cover
    return render(request, "capstone/404.html")

def view_500(request, exception=None): # pragma: no cover
    return render(request, "capstone/500.html")

def view_503(request, exception=None): # pragma: no cover
    return render(request, "capstone/503.html")

@login_required(login_url='login')
def index(request):
    return render(request, "capstone/index.html")

def login_view(request): # pragma: no cover
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) 

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Username or password is/are invalid."
            })
    else:
        return render(request, "capstone/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if re.match(passwordPattern, password) is None:
            return render(request, "capstone/register.html", {
                "message": "Password must have a minimum of 8 characters, at least one uppercase character, at least one lowercase character, at least one digit and at least one special character.",
            })

        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            UserPlaylist.objects.create(user=user, name=user.username+"'s Playlist", creationDate=timezone.now())
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
    
def passwordRecover(request):
    if request.method == "POST":
        try:
            recoverText = request.POST["recoverText"]
            users = User.objects.filter(username=recoverText) | User.objects.filter(email=recoverText)
            
            if (len(users) == 1):
                i = 0
                recoverId = ""
                while(i < 20):
                    charIndex = random.randint(0,len(alphabetAndNumbers)-1)
                    recoverId += alphabetAndNumbers[charIndex] 
                    i += 1
                RecoverUser.objects.create(id=recoverId, user=users[0], insertionDate=timezone.now())
                sendRecoverEmail(settings.CREDENTIAL_EMAIL_ADDRESS, users[0].email, "JustBeat - Recover Email", settings.CREDENTIAL_EMAIL_PASSWORD, settings.CREDENTIAL_SMTP, settings.CREDENTIAL_SMTP_PORT, settings.URL_DOMAIN, recoverId)
            return render(request, "capstone/passwordRecover.html", {
                "message": "If your username or email correspond with an existing account, we'll send you an e-mail with password restoration."
            })
        except Exception as exception:
            print("Exception sending the recover email...",exception)
            return render(request, "capstone/passwordRecover.html", {
                "message": "If your username or email correspond with an existing account, we'll send you an e-mail with password restoration."
            })
    else:
        return render(request, "capstone/passwordRecover.html")
    
def createNewPasswordRecover(request):
    try :
        if request.method == "GET":
            recoverId = request.GET["recoverId"]
            recoverUsers = RecoverUser.objects.filter(id = recoverId)
            if (len(recoverUsers) == 1):
                return render(request, "capstone/createNewPasswordRecover.html")
            else:
                return HttpResponseRedirect(reverse("index"))
        
        elif request.method == "POST":
            recoverId = request.POST["recoverId"]
            recoverUsers = RecoverUser.objects.filter(id = recoverId)
            if (len(recoverUsers) == 1):
                user = recoverUsers[0].user
                password = request.POST["password"]
                confirmation = request.POST["confirmation"]
                
                if re.match(passwordPattern, password) is None:
                    return render(request, "capstone/createNewPasswordRecover.html", {
                        "message": "Password must have a minimum of 8 characters, at least one uppercase character, at least one lowercase character, at least one digit and at least one special character.",
                        "recoverId": recoverId
                    })

                if password != confirmation:
                    return render(request, "capstone/createNewPasswordRecover.html", {
                        "message": "Passwords must match.",
                        "recoverId": recoverId
                    })
                
                user.set_password(password)
                user.save()
                recoverUsers[0].delete()
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    return render(request, "capstone/createNewPasswordRecover.html", {
                        "message": "Generic error during login. Please retry.",
                        "recoverId": recoverId
                    })
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "capstone/login.html")
        else:
            return render(request, "capstone/login.html")
    except:
        return render(request, "capstone/login.html")

@login_required(login_url='login')
def userPlaylistLoadSong(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user).first()
            song = Song.objects.filter(id=songId).first()
            playlistSongs = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
            if (len(playlistSongs) == 1):
                filename = settings.BASE_DIR.replace("\\","/")+"/"+song.audioFile.name
                file = open(filename, "rb").read() 
                response = HttpResponse(file, content_type='audio/mp3')
                response['X-Frame-Options'] = 'SAMEORIGIN'
                response['Content-Type'] = 'audio/mp3'
                response['Accept-Ranges'] = 'bytes'
            else:
                return HttpResponseRedirect(reverse("index"))
            return response
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def userFriendPlaylistLoadSong(request, songId, userFriend):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            userFriend = User.objects.get(username=userFriend)
            areFriends = (FriendRequest.objects.filter(userRequestor=user, userAcceptor=userFriend, accepted=2) | FriendRequest.objects.filter(userAcceptor=user, userRequestor=userFriend, accepted=2))
            if (len(areFriends) == 1):
                playlist = UserPlaylist.objects.filter(user=userFriend).first()
                song = Song.objects.filter(id=songId).first()
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
                if (len(playlistSongs) == 1):
                    filename = settings.BASE_DIR.replace("\\","/")+"/"+song.audioFile.name
                    file = open(filename, "rb").read() 
                    response = HttpResponse(file, content_type='audio/mp3')
                    response['X-Frame-Options'] = 'SAMEORIGIN'
                    response['Content-Type'] = 'audio/mp3'
                    response['Accept-Ranges'] = 'bytes'
                else:
                    return HttpResponseRedirect(reverse("index"))
                return response
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def userPlaylistLoadAlbum(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user).first()
            song = Song.objects.filter(id=songId).first()
            playlistSongs = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
            if (len(playlistSongs) == 1):
                filename = settings.BASE_DIR.replace("\\","/")+"/"+song.albumId.image.name
                file = open(filename, "rb").read() 
                response = HttpResponse(file, content_type='image/jpg')
                response['X-Frame-Options'] = 'SAMEORIGIN'
                response['Content-Type'] = 'image/jpg'
            else:
                return HttpResponseRedirect(reverse("index"))
            return response
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def userFriendPlaylistLoadAlbum(request, songId, userFriend):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            userFriend = User.objects.get(username=userFriend)
            areFriends = (FriendRequest.objects.filter(userRequestor=user, userAcceptor=userFriend, accepted=2) | FriendRequest.objects.filter(userAcceptor=user, userRequestor=userFriend, accepted=2))
            if (len(areFriends) == 1):
                playlist = UserPlaylist.objects.filter(user=userFriend).first()
                song = Song.objects.filter(id=songId).first()
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
                if (len(playlistSongs) == 1):
                    filename = settings.BASE_DIR.replace("\\","/")+"/"+song.albumId.image.name
                    file = open(filename, "rb").read() 
                    response = HttpResponse(file, content_type='image/jpg')
                    response['X-Frame-Options'] = 'SAMEORIGIN'
                    response['Content-Type'] = 'image/jpg'
                else:
                    return HttpResponseRedirect(reverse("index"))
                return response
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def userPlaylistSongs(request):
    if request.method == "GET":
        try:
            jsonObjectPlaylist = {}
            jsonArraySongs = []
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist.first()).order_by('playingOrder')
                if (len(playlistSongs) > 0):
                    lastSongPlayed = ""
                    lastSongPlayedSeconds = ""
                    playlist = playlist.first()
                    for playlistSong in playlistSongs:
                        song = Song.objects.filter(id=playlistSong.songId.id).first()
                        album = Album.objects.filter(id=song.albumId.id).first()
                        jsonObjectSong = {}
                        jsonObjectSong['id'] = song.id
                        
                        if (playlist.lastSongPlayedId == song.id):
                            lastSongPlayed = playlistSong.songId.id
                            lastSongPlayedSeconds = playlist.lastSongPlayedSeconds

                        jsonObjectSong['name'] = song.name
                        jsonObjectSong['artist'] = album.artist
                        jsonObjectSong['album'] = album.name
                        jsonObjectSong['url'] = "/userPlaylistLoadSong/"+str(song.id)
                        jsonObjectSong['cover_art_url'] = "/userPlaylistLoadAlbum/"+str(song.id)
                        jsonObjectSong['liked'] = playlistSong.liked
                        jsonArraySongs.append(jsonObjectSong)
                    jsonObjectPlaylist['lastSongPlayed'] = lastSongPlayed
                    jsonObjectPlaylist['lastSongPlayedSeconds'] = lastSongPlayedSeconds
                    jsonObjectPlaylist['repeat'] = playlist.repeat
                    jsonObjectPlaylist['shuffle'] = playlist.shuffle
                    jsonObjectPlaylist['volume'] = playlist.volume
                    json.dumps(jsonArraySongs)
                    json.dumps(jsonObjectPlaylist)
                    return JsonResponse({"status": "OK", "songs":jsonArraySongs, "playlistProperties":jsonObjectPlaylist},status=200)
                else:
                    return JsonResponse({"status": "OK", "songs":"","playlistProperties":""},status=200)
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def userFriendPlaylistSongs(request,usernameFriend):
    if request.method == "GET":
        try:
            jsonObjectPlaylist = {}
            jsonArraySongs = []
            user = User.objects.get(username=request.user.username)
            userFriend = User.objects.get(username=usernameFriend)
            friends = FriendRequest.objects.filter(userRequestor=user, userAcceptor=userFriend, accepted=2) | FriendRequest.objects.filter(userRequestor=userFriend, userAcceptor=user, accepted=2)
            if (len(friends) == 1):
                playlist = UserPlaylist.objects.filter(user=userFriend)
                if (len(playlist) == 1):
                    playlistSongs = PlaylistSong.objects.filter(playlistId=playlist.first()).order_by('playingOrder')
                    if (len(playlistSongs) > 0):
                        playlist = playlist.first()
                        for playlistSong in playlistSongs:
                            song = Song.objects.filter(id=playlistSong.songId.id).first()
                            album = Album.objects.filter(id=song.albumId.id).first()
                            jsonObjectSong = {}
                            jsonObjectSong['id'] = song.id
                            jsonObjectSong['name'] = song.name
                            jsonObjectSong['artist'] = album.artist
                            jsonObjectSong['album'] = album.name
                            jsonObjectSong['url'] = "/userFriendPlaylistLoadSong/"+str(song.id)+"/"+str(userFriend.username)
                            jsonObjectSong['cover_art_url'] = "/userFriendPlaylistLoadAlbum/"+str(song.id)+"/"+str(userFriend.username)
                            jsonArraySongs.append(jsonObjectSong)
                        jsonObjectPlaylist['repeat'] = playlist.repeat
                        jsonObjectPlaylist['shuffle'] = playlist.shuffle
                        json.dumps(jsonArraySongs)
                        json.dumps(jsonObjectPlaylist)
                        return JsonResponse({"status": "OK", "songs":jsonArraySongs, "playlistProperties":jsonObjectPlaylist},status=200)
                    else:
                        return JsonResponse({"status": "OK", "songs":"","playlistProperties":""},status=200)
                else:
                    return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def updatePlaylistSongLike(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                song = Song.objects.filter(id=songId).first()
                playlistSong = PlaylistSong.objects.filter(playlistId=playlist.first(), songId=song).first()
                
                if (playlistSong.liked):
                    playlistSong.liked = False
                    song.likes -= 1
                else:
                    playlistSong.liked = True
                    song.likes += 1
                
                song.save()
                playlistSong.save()
                return JsonResponse({"status": "OK"},status=200)
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
        
@login_required(login_url='login')
def getPlaylistSongLiked(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                song = Song.objects.filter(id=songId).first()
                playlistSong = PlaylistSong.objects.filter(playlistId=playlist.first(), songId=song).first()
                return JsonResponse({"status": "OK","liked": playlistSong.liked},status=200)
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
        
@login_required(login_url='login')
def savePlaylistSongPlayed(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            songId = data.get("songId")
            secondsPlayed = data.get("secondsPlayed")
            repeat = data.get("repeat")
            shuffle = data.get("shuffle")
            volume = data.get("volume")
            if songId is not None and secondsPlayed is not None:
                user = User.objects.get(username=request.user.username)
                song = Song.objects.filter(id=songId)
                playlist = UserPlaylist.objects.filter(user=user)
                if (len(playlist) == 1 and len(song) == 1):
                    playlist = playlist.first()
                    song = song.first()
                    playlistSong = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
                    if (len(playlistSong) == 1):
                        playlist.lastSongPlayedId = songId
                        playlist.lastSongPlayedSeconds = secondsPlayed
                        playlist.repeat = repeat
                        playlist.shuffle = shuffle
                        playlist.volume = volume
                        playlist.save()
                        return JsonResponse({"status": "OK"},status=200)
                    else:
                        return HttpResponseRedirect(reverse("index"))
                else:
                    return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK", "error":"Generic error occurred."},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
            
@login_required(login_url='login')
def searchSongs(request):
    if request.method == "POST":
        try:
            jsonArraySongs = []
            data = json.loads(request.body)
            queryString = data.get("queryString")
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                playlist = playlist.first()
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist).values_list('songId', flat=True).distinct()
                songs = Song.objects.exclude(id__in=playlistSongs).filter(name__icontains=queryString)[:10]
                if (len(songs) > 0):
                    for song in songs:
                        jsonObjectSong = {}
                        jsonObjectSong['id'] = song.id
                        jsonObjectSong['songName'] = song.name
                        jsonObjectSong['albumName'] = song.albumId.name
                        jsonArraySongs.append(jsonObjectSong)
                else:
                    albums = Album.objects.filter(name__icontains=queryString)
                    songs = Song.objects.exclude(id__in=playlistSongs).filter(albumId__in=albums)[:10]
                
                    if (len(songs) > 0):
                        for song in songs:
                            jsonObjectSong = {}
                            jsonObjectSong['id'] = song.id
                            jsonObjectSong['songName'] = song.name
                            jsonObjectSong['albumName'] = song.albumId.name
                            jsonArraySongs.append(jsonObjectSong)
                    
                return JsonResponse({"status": "OK","songs":jsonArraySongs},status=200)
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def addPlaylistSong(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                jsonObjectSong = {}
                song = Song.objects.filter(id=songId).first()
                playlist = playlist.first()
                album = song.albumId
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist, songId=song)
                if (len(playlistSongs) == 0):
                    playlistSongs = PlaylistSong.objects.all().order_by('-playingOrder')[:1]
                    if (len(playlistSongs) == 0):
                        playingOrder = 1
                    else:
                        playingOrder = playlistSongs.first().playingOrder+1
                    PlaylistSong.objects.create(songId=song,playlistId=playlist,playingOrder=playingOrder)
                    jsonObjectSong['id'] = song.id
                    jsonObjectSong['name'] = song.name
                    jsonObjectSong['artist'] = album.artist
                    jsonObjectSong['album'] = album.name
                    jsonObjectSong['url'] = "/userPlaylistLoadSong/"+str(song.id)
                    jsonObjectSong['cover_art_url'] = "/userPlaylistLoadAlbum/"+str(song.id)
                    jsonObjectSong['liked'] = False
                    json.dumps(jsonObjectSong)
                return JsonResponse({"status": "OK","song":jsonObjectSong},status=200)
            else:
                return JsonResponse({"status": "NOK"},status=500)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
        
@login_required(login_url='login')
def removePlaylistSong(request, songId):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                song = Song.objects.filter(id=songId).first()
                playlist = playlist.first()
                playlistSongs = PlaylistSong.objects.filter(playlistId=playlist,songId=song)
                if (len(playlistSongs) == 1):
                    playlistSongRemoved = playlistSongs.first()
                    playlistSongs.delete()
                    if (playlistSongRemoved.liked):
                        song.likes -= 1
                        song.save()
                    playlistSongs = PlaylistSong.objects.filter(playlistId=playlist).order_by('-playingOrder')
                    
                    if (len(playlistSongs) > 0):
                        for playlistSong in playlistSongs:
                            if playlistSong.playingOrder > playlistSongRemoved.playingOrder:
                                playlistSong.playingOrder -= 1
                            playlistSong.save()
                    else: 
                        playlist.lastSongPlayedId = 0
                        playlist.lastSongPlayedSeconds = 0
                        playlist.save()
                    return JsonResponse({"status": "OK"},status=200)
                else:
                    return JsonResponse({"status": "NOK"},status=500)
            else:
                return JsonResponse({"status": "NOK"},status=500)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def profile(request):
    if request.method == "GET":
        try:
            profile = {}
            user = User.objects.get(username=request.user.username)
            playlist = UserPlaylist.objects.filter(user=user)
            if (len(playlist) == 1):
                playlist = playlist.first()
                profile['username'] = user.username
                profile['email'] = user.email
                if os.path.exists(playlist.profileImage.name):
                    with open(playlist.profileImage.name, "rb") as file:
                        profileImageBase64 = base64.b64encode(file.read())
                else:
                    with open("capstone/profileImages/NoImage.jpg", "rb") as file:
                        profileImageBase64 = base64.b64encode(file.read())
                profile['profileImage'] = "data:image/jpeg;base64,"+profileImageBase64.decode()
                friends = FriendRequest.objects.filter(userRequestor=user, accepted=2) | FriendRequest.objects.filter(userAcceptor=user, accepted=2)
                profile['numberFriends'] = len(friends)
                return render(request, "capstone/profile.html", {
                    "profile": profile
                })
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def profileChangePassword(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            password = data.get("password")
            confirmation = data.get("confirmation")
            user = User.objects.get(username=request.user.username)
            
            if re.match(passwordPattern, password) is None:
                return JsonResponse({"status": "NOK", "error":"Password must have a minimum of 8 characters, at least one uppercase character, at least one lowercase character, at least one digit and at least one special character."},status=500)

            if password != confirmation:
                return JsonResponse({"status": "NOK", "error":"Passwords must match."},status=500)
                    
            user.set_password(password)
            user.save()
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
            return JsonResponse({"status": "OK"},status=200)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return JsonResponse({"status": "NOK"},status=500)

@login_required(login_url='login')
def uploadNewProfileImage(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            imageName = data.get("imageName")
            size = data.get("size")
            base64String = data.get("base64String")
            if (imageName != None):
                extensionIndex = imageName.rfind(".jpeg")
                if (extensionIndex == -1):
                    extensionIndex = imageName.rfind(".jpg")
                    if (extensionIndex == -1):
                        return JsonResponse({"status": "NOK", "error":"The image must have one of these extensions: jpg/jpeg."},status=500)
                
                if (size > 1000000 or len(base64String) > 1048576):
                    return JsonResponse({"status": "NOK", "error":"The maximum size of the image must be 1 MB."},status=500)

                user = User.objects.get(username=request.user.username)
                playlist = UserPlaylist.objects.filter(user=user)
                if (len(playlist) == 1):
                    playlist = playlist.first()
                    streamImage = io.BytesIO(base64.decodebytes(bytes(base64String, "utf-8")))
                    profileImage = ImageFile(streamImage, name=imageName)
                    playlist.profileImage = profileImage
                    playlist.save()
                    return JsonResponse({"status": "OK"},status=200)
                else:
                    return JsonResponse({"status": "NOK", "error":"The name of image is empty."},status=500)
            else:
                return JsonResponse({"status": "NOK", "error":"The name of image is empty."},status=500)
        except:
            return JsonResponse({"status": "NOK","error":"Generic error occurred. Please retry."},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def showFriendsUser(request,pageNumber=1):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            friends = (FriendRequest.objects.filter(userRequestor=user, accepted=2) | FriendRequest.objects.filter(userAcceptor=user, accepted=2)).order_by('id')
            paginator = Paginator(friends, 50)
            pageFriends = paginator.get_page(pageNumber)
            friendsArray = []
            for friend in pageFriends:
                friendObject = {}
                if friend.userAcceptor != user:
                    friendUser = friend.userAcceptor
                else:
                    friendUser = friend.userRequestor
                    
                friendObject['username'] = friendUser.username
                friendObject['email'] = friendUser.email
                playlist = UserPlaylist.objects.filter(user=friendUser)
                if (len(playlist) == 1):
                    playlist = playlist.first()
                    if os.path.exists(playlist.profileImage.name):
                        with open(playlist.profileImage.name, "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    else:
                        with open("capstone/profileImages/NoImage.jpg", "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    friendObject['profileImage'] = "data:image/jpeg;base64,"+profileImageBase64.decode()
                friendsArray.append(friendObject)
            return JsonResponse({"status": "OK","numberFriends":len(friendsArray),
                "friends":friendsArray,
                "paginatorCount":pageFriends.paginator.count,
                "paginatorNumberPage":pageFriends.number,
                "paginatorPerPage":pageFriends.paginator.per_page
            },status=200)
        except:
            return JsonResponse({"status": "NOK","error":"Generic error occurred. Please retry."},status=500)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')  
def showFriendPlaylist(request,usernameFriend):
    if request.method == "GET":
        return render(request, "capstone/friendPlaylist.html",{
            "usernameFriend":usernameFriend
        })
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')  
def friends(request):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            friendRequests = FriendRequest.objects.filter(userAcceptor=user, accepted=1)
            friendRequestsLength = len(friendRequests)
            if (friendRequestsLength >= 100):
                friendRequestsLength = '99+'
            return render(request, "capstone/friends.html", {
                "friendRequestsLength":friendRequestsLength
            })
        except:
            return render(request, "capstone/friends.html", {
                "friendRequestsLength":0
            })
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')  
def friendsJson(request):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            friendRequests = FriendRequest.objects.filter(userAcceptor=user, accepted=1)
            friendRequestsLength = len(friendRequests)
            if (friendRequestsLength >= 100):
                friendRequestsLength = '99+'
            return JsonResponse({"status": "OK","friendRequestsLength":friendRequestsLength})
        except:
            return JsonResponse({"status": "NOK"}, status=500)
    else:
        return JsonResponse({"status": "NOK"}, status=500)
    
@login_required(login_url='login')  
def searchFriends(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
            data = json.loads(request.body)
            pageNumber = data.get("pageNumber")
            queryString = data.get("queryString")
            usersQueryString = (User.objects.filter(username__icontains=queryString) | User.objects.filter(email__icontains=queryString)).exclude(username=user.username).order_by(Lower('username'))
            paginator = Paginator(usersQueryString, 50)
            usersQueryString = paginator.get_page(pageNumber)
            userRequestorFriendRequests = (FriendRequest.objects.filter(userRequestor=user, userAcceptor__in=usersQueryString))
            userAcceptorFriendRequests = (FriendRequest.objects.filter(userAcceptor=user, userRequestor__in=usersQueryString))
            friendsArray = []
            for userQueryString in usersQueryString:
                friendObject = {}
                friendUser = None
                for userRequestorFriendRequest in userRequestorFriendRequests:
                    if userQueryString == userRequestorFriendRequest.userAcceptor:
                        friendUser = userRequestorFriendRequest.userAcceptor
                        friendObject['accepted'] = userRequestorFriendRequest.accepted
                
                for userAcceptorFriendRequest in userAcceptorFriendRequests:
                    if userQueryString == userAcceptorFriendRequest.userRequestor:
                        friendUser = userAcceptorFriendRequest.userRequestor
                        friendObject['accepted'] = userAcceptorFriendRequest.accepted
                        friendObject['acceptor'] = True

                if (friendUser == None):
                    friendUser = userQueryString
                    friendObject['accepted'] = 0
                friendObject['username'] = friendUser.username
                friendObject['email'] = friendUser.email
                playlist = UserPlaylist.objects.filter(user=friendUser)
                if (len(playlist) == 1):
                    playlist = playlist.first()
                    if os.path.exists(playlist.profileImage.name):
                        with open(playlist.profileImage.name, "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    else:
                        with open("capstone/profileImages/NoImage.jpg", "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    friendObject['profileImage'] = "data:image/jpeg;base64,"+profileImageBase64.decode()
                friendsArray.append(friendObject)
            return JsonResponse({"status": "OK","friends":json.dumps(friendsArray),
                "paginatorCount":usersQueryString.paginator.count,
                "paginatorNumberPage":usersQueryString.number,
                "paginatorPerPage":usersQueryString.paginator.per_page
            },status=200)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return JsonResponse({"status": "NOK"},status=500)
    
@login_required(login_url='login')  
def addAsFriend(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
            data = json.loads(request.body)
            usernameFriend = data.get("usernameFriend")
            if (usernameFriend != user.username):
                userFriend = User.objects.get(username=usernameFriend)
                friendRequests = FriendRequest.objects.filter(userRequestor=user, userAcceptor=userFriend) | FriendRequest.objects.filter(userAcceptor=user, userRequestor=userFriend)
                if (len(friendRequests) == 0):
                    FriendRequest.objects.create(userRequestor=user, userAcceptor=userFriend, accepted=1, insertionDate=timezone.now())
                    return JsonResponse({"status": "OK","removeFriend":False},status=200)
                elif (len(friendRequests) == 1):
                    friendRequest = friendRequests.first()
                    friendRequest.accepted = 2
                    friendRequest.save()
                    return JsonResponse({"status": "OK","removeFriend":True},status=200)
                else:
                    return JsonResponse({"status": "NOK"},status=500)
            else:
                return JsonResponse({"status": "NOK"},status=500)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return JsonResponse({"status": "NOK"},status=500)
    
@login_required(login_url='login')  
def removeAsFriend(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
            data = json.loads(request.body)
            usernameFriend = data.get("usernameFriend")
            if (usernameFriend != user.username):
                userFriend = User.objects.get(username=usernameFriend)
                friendRequests = FriendRequest.objects.filter(userRequestor=user, userAcceptor=userFriend) | FriendRequest.objects.filter(userAcceptor=user, userRequestor=userFriend)
                if (len(friendRequests) > 0):
                    friendRequests.delete()
                    return JsonResponse({"status": "OK"},status=200)
                else:
                    return JsonResponse({"status": "OK"},status=200)
            else:
                return JsonResponse({"status": "NOK"},status=500)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return JsonResponse({"status": "NOK"},status=500)
    
@login_required(login_url='login')  
def showFriendRequests(request, pageNumber=1):
    if request.method == "GET":
        try:
            user = User.objects.get(username=request.user.username)
            friends = (FriendRequest.objects.filter(userAcceptor=user, accepted=1)).order_by('id')
            paginator = Paginator(friends, 50)
            pageFriendRequests = paginator.get_page(pageNumber)
            friendRequestsArray = []
            for friend in pageFriendRequests:
                friendObject = {}
                friendUser = friend.userRequestor    
                friendObject['username'] = friendUser.username
                friendObject['email'] = friendUser.email
                playlist = UserPlaylist.objects.filter(user=friendUser)
                if (len(playlist) == 1):
                    playlist = playlist.first()
                    if os.path.exists(playlist.profileImage.name):
                        with open(playlist.profileImage.name, "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    else:
                        with open("capstone/profileImages/NoImage.jpg", "rb") as file:
                            profileImageBase64 = base64.b64encode(file.read())
                    friendObject['profileImage'] = "data:image/jpeg;base64,"+profileImageBase64.decode()
                friendRequestsArray.append(friendObject)
            return JsonResponse({"status": "OK", "friendRequests":friendRequestsArray,
                "paginatorCount":pageFriendRequests.paginator.count,
                "paginatorNumberPage":pageFriendRequests.number,
                "paginatorPerPage":pageFriendRequests.paginator.per_page
            },status=200)
        except:
            return JsonResponse({"status": "NOK"},status=500)
    else:
        return JsonResponse({"status": "NOK"},status=500)