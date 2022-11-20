# comp3335-project
Conducted different Security Authentication and Authorization between the Application and Database based on the predicted Security Threats and Attacks. 



## Installation
Follow the step to create the env document and build up docker container.



### Step 1
Create and environment variable document and edit it.

```bash
cp env/app.env.example env/app.env
cp env/database.env.example env/database.env
```



### Step 2 
Enter the info for the environment variable.

Here are the example of environment variable in [app.env](https://github.com/tomakizu/comp3335-project/blob/master/env/app.env.example)

```
# Set the database hostname
DB_HOST     = database 

# Set the database username
DB_USER     = appuser 

# Set the password for the database
DB_PASSWORD = Pa$$w0rd

# Set the name of the database
DB_DATABASE = comp3335_project 
```



### Step 3 
And also enter the info for the environment variable database.
Here are the example of the [database.env](https://github.com/tomakizu/comp3335-project/blob/master/env/database.env.example)
```
# Set the database name 
MYSQL_DATABASE      = comp3335_project

# Set the root user password
MYSQL_ROOT_PASSWORD = Pa$$w0rd
```



### Step 4 
After finished Step 1-3, build and start the docker container.
Follow these comand
```bash
docker-compose build
docker-compose up -d
```



## Stop the service
You can using this comand to stop the docker container.
```bash
docker-compose down
```
