### HarvardX CS50W: Web Programming with Python and JavaScript - JustBeat

#### Course's link
See [here](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript).

#### My Certificate
See [here](https://certificates.cs50.io/58eb7e8b-b4be-4c44-a7c5-42ad0e94ed0e.pdf).

#### Distinctiveness and Complexity
  - The project was built using Django as a backend framework and JavaScript as a frontend programming language.
  - The project was built following most of the rules of good programming.
  - The project was built following most of the rules of usability, reliability, scalability and security.
  - The project was built to create a new brand as a competitor of an actual brand, with a recognizable design, palette and colors.
  - All webpages of the project are mobile-responsive.
  - The project contains unit tests with line and branch coverage.
  - The project contains scheduling functions to clear database tables.
  - The project has required the study of the documentation of Amplitude.js library, to simplify the front-end.
  - The project currently contains 30 end-points.
  - All generated information are saved in database (SQLite by default).

#### Installation
  - Install project dependencies by running `pip install -r requirements.txt`. Dependencies include Django and Pillow module that allows Django to work with images.
  - (Optional step). If you would like to try the recover password functionality, change environment variables in .env file. (You can also ask me credentials by e-mail). 
  - Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
  - Create superuser with `python manage.py createsuperuser`.
  - Go to admin website address and insert some albums and songs associated. (Song and Album objects can be created only by admin.)
  - Go to website address and register an account.

#### Files and directories
  - `capstone` - this is the main application directory.
    - `audioFiles` this directory contains all audios of Song model.
    - `albumImages` this directory contains all images of Album model.
    - `profileImages` this directory contains a default image (NoImage.jpg), and all images of users' profile photos from UserPlaylist model.
    - `static/capstone` this directory contains all static content.
        - `css` this directory contains CSS files.
        - `images` - this directory contains all svg files and favicon.ico for pages.
        - `scripts` - this directory contains all JavaScript files used in project.
          - `amplitude.min.js` - this file is a lightweight JavaScript library that allows to control the design of media controls.
          - `bootstrap.*` - this files are scripts of bootstrap v.5.3.0.
          - `jquery-3.7.9.min.js` - this file is the script to use jquery framework.
          - `popper.min.js` - this file is the script to use tooltip and popover.
          - `popper.min.js.map` - this file is the map for the script popper.min.js.
          - `common.js` - this file is the script that run in more pages, so it has common features.
          - `friendPlaylist.js` - this file is the script that run in `friendPlaylist.html` template.
          - `index.js` - this file is the script that run in `index.html` template.
          - `profile.js` - this file is the script that run in `profile.html` template.
    - `templates/capstone` this directory contains all application templates.
        - `404.html` - this file is the template for 404 errors.
        - `500.html` - this file is the template for 500 errors.
        - `503.html` - this file is the template for 503 errors.
        - `createNewPasswordRecover.html` - this file is the template to create a new password thanks to a recoverId.
        - `friendPlaylist.html` - this file is the template that shows the playlist of logged user's friend.
        - `friends.html` - this file is the template to search new friends and to show new friendship requests.
        - `index.html` - this file is the template of the homepage after that user logged in.
        - `layout.html` - this file is the common template. All other templates extend it.
        - `login.html` - this file is the template of login.
        - `passwordRecover.html` - this file is the template to recover an user's account/password.
        - `profile.html` - this file is the template to show user's personal profile with statistics and friends.
        - `register.html` - this file is the template to register a new user.
    - `admin.py` - this file contains some admin classes. 
    Due to possible copyright issues, Song and Album objects can be created only by admin.
    - `functionUtilities.py` - this file contains common functions for back-end.
    - `jobscheduler.py` - this file contains scheduling functions to clear database tables.
    - `models.py` this file contains all models that I used in the project:
      * `User` model is the standard User model.
      * `RecoverUser` model represents an user who has requested to recover password.
      * `UserPlaylist` model represents the playlist of the user.
      * `Album` model represents an album of one or many songs.
      * `Song` model represents a song.
      * `PlaylistSong` model represents a song associated to one or many playlist.
      * `FriendRequest` model represent a friendship request between two users.
    - `test.py` - this file contains all application back-end tests.
    - `urls.py` - this file contains all application URLs.
    - `views.py` - this file contains all application views.
  - `project5` - this is the project directory.
    - `.env` - this file contains all environments variables.
    - `requirements.txt` - this file contains all python dependencies.
  - `.coverage` - this file is the executable of branch and line coverage.
  - `coverage.svg` - this file is the svg of the percentage of branch and line coverage.
  - `coverage.xml` - this file is the final report of branch and line coverage.
<br/>

![Tests and Coverage](https://github.com/me50/Gigiox98/actions/workflows/ci.yml/badge.svg)  ![Coverage](./coverage.svg)<br/>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">  <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">  <img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white">  <img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white">

The project's video: [https://www.youtube.com/watch?v=kofweJmpu9E](https://www.youtube.com/watch?v=ey9ZYwroAUg)https://www.youtube.com/watch?v=ey9ZYwroAUg
