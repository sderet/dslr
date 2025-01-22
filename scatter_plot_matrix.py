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

def scatter_plot():
    names, file_content, lines = describe.open_file(sys.argv[1])
    raw_values = {
        "Ravenclaw": [],
        "Slytherin": [],
        "Gryffindor": [],
        "Hufflepuff": []
        }
    
    raw_names = []

    for line in lines:
        split_line = line.split(",")
        if (split_line[1]):
            raw_values[split_line[1]].append(split_line)

    for key in raw_values.keys():
        raw_values[key], raw_names = trim_data(names, raw_values[key])

    figure, axes = pyplot.subplots(nrows=len(raw_names), ncols=len(raw_names))

    for ax in axes.flat:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    for index_first in range(len(raw_names)):
        for index in range(len(raw_names)):
            if (index_first == index):
                axes[index, index].annotate(raw_names[index], (0.5, 0.5), xycoords='axes fraction',
                    ha='center', va='center')
            else:
                for key in raw_values.keys():
                    axes[index_first, index].scatter(
                        raw_values[key][index_first][:len(raw_values[key][index])],
                        raw_values[key][index][:len(raw_values[key][index_first])],
                        s=0.1)

    pyplot.subplots_adjust(wspace=0.01, hspace=0.01, left=0, right=1, top=1, bottom=0)
    pyplot.show()

if __name__ == "__main__":
    scatter_plot()