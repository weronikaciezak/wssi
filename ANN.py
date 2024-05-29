import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class Neuron:
    def __init__(self, n_inputs, bias=0., weights=None):
        self.b = bias
        if weights:
            self.ws = np.array(weights)
        else:
            self.ws = np.random.rand(n_inputs)

    def _f(self, x): 
        return max(x * .1, x)

    def __call__(self, xs):
        return self._f(xs @ self.ws + self.b)

class Layer:
    def __init__(self, n_neurons, n_inputs_per_neuron):
        self.neurons = [Neuron(n_inputs_per_neuron) for _ in range(n_neurons)]

    def __call__(self, inputs):
        return np.array([neuron(inputs) for neuron in self.neurons])

class NeuralNetwork:
    def __init__(self, layer_structure):
        self.layers = []
        for i in range(1, len(layer_structure)):
            self.layers.append(Layer(layer_structure[i], layer_structure[i-1]))

    def __call__(self, inputs):
        for layer in self.layers:
            inputs = layer(inputs)
        return inputs

def visualize_network(layer_structure):
    G = nx.DiGraph()

    for i, num_nodes in enumerate(layer_structure):
        for j in range(num_nodes):
            G.add_node(f'L{i}N{j}', layer=i, pos=(i, -j))

    for i in range(len(layer_structure) - 1):
        for j in range(layer_structure[i]):
            for k in range(layer_structure[i + 1]):
                G.add_edge(f'L{i}N{j}', f'L{i + 1}N{k}')

    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=5000, node_color='skyblue')
    plt.show()

layer_structure = [3, 4, 4, 1]
visualize_network(layer_structure)

nn = NeuralNetwork(layer_structure)
input_data = np.array([1.0, 0.5, -0.5])
output = nn(input_data)
print(f"Output: {output}")
