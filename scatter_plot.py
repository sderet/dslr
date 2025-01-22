import sys
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

def scatter_plot():
    names, file_content, lines = describe.open_file(sys.argv[1])
    raw_values = []

    for line in lines:
        split_line = line.split(",")
        if (split_line[1]):
            raw_values.append(split_line)

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    splitlinevalues, base_final_names = trim_data(names, split_lines)

    #11+1

    for index_first in range(len(base_final_names)):
        for index in range(len(base_final_names)):
            if (index != index_first):

                absolute = abs(math.floor(len(splitlinevalues[index]) - len(splitlinevalues[index_first])))
                if (len(splitlinevalues[index]) > len(splitlinevalues[index_first])):
                    pyplot.scatter(sorted(splitlinevalues[index_first])[:len(splitlinevalues[index])],
                                sorted(splitlinevalues[index])[absolute:],
                                label=base_final_names[index])
                else:
                    pyplot.scatter(sorted(splitlinevalues[index_first])[absolute:],
                                sorted(splitlinevalues[index])[:len(splitlinevalues[index_first])],
                                label=base_final_names[index])

                pyplot.legend(loc='upper right')
                #pyplot.title(key)
                pyplot.title(f'{base_final_names[index]} {index} (y) by {base_final_names[index_first]} {index_first} (x)')
                pyplot.show()



if __name__ == "__main__":
    scatter_plot()