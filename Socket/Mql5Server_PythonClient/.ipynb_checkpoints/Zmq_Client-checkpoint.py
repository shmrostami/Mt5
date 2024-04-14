import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

#  Do 10 requests, waiting each time for a response
#while True:
socket.send(b"Hello")

#  Get the reply.
message = socket.recv()
print(message)
