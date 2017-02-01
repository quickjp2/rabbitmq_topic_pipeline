import pika
import sys
import os
import time
import random
from os import environ as env

host = os.getenv('HOST',"localhost")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = ["fox.#"]
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

# Processes without extra help
def method_one():
    time.sleep(5)
    return "Method One from the fox!!!"
# Processes with potential extra help
def method_two(return_to=None):
    time.sleep(5)
    return "Method Two from the fox!!!"

def method_router(ch, method, props, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    routing_key = method.routing_key.split(".",3)
    if 'method_one' in routing_key[1]:
        response = method_one()
        ch.basic_publish(exchange='topic_logs',routing_key=props.reply_to,
                         body=response)
    elif 'method_two' in routing_key[1]:
        response = method_two()
        ch.basic_publish(exchange='topic_logs',routing_key=props.reply_to,
                         body=response)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(method_router,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
