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

    def leaky_relu(self, x):
        return np.maximum(0.1 * x, x)

    def leaky_relu_derivative(self, x):
        return np.where(x > 0, 1, 0.1)

    def __call__(self, xs):
        self.input = xs
        self.z = xs @ self.ws + self.b
        self.output = self.leaky_relu(self.z)
        return self.output

    def backward(self, d_output):
        d_z = d_output * self.leaky_relu_derivative(self.z)
        self.d_ws = d_z * self.input
        self.d_b = d_z
        return d_z * self.ws

    def update(self, learning_rate):
        self.ws -= learning_rate * self.d_ws
        self.b -= learning_rate * self.d_b


class Layer:
    def __init__(self, n_neurons, n_inputs_per_neuron):
        self.neurons = [Neuron(n_inputs_per_neuron) for _ in range(n_neurons)]

    def __call__(self, inputs):
        self.inputs = inputs
        self.outputs = np.array([neuron(inputs) for neuron in self.neurons])
        return self.outputs

    def backward(self, d_outputs):
        d_inputs = np.zeros(self.inputs.shape)
        for i, neuron in enumerate(self.neurons):
            d_inputs += neuron.backward(d_outputs[i])
        return d_inputs

    def update(self, learning_rate):
        for neuron in self.neurons:
            neuron.update(learning_rate)


class NeuralNetwork:
    def __init__(self, layer_structure):
        self.layers = []
        for i in range(1, len(layer_structure)):
            self.layers.append(Layer(layer_structure[i], layer_structure[i-1]))

    def __call__(self, inputs):
        for layer in self.layers:
            inputs = layer(inputs)
        return inputs

    def backward(self, d_loss):
        for layer in reversed(self.layers):
            d_loss = layer.backward(d_loss)

    def update(self, learning_rate):
        for layer in self.layers:
            layer.update(learning_rate)

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            total_loss = 0
            for i in range(len(X)):
                output = self(X[i])
                loss = (output - y[i])**2
                total_loss += loss
                d_loss = 2 * (output - y[i])
                self.backward(d_loss)
                self.update(learning_rate)
            if epoch % 10 == 0:
                print(f'Epoch {epoch}, Loss: {np.mean(total_loss)}')

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

X = np.array([[1.0, 0.5, -0.5], [0.5, -1.5, 2.0], [-1.0, 2.0, 0.0]])
y = np.array([1.0, -1.0, 0.5])

nn.train(X, y, epochs=100, learning_rate=0.01)
