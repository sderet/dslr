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
            means[name] = "NaN"
            
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
            std[name] = "NaN"

    return (std)

def give_percentiles(names, file_content, percentile):
    percentiles = {}
    for name in names:
        sorted_content = sorted(file_content, key=lambda line: line[name])
        sorted_content = list(filter(lambda line: (line[name] != ""), sorted_content))
        length = len(sorted_content)

        ## TODO: fix this here so it's actually consistent
        # issue is, taking length as is, it'll reach index 1600, which doesn't exist
        # we want to find indexes inbetween 0 and 1599
        # however, if left as is, percentile 0 is gonna be index 0, and percentile 1 is gonna be index 1600
        # doing length-1 doesn't work because then, sure, it'll be between 0 and 1599, but 1/4 is 399.75
        # doing index-1 doesn't work because then, index 0 becomes index -1
        index = length * percentile

        print(index)

        try: 
            try:
                percentiles[name] = float(sorted_content[index][name])
            except TypeError:
                floor = math.floor(index)
                ceiling = math.ceil(index)
                percentiles[name] = (float(sorted_content[floor][name]) + float(sorted_content[ceiling][name])) / 2
        except ValueError:
            percentiles[name] = "NaN"
    
    return (percentiles)
    

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

    print(described_data)

    # Describe function simply prints the data inside described_data, but nicely
    #describe(described_data)

main()
