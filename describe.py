import math
import argparse

def dictionary_from_line(names, line):
    dict_line = {}

    for index, name in enumerate(names):
        if (len(line) > index):
            dict_line[name] = line[index]

    return (dict_line)

def give_counts(names, file_content):
    counts = {}
    for name in names:
        counts[name] = 0
        for line in file_content:
            if (name in line and line[name]):
                counts[name] += 1
    return (counts)

def give_means(names, file_content, counts):
    means = {}
    for name in names:
        total = 0
        for index, line in enumerate(file_content):
            if (name in line and line[name]):
                try:
                    total += float(line[name])
                except ValueError:
                    total = "NaN"
                    break
        
        try:
            means[name] = total / counts[name]
        except TypeError:
            means[name] = "N/A"
            
    return (means)

def give_standard_deviations(names, file_content, means, counts):
    std = {}
    for name in names:
        total = 0
        for line in file_content:
            if (name in line and line[name]):
                try:
                    total += pow((float(line[name]) - means[name]), 2)
                except ValueError:
                    total = "NaN"
                    break

        try:
            std[name] = math.sqrt(total / counts[name])
        except TypeError:
            std[name] = "N/A"

    return (std)

def float_or_zero(value):
    try:
        return (float(value))
    except ValueError:
        return 0

def give_percentiles(names, file_content, percentile, counts):
    percentiles = {}
    for name in names:
        sorted_content = list(filter(lambda line: (line[name] != ""), file_content))
        sorted_content = sorted(sorted_content, key=lambda line: float_or_zero(line[name]))

        index = (counts[name] - 1) * percentile

        try: 
            try:
                percentiles[name] = float(sorted_content[index][name])
            except TypeError:
                floor = math.floor(index)
                ceiling = math.ceil(index)
                percentiles[name] = (float(sorted_content[floor][name]) * (ceiling - index)) + (float(sorted_content[ceiling][name]) * (index - floor))
        except ValueError:
            percentiles[name] = "N/A"
    
    return (percentiles)

def print_describe(described_data):
    print(f'{"": <8}', end='')
    for column_key in described_data["Count"].keys():
        print(f'{column_key[:10]: >12}', end='')
    
    print('')

    for line_key in described_data.keys():
        print(f'{line_key: <8}', end='')
        for column_key in described_data[line_key].keys():
            if (described_data[line_key][column_key] != "N/A"):
                print(f'{f"{described_data[line_key][column_key]: .5f}"[:10]: >12}', end='')
            else:
                print(f'{"N/A": >12}', end='')
        print('')

def describe(names, file_content, to_print):
    # Dict of dicts
    described_data = {}

    try:
        described_data["Count"] = give_counts(names, file_content)
        described_data["Mean"] = give_means(names, file_content, described_data["Count"])
        described_data["Std"] = give_standard_deviations(names, file_content, described_data["Mean"], described_data["Count"])
        described_data["Min"] = give_percentiles(names, file_content, 0, described_data["Count"])
        described_data["25%"] = give_percentiles(names, file_content, 0.25, described_data["Count"])
        described_data["50%"] = give_percentiles(names, file_content, 0.5, described_data["Count"])
        described_data["75%"] = give_percentiles(names, file_content, 0.75, described_data["Count"])
        described_data["Max"] = give_percentiles(names, file_content, 1, described_data["Count"])

    except Exception:
        print("Error parsing the file.")
        return {}

    if (to_print == True):
        # Describe function simply prints the data inside described_data, but nicely
        print_describe(described_data)

    return (described_data)

def open_file(filename):
    try:
        with open(filename, 'r') as fd:
            content = fd.read()
    except FileNotFoundError:
        print(f"{filename}: File not found.")
        return False, False, False

    lines = content.split("\n")

    # Array of dict
    file_content = []
    # Array of the keys in file_content
    names = lines[0].split(",")

    # Remove first and last elements
    # First is the name of columns, last is empty (assuming the file ends in \n)
    del lines[0]
    if (len(lines[-1]) < 1):
        del lines[-1]

    for line in lines:
        file_content.append(dictionary_from_line(names, line.split(",")))

    return names, file_content, lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file in .csv format to describe")

    args = parser.parse_args()

    names, file_content, lines = open_file(args.file)

    if (names and file_content):
        describe(names, file_content, True)
