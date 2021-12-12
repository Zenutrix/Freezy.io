<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="http://Freezy.io">
    <img src="http://laniax.eu/LOGOGITFREZZY.png" alt="Logo" width="250" height="50">
  </a>
   <h3 align="center">Payment System for Refrigerators</h3>

  <p align="center">
    Ideal for businesses and communes
    <br />
    <a href="https://github.com/Thomas-Austria/Freezy.io/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Thomas-Austria/Freezy.io/">View Demo</a>
    ·
    <a href="https://github.com/Thomas-Austria/Freezy.io//issues">Report Bug</a>
    ·
    <a href="https://github.com/Thomas-Austria/Freezy.io/issues">Request Feature</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
# About The Project

This project was born from the need of tracking expenses for our office fridge.
So we strapped a screen and a pi to it and made it "smart".

authentication works with RFID tags.

This system is based on trust. No locking mechanisms... yet.

<!-- GETTING STARTED -->
# Getting Started

Materials:
  - Raspberry Pi
  - MFRC522
  - 7 x Cable
  - Some display
  
## Prerequisites
Software Dependencies:
  - mysql-server
  - nginx
  - mysql
  ```shell
$ sudo apt install nginx mariadb-server python3-venv
```

Python dependencies:
  - CherryPy~=18.6.1
  - mysql~=0.0.3
  - mysql-connector-python~=8.0.26
  - cherrypy_cors

<b>IF YOU'RE USING VENV REMEMBER TO ACTIVATE IT:</b>
```source venv/bin/activate```
```shell
$ python3 -m pip install -r requirements.txt
```

## Installation

1. clone the repo
   ```shell
   $ git clone https://github.com/Thomas-Austria/Freezy.io/
   ```
2. Configure nginx\
   copy `freezy.conf` to `/etc/nginx/sites-available`
   ```shell
   $ sudo cp Freezy.io/freezy.conf /etc/nginx/sites-available
   ```
   create link in `/etc/nginx/sites-enabled` to `/etc/nginx/sites-available`
   ```shell
   $ sudo ln /etc/nginx/sites-available/freezy.conf /etc/nginx/sites-enabled
   ```
3. Set up SQL-Server

   configure mysql
   ```shell
   $ sudo su
   $ mysql
   > CREATE USER 'freezy'@'%' IDENTIFIED BY 'password';
   > GRANT ALL PRIVILEGES ON * . * TO 'freezy'@'%';
   > FLUSH PRIVILEGES;
   ```

   Enter your Credentials in `database.py`
   ```py
   HOST = "localhost"
   USERNAME = "freezy"
   PASSWORD = "password"
   DATABASE = "freezy"
   PORT = 3306
   ```
   
   
   <!-- USAGE EXAMPLES -->
# Usage
Select the working directory
```shell
$ cd Freezy.io
```
### Run:
Start the backend
```shell
$ python3 wsgi.py
```

or start the backend in a screen
```shell
$ screen -S freezy_backend python3 wsgi.py
```

### Manage the backend

use the admin script
```shell
$ python3 -m backend.admin
```

create a new user
```shell
$ python3 -m backend.admin createuser
```
