from board import Board
import numpy as np
from numpy import ndarray

class Perceptron:
    # Alpha usually 0.1 0.01 0.001
    def __init__(self, n, alpha=0.1):
        self.w = np.random.randn(n+1)/np.sqrt(n)
        self.alpha = alpha

    # Step function
    def step(self, x):
        return 1 if x > 0 else 0
    
    def fit(self, x, y, epochs=10):
        x = np.c_[x, np.ones((x.shape[0]))]

        for epochs in np.arange(0, epochs):
            for (value, target) in zip(x, y):
                p = self.step(np.dot(value, self.w))
                print(p)
                print(target)
                if p != target:
                    error = p - target
                    self.w += -self.alpha * error * value

    def predict(self, x, add_bias=True):
        x = np.atleast_2d(x)

        if add_bias:
            x = np.c_[x, np.ones((x.shape[0]))]

        return self.step(np.dot(x, self.w))

def test_perceptron():
    # OR dataset
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [1]])
    # AND dataset
    # x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # y = np.array([[0], [0], [0], [1]])
    # XOR dataset
    # x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # y = np.array([[0], [1], [1], [0]])

    p = Perceptron(x.shape[1], alpha=0.1)
    print("[INFO] training perceptron...")
    p.fit(x, y, epochs=20)

    print("[INFO] testing perceptron...")
    for (value, target) in zip(x, y):
        pred = p.predict(value)
        print(f"[INFO] data={value}, ground-truth={target[0]}, pred={pred}")
        
# test_perceptron()

class NeuralNetwork:
    def __init__(self, layers, alpha=0.1):
        self.weights = []
        self.layers = layers
        self.alpha = alpha

        for i in np.arange(0, len(layers)-2):
            w = np.random.randn(layers[i]+1, layers[i+1]+1)
            self.weights.append(w / np.sqrt(layers[i]))

        w = np.random.randn(layers[-2] + 1, layers[-1])
        self.weights.append(w / np.sqrt(layers[-2]))

    def __repr__(self) -> str:
        return f"NeuralNetwork: {'-'.join(str(l) for l in self.layers)}"

    def sigmoid(self, x: int) -> int:
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x: int) -> int:
        return x * (1 - x)

    def fit(self, x: ndarray, y: ndarray, epochs=100, display_update=100):
        x = np.c_[x, np.ones((x.shape[0]))]

        for epoch in np.arange(0, epochs):
            for (value, target) in zip(x, y):
                self.fit_partial(value, target)

            if epoch == 0 or (epoch+1) % display_update == 0:
                loss = self.calculate_loss(x, y)
                print(f"[INFO] epoch={epoch+1}, loss={round(loss, 5)}")
    
    def fit_partial(self, x, y):
        a = [np.atleast_2d(x)]

        for layer in np.arange(0, len(self.weights)):
            net = a[layer].dot(self.weights[layer])
            out = self.sigmoid(net)

            a.append(out)

        error = a[-1] - y
        d = [error * self.sigmoid_deriv(a[-1])]

        for layer in np.arange(len(a)-2, 0, -1):
            delta = d[-1].dot(self.weights[layer].T)
            delta = delta * self.sigmoid_deriv(a[layer])
            d.append(delta)

        d = d[::-1]

        for layer in np.arange(0, len(self.weights)):
            self.weights[layer] += -self.alpha * a[layer].T.dot(d[layer])

    def predict(self, x, add_bias=True):
        p = np.atleast_2d(x)

        if add_bias:
            p = np.c_[p, np.ones((p.shape[0]))]

        for layer in np.arange(0, len(self.weights)):
            p = self.sigmoid(np.dot(p, self.weights[layer]))

        return p

    def calculate_loss(self, x, target):
        target = np.atleast_2d(target)
        predictions = self.predict(x, add_bias=False)
        loss = 0.5 * np.sum((predictions-target) ** 2)

        return loss 

def test_nn():
    nn = NeuralNetwork([2, 2, 1], alpha=0.5)
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    nn.fit(x, y, epochs=20000)

    for (value, target) in zip(x, y):
        pred = nn.predict(value)[0][0]
        step = 1 if pred > 0.5 else 0
        print(nn)
        print(f"[INFO] data={value}, ground-truth={target[0]}, pred={round(pred, 4)}, step={step}")

def run_nn():
    nn = NeuralNetwork([81, 81, 18, 3], alpha=0.5)
    board = Board(difficulty=0.8, seed=1)

    y = np.array(np.array(board.possible_answers())/9, dtype=np.float64)
    x = np.array([np.array(board.get_board_1d())/9 for _ in range(len(y))], dtype=np.float64)

    nn.fit(x, y, epochs=5000)

    for (value, target) in zip(x, y):
        pred = nn.predict(value)[0]
        
        print(f"[INFO], answer={target*9}, out={np.round(pred*9, 2)}")

# test_nn()
run_nn()