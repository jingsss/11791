import jsonrpc
from simplejson import loads
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                             jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))

sentence1 = "University of Michigan is a large university. It is one of the largerst universities in U.S."
result = loads(server.parse(sentence1))
print result['coref']