'''
Defines Graph class to be used for Graph SLAM algorithm
'''


'''
NOTES:
	- Check out https://github.com/RainerKuemmerle/g2o for graph optimization package
'''




# Define enum-type variables for nodes
POSE = 0
LANDMARK = 1

# Define enum-type variables for edges
MOTION = 0
MEASUREMENT = 1

class Graph:
	def __init__(self):
		self.nodes = {}	# dictionary of dictionaries, keys are node_id
		self.edges = {}	# dictionary of dictionaries, keys are edge_id
		self.node_id_counter = 0
		self.edge_id_counter = 0

	def add_node(self, type, coordinates):
		'''Add a node to the graph
		type (int): type of node being added, either ROBOT_POSITION or LANDMARK
		coordinates (tuple): x coord and y coord in NED frame
		'''
		node_id = self.node_id_counter
		self.node_id_counter += 1

		self.nodes[node_id] = {'type': node_type, 'coordinates': coordinates}

	def add_edge(self, type, node1, node2):
		'''Add an edge (constraint) to the graph
		type (int): type of edge being added, either MOTION or MEASUREMENT
		node1 (dictionary): one end of the edge
		node2 (dictionary): other end of the edge
		'''
		edge_id = self.edge_id_counter
		self.edge_id_counter += 1

		self.edges[edge_id] = {'type': edge_type}