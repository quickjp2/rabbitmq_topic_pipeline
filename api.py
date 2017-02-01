import os, json, hvac, ast, pika, random
from flask import Flask, request, jsonify
from os import environ as env

app = Flask(__name__)
port = int(os.getenv('PORT',8080))
host = os.getenv('HOST',"localhost")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

@app.route('/')
def hello():
    return "Welcome"

@app.route('/bear/method_one')
def bear_method_one():
    print ("Bearing method one")
    routing_key = 'request.bear.method_one'
    message = "This is a test"
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)
    return " [x] Sent %r:%r" % (routing_key, message)

@app.route('/fox/method_one')
def fox_method_one():
    print ("Fox method one")
    routing_key = 'request.fox.method_one'
    message = "This is a test"
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)
    return " [x] Sent %r:%r" % (routing_key, message)

@app.route('/bear/method_two')
def bear_method_two():
    print ("Bearing method two")
    routing_key = 'request.bear.method_two'
    message = "This is a test"
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)
    return " [x] Sent %r:%r" % (routing_key, message)

@app.route('/fox/method_two')
def fox_method_two():
    print ("Fox method two")
    routing_key = 'request.fox.method_two'
    message = "This is a test"
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)
    return " [x] Sent %r:%r" % (routing_key, message)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=port)

    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        connection.close()
