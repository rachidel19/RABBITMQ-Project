import mysql.connector
import pika
import re

# Step1 Connecting to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="toor123",
  database="Streamingdata"
)

mycursor = mydb.cursor()

# Step2 Defining callback function to process messages
def process_message(channel, method, properties, body):
    # Extract data from log line
    log_line = body.decode('utf-8')
    log_data = re.search(r'^(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+|-) "(.*?)" "(.*?)"$', log_line)
    if log_data:
        ip, client_id, user, timestamp, request, status_code, bytes_sent, referrer, user_agent = log_data.groups()
        # Insert data into MySQL database
        sql = "INSERT INTO raw_log (ip, client_id, user, timestamp, request, status_code, bytes_sent, referrer, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (ip, client_id, user, timestamp, request, status_code, bytes_sent, referrer, user_agent)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print('Invalid log line:', log_line)

# Step3 Connecting to RabbitMQ server

credentials = pika.PlainCredentials('root', 'richardroot')
parameters = pika.ConnectionParameters('localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Step4 Creating exchange and bind to queues
channel.exchange_declare(exchange='logs', exchange_type='topic')
channel.queue_declare(queue='queue-data-lake', durable=False)
channel.queue_bind(exchange='logs', queue='queue-data-lake', routing_key='logs')
channel.queue_declare(queue='queue-data-clean', durable=False)
channel.queue_bind(exchange='logs', queue='queue-data-clean', routing_key='logs')

# Step5 Creating producer to read log file and publish to exchange
with open('assets/web-server-nginx.log') as log_file:
    for line in log_file:
        channel.basic_publish(exchange='logs', routing_key='logs', body=line.encode('utf-8'))
        print("Sent log line:", line.strip())

# Step6 Creating consumer to process messages from queue-data-lake
channel.basic_consume(queue='queue-data-lake', on_message_callback=process_message, auto_ack=True)
print('Attente des messages ')
channel.start_consuming()
