import numpy as np


def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)


class RNN:
    def __init__(self, input_space = 5, move_space=6, hidden_dim=3, bptt_truncate=4):
        # Assign instance variables
        self.move_space = move_space
        self.input_space = input_space
        self.hidden_dim = hidden_dim
        self.bptt_truncate = bptt_truncate
        # Randomly initialize the network parameters
        self.U = np.random.uniform(-np.sqrt(1./input_space), np.sqrt(1./input_space), (hidden_dim, input_space))
        self.V = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (move_space, hidden_dim))
        self.W = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (hidden_dim, hidden_dim))
        self.s = np.zeros((2, hidden_dim))

    def forward_propagation(self, x):
        # The total number of time steps
        T = len(x)
        # During forward propagation we save all hidden states in s because need them later.
        # We add one additional element for the initial hidden, which we set to 0
        s = np.zeros((T+1, self.hidden_dim))
        s[-1] = np.zeros(self.hidden_dim)

        if np.all(self.s == 0):
            pass
        else:
            self.s[-1] = self.s[0]
            s[0] = np.zeros(self.hidden_dim) 
            s = self.s
        # The outputs at each time step. Again, we save them for later.
        o = np.zeros((T, self.move_space))
        # For each time step...
        for t in np.arange(T):
            # Note that we are indxing U by x[t]. This is the same as multiplying U with a one-hot vector.
            s[t] = np.tanh(self.U.dot(x[t]) + self.W.dot(s[1]))
            o[t] = softmax(self.V.dot(s[t]))
        return [o, s]

    def predict(self, x):
        # Perform forward propagation and return index of the highest score
        o, s = self.forward_propagation(x)
        self.s = s
        return np.argmax(o, axis=1)
