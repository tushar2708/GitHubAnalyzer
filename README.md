# GitHubAnalyzer
It's a Django project to extract data using GitHub APIs:

##A demo of this app is deployed at below address :
`http://tdwivedi2708.pythonanywhere.com/`

##Steps to deploy the app locally:
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

##Explanation of source code
