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
    # and X being our dataset
    # The return will be an array of probabilities between 0 and 1
    def feed_forward(self, X):
        z = np.matmul(X, self.weights) + self.bias
        A = self.sigmoid(z)
        return A

    # y is an array of 1s and 0s, indicating whether the feature is True or False for any given sample
    # X is a 2D array of lines (samples) per columns (features) that can have any value
    # X might need to be normalized depending on the data, but as long as the values aren't too high it should be fine
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
            # update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        y_hat = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(y_hat)
        #y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        
        return np.array(y_predicted)

    def accuracy(self,y, y_hat):
        accuracy = np.sum(y == y_hat) / len(y)
        return accuracy


def confusion_matrix(y_actual, y_predicted):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    epsilon = 1e-9
    for i in range(len(y_actual)):
        if y_actual[i] > 0:
            if y_predicted[i] > 0.5:
                tp = tp + 1
            else:
                fn = fn + 1
        if y_actual[i] < 1:
            if y_predicted[i] < 0.5:
                tn = tn + 1
            else:
                fp = fp + 1

    cm = [[tp, fp], [tn, fn]]
    accuracy = (tp+tn)/(tp+tn+fp+fn+epsilon)
    sens = tp/(tp+fn+epsilon)
    prec = tp/(tp+fp+epsilon)
    f_score = (2*prec*sens)/(prec+sens+epsilon)
    return cm,accuracy,sens,prec,f_score



if __name__ == "__main__":
    names, file_content, lines = describe.open_file(sys.argv[1])

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    houses_names = ["Gryffindor", "Ravenclaw", "Slytherin", "Hufflepuff"]

    base_nplines = np.array(split_lines)

    full_predictions = []

    # Copy only the houses
    houses_base = base_nplines[:, 1]

    for house_name in houses_names:
        houses = np.array(houses_base)
        houses[houses == house_name] = 1
        houses[houses != '1'] = 0
        houses = np.array(houses, dtype=float)

        nplines = np.array(base_nplines)
        nplines = np.delete(nplines, [0, 1, 2, 3, 4, 5], 1)
        nplines[nplines == ''] = 0
        nplines = np.array(nplines, dtype=float)

        #print(nplines[0])
        nplines = (nplines - nplines.min(0)) / (np.ptp(nplines, axis=0) / 10)
        #print(nplines[0])

        regressor = LogisticRegression(learning_rate=0.0001, n_iters=10000)
        regressor.fit(nplines, houses)

        predictions = regressor.predict(nplines)
        #print(house_name)
        #cm ,accuracy,sens,precision,f_score  = confusion_matrix(np.asarray(houses), np.asarray(predictions))
        #print("Test accuracy: {0:.3f}".format(accuracy))
        #print("Confusion Matrix:")
        #print(np.array(cm))

        full_predictions.append(predictions)

        #print(predictions[predictions > 0.5])

    full_predictions = np.array(full_predictions).argmax(axis=0)
    final_predictions = []
    for prediction in full_predictions:
        final_predictions.append(houses_names[prediction])

    errors = np.where(final_predictions != base_nplines[:, 1])

    for error in errors[0]:
        print("Error: found", final_predictions[error], "where it was", base_nplines[:, 1][error], "on index", error)
    
    print("Error rate:", f'{(len(errors[0]) / len(base_nplines)) * 100: .2f}', "%")

    #print(regressor.losses[0], regressor.losses[-1])
    #print(regressor.weights, regressor.bias, regressor.losses)