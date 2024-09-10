import numpy as np

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
        
test_perceptron()