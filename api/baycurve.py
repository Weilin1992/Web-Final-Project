import numpy as np
from math import pow

def train(x, y, alpha, beta, M):
    N = x.size
    s = np.zeros((M+1, M+1))
    phi = np.zeros((M+1, 1))
    for i in range(N):
        v = ph(x[i], M)
        s = s + np.dot(v, np.transpose(v))
        phi = phi + v*y[i]
    s = alpha * np.eye(M+1) + beta * s
    s = np.matrix(s).I
    return (s, phi)

def ph(x, M):
    v = np.ones((M+1, 1));
    for i in range(M+1):
        v[i] = pow(x, i)
    return v

def test(x, s, phi, beta):
    M = phi.size -1
    y = np.ones((1, x.size))
    for i in range(x.size):
        v = ph(x[i], M)
        y[0,i] = beta * np.dot(np.dot(np.transpose(v), s), phi)
    return y

