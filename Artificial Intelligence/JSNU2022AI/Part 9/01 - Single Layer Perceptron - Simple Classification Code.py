'''
01 - Single Layer Perceptron - Simple Classification Code
'''

# 1. Define the perceptron function where x is the input value
def perceptron(x):
    # 1.1 Set initial weight
    w = 0.5
    # 1.2 Set initial bias
    b = 0.1
    # 1.3 Calculate predicted value (weight * input + bias)
    y_hat = w * x + b
    # 1.4 Determine the prediction output
    if y_hat >= 0.0:
        return 1
    else:
        return 0

# 2. Call the perceptron
prediction = perceptron(-1)

print("The prediction is:", prediction)
