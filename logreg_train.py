import numpy as np
import describe
import argparse

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


def get_mean_per_house(house_name, data, houses):
    means = []
    is_nan = np.isnan(data)

    for column in range(len(data[0])):
        total = 0
        count = 0
        for index, line in enumerate(data):
            if (houses[index] == house_name and not is_nan[index][column] and line[column] and line[column] != np.nan):
                try:
                    total += float(line[column])
                    count += 1
                except ValueError:
                    total = "NaN"
                    break
        try:
            means.append(total / count)
        except TypeError:
            means.append(np.nan)
            
    return (means)


def main(file_to_train, dest_file="weights.lgr", verbose=False):
    dest_file = "weights.lgr" if dest_file is None else dest_file

    names, file_content, lines = describe.open_file(file_to_train)

    if not lines:
        exit()

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    houses_names = ["Gryffindor", "Ravenclaw", "Slytherin", "Hufflepuff"]

    full_data = np.array(split_lines)
    # Copy only the houses part of the data
    actual_houses = full_data[:, 1]

    # Delete all fields that don't have numerical values (name, dominant hand, etc...)
    full_data = np.delete(full_data, [0, 1, 2, 3, 4, 5, 15, 16], 1)

    # Here we set unknown values to the mean of their respective features among their own house
    full_data[full_data == ''] = np.nan
    full_data = np.array(full_data, dtype=float)
    for house_name in houses_names:
        # Get the column means for the specific house
        col_mean = get_mean_per_house(house_name, full_data, actual_houses)
        # Find the indices of NaNs
        inds = np.where(np.isnan(full_data))
        # Replace them with the mean
        full_data[inds] = np.take(col_mean, inds[1])

    full_data = np.array(full_data, dtype=float)
    # Normalize data between 0 and 10
    # This is because values going too high can be very complicated to compute (especially with exponentials)
    # and can cause trouble with the sigmoid function
    full_data = (full_data - full_data.min(0)) / (np.ptp(full_data, axis=0) / 10)

    # Delete current contents of file
    open(dest_file, "w").close()

    # Test each house in one-vs-all
    for house_name in houses_names:
        # Set houses to either 0 or 1
        # 1 means it's the house we're currently evaluating, 0 means it's any other
        houses = np.array(actual_houses)
        houses[houses == house_name] = 1
        houses[houses != '1'] = 0
        houses = np.array(houses, dtype=float)

        regressor = LogisticRegression(learning_rate=0.001, n_iters=10000)
        regressor.fit(full_data, houses)

        # Write to file
        # Format:
        # house, bias, [weights (comma-separated)]
        with open(dest_file, "a") as f:
            f.write(f'{house_name},{regressor.bias},{','.join(map(str, regressor.weights))}\n')
        if (verbose):
            print(f'Training done for {house_name}')

    print(f'Weights and bias have been written to weights.lgr')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_to_train", help="the file in .csv format to train off of")
    parser.add_argument("-d", "--destination", default="weights.lgr", help="the destination file to create containing the weights and biases")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    main(args.file_to_train, args.destination, args.verbose)