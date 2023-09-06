var timeout = null;
var showFriendRequestsModalBody = document.getElementById("showFriendRequestsModalBody");

$('#showFriendRequestsModal').on('hidden.bs.modal', function (e) {
    showFriendRequestsModalBody.innerHTML = "";
})

function createEmptyDiv() {
    var div = document.getElementById("emptyFriendRequestsListDiv");
    if (div == null) {
        div = document.createElement("div")
        div.id = "emptyFriendRequestsListDiv";
    } else {
        div.innerHTML = "";
        div.className = "";
        div.style="";
    }

    var imageFrownFill = document.createElement("img");
    var h1 = document.createElement("h1");
    div.style.textAlign = "center";
    imageFrownFill.src = "/static/capstone/images/check-circle.svg";
    imageFrownFill.style.width = "30%";
    imageFrownFill.style.height = "30%";
    imageFrownFill.style.marginTop = "20px";
    h1.innerText = "You haven't new friend requests.";
    h1.style.textAlign = "center";
    h1.style.color = "black";
    h1.style.marginTop = "30px";
    div.append(imageFrownFill);
    div.append(h1);
    showFriendRequestsModalBody.append(div);
}

function createAcceptRejectFriendDiv(id, isModal) {
    var divAcceptRejectAsFriend;
    if (isModal)
        divAcceptRejectAsFriend = document.getElementById(id+"-modal");
    else
        divAcceptRejectAsFriend = document.getElementById(id);
    var divAcceptAsFriend = document.createElement("div");
    var divRejectAsFriend = document.createElement("div");
    if (divAcceptRejectAsFriend != null) {
        divAcceptRejectAsFriend.innerHTML = "";
        divAcceptRejectAsFriend.className = "";
        divAcceptRejectAsFriend.style="";
    } else {
        divAcceptRejectAsFriend = document.createElement("div");
    }

    if (!isModal) {
        divAcceptRejectAsFriend.id = id;
        divAcceptRejectAsFriend.style.display = "flex";
        divAcceptRejectAsFriend.style.padding = "0px";
        divAcceptAsFriend.id = id+"-accept";
        divRejectAsFriend.id = id+"-reject";
    } else {
        divAcceptRejectAsFriend.id = id+"-modal";
        divAcceptAsFriend.id = id+"-accept-modal";
        divRejectAsFriend.id = id+"-reject-modal";
    }
    var iconAcceptFriend = document.createElement("img");
    var h6Accept = document.createElement("h6");
    h6Accept.innerText = "Accept";
    h6Accept.style.display = "inline";
    h6Accept.style.marginLeft = "5px";
    iconAcceptFriend.src = "/static/capstone/images/check.svg";
    divAcceptAsFriend.classList.add("btn","btn-success");
    divAcceptAsFriend.style.marginRight = "10%";
    divAcceptAsFriend.style.width = "45%";
    divAcceptAsFriend.onclick = function() {
        addAsFriend(id);
    }
    divAcceptAsFriend.append(iconAcceptFriend);
    divAcceptAsFriend.append(h6Accept);
    divAcceptRejectAsFriend.append(divAcceptAsFriend);

    var iconRejectFriend = document.createElement("img");
    var h6Reject = document.createElement("h6");
    h6Reject.innerText = "Reject";
    h6Reject.style.display = "inline";
    h6Reject.style.marginLeft = "5px";
    iconRejectFriend.src = "/static/capstone/images/x.svg";
    divRejectAsFriend.style.width = "45%";
    divRejectAsFriend.classList.add("btn","btn-danger");
    divRejectAsFriend.onclick = function() {
        removeAsFriend(id);
    }
    divRejectAsFriend.append(iconRejectFriend);
    divRejectAsFriend.append(h6Reject);
    divAcceptRejectAsFriend.append(divRejectAsFriend);
    return divAcceptRejectAsFriend;
}

