# ElevatorSystem

#Overview
Elevator System is an application built in Django. It depicts real time elevator system providing functonlities like, adding a floor to elevator, seeing all the floors requested, opening door, closing door, maintainace, maintainance completed, current floor of elevator, its direction.

# Local SetUP
1. Install Ananconda
2. Create a python enviroment in Ananconda.
3. Insatll Django and Django Rest Framework
4. Also install postgres as postgres is used for db
5. Clone project from git hub
6. Activate django environment in Conda by **activate {env_name}**
7. Run the Project by **python manage.py runserver**
8. Import the collection and environment attacted in project to Postman
9. Hit the enpoints and validate

# Code Flow
1. There is one project dir which is the main dir
2. Project dir has settings.py which contains all project settings. It contains postgres db settings, installed and created apps, static media file dir path etc.
3. Urls.py contains endpoint of the applcation
4. Next is app which is elevators, it contains following:
5. model.py which has elevator model and conains fields like current floor direction, is operational
6. urls.py that has endpoint for this app
7. serializers.py which is used to convert python objects to json data
8. views.py which has business logic for different endpoints an some helper functions 
