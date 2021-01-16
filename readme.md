Make sure you are running this projct in Operating system ubuntu 20.0+
use terminal for all the followiing commands.

Unzip the project folder "Integrum"
After unzipping the folder
use cd command to ennter the project directory
then execute all the following command


Make virtual environment by using the following command

    Virtualenv venv -p python3

Activate the virtual environment by using the following command

    source venv/bin/activate

Install the requirnments, from requirnment.txt file by using following command

    pip3 install -r requirnments.txt

then apply this command for migrations

    python3 manage.py migrate

    python3 manage.py makemigrations

then apply this command and create super user

    python3 manage.py createsuperuser

fill all the following fields

    enter name 
    enter email
    enter password
    confrim password

then apply this command and runserver

    python3 manage.py runserver 
    (make sure port 8000 is not busy)

    if 8000 port is busy, then use following command

    python3 manage.py runserver 0.0.0.0:8002

open the link given in the terminal 

Project will run (InshaAllah).
