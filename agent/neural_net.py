# agent/neural_net.py
#
# Description:
# This module defines a simple feedforward neural network class. This network
# is intended to serve as the "brain" for agents, taking in environmental
# observations and internal state, and outputting decisions that drive the
# agent's behavior. This file provides the basic structure for the network,
# which will be trained externally using reinforcement learning.
#
# Key responsibilities of this file:
# - Define a `NeuralNetwork` class capable of forward propagation.
# - Hold the weights and biases of the network's layers.
# - Implement a simple activation function.
# - Provide a method to compute the network's output given an input vector.
# - (Future) Include methods for loading/saving weights, and potentially
#   basic training functionalities or integration points for training libraries.
#
# Design Philosophy/Notes:
# - Keep the network structure simple initially (e.g., one hidden layer).
# - Use a common activation function like Sigmoid or ReLU.
# - The network design must align with the defined observation and action spaces
#   expected by `agent.behavior`.
# - This class represents *one instance* of a network, which will be held by
#   each agent or type of agent.

# Imports Description:
# This section lists the modules imported by agent/neural_net.py and their purpose.
# - numpy: Standard library for numerical operations, especially matrix/vector math required for neural network calculations.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Class: NeuralNetwork
# Description:
# Represents a simple feedforward neural network. It consists of an input layer,
# one hidden layer, and an output layer. It stores the weights and biases for
# the connections between these layers. The network's size is determined by
# the dimensions of the input and output vectors, and the number of neurons
# in the hidden layer.
#
# Attributes:
# - input_size (int): The number of inputs the network expects.
# - hidden_size (int): The number of neurons in the hidden layer.
# - output_size (int): The number of outputs the network produces.
# - weights_input_hidden (numpy.ndarray): Matrix of weights connecting the input layer to the hidden layer.
# - bias_hidden (numpy.ndarray): Vector of biases for the hidden layer neurons.
# - weights_hidden_output (numpy.ndarray): Matrix of weights connecting the hidden layer to the output layer.
# - bias_output (numpy.ndarray): Vector of biases for the output layer neurons.
#
# Primary Role: Evaluate observations to produce behavioral decisions.

# 1.1 Method: __init__
# Description:
# Constructor for the NeuralNetwork class. Initializes the network structure
# based on input, hidden, and output sizes, and initializes the weights and
# biases. Weights are typically initialized with small random values, and biases
# can be initialized to zeros or small values.
# Inputs:
#   - self: The instance being initialized.
#   - input_size: The expected dimension of the input observation vector. Type: int.
#                 Origin: Determined by the defined observation space (e.g., size of the array from `get_observation`).
#                 Restrictions: Must be a positive integer.
#   - hidden_size: The number of neurons in the hidden layer. Type: int.
#                  Origin: A design choice (e.g., 8, 16, 32).
#                  Restrictions: Must be a positive integer.
#   - output_size: The dimension of the output vector, corresponding to the action space. Type: int.
#                  Origin: Determined by the defined action space (e.g., 1 for binary choice, number of states).
#                  Restrictions: Must be a positive integer.
# Where Inputs Typically Come From: Called by `Agent.__init__` when creating an agent.
# Restrictions on Inputs: All sizes should be positive integers.
# Other Relevant Info: Initializes weights and biases using NumPy's random functions.
#
# Description of Algorithm/Process:
# 1. Store `input_size`, `hidden_size`, and `output_size` as instance attributes.
# 2. Initialize `weights_input_hidden` as a NumPy array of shape `(input_size, hidden_size)` with random small values (e.g., using `numpy.random.randn`). Multiply by a small factor (like 0.01) to keep initial values small.
# 3. Initialize `bias_hidden` as a NumPy array of shape `(1, hidden_size)` (or `(hidden_size,)`) with zeros.
# 4. Initialize `weights_hidden_output` as a NumPy array of shape `(hidden_size, output_size)` with random small values.
# 5. Initialize `bias_output` as a NumPy array of shape `(1, output_size)` (or `(output_size,)`) with zeros.
#
# Description of Output:
# None. Side effect is initializing the network's structure (sizes) and parameters (weights, biases).

