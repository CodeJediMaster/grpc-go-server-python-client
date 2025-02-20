package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time" // Added time package

	pb "server/proto/go"

	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedChatServiceServer
}

// ChatStream implements the bidirectional streaming RPC.
func (s *server) ChatStream(stream pb.ChatService_ChatStreamServer) error {
	firstMessageReceived := false // flag to start go routine once

	for {
		in, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		if !firstMessageReceived {
			firstMessageReceived = true
			// Start go routine to send a periodic message every 5 seconds.
			go func() {
				ticker := time.NewTicker(5 * time.Second)
				defer ticker.Stop()
				for range ticker.C {
					reply := &pb.ChatMessage{Message: "Periodic message from server"}
					if err := stream.Send(reply); err != nil {
						log.Printf("Error sending periodic message: %v", err)
						return
					}
				}
			}()
		}

		// Echo back the received message with a prefix.
		reply := &pb.ChatMessage{Message: "Echo: " + in.Message}
		if err := stream.Send(reply); err != nil {
			return err
		}
		log.Printf("Received: %s", in.Message)
	}
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterChatServiceServer(s, &server{})
	fmt.Println("gRPC server listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
