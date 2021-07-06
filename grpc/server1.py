# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

from datetime import datetime

REPLY="done_1"
PORT=4444

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        msg=request.name
        print("request from the client with the message: %s" % msg)
        if (msg=="time"):
            return helloworld_pb2.HelloReply(message='%s' % time())
        else:
            return helloworld_pb2.HelloReply(message='%s' % refuse())
    def SayHelloAgain(self, request_iterator, context):
        for request in request_iterator:
            print("streaming: request from the client with the message %s" % request.name)
        response=helloworld_pb2.HelloReply(message='streaming: %s! ' % REPLY)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:4444')
    print("Server 1 is listening on port 4444 ...")
    server.start()
    server.wait_for_termination()

def time():
    now=datetime.now()
    return now.strftime("%H:%M:%S")

def refuse():
    return "time was not requested"

if __name__ == '__main__':
    serve()
