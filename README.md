# GitHubAnalyzer
It's a Django project to extract data using GitHub APIs:

##Active demo of the application

`http://tdwivedi2708.pythonanywhere.com/`

Test account credentials :

**Username** : tester

**Password** : Test@123

##Steps to deploy the app locally


* Get the source code :
```shell
git clone https://github.com/tushar2708/GitHubAnalyzer.git
```
* Run following command to set up a virtual envionment :
```shell
cd GitHubAnalyzer
virtualenv myvenv
```
* Start your virtual environment by running :
```shell
source myvenv/bin/activate
```
* Install the required python packages :
```shell
pip install -r requirements.txt
```
* Create default Django database :
```shell
python manage.py migrate
```
* Create Django database for GitIssues App :
```shell
python manage.py makemigrations GitIssues
python manage.py migrate GitIssues
```
* Create superuser admin for your app :
```shell
python manage.py createsuperuser
```
* Start local server for the app :
```shell
python manage.py runserver
```

* Visit `http://127.0.0.1:8000` and login to the app.

##Explanation of basic logic of source code

* (**Source** : https://github.com/tushar2708/GitHubAnalyzer/blob/master/GitIssues/models.py **Function** : Query.CreateQuery(option) )

Simple Logic of extracting open issues from GitHub APIs (https://developer.github.com/v3/issues/) works by taking a public repo's URL, and converting it to appropriate GitHub API string.
* (**Source** : https://github.com/tushar2708/GitHubAnalyzer/blob/master/GitIssues/models.py **Function** : Result.createResult() )

By default, we fetch 100 results per page (max possible value, supported by the API) to minimize the number of times we hit the APIs (a resource limited by gitHub, to 60requests/hour). If there are more results, then we keep fetching more pages, till the last page is fetched.

##Introduction to Django views used in the project
(**Source** : https://github.com/tushar2708/GitHubAnalyzer/blob/master/GitIssues/views.py)
* query_new : A view (also the homepage, currently), to accept user's input as a public github repo.
* result_detail : A view, to display the result of user's input, or any query listed on Query hostory page(query_list view).
* query_list : Lists the older queries made by different users in past.

##TODO List for future

* To figure out a mechanism to cache the user queries, and first checking the existing results, to provide the results.
* Providing sorting based on different column names, on the query_list page
* Using authorised API calls on GitHub to get a higher request/hour rate.
* Figuring out a better platform to deploy the app, by exploring services like heroku, openshift, etc
* In future, I intend to scale this project to make an app to prepare a rank of most active GitHub repositories (based on ratio of "number of issues being closed" to "issues being opened", or some other criteria)
