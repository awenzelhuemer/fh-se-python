import numpy as np

print(np.ones((2, 2), dtype=np.bool_))

a = np.random.randint(5, size=(3, 4))

b = np.ones((2,3))
print(b[:,2])
# print(np.rot90(a))

# print(np.matmul(a, np.rot90(a)))
# print(np.multiply(a, a))