# Projet programation spécialisée : Datastream avec python, MySQL et RabbitMQ 

# contributors of the projet
LHALOUI Aoulia - ABDELLAOUI Rachid

# introduction
This project concretizes the process of streaming data, commonly known as stream or data streaming,
is integrated into stream processing software to extract valuable information in real time.

# Objective  
The goal of the project is to create a real-time web server log analysis system using Python, MySQL and RabbitMQ. 
The system includes a Producer called logs-producer which reads a web-server-nginx.log log file line by line, publishes them in a topic type exchange, 
and sends them to two queue files, one called queue -data-lake and the other queue-data-clean.
The system also includes two consumers, the data-lake-consumer and the data-clean-consumer, which require each queue file differently in real time.

 # Prerequisite
•	Python
•	Docker
•	Docker compose

# Installation

Executor:
git clone https://github.com/MichDeRoanne/Project_RabbitMQ

python -m venv venv

pip install -r requirements.txt

# Configuration
A configuration of the environment variables in the .env file is necessary before the execution of the application.
Here are the variables to configure:
* Utilisation du conteneur rabbit MQ
RABBIT_USER=""   
RABBIT_PASSWORD=""

* Utilisation du conteneur MySQL
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_ROOT_PASSWORD=""

# Virtual environment
We worked in a virtual environment which is a mechanism that allows to separate the dependencies required by different projects by creating virtual environments that are isolated from each other.
The we created the RABBITMQ instance with the help of docker-composer and the file. .env we will execute the following command: __docker-compose --env-file .env -f docker-compose.yml -p data-stream up -d__

The script .env :

[<img src="Picture2.PNG" alt="Superset">](Picture2.PNG)

The script sets environment variables for different database and host IDs and passwords.
- RABBIT_USER: Sets the username of the RabbitMQ server (an open-source mail server).
- RABBIT_PASSWORD: Sets the password associated with the RabbitMQ user.
- MYSQL_ROOT_PASSWORD: Sets the root user password for the MySQL database. In this case, it is defined as "root".
- MYSQL_DATABASE: Defines the name of the MySQL database to use.
- MYSQL_USER: Defines the username to use to connect to the MySQL database.
- MYSQL_PASSWORD: Sets the password associated with the MySQL user.
- HOST: Sets the host address where the database is located.
- PORT: Defines the port to use to connect to the database.
- The docker-compose.yml script: This file is a configuration file for docker-compose, a tool for deploying and managing applications using Docker containers.

 The configuration file also creates a volume named RabbitMQ which will be used to store RabbitMQ service data.

* Architecture 

[<img src="Picture1.PNG" alt="Superset">](Picture1.PNG)


# The application
*The first step: RabbitMR
Run the python server.py file to create a connection to the server through a channel so that it can be used by producers and consume.
-- python server.py
*The 2nd step :  The web server
Run the python logs-producer.py file to create an exchange and queues. 
This will then allow the logs to be published in the queues and to be routed correctly using routing_key.
python logs-producer.py
*The 3rd step: the SQL database
Run the python consumer.py file to consume the logs pending in our two queues.
The logs will then be processed in FIFO (First In First Out) until the 2 queues are empty.
-- python consumer.py
For each queue, we apply specific processing before pushing a log into the database:
•	process_msg_data_clean: allows to 'parse' our log using functions and regular expressions (RegEx) for storage in a deformed way in base.
    It can thus be easily used for analysis, dashboard or ML purposes.
•	process_raw_message: allows us to store our raw log so as not to lose it.
    All processing functions are in the file models.py

* The 4th step :  Loading logs into the SQL database
To interact with the MySQL database, we use SQLAlchemy, an ORM. This kind of tool greatly simplifies the interface between the code and a database.

