from django.test import Client,TestCase
from django.core.files import File
from django.utils import timezone
import os,json
from .models import User, RecoverUser, UserPlaylist, Album, Song, PlaylistSong,FriendRequest

# Create your tests here.
class CapstoneTest(TestCase): # pragma: no cover

    def setUp(self):
        User.objects.create(username="test0", email="test0.test0@test0.it", password="test123")
        user1=User.objects.create(username="test1", email="test1.test1@test1.it", password="test123")
        User.objects.create(username="test2", email="test2.test2@test2.it", password="test123")
        User.objects.create(username="test4", email="test4.test4@test4.it", password="test123")
        User.objects.create(username="test5", email="test5.test5@test5.it", password="test123")
        RecoverUser.objects.create(id="12345", user=user1, insertionDate=timezone.now())
    
    def test_IndexViewGet(self):
        user1 = User.objects.get(username="test1")
        client = Client()
        client.force_login(user1)
        response = client.get("")
        self.assertEqual(response.status_code,200)

    def test_LogoutView(self):
        user1 = User.objects.get(username="test1")
        client = Client()
        client.force_login(user1)
        response = client.get("/logout")
        self.assertEqual(response.status_code,302)

    def test_RegisterViewGet(self):
        client = Client()
        response = client.get("/register")
        self.assertEqual(response.status_code,200)

    def test_RegisterViewPostOK(self):
        client = Client()
        response = client.post("/register", {"username":"test3","email":"test3.test3@test3.it","password":"Test123!","confirmation":"Test123!"})
        self.assertEqual(response.status_code,302)
    
    def test_RegisterViewPostNOK1(self):
        client = Client()
        response = client.post("/register", {"username":"test3","email":"test3.test3@test3.it","password":"Test123","confirmation":"Test123"})
        self.assertEqual(response.status_code,200)
    
    def test_RegisterViewPostNOK2(self):
        client = Client()
        response = client.post("/register", {"username":"test3","email":"test3.test3@test3.it","password":"Test123!!","confirmation":"Test123!"})
        self.assertEqual(response.status_code,200)

    def test_RegisterViewPostNOK3(self):
        client = Client()
        response = client.post("/register", {"username":"test1","email":"test3.test3@test3.it","password":"Test123!!","confirmation":"Test123!!"})
        self.assertEqual(response.status_code,200)

    def test_PasswordRecoverViewGet(self):
        client = Client()
        response = client.get("/passwordRecover")
        self.assertEqual(response.status_code,200)

    def test_PasswordRecoverViewPostNOK1(self):
        client = Client()
        response = client.post("/passwordRecover", {"recoverText":"test3"})
        self.assertEqual(response.status_code,200)
    
    def test_PasswordRecoverViewPostNOK2(self):
        client = Client()
        response = client.post("/passwordRecover", {"recoverText":"test3.test3@test3.it"})
        self.assertEqual(response.status_code,200)

    def test_PasswordRecoverViewPostOK(self):
        client = Client()
        response = client.post("/passwordRecover", {"recoverText":"test1"})
        self.assertEqual(response.status_code,200)

    def test_CreateNewPasswordRecoverViewGetNOK(self):
        client = Client()
        response = client.get("/createNewPasswordRecover", {"recoverId":"1"})
        self.assertEqual(response.status_code,302)

    def test_CreateNewPasswordRecoverViewGetOK(self):
        client = Client()
        response = client.get("/createNewPasswordRecover", {"recoverId":"12345"})
        self.assertEqual(response.status_code,200)

    def test_CreateNewPasswordRecoverViewPutOK(self):
        client = Client()
        response = client.put("/createNewPasswordRecover")
        self.assertEqual(response.status_code,200)

    def test_CreateNewPasswordRecoverViewPostNOK1(self):
        client = Client()
        response = client.post("/createNewPasswordRecover", {"recoverId":"1"})
        self.assertEqual(response.status_code,200)
    
    def test_CreateNewPasswordRecoverViewPostNOK2(self):
        client = Client()
        response = client.post("/createNewPasswordRecover", {"recoverId":"12345","password":"Test123","confirmation":"Test123"})
        self.assertEqual(response.status_code,200)

    def test_CreateNewPasswordRecoverViewPostNOK3(self):
        client = Client()
        response = client.post("/createNewPasswordRecover", {"recoverId":"12345","password":"Test123!!","confirmation":"Test123!"})
        self.assertEqual(response.status_code,200)
    
    def test_CreateNewPasswordRecoverViewPostNOK4(self):
        client = Client()
        response = client.post("/createNewPasswordRecover", {"recoverId":"12345","password":"Test123!!"})
        self.assertEqual(response.status_code,200)

    def test_CreateNewPasswordRecoverViewPostOK(self):
        client = Client()
        response = client.post("/createNewPasswordRecover", {"recoverId":"12345","password":"Test123!!","confirmation":"Test123!!"})
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistLoadSongViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userPlaylistLoadSong/2")
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistLoadSongViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userPlaylistLoadSong/2")
        self.assertEqual(response.status_code,302)
    
    def test_UserPlaylistLoadSongViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/userPlaylistLoadSong/3")
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistLoadSongViewGetOK(self):
        file1 = open("./test.mp3", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.mp3"))
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1, audioFile=file1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/userPlaylistLoadSong/3")
        self.assertEqual(response.status_code,200)
        file1.close()
        os.remove("./test.mp3")
        os.remove("./capstone/audioFiles/test.mp3")

    def test_UserFriendPlaylistLoadSongViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userFriendPlaylistLoadSong/2/test1")
        self.assertEqual(response.status_code,302)

    def test_UserFriendPlaylistLoadSongViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userFriendPlaylistLoadSong/2/test1")
        self.assertEqual(response.status_code,302)
    
    def test_UserFriendPlaylistLoadSongViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        response = client.get("/userFriendPlaylistLoadSong/3/test2")
        self.assertEqual(response.status_code,302)
        playlist2 = UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist2, playingOrder=1)
        response = client.get("/userFriendPlaylistLoadSong/3/test2")
        self.assertEqual(response.status_code,302)

    def test_UserFriendPlaylistLoadSongViewGetOK(self):
        file1 = open("./test.mp3", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.mp3"))
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist2 = UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1, audioFile=file1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist2, playingOrder=1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        response = client.get("/userFriendPlaylistLoadSong/3/test2")
        self.assertEqual(response.status_code,200)
        file1.close()
        os.remove("./test.mp3")
        os.remove("./capstone/audioFiles/test.mp3")

    def test_UserPlaylistLoadAlbumViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userPlaylistLoadAlbum/2")
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistLoadAlbumViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userPlaylistLoadAlbum/2")
        self.assertEqual(response.status_code,302)
    
    def test_UserPlaylistLoadAlbumViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/userPlaylistLoadAlbum/3")
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistLoadAlbumViewGetOK(self):
        file1 = open("./test.jpg", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.jpg"))
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1", image=file1)
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/userPlaylistLoadAlbum/3")
        self.assertEqual(response.status_code,200)
        file1.close()
        os.remove("./test.jpg")
        os.remove("./capstone/albumImages/test.jpg")

    def test_UserFriendPlaylistLoadAlbumViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userFriendPlaylistLoadAlbum/2/test1")
        self.assertEqual(response.status_code,302)

    def test_UserFriendPlaylistLoadAlbumViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userFriendPlaylistLoadAlbum/2/test1")
        self.assertEqual(response.status_code,302)
    
    def test_UserFriendPlaylistLoadAlbumViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist2 = UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist2, playingOrder=1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        response = client.get("/userFriendPlaylistLoadAlbum/3/test2")
        self.assertEqual(response.status_code,302)

    def test_UserFriendPlaylistLoadAlbumViewGetOK(self):
        file1 = open("./test.jpg", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.jpg"))
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        album1 = Album.objects.create(name="Album1", artist="test1", image=file1)
        playlist2 = UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist2, playingOrder=1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        response = client.get("/userFriendPlaylistLoadAlbum/3/test2")
        self.assertEqual(response.status_code,200)
        file1.close()
        os.remove("./test.jpg")
        os.remove("./capstone/albumImages/test.jpg")

    def test_UserPlaylistSongsViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userPlaylistSongs")
        self.assertEqual(response.status_code,302)

    def test_UserPlaylistSongsViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userPlaylistSongs")
        self.assertEqual(response.status_code,302)
    
    def test_UserPlaylistSongsViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        response = client.get("/userPlaylistSongs")
        self.assertEqual(response.status_code,200)
    
    def test_UserPlaylistSongsViewGetOK2(self):
        file1 = open("./test.jpg", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.jpg"))
        file2 = open("./test.mp3", "w")
        file2.write("test")
        file2.close()
        file2 = File(open("./test.mp3"))
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1", image=file1)
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", audioFile=file2, albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        response = client.get("/userPlaylistSongs")
        self.assertEqual(response.status_code,200)
        file1.close()
        file2.close()
        os.remove("./test.jpg")
        os.remove("./capstone/albumImages/test.jpg")
        os.remove("./test.mp3")
        os.remove("./capstone/audioFiles/test.mp3")
    
    def test_UserPlaylistSongsViewGetOK3(self):
        file1 = open("./test.jpg", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.jpg"))
        file2 = open("./test.mp3", "w")
        file2.write("test")
        file2.close()
        file2 = File(open("./test.mp3"))
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1", image=file1)
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now(), lastSongPlayedId=3, lastSongPlayedSeconds=10)
        song1 = Song.objects.create(id=3, name="test1", audioFile=file2, albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        response = client.get("/userPlaylistSongs")
        self.assertEqual(response.status_code,200)
        file1.close()
        file2.close()
        os.remove("./test.jpg")
        os.remove("./capstone/albumImages/test.jpg")
        os.remove("./test.mp3")
        os.remove("./capstone/audioFiles/test.mp3")

    def test_UserFriendPlaylistSongsViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/userFriendPlaylistSongs/test2")
        self.assertEqual(response.status_code,302)

    def test_UserFriendPlaylistSongsViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/userFriendPlaylistSongs/test1")
        self.assertEqual(response.status_code,302)
    
    def test_UserFriendPlaylistSongsViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        response = client.get("/userFriendPlaylistSongs/test2")
        self.assertEqual(response.status_code,302)
    
    def test_UserPlaylistSongsViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        response = client.get("/userFriendPlaylistSongs/test2")
        self.assertEqual(response.status_code,200)
    
    def test_UserFriendPlaylistSongsViewGetOK2(self):
        file1 = open("./test.jpg", "w")
        file1.write("test")
        file1.close()
        file1 = File(open("./test.jpg"))
        file2 = open("./test.mp3", "w")
        file2.write("test")
        file2.close()
        file2 = File(open("./test.mp3"))
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1", image=file1)
        playlist1 = UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", audioFile=file2, albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        response = client.get("/userFriendPlaylistSongs/test2")
        self.assertEqual(response.status_code,200)
        file1.close()
        file2.close()
        os.remove("./test.jpg")
        os.remove("./capstone/albumImages/test.jpg")
        os.remove("./test.mp3")
        os.remove("./capstone/audioFiles/test.mp3")

    def test_UpdatePlaylistSongLikeViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/updatePlaylistSongLike/1")
        self.assertEqual(response.status_code,302)

    def test_UpdatePlaylistSongLikeViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/updatePlaylistSongLike/3")
        self.assertEqual(response.status_code,302)

    def test_UpdatePlaylistSongLikeViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/updatePlaylistSongLike/3")
        self.assertEqual(response.status_code,200)

    def test_UpdatePlaylistSongLikeViewGetOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1, liked=True)
        client.force_login(user1)
        response = client.get("/updatePlaylistSongLike/3")
        self.assertEqual(response.status_code,200)

    def test_GetPlaylistSongLikedViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/getPlaylistSongLiked/1")
        self.assertEqual(response.status_code,302)

    def test_GetPlaylistSongLikedViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/getPlaylistSongLiked/3")
        self.assertEqual(response.status_code,302)

    def test_GetPlaylistSongLikedViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.get("/getPlaylistSongLiked/3")
        self.assertEqual(response.status_code,200)

    def test_SavePlaylistSongPlayedViewGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/savePlaylistSongPlayed")
        self.assertEqual(response.status_code,302)

    def test_SavePlaylistSongPlayedViewPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/savePlaylistSongPlayed")
        self.assertEqual(response.status_code,500)

    def test_SavePlaylistSongPlayedViewPostNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":None, "secondsPlayed":None, "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,302)
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":"", "secondsPlayed":None, "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,302)

    def test_SavePlaylistSongPlayedViewPostNOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":"3", "secondsPlayed":"10", "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,302)

    def test_SavePlaylistSongPlayedViewPostNOK4(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":"3", "secondsPlayed":"10", "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,302)
        Song.objects.create(id=3, name="test1", albumId=album1)
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":"3", "secondsPlayed":"10", "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,302)

    def test_SavePlaylistSongPlayedViewPostOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        playlist1 = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=playlist1, playingOrder=1)
        client.force_login(user1)
        response = client.post("/savePlaylistSongPlayed",json.dumps({"songId":"3", "secondsPlayed":"10", "repeat":True, "shuffle":True, "volume":100}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_SearchSongsViewGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/searchSongs")
        self.assertEqual(response.status_code,302)

    def test_SearchSongsViewPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/searchSongs")
        self.assertEqual(response.status_code,500)

    def test_SearchSongsViewPostNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/searchSongs", json.dumps({"queryString":"testtest2"}),content_type="application/json")
        self.assertEqual(response.status_code,302)

    def test_SearchSongsViewPostOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        response = client.post("/searchSongs",json.dumps({"queryString":"testtest2"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_SearchSongsViewPostOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        response = client.post("/searchSongs",json.dumps({"queryString":"album"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_SearchSongsViewPostOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        response = client.post("/searchSongs",json.dumps({"queryString":"test"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_AddPlaylistSongViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/addPlaylistSong/1")
        self.assertEqual(response.status_code,302)

    def test_AddPlaylistSongViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/addPlaylistSong/1")
        self.assertEqual(response.status_code,500)

    def test_AddPlaylistSongViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        client.force_login(user1)
        response = client.get("/addPlaylistSong/1")
        self.assertEqual(response.status_code,500)
    
    def test_AddPlaylistSongViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        client.force_login(user1)
        response = client.get("/addPlaylistSong/3")
        self.assertEqual(response.status_code,200)

    def test_AddPlaylistSongViewGetOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        userPlaylist = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=userPlaylist, playingOrder=1)
        Song.objects.create(id=4, name="test2", albumId=album1)
        client.force_login(user1)
        response = client.get("/addPlaylistSong/3")
        self.assertEqual(response.status_code,200)

    def test_AddPlaylistSongViewGetOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        userPlaylist = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        song2 = Song.objects.create(id=4, name="test2", albumId=album1)
        PlaylistSong.objects.create(songId=song2, playlistId=userPlaylist, playingOrder=1)
        client.force_login(user1)
        response = client.get("/addPlaylistSong/3")
        self.assertEqual(response.status_code,200)

    def test_RemovePlaylistSongViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/removePlaylistSong/1")
        self.assertEqual(response.status_code,302)

    def test_RemovePlaylistSongViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/removePlaylistSong/1")
        self.assertEqual(response.status_code,500)

    def test_RemovePlaylistSongViewGetNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        client.force_login(user1)
        response = client.get("/removePlaylistSong/1")
        self.assertEqual(response.status_code,500)
    
    def test_RemovePlaylistSongViewGetNOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        client.force_login(user1)
        response = client.get("/removePlaylistSong/3")
        self.assertEqual(response.status_code,500)

    def test_RemovePlaylistSongViewGetNOK4(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        userPlaylist = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        Song.objects.create(id=3, name="test1", albumId=album1)
        song2 = Song.objects.create(id=4, name="test2", albumId=album1)
        PlaylistSong.objects.create(songId=song2, playlistId=userPlaylist, playingOrder=1)
        client.force_login(user1)
        response = client.get("/removePlaylistSong/3")
        self.assertEqual(response.status_code,500)

    def test_RemovePlaylistSongViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        userPlaylist = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=userPlaylist, playingOrder=1)
        Song.objects.create(id=4, name="test2", albumId=album1)
        client.force_login(user1)
        response = client.get("/removePlaylistSong/3")
        self.assertEqual(response.status_code,200)

    def test_RemovePlaylistSongViewGetOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        album1 = Album.objects.create(name="Album1", artist="test1")
        userPlaylist = UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        song1 = Song.objects.create(id=3, name="test1", albumId=album1)
        song2 = Song.objects.create(id=4, name="test2", albumId=album1)
        song3 = Song.objects.create(id=5, name="test2", albumId=album1)
        PlaylistSong.objects.create(songId=song1, playlistId=userPlaylist, playingOrder=2, liked=True)
        PlaylistSong.objects.create(songId=song2, playlistId=userPlaylist, playingOrder=1)
        PlaylistSong.objects.create(songId=song3, playlistId=userPlaylist, playingOrder=3)
        client.force_login(user1)
        response = client.get("/removePlaylistSong/3")
        self.assertEqual(response.status_code,200)

    def test_ProfileViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/profile")
        self.assertEqual(response.status_code,302)

    def test_ProfileViewGetNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/profile")
        self.assertEqual(response.status_code,302)

    def test_ProfileViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        client.force_login(user1)
        response = client.get("/profile")
        self.assertEqual(response.status_code,200)

    def test_ProfileViewGetOK2(self):
        client = Client()
        user0 = User.objects.get(username="test0")
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now(), profileImage="/capstone/profileImages/NoImage1.jpg")
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user0, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        client.force_login(user1)
        response = client.get("/profile")
        self.assertEqual(response.status_code,200)

    def test_ProfileChangePasswordViewGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/profileChangePassword")
        self.assertEqual(response.status_code,500)

    def test_ProfileChangePasswordViewPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/profileChangePassword")
        self.assertEqual(response.status_code,500)

    def test_ProfileChangePasswordViewPostOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/profileChangePassword",json.dumps({"password":"test","confirmation":"test"}),content_type="application/json")
        self.assertEqual(response.status_code,500)
        response = client.post("/profileChangePassword",json.dumps({"password":"Test123!!","confirmation":"Test123!"}),content_type="application/json")
        self.assertEqual(response.status_code,500)
        response = client.post("/profileChangePassword",json.dumps({"password":"Test123!!","confirmation":"Test123!!"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_UploadNewProfileImageViewGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/uploadNewProfileImage")
        self.assertEqual(response.status_code,302)

    def test_UploadNewProfileImageViewPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/uploadNewProfileImage")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/uploadNewProfileImage", json.dumps({"size":100}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostNOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/uploadNewProfileImage", json.dumps({"base64String":"YWJj","imageName":"abcd.jpg","size":100}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostNOK4(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/uploadNewProfileImage", json.dumps({"base64String":"YWJj","imageName":"abcd.jpeg","size":1000000000}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostNOK5(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/uploadNewProfileImage", json.dumps({"imageName":"abcd.abcd","size":100}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostNOK6(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        base64String = "a"*1048577
        response = client.post("/uploadNewProfileImage", json.dumps({"base64String":base64String,"imageName":"abcd.jpg","size":100}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_UploadNewProfileImageViewPostOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        response = client.post("/uploadNewProfileImage", json.dumps({"base64String":"YWJj","imageName":"abcd.jpg","size":100}),content_type="application/json")
        self.assertEqual(response.status_code,200)
        os.remove("./capstone/profileImages/abcd.jpg")

    def test_ShowFriendsUserViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/showFriendsUser/1")
        self.assertEqual(response.status_code,302)

    def test_ShowFriendsUserViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/showFriendsUser/1")
        self.assertEqual(response.status_code,200)

    def test_ShowFriendsUserViewGetOK2(self):
        client = Client()
        user0 = User.objects.get(username="test0")
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user0, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        response = client.get("/showFriendsUser/1")
        self.assertEqual(response.status_code,200)

    def test_ShowFriendsUserViewGetOK3(self):
        client = Client()
        user0 = User.objects.get(username="test0")
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        user4 = User.objects.get(username="test4")
        user5 = User.objects.get(username="test5")
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user0, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user4, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user4, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user5, accepted=2, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user5, creationDate=timezone.now(), profileImage="capstone/profileImages/NoImage1.jpg")
        response = client.get("/showFriendsUser/1")
        self.assertEqual(response.status_code,200)

    def test_ShowFriendPlaylistViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/showFriendPlaylist/test2")
        self.assertEqual(response.status_code,302)

    def test_ShowFriendPlaylistViewGetOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/showFriendPlaylist/test2")
        self.assertEqual(response.status_code,200)

    def test_FriendsViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/friends")
        self.assertEqual(response.status_code,302)

    def test_FriendsViewGetOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/friends")
        self.assertEqual(response.status_code,200)

    def test_FriendsJsonViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/friendsJson")
        self.assertEqual(response.status_code,500)

    def test_FriendsJsonViewGetOK(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/friendsJson")
        self.assertEqual(response.status_code,200)

    def test_SearchFriendsViewGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/searchFriends")
        self.assertEqual(response.status_code,500)

    def test_SearchFriendsViewPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/searchFriends")
        self.assertEqual(response.status_code,500)

    def test_SearchFriendsViewPostOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/searchFriends",json.dumps({"pageNumber":1,"queryString":""}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_SearchFriendsViewPostOK2(self):
        client = Client()
        user0 = User.objects.get(username="test0")
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        user4 = User.objects.get(username="test4")
        user5 = User.objects.get(username="test5")
        client.force_login(user1)
        UserPlaylist.objects.create(name="test1", user=user1, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user0, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user4, userAcceptor=user1, accepted=2, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user4, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user5, accepted=2, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user5, creationDate=timezone.now(), profileImage="capstone/profileImages/NoImage1.jpg")
        response = client.post("/searchFriends",json.dumps({"pageNumber":1,"queryString":""}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_AddAsFriendGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/addAsFriend")
        self.assertEqual(response.status_code,500)

    def test_addAsFriendPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/addAsFriend")
        self.assertEqual(response.status_code,500)
    
    def test_addAsFriendPostNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/addAsFriend",json.dumps({"usernameFriend":"test1"}),content_type="application/json")
        self.assertEqual(response.status_code,500)
    
    def test_addAsFriendPostNOK3(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        client.force_login(user1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=1, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=2, insertionDate=timezone.now())
        response = client.post("/addAsFriend",json.dumps({"usernameFriend":"test2"}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_addAsFriendPostOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/addAsFriend",json.dumps({"usernameFriend":"test2"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_addAsFriendPostOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        client.force_login(user1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=1, insertionDate=timezone.now())
        response = client.post("/addAsFriend",json.dumps({"usernameFriend":"test2"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_removeAsFriendGet(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/removeAsFriend")
        self.assertEqual(response.status_code,500)

    def test_removeAsFriendPostNOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/removeAsFriend")
        self.assertEqual(response.status_code,500)
    
    def test_removeAsFriendPostNOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/removeAsFriend",json.dumps({"usernameFriend":"test1"}),content_type="application/json")
        self.assertEqual(response.status_code,500)

    def test_removeAsFriendPostOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/removeAsFriend",json.dumps({"usernameFriend":"test2"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_removeAsFriendPostOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        client.force_login(user1)
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user2, accepted=1, insertionDate=timezone.now())
        response = client.post("/removeAsFriend",json.dumps({"usernameFriend":"test2"}),content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_ShowFriendRequestsViewPost(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.post("/showFriendRequests/1")
        self.assertEqual(response.status_code,500)

    def test_ShowFriendRequestsViewGetOK1(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        client.force_login(user1)
        response = client.get("/showFriendRequests/1")
        self.assertEqual(response.status_code,200)

    def test_ShowFriendRequestsViewGetOK2(self):
        client = Client()
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        user4 = User.objects.get(username="test4")
        user5 = User.objects.get(username="test5")
        client.force_login(user1)
        FriendRequest.objects.create(userRequestor=user2, userAcceptor=user1, accepted=1, insertionDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user4, userAcceptor=user1, accepted=1, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user4, creationDate=timezone.now())
        FriendRequest.objects.create(userRequestor=user1, userAcceptor=user5, accepted=1, insertionDate=timezone.now())
        UserPlaylist.objects.create(name="test1", user=user2, creationDate=timezone.now(), profileImage="capstone/profileImages/NoImage1.jpg")
        response = client.get("/showFriendRequests/1")
        self.assertEqual(response.status_code,200)