# ets-demo
ETS demo

### Requirements
1) apt-get python-pip

## Installation
1) git clone https://github.com/flyingbot91/ets-demo.git
2) virtualenv env
3) source env/bin/activate
4) pip3 install -r requirements.txt

### How to run the tests
nosetests

## DB setup
python3 manage.py migrate
python3 manage.py createsuperuser

## Execution
1) python3 manage.py runserver
2) python3 manage.py run_demo (in a different terminal)
3) Go to http://localhost/8000/indexes/prices/<CURRENT_DATE>
Where <CURRENT_DATE> must be YYYYMMDD (e.g. '20181025')


