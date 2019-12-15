# Virtual Joystic + Flask webserver 

## Steps to install

Step 1: Install virtual Environment 
-----------------------------------

Debian/Ubuntu 
```
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 
```

CentOs
```
$ yum install epel-release 
$ yum install python-pip python-devel
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 
```

Step 2: Create Virtual Environment 
----------------------------------
```
$ mkdir ~/virtualenvironment
$ virtualenv ~/virtualenvironment/joystick
```

Step 3 : Clone the repo   
-----------------------
```
$ cd ~
$ git clone https://github.com/dramasamy/virtualJoystick.git
```

Step 4 : Install dependencies  
-----------------------------
```
$ cd ~/virtualJoystick
$ source ~/virtualenvironment/joystick/bin/activate
(joystick)dramasamy@hostname$ pip install  -r requirements.txt
```

Step 5 : Start the application 
-----------------------------
```
(joystick)dramasamy@hostname$ python app.py
```


Step 6 : Admin Webpage (Chrome/Firefox/Safari)
-----------------------------
```
http://127.0.0.1:5000/admin
```

Step 7 : Joystick (Chrome/Firefox/Safari)
-----------------------------
```
http://127.0.0.1:5000
```

License
-------

Apache License Version 2.0

Courtesy
--------

This project is based on following repos,

Flask WebSocket Example 1 : [FLASK](https://github.com/shanealynn/async_flask)

Flask WebSocket Example 2 : [FLASK](https://github.com/miguelgrinberg/Flask-SocketIO)

Virtual Joystick : [vJoyStick](https://github.com/jeromeetienne/virtualjoystick.js)