# 1.2 Method: _sigmoid (Helper)
# Description:
# Implements the sigmoid activation function, applied to the output of neurons
# in the hidden layer (and potentially the output layer, depending on the
# interpretation of the output).
# Inputs:
#   - x: The input value or array/vector to apply the sigmoid function to. Type: numpy.ndarray or float.
#        Origin: Output of a layer calculation.
#        Restrictions: Can be any real number or array of real numbers.
# Where Inputs Typically Come From: Called internally by the `forward` method.
# Restrictions on Inputs: None.
# Other Relevant Info: The sigmoid function squashes values between 0 and 1.
#
# Description of Algorithm/Process:
# 1. Calculate `1 / (1 + numpy.exp(-x))`.
# 2. Return the result.
#
# Description of Output:
# The sigmoid of the input. Type: numpy.ndarray or float.
# Output Range: (0, 1).

# 1.3 Method: forward
# Description:
# Performs a forward pass through the neural network. Takes an input observation
# vector and computes the network's output vector by applying weights, biases,
# and activation functions through the layers.
# Inputs:
#   - self: The NeuralNetwork instance.
#   - input_data: The input observation vector for the network. Type: numpy.ndarray.
#                 Origin: Generated by the agent's sensing/observation logic (`get_observation`).
#                 Restrictions: Must be a NumPy array of shape `(1, input_size)` or `(input_size,)`.
# Where Inputs Typically Come From: Called by `Agent.update` (or potentially a function it calls).
# Restrictions on Inputs: The shape must match `self.input_size`.
# Other Relevant Info: Performs matrix multiplications (`numpy.dot`) and applies activation functions.
#
# Description of Algorithm/Process:
# 1. Calculate the output of the hidden layer *before* activation: `hidden_output_pre_activation = numpy.dot(input_data, self.weights_input_hidden) + self.bias_hidden`.
# 2. Apply the sigmoid activation function to the hidden layer output: `hidden_output_post_activation = self._sigmoid(hidden_output_pre_activation)`.
# 3. Calculate the output of the output layer *before* activation: `output_pre_activation = numpy.dot(hidden_output_post_activation, self.weights_hidden_output) + self.bias_output`.
# 4. (Optional) Apply an activation function to the output layer depending on the action space. For a binary decision (Wandering/Seeking), sigmoid is suitable. For choosing one of many states (classification), softmax is typical. For simplicity with 2 states, let's apply sigmoid to get a value between 0 and 1. `output_post_activation = self._sigmoid(output_pre_activation)`.
# 5. Return the final output vector.
#
# Description of Output:
# The network's output vector. Type: numpy.ndarray.
# Output Range: For a single sigmoid output, (0, 1). For multiple outputs with sigmoid, element-wise (0, 1). For softmax, outputs sum to 1.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import numpy as np # Use np alias as is common practice


### 1. Class: NeuralNetwork Implementation ###
class NeuralNetwork:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initializes a simple feedforward neural network with one hidden layer.
        Weights and biases are initialized randomly.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights and biases
        # Weights connecting input to hidden layer
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01
        self.bias_hidden = np.zeros((1, hidden_size)) # Bias for hidden layer

        # Weights connecting hidden layer to output layer
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01
        self.bias_output = np.zeros((1, output_size)) # Bias for output layer

        # Optional: Store learning rate and other RL parameters here later


    ### 1.2 Method: _sigmoid (Helper) Implementation ###
    def _sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    # Optional: Could add other activation functions like ReLU here


    ### 1.3 Method: forward Implementation ###
    def forward(self, input_data):
        """
        Performs a forward pass through the network.
        Expects input_data to be a numpy array (1, input_size).
        Returns output numpy array (1, output_size).
        """
        # Ensure input data is a numpy array and has the correct shape (handle (input_size,) vs (1, input_size))
        input_data = np.atleast_2d(input_data) # Ensure it's at least 2D, like (1, size)
        if input_data.shape[1] != self.input_size:
            raise ValueError(f"Input data shape {input_data.shape} mismatch with input size {self.input_size}")

        # Calculate output of hidden layer before activation
        hidden_output_pre_activation = np.dot(input_data, self.weights_input_hidden) + self.bias_hidden

        # Apply activation function to hidden layer
        hidden_output_post_activation = self._sigmoid(hidden_output_pre_activation)

        # Calculate output of output layer before activation
        output_pre_activation = np.dot(hidden_output_post_activation, self.weights_hidden_output) + self.bias_output

        # Apply activation function to output layer (e.g., sigmoid for binary/value output)
        final_output = self._sigmoid(output_pre_activation) # Use sigmoid for a single output between 0 and 1

        return final_output


# --- END CODE IMPLEMENTATION ---