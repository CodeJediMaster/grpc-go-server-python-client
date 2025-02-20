import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

import grpc
import chat_pb2
import chat_pb2_grpc
import time
import threading
import queue

message_queue = queue.Queue()

def generate_messages():
    # Yields messages enqueued from other threads.
    while True:
        msg = message_queue.get()  # blocking on new message
        yield msg

def receive_responses(stub):
    # Handles response stream in a separate thread.
    responses = stub.ChatStream(generate_messages())
    for response in responses:
        print("Received from server:", response.message)

def send_messages():
    # Example: periodically send a "ping" message.
    while True:
        time.sleep(10)
        message_queue.put(chat_pb2.ChatMessage(message="ping"))

def main():
    # Create channel with keepalive options to maintain the connection.
    channel = grpc.insecure_channel(
        'localhost:50051',
        options=[
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', 1)
        ]
    )
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    
    # Enqueue initial subscription message.
    message_queue.put(chat_pb2.ChatMessage(message="subscribe"))
    
    # Start threads for receiving responses and sending messages.
    threading.Thread(target=receive_responses, args=(stub,), daemon=True).start()
    threading.Thread(target=send_messages, daemon=True).start()
    
    # Keep main thread alive.
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
