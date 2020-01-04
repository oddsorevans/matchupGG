# matchupGG
While trying to seed brackets, as well as inevitably create pr, it is very easy to forget how individuals are doing. While going back through old tournaments is easy, it is difficult to see the big picture while doing so. The goal is to create a script that will pull the events sets, and create a mini csv for the matchups in that tournament. Another function or script will be written that takes the small mu chart and combines it to the big one that will be kept update throughout the season.

## API
Here is the link to the API documentation. The main idea right now is to use the event sets, and the set score requests to get all the data since there is no way to get it all with one pull as of now.

[Smash.GG Restful API](https://developer.smash.gg/docs/intro)

## Table of Goals
To-Do | Description
----- | -----------
Certificate | Get Certificate to work with API
Requests | Experiment with the requests and learn how to use them
Table | Take data and put it into a useable CSV file
Update Table | Combine a new and old CSV to create an updated CSV
