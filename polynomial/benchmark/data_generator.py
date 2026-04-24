import numpy as np

def get_test_data():
    np.random.seed(42)
    return [(np.random.rand(5).tolist(), np.random.rand()) for _ in range(100_000)]
