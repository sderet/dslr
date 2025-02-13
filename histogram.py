import matplotlib.pyplot as pyplot
import describe
import argparse

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

def histogram(filename):
    names, file_content, lines = describe.open_file(filename)
    raw_values = {
        "Ravenclaw": [],
        "Slytherin": [],
        "Gryffindor": [],
        "Hufflepuff": []
        }

    for line in lines:
        split_line = line.split(",")
        if (split_line[1]):
            raw_values[split_line[1]].append(split_line)

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    #1 arithmancy 11 care of magical creatures
    # Are the most homogeneous between different houses
    index = 1
    
    fullfeatures = []
    for key in raw_values.keys():
        features_values, final_names = trim_data(names, raw_values[key])
        fullfeatures.append(features_values[index])
        pyplot.hist(features_values[index], bins="auto", alpha=0.5, label=key)

    pyplot.legend(loc='upper right')
    pyplot.title(f'Number of students (Y) by {final_names[index]} scores (X)')
    pyplot.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file in .csv format to display an histogram for")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    try:
        histogram(args.file)
    except Exception as e:
        if (args.verbose):
            print(f"{e}: invalid file formatting.")
        else:
            print(f"Invalid file formatting.")