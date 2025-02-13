import argparse
import matplotlib.pyplot as pyplot
import matplotlib.patheffects as pe
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

def scatter_plot(filename, verbose=False, fast=False):
    names, file_content, lines = describe.open_file(filename)
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

    legend_values = []

    for index_first in range(len(raw_names)):
        for index in range(len(raw_names)):
            if (index_first == index):
                if not fast:
                    for key in raw_values.keys():
                        axes[index_first, index].hist(raw_values[key][index_first], bins="auto", alpha=0.5)
                # Cut on character 15 so it doesn't get outside the box
                axes[index, index].annotate('\n'.join([raw_names[index][:15], raw_names[index][15:]]), (0.5, 0.5), xycoords='axes fraction',
                    ha='center', va='center', path_effects=[pe.withStroke(linewidth=2, foreground="white")])
            else:
                for key in raw_values.keys():
                    axes[index_first, index].scatter(
                        raw_values[key][index_first][:len(raw_values[key][index])],
                        raw_values[key][index][:len(raw_values[key][index_first])],
                        s=0.1)

        if (verbose):
            print(f'Finished drawing plots for {raw_names[index_first]}.')
            
    figure.legend(raw_values.keys(), loc='outside right upper')
    pyplot.subplots_adjust(wspace=0.01, hspace=0.01, left=0, right=0.9, top=1, bottom=0)
    pyplot.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file in .csv format to display a scatter plot for")
    parser.add_argument("-f", "--fast", help="do not display histograms", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    try:
        scatter_plot(args.file, args.verbose, args.fast)
    except Exception as e:
        if (args.verbose):
            print(f"{e}: invalid file formatting.")
        else:
            print(f"Invalid file formatting.")