function createAddFriendDiv(id) {
    var divAddAsFriend = document.getElementById(id);
    if (divAddAsFriend != null) {
        divAddAsFriend.innerHTML = "";
        divAddAsFriend.className = "";
        divAddAsFriend.style="";
    } else {
        divAddAsFriend = document.createElement("div");
    }

    var iconAddFriend = document.createElement("img");
    var h6 = document.createElement("h6");
    h6.innerText = "Add as friend";
    h6.style.display = "inline";
    h6.style.marginLeft = "5px";
    iconAddFriend.src = "/static/capstone/images/person-fill-add.svg";
    divAddAsFriend.id = id;
    divAddAsFriend.classList.add("col-12","col-sm-12","col-md-12","col-lg-12","col-xl-12","btn","btn-success");
    divAddAsFriend.onclick = function() {
        addAsFriend(id);
    }
    divAddAsFriend.append(iconAddFriend);
    divAddAsFriend.append(h6);
    return divAddAsFriend;
}

function createRemoveRequestDiv(id) {
    var divSentRequest = document.getElementById(id);
    if (divSentRequest != null) {
        divSentRequest.innerHTML = "";
        divSentRequest.className = "";
        divSentRequest.style="";
    } else {
        divSentRequest = document.createElement("div");
    }
    
    var iconSentRequest = document.createElement("img");
    var h6 = document.createElement("h6");
    h6.innerText = "Remove request";
    h6.style.display = "inline";
    h6.style.marginLeft = "5px";
    iconSentRequest.src = "/static/capstone/images/send-fill-x.svg";
    divSentRequest.id = id;
    divSentRequest.classList.add("col-12","col-sm-12","col-md-12","col-lg-12","col-xl-12","btn","btn-danger");
    divSentRequest.onclick = function() {
        removeAsFriend(id);
    }
    divSentRequest.append(iconSentRequest);
    divSentRequest.append(h6);
    return divSentRequest;
}

function createRemoveFriendDiv(id) {
    var divRemoveAsFriend = document.getElementById(id);
    if (divRemoveAsFriend != null) {
        divRemoveAsFriend.innerHTML = "";
        divRemoveAsFriend.className = "";
        divRemoveAsFriend.style="";
    } else {
        divRemoveAsFriend = document.createElement("div");
    }
    
    var iconRemoveFriend = document.createElement("img");
    var h6 = document.createElement("h6");
    h6.innerText = "Remove as friend";
    h6.style.display = "inline";
    h6.style.marginLeft = "5px";
    iconRemoveFriend.src = "/static/capstone/images/person-fill-dash.svg";
    divRemoveAsFriend.id = id;
    divRemoveAsFriend.classList.add("col-12","col-sm-12","col-md-12","col-lg-12","col-xl-12","btn","btn-danger");
    divRemoveAsFriend.onclick = function() {
        removeAsFriend(id);
    }
    divRemoveAsFriend.append(iconRemoveFriend);
    divRemoveAsFriend.append(h6);
    return divRemoveAsFriend;
}

function friendsJson() {
    fetch('/friendsJson', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            friendRequestsCounter.innerText = response.friendRequestsLength;
        }
    });
}

function addAsFriend(usernameFriend) {
    fetch('/addAsFriend', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
            usernameFriend: usernameFriend
        })
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            if (response.removeFriend) {
                createRemoveFriendDiv(usernameFriend);
            } else {
                createRemoveRequestDiv(usernameFriend);
            }
            
            var modalElement = document.getElementById(usernameFriend+"-modal");
            if (modalElement != null) {
                modalElement.parentElement.parentElement.remove();
                if (showFriendRequestsModalBody.children.length == 0) {
                    createEmptyDiv();
                }
            }
            friendsJson();
        }
    });
}

function removeAsFriend(usernameFriend) {
    fetch('/removeAsFriend', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
            usernameFriend: usernameFriend
        })
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            createAddFriendDiv(usernameFriend);
            var modalElement = document.getElementById(usernameFriend+"-modal");
            if (modalElement != null) {
                modalElement.parentElement.parentElement.remove();
                if (showFriendRequestsModalBody.children.length == 0) {
                    createEmptyDiv();
                }
            }
            friendsJson();
        }
    });
}

