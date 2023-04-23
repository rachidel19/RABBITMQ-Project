import hashlib
import pika
import mysql.connector
import re



# Opening a connection to RabbitMQ server

credentials = pika.PlainCredentials('root', 'richardroot')

parameters = pika.ConnectionParameters('localhost', credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# Declaring the queue

channel.queue_declare(queue='queue-data-lake')

# Defining a function to clean up the log line

def clean_log_line(log_line):
    # Remove any leading/trailing white space
    log_line = log_line.strip()

    # Extract the IP address from the log line
    ip_address = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', log_line).group(0)

    # Extract the timestamp from the log line
    timestamp = re.search('\[.*\]', log_line).group(0)

    # Extract the HTTP method from the log line
    http_method = re.search('\".*\"', log_line).group(0).split()[0]

    # Extract the URL from the log line
    url = re.search('\".*\"', log_line).group(0).split()[1]

    # Extract the status code from the log line
    status_code = re.search('\s\d{3}\s', log_line).group(0).strip()

# Combine the extracted fields into a new, cleaned up log line
    cleaned_log_line = f"{ip_address} {timestamp} \"{http_method} {url}\" {status_code}"

    return cleaned_log_line

# Defining a function to handle incoming messages

def callback(ch, method, properties, body):
    # Decode the message body from bytes to string
    log_line = body.decode('utf-8')
    

    # Clean up the log line
    cleaned_log_line = clean_log_line(log_line)

    # Insert the cleaned log line into the database
    cnx = mysql.connector.connect(user='root', password='passer', host='localhost', database='datastream')
    cursor = cnx.cursor()
    add_log = ("INSERT INTO raw_log "
           "(id, timestamp, log) "
           "VALUES (%s, %s, %s)")
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_log = (hashlib.sha256(cleaned_log_line.encode('utf-8')).hexdigest(), timestamp, cleaned_log_line)
    cursor.execute(add_log, data_log)
    cnx.commit()
    cursor.close()
    cnx.close()

    # Print a message to indicate that the log line has been processed
    print("log line is processed : " + log_line)

# Set up the consumer to receive messages from the queue
channel.basic_consume(queue='queue-data-lake', on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages...')
channel.start_consuming()
