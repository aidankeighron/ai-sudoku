import numpy as np, pytest
from ai import Perceptron, test_perceptron

class TestPerceptron:
    def test_or_dataset(self):
        # OR dataset
        x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([[0], [1], [1], [1]])

        p = Perceptron(x.shape[1], alpha=0.1)
        p.fit(x, y, epochs=20)

        for (value, target) in zip(x, y):
            pred = p.predict(value)
            assert target[0] == pred

    def test_and_dataset(self):
        # OR dataset
        x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([[0], [0], [0], [1]])

        p = Perceptron(x.shape[1], alpha=0.1)
        p.fit(x, y, epochs=20)

        for (value, target) in zip(x, y):
            pred = p.predict(value)
            assert target[0] == pred

    def test_xor_dataset(self):
        # XOR dataset
        x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([[0], [1], [1], [0]])

        p = Perceptron(x.shape[1], alpha=0.1)
        p.fit(x, y, epochs=20)

        with pytest.raises(Exception):
            for (value, target) in zip(x, y):
                pred = p.predict(value)
                assert target[0] == pred