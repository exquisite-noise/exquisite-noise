# Exquisite Noise

**Authors**:
- [Beverly Pham](https://github.com/zarkle)
- [Tyler Fishbone](https://github.com/tyler-fishbone)
- [Brandon Holderman](https://github.com/brandonholderman)

**Version**: 1.0.0

[![Build Status](https://travis-ci.org/exquisite-noise/exquisite-noise.svg?branch=master)](https://travis-ci.org/exquisite-noise/exquisite-noise) [![Coverage Status](https://coveralls.io/repos/github/exquisite-noise/exquisite-noise/badge.svg?branch=master)](https://coveralls.io/github/exquisite-noise/exquisite-noise?branch=master)

## Overview
<!-- Provide a high level overview of what this application is and why you are building it, beyond the fact that it's an assignment for a Code Fellows 401 class. (i.e. What's your problem domain?) -->
Our daily lives are so bombarded with technology that our team wanted to create an application built off of games we played growing up. This is an interactive game where you create a topic and record a portion of a story. Once you're finished you will be provided with a link to send to your friends who can add to the story.

## Getting Started
<!-- What are the steps that a user must take in order to build this app on their own machine and get it running? -->
- Install ffmpeg (on Mac, run command `brew install ffmpeg --with-libvorbis --with-sdl2 --with-theora`)
- Start a virtual environment
- Add the following to your activate script:
    ```
    # Project-specific env variables
    export SECRET_KEY=<paste in SECRET_KEY>
    export DEBUG=True
    export DB_NAME='noise'
    export DB_USER=''
    export DB_PASSWORD=''
    export DB_HOST='localhost'
    ```
- Activate your virtual environment
- Clone this repo onto your machine
- Inside the directory, install the requirements `pip install -r requirements.txt`
- Follow the directions to add an `audio_recorder` component from `https://github.com/voxy/django-audio-recorder`
- Make a database called `noise`
- Use command `noise/manage.py runserver` to start the server
- Use command `noise/manage.py createsuperuser` to create an admin user
- Open `localhost:8000` in your browser

## Architecture
<!-- Provide a detailed description of the application design. What technologies (languages, libraries, etc) you're using, and any other relevant design information. This is also an area which you can include any visuals; flow charts, example usage gifs, screen captures, etc.-->
Python 3, Django 2, CSS/SCSS, HTML, PostgreSQL, Travis CI, Coveralls, Pydub, Django-Audio-Recorder, Django Sass Processor

## API
<!-- Provide detailed instructions for your applications usage. This should include any methods or endpoints available to the user/client/developer. Each section should be formatted to provide clear syntax for usage, example calls including input data requirements and options, and example responses or return values. -->
Endpoints:
- `audio/new/`: Create new story
- `audio/add/<id>`: Add to an existing story
- `audio/add/<id>`: Details of an existing story
- `profile/<id>`: To view a user's stories
- `accounts/login/`: Login
- `accounts/register/`: Make an account

## Change Log
| Date | |
|:--|:--|
| 5-25-2018 | Final Touches and Presentation |
| 5-24-2018 | Styling, link page added, detail page added, profile page added, testing, deployment began |
| 5-23-2018 | Able to start story, add to database, grab current story to play on add page, concatenate new clip to existing story and update database |
| 5-22-2018 | Able to record audio files and add to database |
| 5-21-2018 | Connect Travis and Coveralls; able to upload sound files and add to database |
| 5-19-2018 | Initial Setup, install Django, create base home page with base css files, make profile component, install registration for user accounts, prepare for coveralls and travis |

## Resources
- gitignore.io
- editorconfig.org
- http://meyerweb.com/eric/tools/css/reset
- github.com/jiaaro/pydub
- github.com/jrief/django-sass-processor
- github.com/voxy/django-audio-recorder
- stackoverflow.com/questions/35825680/concatenate-audio-files-python-2-7
