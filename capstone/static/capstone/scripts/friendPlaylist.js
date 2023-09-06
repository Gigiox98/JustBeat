var amplitudeLikeElement;
var amplitudeLikeOffElement;
var amplitudeLikeOnElement;
var containerSongs;
var volumeElement;
var playPauseButtonFrontElement;
var playPauseButtonBackElement;
var usernameParameter;

function createPlaylistRow(song, index, added, userFriend) {
    var divAmplitudeSongContainer = document.createElement("div");
    var spanSongPosition = document.createElement("span");
    var imageSongAlbumArt = document.createElement("img");
    var divSongMetaDataContainer = document.createElement("div");
    var spanSongName = document.createElement("span");
    var spanSongArtist = document.createElement("span");
    divAmplitudeSongContainer.classList.add("song","amplitude-song-container","amplitude-play-pause");
    divAmplitudeSongContainer.setAttribute("data-amplitude-song-index",index);
    if (added) {
        divAmplitudeSongContainer.onclick = function() {
            if (Amplitude.getActiveIndex() == index) {
                var songsLength = Amplitude.getSongs().length;
                document.getElementsByClassName("amplitude-play-pause")[songsLength+1].click();
            } else {
                Amplitude.playSongAtIndex(index);
            }
        };
    }
    spanSongPosition.classList.add("song-position");
    spanSongPosition.innerText = index+1;
    imageSongAlbumArt.classList.add("song-album-art");
    imageSongAlbumArt.setAttribute("data-amplitude-song-info","cover_art_url");
    imageSongAlbumArt.setAttribute("data-amplitude-song-index",index);
    imageSongAlbumArt.src = song.cover_art_url;
    divSongMetaDataContainer.classList.add("song-meta-data-container");
    spanSongName.classList.add("song-name");
    spanSongName.setAttribute("data-amplitude-song-index",index);
    spanSongName.setAttribute("data-amplitude-song-info","name");
    spanSongName.innerText = song.name
    spanSongArtist.classList.add("song-artist");
    spanSongArtist.setAttribute("data-amplitude-song-index",index);
    spanSongArtist.setAttribute("data-amplitude-song-info","artist");
    spanSongArtist.innerText = song.artist
    divSongMetaDataContainer.append(spanSongName);
    divSongMetaDataContainer.append(spanSongArtist);
    divAmplitudeSongContainer.append(spanSongPosition);
    divAmplitudeSongContainer.append(imageSongAlbumArt);
    divAmplitudeSongContainer.append(divSongMetaDataContainer);
    return divAmplitudeSongContainer;
}

function createEmptyList(usernameParameter) {
    var visualizationsPlayer = document.getElementById("visualizations-player");
    var visualizationsPlayerChildren = document.getElementById("visualizations-player").children;
    var visualizationsPlayerLength = visualizationsPlayerChildren.length;
    
    for (var i=0; i<visualizationsPlayerLength; i++) {
        if (i<visualizationsPlayerLength-2)
            visualizationsPlayerChildren[i].style.display = "none";
    }
    
    var div = document.createElement("div");
    var imageFrownFill = document.createElement("img");
    var h1 = document.createElement("h1");
    div.id = "emptyListDiv";
    imageFrownFill.src = "/static/capstone/images/emoji-frown-black.svg";
    imageFrownFill.style.width = "30%";
    imageFrownFill.style.height = "30%";
    h1.innerText = "There aren't songs in "+usernameParameter+"'s playlist yet.";
    h1.style.textAlign = "center";
    h1.style.color = "black";
    h1.style.marginTop = "30px";
    visualizationsPlayer.style.textAlign = "center";
    visualizationsPlayer.style.display = "block";
    div.append(imageFrownFill);
    div.append(h1);
    visualizationsPlayer.append(div);
}

window.onload = function() {
    amplitudeLikeElement = document.getElementsByClassName('amplitude-like')[0];
    amplitudeLikeOffElement = document.getElementsByClassName('amplitude-like-off')[0];
    amplitudeLikeOnElement = document.getElementsByClassName('amplitude-like-on')[0];
    containerSongs = document.getElementsByClassName('songs-container')[0];
    volumeElement = document.getElementById("range");
    playPauseButtonFrontElement = document.getElementsByClassName("control-container")[0].children[1];
    playPauseButtonBackElement = document.getElementsByClassName("active-audio-controls")[0].children[1];
    searchSongs = document.getElementById("searchSongs");
    searchSongs.parentElement.parentElement.style.display = "none";
    
    fetch('/userFriendPlaylistSongs/'+usernameParameter, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK" && response.songs != "") {
            var songsLength = response.songs.length;
            for (var index = 0; index < songsLength; index++) {
                containerSongs.append(createPlaylistRow(response.songs[index], index, false, usernameParameter));
            }
          
            Amplitude.init({
                songs: response.songs
            });

            if (response.playlistProperties != "") {

                if (response.playlistProperties.repeat) {
                    Amplitude.setRepeat(true)
                }
    
                if (response.playlistProperties.shuffle) {
                    Amplitude.setShuffle(true)
                }

                Amplitude.setVolume(50);
            }

            document.getElementById("visualizations-player").style.display = "block";
        } else {
            if (response.status == "NOK") {
                showToast("Fail", "Generic Error occurred.","bg-danger","bg-success");
            } else {
                createEmptyList(usernameParameter);
            }
        }});

    volumeElement.addEventListener("input", (event) => {
        Amplitude.setVolume(event.target.value);
    });

    document.getElementsByClassName('arrow-up-icon')[0].addEventListener('click', function(){
        document.getElementById('visualizations-player-playlist').style.display = 'block';
    });
        
    document.getElementsByClassName('arrow-down-icon')[0].addEventListener('click', function(){
        document.getElementById('visualizations-player-playlist').style.display = 'none';
    });
}