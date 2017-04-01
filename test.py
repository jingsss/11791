import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

class StanfordNLP:
	def __init__(self):
		self.server = ServerProxy(JsonRpc20(),TransportTcpIp(addr=("127.0.0.1", 9000)))
	def parse(self, text):
		return json.loads(self.server.parse(text))

nlp = StanfordNLP()
#result = nlp.parse("CMU is a university. It is a big university")
result = nlp.parse("Architecturally, the school has a Catholic character. Atop the Main Building's gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend \"Venite Ad Me Omnes\". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.")
print result
#for a in result['coref'][0]:
#  print a

#
#from nltk.tree import Tree
#tree = Tree.parse(result['sentences'][0]['parsetree'])
#pprint(tree)
