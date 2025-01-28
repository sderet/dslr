import argparse
import math
import matplotlib.pyplot as pyplot
import describe

def trim_data(names, split_lines):
    features_values = []
    final_names = []

    for ft_index in range(len(names)):
        feature = []
        is_float = True
        for index in range(len(split_lines)):
            try:
                if (split_lines[index][ft_index]):
                    feature.append(float(split_lines[index][ft_index]))
            except ValueError:
                is_float = False
                break
        if is_float:
            final_names.append(names[ft_index])
            features_values.append(feature)
    
    return features_values, final_names

def scatter_plot(filename):
    names, file_content, lines = describe.open_file(filename)

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    splitlinevalues, base_final_names = trim_data(names, split_lines)

    #11+1 are the most similar
    index = 1
    index_first = 11

    if (index != index_first):

        absolute = abs(math.floor(len(splitlinevalues[index]) - len(splitlinevalues[index_first])))
        if (len(splitlinevalues[index]) > len(splitlinevalues[index_first])):
            pyplot.scatter(sorted(splitlinevalues[index_first])[:len(splitlinevalues[index])],
                        sorted(splitlinevalues[index])[absolute:])
        else:
            pyplot.scatter(sorted(splitlinevalues[index_first])[absolute:],
                        sorted(splitlinevalues[index])[:len(splitlinevalues[index_first])])

        pyplot.title(f'Scores for {base_final_names[index]} (Y) by {base_final_names[index_first]} (X)')
        pyplot.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file in .csv format to display a scatter plot for")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    try:
        scatter_plot(args.file)
    except Exception as e:
        if (args.verbose):
            print(f"{e}: invalid file formatting.")
        else:
            print(f"Invalid file formatting.")