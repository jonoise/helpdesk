# Helpdesk System (potencially!)
Helpdesk system to manage tickets, comments, attachments and vacation (for now :P). Custom user models: Regulars (for regular employees) and Agents (for issue solver team member). The project was developed using Python and Django for the Backend♥ and using a Bootstrap template from google for the Frontend.

____
## Welcome to my Helpdesk System README.md ladies and gentlemen.

I'll be your host tonight! My name is Amilkar, i'm a ...what it is called? a "self-taught" software developer. More like a google-taught software developer. But yeah, basically I'm gonna cover general aspects of this project in this README so you can have it running in your desktop aswell. (There's a bit of spaggetti code in here so don't panic if you don't understand something... it is my fault, not yours! I commented the code when i tougth it was necessary (comments are in spanish tho lol, sorry for that)).

Esta es una imagen del Dashboard del proyecto, podemos ver que se listan los ticketes, las vacaciones pendientes y las aprobadas. También una lista con todos los tickets e información sobre ellos como un link para ver información más detallada. También podemos ver el navbar lateral con el que podemos navegar por la aplicación. 

![image](https://user-images.githubusercontent.com/71573508/108613509-5e684300-73b8-11eb-805c-bdb076066dc1.png)

___
# Installation

* Create a new folder to foster this project and cd into the folder and create a virtual environment and activate it.
* Crea una nueva carpeta para albergar el proyecto y haz cd dentro de la carpeta y crea un ambiente virtual y actívalo.

* Clone this repository:
* Clona este repositorio:

```
$ git clone https://github.com/soloamilkar/helpdesk
```

* Install requirements.txt within your virtual environment.
* Instala el archivos requirements.txt dentro de tu ambiente virtual.

```
$ pip install -r requirements.txt
```

* Run make migrations.
* Corre hacer migraciones.

```
python manage.py makemigrations
```

* Run migrations.
* Crea las migraciones.

```
python manage.py migrate
```

* Runserver

```
$ python manage.py runserver
```
