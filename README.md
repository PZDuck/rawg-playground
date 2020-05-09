# RAWG Playground #

Application that utilizes [RAWG API](https://api.rawg.io/docs/) to let a user search for desired games depending on the search criteria (either by the part of the name, or by additional query parameters including publisher and genre).
 
**Core functionality**: Searching for games

**Additional functionality**:

* Basic authentication system
* Create and customize your profile
* Viewing a particular game’s additional information: description, available platforms, screenshots, similar games
* Combining games in one place by creating collections of user’s preference (e.g. “Favorite strategy games”, “Best games of 2019”, “Must Play Games” etc.)
* Keeping track of games the user wants to play, is currently playing, or has finished playing and marking them accordingly in their profile


Live Demo can be found at https://fathomless-retreat-05089.herokuapp.com/

The tools used in development include

*	HTML/CSS3
*	Bootstrap 4
*	Flask
*	JavaScript
*	jQuery
*	Axios.js
*	MongoDB

## Installation ##

No API key or token are needed to utilize the RAWG API. In order to run this project, virtual environment and MongoDB are needed. All the requirements could be found in requrements.txt file.

To run locally:

* Download and unzip the project files in the desired directory or clone it via Git `git clone https://github.com/PZduck/rawg-playground.git`
* Create a Python virtual environment `python -m venv myvenv`
* Activate your virtual environment and install all necessary modules from requirements.txt `pip install -r requirements.txt`
* Add your local MongoDB database and Secret Key to the config at `__init__.py`
* Run the application `flask run`