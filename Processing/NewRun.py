import math
import os
import random

from matplotlib import pyplot as plt
import numpy as np
import Filtering.CSVUtility as csvu
import Filtering.JSONUtility as jsonu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import Embed_watermark as ew
import Adversary as ad
import Analyze as an
import random
import sys
from Processors import IVTProcessor, WMProcessor, AttackProcessor, NCCProcessor, SaccadeProcessor, AttackNCCProcessor

dispatch_table = {
    "IVT": IVTProcessor,
    "WM": WMProcessor,
    "ATTACK": AttackProcessor,
    "NCC": NCCProcessor,
    "ATTACKNCC": AttackNCCProcessor,
    "SACC": SaccadeProcessor
}

def parse_parameters(args):
    """
    Parse parameters from command-line arguments.

    Args:
        args (list): List of command-line arguments.

    Returns:
        list: Ordered mode parameters, with values converted to float if possible.
    """
    ordered_mode_parameters = []
    for arg in args:
        try:
            # Attempt to convert the argument to a float
            float_value = float(arg)
            ordered_mode_parameters.append(float_value)
        except ValueError:
            # If conversion fails, keep the argument as a string
            ordered_mode_parameters.append(arg)
    return ordered_mode_parameters

def process_pipeline(args, filename):
    i = 0
    while i < len(args):
        mode = args[i]
        if mode in dispatch_table:
            processor_class = dispatch_table[mode]
            # Move to the next element after mode to start capturing parameters
            next_index = i + 1

            # Find the next mode start to limit parameter parsing
            while next_index < len(args) and args[next_index] not in dispatch_table:
                next_index += 1

            parameters = parse_parameters(args[i + 1:next_index])
            print(f"Executing {mode} with parameters {parameters}")
            processor = processor_class(filename, *parameters)
            filename = processor.process_data()

            # Move index past the current mode and its parameters
            i = next_index
        else:
            print(f"Skipping unrecognized mode: {mode}")
            i += 1  # Move to the next potential mode


def plot_comparison(first_file, second_file, strength):
    first_data = csvu.extract_data(first_file)
    second_data = csvu.extract_data(second_file)
    _,first_data_x,first_data_y,_ = list(zip(*first_data))
    _,second_data_x,second_data_y,_ = list(zip(*second_data))
    plt.figure()
    plt.scatter(first_data_x, first_data_y, color='blue', label='Original data', s= 0.5)
    plt.scatter(second_data_x, second_data_y, color='#fc8403', label='Watermarked data', s= 0.5)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()
    plt.xlim(-7,7)
    plt.ylim(-6,6)
    plt.title('Strength: ' +str(strength))
    plt.show()

def plot_results(filename):
    data = csvu.extract_results2(filename)
    data_x,data_y,visualDegrees,rms = list(zip(*data))
    plt.figure()
    plt.scatter(data_x, data_y, color='blue', s= 1)
    plt.xlabel('WM_Strength')
    plt.ylabel('Saccade Accuracy')
    plt.grid(True)
    plt.title('Watermark embedding utility')
    results_location = '/Results/Plots/'
    plot = results_location + "S_SA_" + filename[8:-4] + ".png"
    print(plot)
    plt.savefig("Results/Plots/S_SA.png")
    plt.show()

def plot_attack_results(filename, attackType):
    data = []
    with open(filename, 'r') as file:
        reader = csvu.get_reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == attackType:
                data.append((float(row[1]), float(row[2])))
    if not data:
        print("No data found for the given attack type.")
        return 
    data_x,data_y = list(zip(*data))
    plt.figure()
    plt.scatter(data_x, data_y, color='blue', s= 0.5)
    plt.xlabel('Attack Variable')
    plt.ylabel('Normalized Cross Correlation')
    plt.grid(True)
    plt.title(f'Attack Type: {attackType}')
    plt.savefig(f'Results/Plots/{attackType}_plot.png')
    plt.show()

def main():
    # Get command-line arguments excluding the script name
    args = sys.argv[1:]

    # Ensure that at least one argument is provided
    if not args:
        print("Usage: python main.py <mode1> <parameters1> <mode2> <parameters2> ...")
        sys.exit(1)

    # Extract the filename from the first argument
    filename = args.pop(0)

    # Process the pipeline
    process_pipeline(args, filename)

if __name__ == "__main__":
    #plot_results('Results/SaccadeAccuracies.csv')
    #plot_attack_results('Results/NCC_AT_AV.csv', "GWN")
    main()



#Run examples
#Watermark
#py .\NewRun.py ProcessedDataSets/CLEAN/RandomSaccades/ WM 1
#Saccade accuracy
#py .\NewRun.py ProcessedDataSets/WM/RandomSaccades/ SACC