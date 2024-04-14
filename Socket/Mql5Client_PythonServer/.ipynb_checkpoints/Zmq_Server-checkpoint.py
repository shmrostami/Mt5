# https://zeromq.org/languages/python/
# https://github.com/dingmaotu/mql-zmq#introduction

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message_recv = socket.recv()
    print("Received request: %s" % message_recv)

    #  Do some 'work'
    #time.sleep(1)
    
    message_recv = "{}-OK".format(message_recv);    
    #  Send reply back to client
    socket.send_string(message_recv)
