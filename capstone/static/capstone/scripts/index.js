var amplitudeLikeElement;
var amplitudeLikeOffElement;
var amplitudeLikeOnElement;
var containerSongs;
var volumeElement;
var playPauseButtonFrontElement;
var playPauseButtonBackElement;
var timeout = null;

function showToast(headerText, bodyText, addColorClass,removeColorClass) {
    document.getElementsByClassName("toast")[0].style.marginBottom = "25px";
    document.getElementsByClassName("toast-header")[0].classList.add(addColorClass);
    document.getElementsByClassName("toast-header")[0].classList.remove(removeColorClass);
    document.getElementsByClassName("toast-header")[0].children[0].innerText=headerText;
    document.getElementsByClassName("toast-header")[0].nextElementSibling.innerText=bodyText;
    if (document.getElementById("navbarCollapse").classList.contains("show"))
        document.getElementById("navbarCollapse").previousElementSibling.click();
    $('.toast').toast('show');
    window.scrollTo(0,0);
}

function createTrashBinRow(song, index) {
    var imageTrashBin = document.createElement("img");
    imageTrashBin.src = "/static/capstone/images/trash-bin.svg";
    imageTrashBin.style.marginTop = "15px";
    imageTrashBin.style.width = "20px";
    imageTrashBin.style.cursor = "pointer";
    imageTrashBin.onclick = function() {
        removePlaylistSong(song.id,index);
    };
    return imageTrashBin;
}

function createPlaylistRow(song, index, added) {
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
    imageSongAlbumArt.src = song.cover_art_url
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
    divAmplitudeSongContainer.append(createTrashBinRow(song, index));
    divAmplitudeSongContainer.append(spanSongPosition);
    divAmplitudeSongContainer.append(imageSongAlbumArt);
    divAmplitudeSongContainer.append(divSongMetaDataContainer);
    return divAmplitudeSongContainer;
}

function getPlaylistSongLiked() {
    setTimeout(function() {
    fetch('/getPlaylistSongLiked/'+Amplitude.getActiveSongMetadata().id, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            if (response.liked) {
                amplitudeLikeOffElement.style.display = 'none';
                amplitudeLikeOnElement.style.display = 'block';
            } else {
                amplitudeLikeOnElement.style.display = 'none';
                amplitudeLikeOffElement.style.display = 'block';
            }
        } else {
            showToast("Fail", "Generic Error occurred.","bg-danger","bg-success");
        }
    });
    },100);
}

function savePlaylistInformations() {
    var songId = Amplitude.getActiveSongMetadata().id
    var secondsPlayed = parseInt(Amplitude.getSongPlayedSeconds())
    var repeat = Amplitude.getRepeat();
    var shuffle = Amplitude.getShuffle();
    var volume = Amplitude.getVolume();

    fetch('/savePlaylistSongPlayed', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            songId: songId,
            secondsPlayed: secondsPlayed,
            repeat: repeat,
            shuffle: shuffle,
            volume: volume
        }),
        method: "POST",
    }).then(response => response.json()).then(response => {});
}

function addSongToPlaylist(songId) {
    fetch('/addPlaylistSong/'+songId, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            if (response.song != null) {
                var emptyListDiv = document.getElementById("emptyListDiv");
                if (emptyListDiv != null) {
                    window.location.reload();
                }

                Amplitude.addSong(response.song)
                var songsLength = Amplitude.getSongs().length;
                containerSongs.append(createPlaylistRow(response.song, songsLength-1,true));
                showToast("Success","Song successfully added to your playlist!","bg-success","bg-danger");
            }
        } else {
            showToast("Fail", "Song not added on your playlist!","bg-danger","bg-success");
        }
    });
}

