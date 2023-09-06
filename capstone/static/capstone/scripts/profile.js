var showFriendsModalBody = document.getElementById("showFriendsModalBody");
$('#showFriendsModal').on('hidden.bs.modal', function (e) {
    showFriendsModalBody.innerHTML = "";
})

function showToast(headerText, bodyText, addColorClass,removeColorClass) {
    document.getElementsByClassName("toast")[0].style.marginBottom="25px";
    document.getElementsByClassName("toast-header")[0].classList.add(addColorClass);
    document.getElementsByClassName("toast-header")[0].classList.remove(removeColorClass);
    document.getElementsByClassName("toast-header")[0].children[0].innerText=headerText;
    document.getElementsByClassName("toast-header")[0].nextElementSibling.innerText=bodyText;
    $('.toast').toast('show');
    window.scrollTo(0,0);
}

function showFriends(index) {
    fetch('/showFriendsUser/'+index, {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        method: "GET",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            var numberOfFriends = document.getElementById("friends");
            if (numberOfFriends != null) {
                numberOfFriends.innerText = response.numberFriends;
            }

            var emptyListDiv = document.getElementById("emptyListDiv");
            if (emptyListDiv != null) {
                showFriendsModalBody.removeChild(emptyListDiv);
            }

            var friends = response.friends;
            var paginatorCount = response.paginatorCount;
            var paginatorPerPage = response.paginatorPerPage;
            var paginatorNumberPage = response.paginatorNumberPage;
            if (friends.length > 0) {
                for(var i=0; i<friends.length; i++) {
                    var anchorCard = document.createElement("a");
                    var cardElement = document.createElement("div");
                    var rowCard = document.createElement("div");
                    var colDivImage = document.createElement("div");
                    var image = document.createElement("img");
                    var colDivBody = document.createElement("div");
                    var cardBody = document.createElement("div");
                    var cardUsername = document.createElement("div");
                    var cardEmail = document.createElement("div");
                    anchorCard.href = "/showFriendPlaylist/"+friends[i].username;
                    anchorCard.style.textDecoration = "none";
                    cardElement.style.height = "100px";
                    cardElement.style.marginBottom = "30px";
                    cardElement.classList.add("card");
                    rowCard.classList.add("row");
                    colDivImage.style.textAlign="left";
                    colDivImage.classList.add("col-md-3","col-sm-3","col-4");
                    image.classList.add("img-fluid","rounded-circle");
                    image.src = friends[i].profileImage;
                    image.style.height = "100px";
                    image.style.width = "100px";
                    colDivBody.classList.add("col-md-9","col-sm-9","col-8");
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
                    anchorCard.append(cardElement);
                    showFriendsModalBody.append(anchorCard);
                }

                if (paginatorCount > paginatorPerPage) {
                    var loadOtherFriendsButton = document.getElementById("loadOtherFriends");
                    var pagesNumber = parseInt(Math.ceil(paginatorCount/paginatorPerPage));
                    if (loadOtherFriendsButton != null) {
                        showFriendsModalBody.removeChild(loadOtherFriendsButton);
                    } else {
                        loadOtherFriendsButton = document.createElement("button");
                        loadOtherFriendsButton.id = "loadOtherFriends";
                        loadOtherFriendsButton.classList.add("btn","btn-secondary");
                        loadOtherFriendsButton.innerText = "Load other 50 friends";
                    }

                    loadOtherFriendsButton.onclick = function() {
                        showFriends(paginatorNumberPage+1);
                    }

                    if (paginatorNumberPage >= pagesNumber) {
                        loadOtherFriendsButton.style.display = "none";
                    }

                    showFriendsModalBody.append(loadOtherFriendsButton);
                    if (numberOfFriends != null) {
                        numberOfFriends.value=paginatorCount;
                    }
                }
            } else {
                var div = document.createElement("div");
                var imageFrownFill = document.createElement("img");
                var h1 = document.createElement("h1");
                div.id = "emptyListDiv";
                div.style.textAlign = "center";
                imageFrownFill.src = "/static/capstone/images/emoji-frown-black.svg";
                imageFrownFill.style.width = "30%";
                imageFrownFill.style.height = "30%";
                imageFrownFill.style.marginTop = "20px";
                h1.innerText = "You haven't friends yet.";
                h1.style.color = "black";
                h1.style.marginTop = "30px";
                div.append(imageFrownFill);
                div.append(h1);
                showFriendsModalBody.append(div);
            }

            $('#showFriendsModal').modal('show');
        }
    });
}

function loadNewProfileImage() {
    var imageInput = document.getElementById("imageInput");
    if (imageInput == null) {
      imageInput = document.createElement("input");
      imageInput.id = "imageInput";
      imageInput.type = "file";
      imageInput.setAttribute("accept","image/jpeg");
    }

    imageInput.oninput = function(event) {
      files = event.target.files 
      if (files.length >= 1) {
        imageFile = event.target.files[0];
        var reader = new FileReader();
        if (imageFile.type != "image/jpeg" && imageFile.type != "image/jpg") {
            showToast("Fail","The image must have one of these extensions: jpg/jpeg.","bg-danger","bg-success")
            return;
        } else if (imageFile.size > 1000000) {
            showToast("Fail","The maximum size of the image must be 1 MB.","bg-danger","bg-success")
            return;
        }
        reader.readAsDataURL(imageFile);
        reader.onload = function() {
            base64String = this.result.split("base64,")[1];
            fetch('/uploadNewProfileImage', {
                headers: {
                    "X-CSRFToken": document.cookie.split("csrftoken=")[1],
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    imageName: imageFile.name,
                    size: imageFile.size,
                    base64String: base64String
                }),
                method: "POST",
            }).then(response => response.json()).then(response => {
                if (response.status == "OK") {
                    window.location.reload();
                } else {
                    showToast("Fail",response.error,"bg-danger","bg-success")
                }
            });
        }
      }  
    };

    imageInput.click();
}

function changePassword() {
    var password = document.getElementById("password");
    var confirmation = document.getElementById("confirmation");
    fetch('/profileChangePassword', {
        headers: {
            "X-CSRFToken": document.cookie.split("csrftoken=")[1],
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            password: password.value,
            confirmation: confirmation.value
        }),
        method: "POST",
    }).then(response => response.json()).then(response => {
        if (response.status == "OK") {
            showToast("Success","Password changed successfully!","bg-success","bg-danger");
            password.value="";
            confirmation.value="";
        } else {
            showToast("Fail",response.error,"bg-danger","bg-success")
        }
    });
}