function searchFriends(index) {
    var searchElement = document.getElementById("searchFriends");
    var friendsResultElement = document.getElementById("friendsResult");
    fetch('/searchFriends', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
            queryString: searchElement.value,
            pageNumber: index
        })
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            if (friendsResultElement != null && index == 1) {
                friendsResultElement.innerHTML = "";
            }

            var emptyListDiv = document.getElementById("emptyListDiv");
            if (emptyListDiv != null) {
                emptyListDiv.innerHTML = "";
            }

            var friends = JSON.parse(response.friends);
            var paginatorCount = response.paginatorCount;
            var paginatorPerPage = response.paginatorPerPage;
            var paginatorNumberPage = response.paginatorNumberPage;
            if (friends.length > 0) {
                for(var i=0; i<friends.length; i++) {
                    var cardElement = document.createElement("div");
                    var rowCard = document.createElement("div");
                    var rowButtons = document.createElement("div");
                    var colDivImage = document.createElement("div");
                    var image = document.createElement("img");
                    var colDivBody = document.createElement("div");
                    var cardBody = document.createElement("div");
                    var cardUsername = document.createElement("div");
                    var cardEmail = document.createElement("div");
                    cardElement.classList.add("col-12","col-sm-12","col-md-5","col-lg-5","col-xl-5");
                    cardElement.style.marginBottom = "50px";
                    cardElement.classList.add("card");
                    rowCard.classList.add("row");
                    rowButtons.classList.add("row");
                    switch (friends[i].accepted) {
                        case 0:
                            rowButtons.append(createAddFriendDiv(friends[i].username));
                        break;
                          
                        case 1:
                            if (friends[i].acceptor)
                                rowButtons.append(createAcceptRejectFriendDiv(friends[i].username));
                            else 
                                rowButtons.append(createRemoveRequestDiv(friends[i].username));
                        break;

                        case 2:
                            rowButtons.append(createRemoveFriendDiv(friends[i].username));
                        break;
                    }

                    colDivImage.style.textAlign="left";
                    colDivImage.classList.add("col-4","col-sm-4","col-md-4","col-lg-4","col-xl-3");
                    colDivImage.style.padding = "0px";
                    image.classList.add("img-fluid","rounded-circle");
                    image.src = friends[i].profileImage;
                    image.style.height = "100px";
                    image.style.width = "100px";
                    colDivBody.classList.add("col-8","col-sm-8","col-md-8","col-lg-8","col-xl-9");
                    cardBody.classList.add("card-body");
                    cardBody.style.textAlign = "left";
                    cardUsername.classList.add("card-title","threePointsDiv");
                    cardUsername.innerText = friends[i].username;
                    cardUsername.setAttribute("title",friends[i].username);
                    cardEmail.classList.add("card-title","threePointsDiv");
                    cardEmail.innerText = friends[i].email;
                    cardEmail.setAttribute("title",friends[i].email);
                    colDivImage.append(image);
                    cardBody.append(cardUsername);
                    cardBody.append(cardEmail);
                    colDivBody.append(cardBody);
                    rowCard.append(colDivImage);
                    rowCard.append(colDivBody);
                    cardElement.append(rowCard);
                    cardElement.append(rowButtons);
                    friendsResultElement.append(cardElement);
                }

                if (paginatorCount > paginatorPerPage) {
                    var loadOtherUsersButton = document.getElementById("loadOtherUsers");
                    var pagesNumber = parseInt(Math.ceil(paginatorCount/paginatorPerPage));
                    if (loadOtherUsersButton != null) {
                        friendsResultElement.removeChild(loadOtherUsersButton);
                    } else {
                        loadOtherUsersButton = document.createElement("button");
                        loadOtherUsersButton.id = "loadOtherUsers";
                        loadOtherUsersButton.classList.add("col-12","col-sm-12","col-md-8","col-lg-8","col-xl-8","btn","btn-secondary");
                        loadOtherUsersButton.innerText = "Load other 50 users";
                    }

                    loadOtherUsersButton.onclick = function() {
                        searchFriends(paginatorNumberPage+1);
                    }

                    if (paginatorNumberPage >= pagesNumber) {
                        loadOtherUsersButton.style.display = "none";
                    }

                    friendsResultElement.append(loadOtherUsersButton);
                    document.getElementById("friendsResult").value=paginatorCount;
                }
            } else {
                var div = document.createElement("div");
                var imageFrownFill = document.createElement("img");
                var h1 = document.createElement("h1");
                div.id = "emptyListDiv";
                div.style.textAlign = "center";
                div.style.maxHeight = "250px";
                imageFrownFill.src = "/static/capstone/images/emoji-frown-black.svg";
                imageFrownFill.style.width = "50%";
                imageFrownFill.style.height = "40%";
                h1.innerText = "No results found.";
                h1.style.textAlign = "center";
                h1.style.color = "black";
                h1.style.marginTop = "10px";
                h1.style.marginBottom = "0px";
                div.append(imageFrownFill);
                div.append(h1);
                friendsResultElement.append(div);
            }
        }
    });
}

