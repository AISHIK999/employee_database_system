# Employee Database System

## Description
A command-line application for seamless management of a company's employee database. Experience effortless control as you view, add, and update employee details, roles, and departments. This application offers comprehensive CRUD operations and ensures strict ACID compliance for data integrity

## Libraries and Technologies
* MariaDB - The database used to store employee information
* Adminer - A web interface used to view and manage the database
* Docker - A containerization platform used to run the database and web interface
* PyMySQL - A python library used to connect to the database
* Pickle - To backup the database into a file

## Usage and Installation
To use this application, you must have Docker installed on your machine. To install Docker, follow the instructions on their website: https://docs.docker.com/get-docker/

You can use your package manager to install docker and docker-compose. Since I use Arch btw:
```bash
sudo pacman -S docker docker-compose
```
Clone the contents of this repo
```bash
git clone https://github.com/AISHIK999/employee_database_system.git
```
Change directory into the cloned repo
```bash
cd employee_database_system
```
Make changes to the docker-compose.yml file if you need . Then run the docker-compose command to start the database and web interface
```bash
sudo docker-compose up --build -d
```
Run the python script to start the application. Run the script atleast once to properly create the database and table.
```bash
pip install PyMySQL
```
```bash
python3 program.py
```

To use the web interface, go to http://localhost:8080/ in your browser once the docker container is live.
As per default configurations:<br>
Username: `root`<br>
Password: `rootpass`<br>
Server: `db` <br>
Database: `employee_db`<br>
You can change these by modifying the docker-compose.yml file.