# COMP3335 Database Security - Project (Group 10)
This project conducts different security authentication and authorization between the Application and Database based on the predicted security threats and attacks. 

# Table of Contents
* [Pre-requisite](#pre-requisite)
* [Installation](#installation)
    * [Generate Environment Variable File](#generate-environment-variable-file)
    * [Update Environment Variable](#update-environment-variable)
    * [Build and Start the Container](#build-and-start-the-container)
    * [Stop the Container](#stop-the-container)
* [Demonstration](#demonstration)

# Pre-requisite
- The latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- At least 2GB of local storage
# Installation

## Generate Environment Variable File
Execute the following command to generate the environment variable file `env/app.env` and `env/database.env`.
```
cp env/app.env.example env/app.env
cp env/database.env.example env/database.env
```

## Update Environment Variable
### Variable Dictionary for `env/app.env`
Variable|Description
:---|:---
`DB_HOST`| The hostname of the database
`DB_USER`| The username to access the database
`DB_PASSWORD`| The password assigned to the user defined above
`DB_DATABASE`| The name of the database; this value should be the same as `MYSQL_DATABASE` defined in `env/database.env`
### Variable Dictionary for `env/database.env`
Variable|Description
:---|:---
`MYSQL_DATABASE`| The name of the database; this value should be the same as `DB_DATABASE` defined in `env/app.env`
`MYSQL_ROOT_PASSWORD`| The password of `'root'@'localhost'`
### Sample env File Input
If you just want to test the functionality of the system, you may simply copy and paste the following code into the corresponding file.
#### `env/app.env`
```
DB_HOST=database
DB_USER=appuser
DB_PASSWORD=Pa$$w0rd
DB_DATABASE=comp3335_project
```
#### `env/database.env`
```
MYSQL_DATABASE=comp3335_project
MYSQL_ROOT_PASSWORD=Pa$$w0rd
```
## Build and Start the Container
Execute the following command to build the start the container.
```bash
docker-compose build
docker-compose up -d
```
## Stop the Container
Execute the following command to stop the container.
```bash
docker-compose down
```
# Demonstration
https://youtu.be/XEoz1jKk9Sc