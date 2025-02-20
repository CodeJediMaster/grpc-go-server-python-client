import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

import grpc
import chat_pb2
import chat_pb2_grpc
import time

def generate_messages():
    # Send an initial subscription message.
    yield chat_pb2.ChatMessage(message="subscribe")
    # Keep generator open without sending additional messages.
    while True:
        time.sleep(1)
        # ...no yield...

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
    
    responses = stub.ChatStream(generate_messages())
    
    for response in responses:
        print("Received from server:", response.message)

if __name__ == '__main__':
    main()
