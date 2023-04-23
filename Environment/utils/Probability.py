
prob = [0.8, 0.9, 0.95]

def compute_prob(dis):
    if 70<= dis < 200:
        return prob[0]
    elif 20<= dis < 70:
        return prob[1]
    return prob[2]