function searchSongs(){
    var searchElement = document.getElementById("searchSongs");
    if (searchElement.value == null) {
        searchElement.value = "";
    }
    searchElement.focus();
    fetch('/searchSongs', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            queryString: searchElement.value,
        }),
        method: "POST",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            var dropdownMenuAnchor = document.getElementById("searchSongsDropdown");
            if (dropdownMenuAnchor.nextElementSibling != null) {
                $('#searchSongsDropdown').dropdown('dispose');
                dropdownMenuAnchor.parentElement.removeChild(dropdownMenuAnchor.nextElementSibling);
            }

            var dropdownMenu = document.createElement('div')
            dropdownMenu.style.maxHeight = "200px";
            dropdownMenu.style.overflowY = "auto";
            dropdownMenu.classList.add("dropdown-menu");
            dropdownMenu.setAttribute("data-bs-theme","dark");
            var songsLength = response.songs.length;
            if (songsLength > 0) {
                for (var index = 0; index < songsLength; index++) {
                    var dropdownItemDiv = document.createElement('div');
                    dropdownItemDiv.classList.add("dropdown-item");
                    dropdownItemDiv.id = "dropdownItemAnchorSong-"+response.songs[index].id
                    dropdownItemDiv.style.paddingTop = '10px';
                    dropdownItemDiv.style.paddingBottom = '10px';
                    dropdownItemDiv.innerText = response.songs[index].songName+" - "+response.songs[index].albumName;
                    dropdownItemDiv.onclick = function(event) {
                        var idSplitted = event.target.id.split("-");
                        addSongToPlaylist(idSplitted[1]);
                    }
                    dropdownMenu.append(dropdownItemDiv);
                }
            } else {
                var dropdownItemDiv = document.createElement('div');
                dropdownItemDiv.classList.add("dropdown-item");
                dropdownItemDiv.style.paddingTop = '10px';
                dropdownItemDiv.style.paddingBottom = '10px';
                dropdownItemDiv.innerText = "No results found.";
                dropdownMenu.append(dropdownItemDiv);
                dropdownMenu.style.pointerEvents = "none";
            }

            dropdownMenuAnchor.parentElement.append(dropdownMenu);
            $('#searchSongsDropdown').dropdown('toggle');
        } else {
            showToast("Fail", "Generic Error occurred.","bg-danger","bg-success");
        }
    });
}

function removePlaylistSong(songId,songIndex) {
    fetch('/removePlaylistSong/'+songId, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            containerSongs.innerHTML = "";
            var songsLength = Amplitude.getSongs().length;
            var songActiveIndex;
            var songActiveSongMetadata = Amplitude.getActiveSongMetadata();
            for (var index = 0; index < songsLength; index++) {
                if (Amplitude.getSongAtIndex(index).id == songActiveSongMetadata.id) {
                    songActiveIndex = index;
                }

                if (index < songIndex) {
                    containerSongs.append(createPlaylistRow(Amplitude.getSongAtIndex(index), index, true));
                } else if (index > songIndex) {
                    containerSongs.append(createPlaylistRow(Amplitude.getSongAtIndex(index), index-1, true));
                }
            }

            var songPlayedSeconds = Amplitude.getSongPlayedSeconds();
            var sameSongFlag = songActiveIndex == songIndex;
            var greaterThanActiveIndex = songActiveIndex > songIndex;
            var isPaused = playPauseButtonFrontElement.classList.contains("amplitude-paused");
            Amplitude.removeSong(songIndex);
            if (songsLength > 1) {
                Amplitude.next();
                Amplitude.prev();
                if (sameSongFlag) {
                    Amplitude.pause();
                    playPauseButtonFrontElement.classList.remove("amplitude-played"); 
                    playPauseButtonFrontElement.classList.add("amplitude-paused");
                    playPauseButtonBackElement.classList.add("amplitude-paused");
                    playPauseButtonBackElement.classList.remove("amplitude-playing");
                } else {
                    if (greaterThanActiveIndex) {
                        document.getElementsByClassName("song")[songActiveIndex-1].classList.add("amplitude-active-song-container");
                        Amplitude.skipTo(songPlayedSeconds,songActiveIndex-1);
                    } else {
                        document.getElementsByClassName("song")[songActiveIndex].classList.add("amplitude-active-song-container");
                        Amplitude.skipTo(songPlayedSeconds,songActiveIndex);
                    }
                    
                    if (isPaused) {
                        Amplitude.pause();
                        playPauseButtonFrontElement.classList.remove("amplitude-played"); 
                        playPauseButtonFrontElement.classList.add("amplitude-paused");
                        playPauseButtonBackElement.classList.add("amplitude-paused");
                        playPauseButtonBackElement.classList.remove("amplitude-playing");
                    }
                }
            } else {
                window.location.reload();
            }
            showToast("Success", "Song successfully removed to your playlist!","bg-success","bg-danger");
        } else {
            showToast("Fail", "Song not removed on your playlist!","bg-danger","bg-success");
        }
    });
}

function createEmptyList() {
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
    h1.innerText = "There aren't songs in your playlist yet.";
    h1.style.textAlign = "center";
    h1.style.color = "black";
    h1.style.marginTop = "30px";
    visualizationsPlayer.style.textAlign = "center";
    visualizationsPlayer.style.display = "block";
    div.append(imageFrownFill);
    div.append(h1);
    visualizationsPlayer.append(div);
}

window.onbeforeunload = function() {
    savePlaylistInformations();
}

window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();
    }
};

