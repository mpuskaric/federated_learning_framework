from concurrent import futures

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

REPLY="done_2"
PORT=4445

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("request received ... sending to top level node")
        #response = helloworld_pb2.HelloReply(message='%s!' % REPLY)
        with grpc.insecure_channel('localhost:4444') as channel:
            stub      = helloworld_pb2_grpc.GreeterStub(channel)
            request   = helloworld_pb2.HelloRequest(name=request.name)
            response2 = stub.SayHello(request)
        # return message to the client
        return helloworld_pb2.HelloReply(message='%s' % response2.message)

    def SayHelloAgain(self, request_iterator, context):
        for request in request_iterator:
            print("streaming: request from the client with the message %s" % request.name)
        response=helloworld_pb2.HelloReply(message='streaming: %s! ' % REPLY)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:4445')
    print("Server 2 is listening on port 4445 ...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
