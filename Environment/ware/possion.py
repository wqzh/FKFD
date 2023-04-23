
import numpy as np
from numpy import exp
import matplotlib.pyplot as plt

## possion 
def possion(lbd=1.5, n = 20):
    fact = [1,]
    for i in range(1, n): fact.append(i*fact[-1])
    fact = np.array(fact)
    lbd = np.array([lbd])
    x = np.arange(n)
    lambdak =  np.power(lbd, x)
    possion = exp(-lbd) * lambdak / fact
    
    plt.scatter(x, possion)
    plt.ylim(-0.01,0.4)
    plt.margins(0.01,0)
    plt.show()

def exponential(lbd, n = 20):
    x = np.linspace(0, 20, 200)
    p = lbd * exp(-lbd*x)
    plt.plot(x, p)
    plt.show()

# possion(1.5, 10)
# exponential(1.5)



