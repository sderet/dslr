import sys
import math

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

def give_means(names, file_content):
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
            means[name] = total / index
        except TypeError:
            means[name] = 0
            
    return (means)

def give_standard_deviations(names, file_content, means):
    std = {}
    for name in names:
        total = 0
        for index, line in enumerate(file_content):
            if (name in line and line[name]):
                try:
                    total += pow((float(line[name]) - means[name]), 2)
                except ValueError:
                    total = "NaN"
                    break
        
        try:
            std[name] = math.sqrt(total / index)
        except TypeError:
            std[name] = 0

    return (std)

def float_or_zero(value):
    try:
        return (float(value))
    except ValueError:
        return (0)

def give_percentiles(names, file_content, percentile):
    percentiles = {}
    for name in names:
        sorted_content = sorted(file_content, key=lambda line: float_or_zero(line[name]))
        sorted_content = list(filter(lambda line: (line[name] != ""), sorted_content))
        length = len(sorted_content)

        index = (length - 1) * percentile

        try: 
            try:
                percentiles[name] = float(sorted_content[index][name])
            except TypeError:
                floor = math.floor(index)
                ceiling = math.ceil(index)
                percentiles[name] = (float(sorted_content[floor][name]) + float(sorted_content[ceiling][name])) / 2
        except ValueError:
            percentiles[name] = 0
    
    return (percentiles)

def describe(described_data):
    print(f'{'': <8}', end='')
    for column_key in described_data["Count"].keys():
        print(f'{column_key[:13]: >15}', end='')
    
    print('')

    for line_key in described_data.keys():
        print(f'{line_key: <8}', end='')
        for column_key in described_data[line_key].keys():
            print(f'{f"{described_data[line_key][column_key]: .5f}"[:13]: >15}', end='')
        print('')

def main():
    fd = open(sys.argv[1], "r")
    content = fd.read()
    lines = content.split("\n")

    # Array of dict
    file_content = []
    # Array of the keys in file_content
    names = lines[0].split(",")

    for line in lines:
        file_content.append(dictionary_from_line(names, line.split(",")))

    # Remove first and last elements
    # First is the name of columns, last is empty (assuming the file ends in \n)
    del file_content[0]
    del file_content[-1]

    # Dict of dicts
    described_data = {}
    
    described_data["Count"] = give_counts(names, file_content)
    described_data["Mean"] = give_means(names, file_content)
    described_data["Std"] = give_standard_deviations(names, file_content, described_data["Mean"])
    described_data["Min"] = give_percentiles(names, file_content, 0)
    described_data["25%"] = give_percentiles(names, file_content, 0.25)
    described_data["50%"] = give_percentiles(names, file_content, 0.5)
    described_data["75%"] = give_percentiles(names, file_content, 0.75)
    described_data["Max"] = give_percentiles(names, file_content, 1)

    # Describe function simply prints the data inside described_data, but nicely
    describe(described_data)

main()
