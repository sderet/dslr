import sys
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

def histogram():
    names, file_content, lines = describe.open_file(sys.argv[1])
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

    dict_values = {
        "Ravenclaw": [],
        "Slytherin": [],
        "Gryffindor": [],
        "Hufflepuff": []
        }

    described_values = {}
    
    for key in raw_values.keys():
        split_line = line.split(",")
        for split_line in raw_values[key]:
            dict_values[key].append(describe.dictionary_from_line(names, split_line))
        
        described_values[key] = describe.describe(names, dict_values[key], False)

    split_lines = []
    for line in lines:
        split_lines.append(line.split(","))

    splitlinevalues, base_final_names = trim_data(names, split_lines)

    #1 arithmancy 11 care of magical creatures
    # Are the most homogeneous between different houses

    for index in range(len(base_final_names)):
        fullfeatures = []
        for key in raw_values.keys():
            features_values, final_names = trim_data(names, raw_values[key])
            fullfeatures.append(features_values[index])
            #pyplot.hist(features_values[index], bins="auto", alpha=0.5, label=final_names[index])
            pyplot.hist(features_values[index], bins="auto", alpha=0.5, label=key)
        
        #pyplot.hist(fullfeatures, bins="auto", alpha=0.5, label=raw_values.keys())

        pyplot.legend(loc='upper right')
        #pyplot.title(key)
        pyplot.title(f'{final_names[index]} {index}')
        pyplot.show()



if __name__ == "__main__":
    histogram()