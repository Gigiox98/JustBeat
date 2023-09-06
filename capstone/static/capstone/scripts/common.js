var eyeIcon = document.getElementById("eyeIcon");
var eyeIcon2 = document.getElementById("eyeIcon2");

if (eyeIcon != null) {
    var passwordField = eyeIcon.previousElementSibling;
    eyeIcon.addEventListener('click', function() {
        if (passwordField.type == "password") {
            passwordField.type = "text";
            eyeIcon.src="static/capstone/images/eye-fill.svg";
        } else {
            passwordField.type = "password";
            eyeIcon.src="static/capstone/images/eye-slash-fill.svg";
        }
    });
}

if (eyeIcon2 != null) {
    var passwordField2 = eyeIcon2.previousElementSibling;
    eyeIcon2.addEventListener('click', function() {
        if (passwordField2.type == "password") {
            passwordField2.type = "text";
            eyeIcon2.src="static/capstone/images/eye-fill.svg";
        } else {
            passwordField2.type = "password";
            eyeIcon2.src="static/capstone/images/eye-slash-fill.svg";
        }
    });
}

