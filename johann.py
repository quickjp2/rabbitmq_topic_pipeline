import pika
import sys
import os
import random
from os import environ as env

host = os.getenv('HOST',"localhost")
request_list = []

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = ["request.#"]
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def router(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    routing_key = method.routing_key.split('.',1)
    new_key = routing_key[1]
    checker = new_key.split('.')
    if checker[0] == 'id':
        if int(checker[1]) in request_list:
            # print("Request %r came through!" % checker[1])
            request_list.remove(int(checker[1]))
            # print(body)
    elif 'bear' in checker[0]:
        request_id = random.randint(1000000000,9999999999)
        request_list.append(request_id)
        reply_to = "request.id."+str(request_id)
        channel.basic_publish(exchange='topic_logs',
                              routing_key=new_key,
                              properties=pika.BasicProperties(reply_to = reply_to),
                              body=body)
    elif 'fox' in checker[0]:
        request_id = random.randint(1000000000,9999999999)
        request_list.append(request_id)
        reply_to = "request.id."+str(request_id)
        channel.basic_publish(exchange='topic_logs',
                              routing_key=new_key,
                              properties=pika.BasicProperties(reply_to = reply_to),
                              body=body)

channel.basic_consume(router,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
