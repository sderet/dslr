import numpy as np
import describe
import sys

class LogisticRegression:
    def __init__(self, learning_rate, n_iters):
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.losses = []

    # Given a number X (which represents log(odds)), returns a value in between 0 and 1 which represents the probability
    # on the sigmoid function (with a nice S curve)
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Loss serves to determine the quality of the current weights and bias 
    # Calculated using Binary Cross Entropy
    def compute_loss(self, y_true, y_pred):
        epsilon = 1e-9

        # Gives quality of prediction for every True sample
        y1 = y_true * np.log(y_pred + epsilon)
        # Gives quality of prediction for every False sample
        y2 = (1-y_true) * np.log(1 - y_pred + epsilon)

        # Gives the (negative) mean of these for the overall quality of prediction
        return -np.mean(y1 + y2)

    # Calculates the a*x + b linear function in "sigmoid space" with a being our weights, b being our bias
    # and X being our full_dataset
    # The return will be an array of probabilities between 0 and 1
    def feed_forward(self, X):
        z = np.matmul(X, self.weights) + self.bias
        A = self.sigmoid(z)
        return A

    # y is an array of 1s and 0s, indicating whether the feature is True or False for any given sample
    # X is a 2D array of lines (samples) per columns (features) that can have any value
    # X might need to be normalized depending on the full_data, but as long as the values aren't too large it should be fine
    def fit(self, X, y):
        n_samples, n_features = X.shape

        # Initialize everything to 0 before training
        self.weights = np.zeros(n_features)
        self.bias = 0

        # gradient descent
        for _ in range(self.n_iters):
            # Get prediction with current weights
            A = self.feed_forward(X)
            # Calculate the loss (accuracy) of that prediction
            self.losses.append(self.compute_loss(y,A))

            dz = A - y # derivative of sigmoid and bce X.T*(A-y)

            # compute gradients
            dw = (1 / n_samples) * np.dot(X.T, dz)
            db = (1 / n_samples) * np.sum(dz)

            # Update weights and bias to go towards the local minimum
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    # Returns a prediction for each sample between 0 and 1
    def predict(self, X):
        y_hat = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(y_hat)
        #y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        
        return np.array(y_predicted)


if __name__ == "__main__":
    names, file_content, lines = describe.open_file(sys.argv[1])

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    houses_names = ["Gryffindor", "Ravenclaw", "Slytherin", "Hufflepuff"]

    full_data = np.array(split_lines)
    # Copy only the houses part of the data
    actual_houses = full_data[:, 1]

    # Delete all fields that don't have numerical values (name, dominant hand, etc...)
    full_data = np.delete(full_data, [0, 1, 2, 3, 4, 5], 1)
    # Make any field with missing data 0, which isn't ideal but necessary (?)
    full_data[full_data == ''] = 0
    full_data = np.array(full_data, dtype=float)
    # Normalize data between 0 and 10
    # This is because values going too high can be very complicated to compute (especially with exponentials)
    # and can cause trouble with the sigmoid function
    full_data = (full_data - full_data.min(0)) / (np.ptp(full_data, axis=0) / 10)

    predictions_list = []

    # Delete current contents of file
    open("weights.lgr", "w").close()

    # Test each house in one-vs-all
    for house_name in houses_names:
        # Set houses to either 0 or 1
        # 1 means it's the house we're currently evaluating, 0 means it's any other
        houses = np.array(actual_houses)
        houses[houses == house_name] = 1
        houses[houses != '1'] = 0
        houses = np.array(houses, dtype=float)

        regressor = LogisticRegression(learning_rate=0.0001, n_iters=10000)
        regressor.fit(full_data, houses)

        # Write to file
        # Format:
        # house, bias, [weights (comma-separated)]
        with open("weights.lgr", "a") as f:
            f.write(f'{house_name},{regressor.bias},{','.join(map(str, regressor.weights))}\n')

    print(f'Weights and bias have been written to weights.lgr.')

