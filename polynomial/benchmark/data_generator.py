import numpy as np

def get_test_data():
    np.random.seed(42) # Фиксация seed для воспроизводимости [cite: 271]
    # 100к наборов: [a0, a1, a2, a3, a4] и x
    return [(np.random.rand(5).tolist(), np.random.rand()) for _ in range(100_000)]
