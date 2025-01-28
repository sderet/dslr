import numpy as np
import describe
import argparse

# Given a number X (which represents log(odds)), returns a value in between 0 and 1 which represents the probability
# on the sigmoid function (with a nice S curve)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Returns a prediction for each sample between 0 and 1
def predict(X, weights, bias):
    y_hat = np.dot(X, weights) + bias
    y_predicted = sigmoid(y_hat)

    return np.array(y_predicted)


def open_weights_file(weights_file):
    try:
        with open(weights_file, 'r') as fd:
            content = fd.read()
    except FileNotFoundError:
        print(f"{weights_file}: File not found.")
        return False
    
    return content.split('\n')

def get_mean(data):
    means = []
    is_nan = np.isnan(data)

    for column in range(len(data[0])):
        total = 0
        count = 0
        for index, line in enumerate(data):
            if (not is_nan[index][column] and line[column] and line[column] != np.nan):
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


def main(file_to_test, weights_file, dest_file="houses.csv", verbose=False):
    dest_file = "houses.csv" if dest_file is None else dest_file

    names, file_content, lines = describe.open_file(file_to_test)

    if not lines:
        exit()

    raw_weights = open_weights_file(weights_file)
    if not raw_weights:
        exit()

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    full_data = np.array(split_lines)
    # Delete all fields that don't have numerical values (name, dominant hand, etc...)
    full_data = np.delete(full_data, [0, 1, 2, 3, 4, 5, 15, 16], 1)

    # Here we set unknown values to the mean of their respective features among their own house
    full_data[full_data == ''] = np.nan
    full_data = np.array(full_data, dtype=float)
    # Get the column means for the specific house
    col_mean = get_mean(full_data)
    # Find the indices of NaNs
    inds = np.where(np.isnan(full_data))
    # Replace them with the mean
    full_data[inds] = np.take(col_mean, inds[1])


    full_data = np.array(full_data, dtype=float)
    # Normalize data between 0 and 10
    # This is because values get normalized before training
    full_data = (full_data - full_data.min(0)) / (np.ptp(full_data, axis=0) / 10)
        
    weights = {}
    houses_names = []
    for line in raw_weights:
        split_weights = line.split(",")
        if split_weights[0]:
            houses_names.append(split_weights[0])
            weights[split_weights[0]] = {
                "bias": float(split_weights[1]),
                "weights": np.array(split_weights[2:], dtype=float)
            }
    
    full_predictions = []
    
    for house in weights.keys():
        full_predictions.append(predict(full_data, weights[house]["weights"], weights[house]["bias"]))
        if verbose:
            print(f'Prediction done for {house}')

    with open(dest_file, "w") as f:
        f.write(f'Index,Hogwarts House\n')

    full_predictions = np.array(full_predictions).argmax(axis=0)
    for index, house_index in enumerate(full_predictions):
        with open(dest_file, "a") as f:
            f.write(f'{index},{houses_names[house_index]}\n')

    if verbose:
        print(f'Predictions written to {dest_file}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_to_test", help="the file in .csv format to predict values for")
    parser.add_argument("weights_file", help="the file in .lgr containing weights and biases")
    parser.add_argument("-d", "--destination", default="houses.csv", help="the destination file for the predicted values")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    try:
        main(args.file_to_test, args.weights_file, args.destination, args.verbose)
    except Exception as e:
        if (args.verbose):
            print(f"{e}: invalid file formatting.")
        else:
            print(f"Invalid file formatting.")