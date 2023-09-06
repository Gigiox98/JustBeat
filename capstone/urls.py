
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("passwordRecover", views.passwordRecover, name="passwordRecover"),
    path("createNewPasswordRecover", views.createNewPasswordRecover, name="createNewPasswordRecover"),
    path("userPlaylistLoadSong/<str:songId>",views.userPlaylistLoadSong, name="userPlaylistLoadSong"),
    path("userFriendPlaylistLoadSong/<str:songId>/<str:userFriend>",views.userFriendPlaylistLoadSong, name="userFriendPlaylistLoadSong"),
    path("userPlaylistLoadAlbum/<str:songId>",views.userPlaylistLoadAlbum, name="userPlaylistLoadAlbum"),
    path("userFriendPlaylistLoadAlbum/<str:songId>/<str:userFriend>",views.userFriendPlaylistLoadAlbum, name="userFriendPlaylistLoadAlbum"),
    path("userPlaylistSongs",views.userPlaylistSongs, name="userPlaylistSongs"),
    path("userFriendPlaylistSongs/<str:usernameFriend>",views.userFriendPlaylistSongs, name="userFriendPlaylistSongs"),
    path("updatePlaylistSongLike/<str:songId>",views.updatePlaylistSongLike, name="updatePlaylistSongLike"),
    path("getPlaylistSongLiked/<str:songId>",views.getPlaylistSongLiked, name="getPlaylistSongLiked"),
    path("savePlaylistSongPlayed", views.savePlaylistSongPlayed, name="savePlaylistSongPlayed"),
    path("searchSongs",views.searchSongs, name="searchSongs"),
    path("addPlaylistSong/<str:songId>", views.addPlaylistSong, name="addPlaylistSong"),
    path("removePlaylistSong/<str:songId>", views.removePlaylistSong, name="removePlaylistSong"),
    path("profile", views.profile, name="profile"),
    path("profileChangePassword", views.profileChangePassword, name="profileChangePassword"),
    path("uploadNewProfileImage", views.uploadNewProfileImage, name="uploadNewProfileImage"),
    path("showFriendsUser/<int:pageNumber>", views.showFriendsUser, name="showFriendsUser"),
    path("showFriendPlaylist/<str:usernameFriend>", views.showFriendPlaylist, name="showFriendPlaylist"),
    path("friends", views.friends, name="friends"),
    path("friendsJson", views.friendsJson, name="friendsJson"),
    path("searchFriends", views.searchFriends, name="searchFriends"),
    path("addAsFriend", views.addAsFriend, name="addAsFriend"),
    path("removeAsFriend", views.removeAsFriend, name="removeAsFriend"),
    path("showFriendRequests/<int:pageNumber>", views.showFriendRequests, name="showFriendRequests")
]