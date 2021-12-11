<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="http://Freezy.io">
    <img src="http://laniax.eu/LOGOGITFREEZY.png" alt="Logo" width="250" height="50">
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

  - Raspberry Pi
  - MFRC522
  - 7 x Cable
  - Some display
  
### Prerequisites
```shell
$ sudo apt install nginx mysql mysql-server
```

### Installation

1. Clone the repo
   ```shell
   $ git clone https://github.com/Thomas-Austria/Freezy.io/
   ```
2. Configure nginx 
   1. copy freezy.conf to /etc/nginx/sites-available 
   2. create link in /etc/nginx/sites-enabled to /etc/nginx/sites-available
   ```shell
   $ sudo cp Freezy.io/freezy.conf /etc/nginx/sites-available
   ```
   ```shell
   $ sudo ln /etc/nginx/sites-available/freezy.conf /etc/nginx/sites-enabled
   ```
2. Install python libraries
   ```shell
   $ pip3 install -r requirements.txt 
   ```
3. Enter your Credentials in `database.py`
   ```py
   DB = 'DB';
   DB_PW = 'DB_PW';
   DB_User = 'DB_USER';
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
