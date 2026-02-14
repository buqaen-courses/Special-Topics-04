### Special Topics 
In this course, we will work with some **new technology** such as *gRPC*/*AI Coding*/ 

> AI coding Helps us to ... 

#### Quick Start (gRPC + AI coding)

Prerequisites
- Install protoc and runtime (Go/Python/Node) and the gRPC plugin for your language.
- Familiarity with your chosen language's package manager.

Minimal proto (save as todo.proto)
```proto
syntax = "proto3";
package todo;

service Todo {
    rpc Add (TodoItem) returns (TodoResp);
}

message TodoItem { string text = 1; }
message TodoResp { bool ok = 1; }
```

Generate stubs (examples)
- Go: protoc --go_out=. --go-grpc_out=. todo.proto
- Python: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto

Server sketch (Python)
```py
import grpc, todo_pb2, todo_pb2_grpc

class TodoServicer(todo_pb2_grpc.TodoServicer):
        def Add(self, request, context):
                return todo_pb2.TodoResp(ok=True)

# bind server to port 50051 and start (omitted boilerplate)
```

Client sketch (Python)
```py
import grpc, todo_pb2, todo_pb2_grpc

with grpc.insecure_channel('localhost:50051') as ch:
        stub = todo_pb2_grpc.TodoStub(ch)
        resp = stub.Add(todo_pb2.TodoItem(text="Example"))
        print(resp.ok)
```

AI coding tips (practical)
- Give the model a clear goal, input/output examples, and constraints.
- Start with a small prompt and ask for tests or edge cases.
- Iterate: review generated code, run tests, and request fixes for failing cases.
- Validate security, input handling, and dependencies before merging.

Next steps
- Add error handling, authentication, and protobuf versioning.
- Write unit/integration tests for server and client interactions.
- Use CI to regenerate stubs and run tests automatically.
## Comparison Table

| Feature | gRPC | REST API |
|---------|------|----------|
| Protocol | HTTP/2 | HTTP/1.1 |
| Serialization | Protocol Buffers | JSON |
| Performance | High | Moderate |
| Learning Curve | Steep | Gentle |

## Architecture Diagram

```
┌─────────────┐         gRPC          ┌─────────────┐
│   Client    │◄──────────────────►   │   Server    │
│  (Python)   │   (Protocol Buffers)  │  (Python)   │
└─────────────┘                       └─────────────┘
    │                                     │
    └──────── Port 50051 ────────────────┘
```

## AI Coding Workflow

| Stage | Action | Tools |
|-------|--------|-------|
| 1. Design | Define proto schema | protoc |
| 2. Generate | Create stubs | grpc-tools |
| 3. Implement | Code server/client | IDE + Copilot |
| 4. Test | Validate functionality | pytest |
| 5. Deploy | Release to production | CI/CD |
