Project: grpc-go-server-python-client

Overview:
  This project demonstrates a bidirectional gRPC server in Go and a Python client that communicates via a streaming API.
  
Prerequisites:
  - Go (for the server)
  - Python 3.x (for the client)
  - Protocol Buffers compiler (protoc)
  - gRPC and protobuf libraries for both Go and Python

Setup:
  1. Generate Protobuf code:
     - For Go:
       $ protoc --go_out=plugins=grpc:./server/proto/go server/proto/chat.proto
     - For Python:
       $ python -m grpc_tools.protoc -Iserver/proto --python_out=client/python --grpc_python_out=client/python server/proto/chat.proto

  2. Build and run the gRPC server:
     - Navigate to the server directory.
     - Run:
       $ go run main.go

  3. Run the Python client:
     - Navigate to the client directory.
     - Run:
       $ python main.py

Notes:
  - The server sends periodic messages every 5 seconds upon the first client message.
  - The Python client uses a keepalive configuration to maintain the connection.

# ...existing content...