function showFriendRequests(index) {
    fetch('/showFriendRequests/'+index, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            var emptyFriendRequestsListDiv = document.getElementById("emptyFriendRequestsListDiv");
            if (emptyFriendRequestsListDiv != null) {
                showFriendRequestsModalBody.removeChild(emptyFriendRequestsListDiv);
            }

            var friendRequests = response.friendRequests;
            var paginatorCount = response.paginatorCount;
            var paginatorPerPage = response.paginatorPerPage;
            var paginatorNumberPage = response.paginatorNumberPage;
            if (friendRequests.length > 0) {
                for(var i=0; i<friendRequests.length; i++) {
                    var cardElement = document.createElement("div");
                    var rowCard = document.createElement("div");
                    var rowButtons = document.createElement("div");
                    var colDivImage = document.createElement("div");
                    var image = document.createElement("img");
                    var colDivBody = document.createElement("div");
                    var cardBody = document.createElement("div");
                    var cardUsername = document.createElement("div");
                    var cardEmail = document.createElement("div");
                    cardElement.style.marginBottom = "30px";
                    cardElement.classList.add("card");
                    rowCard.classList.add("row");
                    rowButtons.classList.add("row");
                    rowButtons.append(createAcceptRejectFriendDiv(friendRequests[i].username, true));
                    colDivImage.style.textAlign="left";
                    colDivImage.classList.add("col-md-3","col-sm-3","col-4");
                    image.classList.add("img-fluid","rounded-circle");
                    image.src = friendRequests[i].profileImage;
                    image.style.height = "100px";
                    image.style.width = "100px";
                    colDivBody.classList.add("col-md-9","col-sm-9","col-8");
                    cardBody.classList.add("card-body");
                    cardBody.style.textAlign = "left";
                    cardUsername.classList.add("card-title","threePointsDiv");
                    cardUsername.innerText = friendRequests[i].username;
                    cardUsername.setAttribute("title",friendRequests[i].username);
                    cardEmail.classList.add("card-title","threePointsDiv");
                    cardEmail.innerText = friendRequests[i].email;
                    cardEmail.setAttribute("title",friendRequests[i].email);
                    colDivImage.append(image);
                    cardBody.append(cardUsername);
                    cardBody.append(cardEmail);
                    colDivBody.append(cardBody);
                    rowCard.append(colDivImage);
                    rowCard.append(colDivBody);
                    cardElement.append(rowCard);
                    cardElement.append(rowButtons);
                    showFriendRequestsModalBody.append(cardElement);
                }

                if (paginatorCount > paginatorPerPage) {
                    var loadOtherFriendRequestsButton = document.getElementById("loadOtherFriendRequests");
                    var pagesNumber = parseInt(Math.ceil(paginatorCount/paginatorPerPage));
                    if (loadOtherFriendRequestsButton != null) {
                        showFriendRequestsModalBody.removeChild(loadOtherFriendRequestsButton);
                    } else {
                        loadOtherFriendRequestsButton = document.createElement("button");
                        loadOtherFriendRequestsButton.id = "loadOtherFriendRequests";
                        loadOtherFriendRequestsButton.classList.add("btn","btn-secondary");
                        loadOtherFriendRequestsButton.innerText = "Load other 50 friend requests";
                    }

                    loadOtherFriendRequestsButton.onclick = function() {
                        showFriendRequests(paginatorNumberPage+1);
                    }

                    if (paginatorNumberPage >= pagesNumber) {
                        loadOtherFriendRequestsButton.style.display = "none";
                    }

                    showFriendRequestsModalBody.append(loadOtherFriendRequestsButton);
                }
            } else {
                createEmptyDiv();
            }
            $('#showFriendRequestsModal').modal('show');
        }
    });
}

document.getElementById("searchFriendsSpan").addEventListener('click',function() {
    searchFriends(1);
});

document.getElementById("searchFriends").addEventListener('keyup',function(){
    clearTimeout(timeout)
    timeout = setTimeout(function() {
        searchFriends(1);
    }, 1000)
});

window.onload = function() {
    setInterval(function() {
        friendsJson();
    }, 10000)
    searchFriends(1);
}