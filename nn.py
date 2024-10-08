import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Input
import matplotlib.pyplot as plt
from numpy import ndarray
from typing import List
from board import Board
import numpy as np, json

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
    def __init__(self, layers, learning_rate=0.1):
        self.weights = []
        self.layers = layers
        self.learning_rate = learning_rate

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
            self.weights[layer] += -self.learning_rate * a[layer].T.dot(d[layer])

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
    nn = NeuralNetwork([2, 2, 1], learning_rate=0.5)
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    nn.fit(x, y, epochs=20000)

    for (value, target) in zip(x, y):
        pred = nn.predict(value)[0][0]
        step = 1 if pred > 0.5 else 0
        print(nn)
        print(f"[INFO] data={value}, ground-truth={target[0]}, pred={round(pred, 4)}, step={step}")

def run_nn():
    nn = NeuralNetwork([81, 160, 120, 100, 81], learning_rate=0.5)

    start_seed = 0
    end_seed = 1000
    training_data: List[Board] = [Board(difficulty=0.2, seed=i) for i in range(start_seed, end_seed)]
    print("Boards Generated")
    y = np.array(np.array([data.solve().get_board_1d() for data in training_data])/10, dtype=np.float64)
    print("Answer Generated")
    x = np.array(np.array([data.get_board_1d() for data in training_data])/10, dtype=np.float64)
    print("Data Generated")

    with open("data.json", "w") as f:
        json.dump({"data": x.tolist(), "answer": y.tolist(), "start_seed": start_seed, "end_seed": end_seed}, f)

    print("Training")
    nn.fit(x, y, epochs=5000)
    print("Training Done")

    testing_data: List[Board] = [Board(difficulty=0.2, seed=i) for i in range(end_seed, end_seed+5)]
    
    y = np.array(np.array([data.solve().get_board_1d() for data in testing_data])/10, dtype=np.float64)
    x = np.array(np.array([data.get_board_1d() for data in testing_data])/10, dtype=np.float64)

    for (value, target) in zip(x, y):
        pred = nn.predict(value)[0]
        ai_mse = mean_squared_error(target, pred)
        nothing_mse = mean_squared_error(target, value)
        print(f"[INFO], AI mse={np.round(ai_mse, 2)}, Nothing mse={np.round(nothing_mse, 2)}")

# test_nn()
# run_nn()

class Keras:
    def __init__(self, learning_rate=0.01):
        self.model = Sequential()
        # self.model.add(Dense(256, input_shape=(81,), activation="sigmoid"))
        self.model.add(Input(shape=(81,)))
        self.model.add(Dense(128, activation="sigmoid"))
        self.model.add(Dense(81, activation="softmax"))
        self.learning_rate = learning_rate

    def fit(self, train_x, train_y, test_x, test_y, epochs=5000):

        sgd = SGD(self.learning_rate)
        self.model.compile(loss="categorical_crossentropy", optimizer=sgd,
            metrics=["accuracy"])
        H = self.model.fit(train_x, train_y, validation_data=(test_x, test_y),
            epochs=epochs, batch_size=128)
        
        print("[INFO] evaluating network...")
        predictions = self.model.predict(test_x, batch_size=128)
        print(classification_report(test_y.argmax(axis=1), predictions.argmax(axis=1)))
        
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0, epochs), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, epochs), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, epochs), H.history["accuracy"], label="train_acc")
        plt.plot(np.arange(0, epochs), H.history["val_accuracy"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend()
        plt.savefig("plot.png")
        
def test_keras():
    keras = Keras(learning_rate=0.01)
    
    start_seed = 0
    end_seed = 1000

    training_data: List[Board] = [Board(difficulty=0.2, seed=i) for i in range(start_seed, end_seed)]
    print("Boards Generated")
    train_y = np.array(np.array([data.solve().get_board_1d() for data in training_data])/10, dtype=np.float64)
    print("Answer Generated")
    train_x = np.array(np.array([data.get_board_1d() for data in training_data])/10, dtype=np.float64)
    print("Data Generated")

    testing_data: List[Board] = [Board(difficulty=0.2, seed=i) for i in range(end_seed, end_seed+5)]
    test_y = np.array(np.array([data.solve().get_board_1d() for data in testing_data])/10, dtype=np.float64)
    test_x = np.array(np.array([data.get_board_1d() for data in testing_data])/10, dtype=np.float64)

    keras.fit(train_x, train_y, test_x, test_y, epochs=1000)

test_keras()