window.onload = function() {
    var firstSongLiked = false;
    amplitudeLikeElement = document.getElementsByClassName('amplitude-like')[0];
    amplitudeLikeOffElement = document.getElementsByClassName('amplitude-like-off')[0];
    amplitudeLikeOnElement = document.getElementsByClassName('amplitude-like-on')[0];
    containerSongs = document.getElementsByClassName('songs-container')[0];
    volumeElement = document.getElementById("range");
    playPauseButtonFrontElement = document.getElementsByClassName("control-container")[0].children[1];
    playPauseButtonBackElement = document.getElementsByClassName("active-audio-controls")[0].children[1];
    
    fetch('/userPlaylistSongs', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        amplitudeLikeElement.style.display = 'block';
        if (response.status == "OK" && response.songs != "") {
            var songsLength = response.songs.length;
            for (var index = 0; index < songsLength; index++) {
                containerSongs.append(createPlaylistRow(response.songs[index], index, false));
            }
          
            Amplitude.init({
                songs: response.songs
            });

            if (response.playlistProperties != "") {
                if (response.playlistProperties.lastSongPlayed !== "" && 
                response.playlistProperties.lastSongPlayedSeconds !== "") {
                    var songs = response.songs;
                    var index = null;
                    var firstSong = null;
                    
                    for (song in songs) {
                        if (songs[song].id == response.playlistProperties.lastSongPlayed) {
                            index = song;
                            firstSong = songs[song];
                        }
                    }

                    if (firstSong != null) {
                        Amplitude.skipTo(response.playlistProperties.lastSongPlayedSeconds, index)
                        Amplitude.pause();
                        playPauseButtonFrontElement.classList.remove("amplitude-played"); 
                        playPauseButtonFrontElement.classList.add("amplitude-paused");
                        playPauseButtonBackElement.classList.add("amplitude-paused");
                        playPauseButtonBackElement.classList.remove("amplitude-playing");
                        firstSongLiked = firstSong.liked;
                    }
                } else {
                    firstSongLiked = response.songs[0].liked
                }

                if (firstSongLiked) {
                    amplitudeLikeOnElement.style.display = 'block';
                    amplitudeLikeOffElement.style.display = 'none';
                } else {
                    amplitudeLikeOffElement.style.display = 'block'
                    amplitudeLikeOnElement.style.display = 'none';
                }

                if (response.playlistProperties.repeat) {
                    Amplitude.setRepeat(true)
                }
    
                if (response.playlistProperties.shuffle) {
                    Amplitude.setShuffle(true)
                }

                if (response.playlistProperties.volume != 50) {
                    Amplitude.setVolume(response.playlistProperties.volume);
                    volumeElement.value = response.playlistProperties.volume;
                } else {
                    Amplitude.setVolume(50);
                }
            }

            document.getElementById("visualizations-player").style.display = "block";
        } else {
            if (response.status == "NOK") {
                showToast("Fail", "Generic Error occurred.","bg-danger","bg-success");
            } else {
                createEmptyList();
            }
        }});

    volumeElement.addEventListener("input", (event) => {
        Amplitude.setVolume(event.target.value);
    });

    document.getElementById("searchSongsSpan").addEventListener('click',searchSongs);
    document.getElementById("searchSongs").addEventListener('keyup',function(){
        clearTimeout(timeout)
        timeout = setTimeout(function() {
            searchSongs();
        }, 1000)
    });

    document.getElementById("removePlaylistSong").addEventListener('click',function() {
        removePlaylistSong(Amplitude.getActiveSongMetadata().id,Amplitude.getActiveIndex());
    });

    document.getElementsByClassName('arrow-up-icon')[0].addEventListener('click', function(){
        document.getElementById('visualizations-player-playlist').style.display = 'block';
    });
        
    document.getElementsByClassName('arrow-down-icon')[0].addEventListener('click', function(){
        document.getElementById('visualizations-player-playlist').style.display = 'none';
    });

    document.getElementsByClassName('amplitude-like')[0].addEventListener('click', function(){
        var songId = Amplitude.getActiveSongMetadata().id
        fetch('/updatePlaylistSongLike/'+songId, {
            headers: {
                "X-CSRFToken": document.cookie.split("csrftoken=")[1],
                "Content-Type": "application/json"
            },
            method: "GET",
        }).then(response => response.json()).then(response => {
            if (response.status == "OK") {
                if (amplitudeLikeOffElement.style.display == 'none') {
                    amplitudeLikeOnElement.style.display = 'none';
                    amplitudeLikeOffElement.style.display = 'block';
                } else {
                    amplitudeLikeOffElement.style.display = 'none';
                    amplitudeLikeOnElement.style.display = 'block';
                }
            } else {
                showToast("Fail", "Generic Error occurred.","bg-danger","bg-success");
            }
        });
    });

    document.getElementsByClassName('amplitude-next')[0].addEventListener('click', getPlaylistSongLiked);
    document.getElementsByClassName('amplitude-prev')[0].addEventListener('click', getPlaylistSongLiked);
}