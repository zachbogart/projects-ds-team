# projects-ds-team
Projects in Data Science (Python) Team Page

How to use this code:

CHANGE YOUR PYTHONPATH
We ran this project through PyCharm, which uses absolute paths from the root directory of our project.
In order for the code to run at all outside of PyCharm run the following command:
export PYTHONPATH="${PYTHONPATH}:/<path_to_project_root>

Collect
____________

To collect twitter data we used the saveTweets function in twitterAPI.py

An example of this can be found in twitter/denver.py
(Information on the places we used can be found in data/places.json)


Enrich
___________

To enrich data we used the enrichAllPlaces function in enrich/enrichData.py
(EnrichRedditData function for reddit data)


Learn
___________

To run our regressors we used the functions in learn/machineLearning.py
An example of this can be found in learn/randomForest.py