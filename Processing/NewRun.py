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
from Processors import IVTProcessor, WMProcessor, AttackProcessor, NCCProcessor, NCCProcessorWithLength, SaccadeProcessor, AttackAnalysisProcessor

dispatch_table = {
    "IVT": IVTProcessor,
    "WM": WMProcessor,
    "ATTACK": AttackProcessor,
    "NCC": NCCProcessor,
    "NCCL": NCCProcessorWithLength,
    "ATTACK_ANALYSIS": AttackAnalysisProcessor,
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
                data.append((float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])))
    if not data:
        print("No data found for the given attack type.")
        return 
    s,ncc,sa,vd,rms = list(zip(*data))
    plt.figure()
    plt.plot(s, rms, marker='o', linestyle='-')
    plt.xlabel('Standard deviation')
    plt.ylabel('RMS')
    plt.grid(True)
    plt.title(f'Attack Type: {attackType} \n Watermark Strength: 3')
    plt.savefig(f'Results/Plots/{attackType}_AV_RMS_plot.png')
    #plt.show()

def main(args):
    # Get command-line arguments excluding the script name
    #args = sys.argv[1:]

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
    #plot_comparison('ProcessedDatasets/WM/RandomSaccades/S_1002_S1_RAN.csv','ProcessedDatasets/CLEAN/RandomSaccades/S_1002_S1_RAN.csv',3)
    #values = [range(0.001,0.01,0.001)]
    values_list = []

    # Define the start and end points, and the increment
    start = 1.1
    end = 1.8
    increment = 0.1

    # Loop to generate the values and add them to the list
    current_value = start
    while current_value <= end:
        values_list.append(round(current_value,5))
        current_value += increment
    dict = {
        'DEA': [1.1,1.2,1.3,1.4,1.5,1.6,1.7],
        #'GWN': values_list,
        #'RRP': values_list,
        #'LIA': values_list,
        #'CA': values_list,
    }
    #main(['../Datasets/RandomSaccades/','IVT'])
    #main(['ProcessedDataSets/CLEAN/RandomSaccades/','WM','3'])
    #main(['ProcessedDataSets/WM/RandomSaccades/','SACC'])
    for key,values in dict.items():
        print(values)
        for value in values:
            main(['ProcessedDataSets/WM/RandomSaccades/', 'ATTACK_ANALYSIS', key, value])  
            #continue
    #for i in values_list:

    
    
    #    main(['ProcessedDataSets/WM/RandomSaccades/', 'ATTACK_ANALYSIS', 'DEA', str(i)])
    #    main(['ProcessedDataSets/WM_ATTACKED/RandomSaccades/RRP/', 'SACC'])
    #main("xd")


#Run examples
#Watermark
#py .\NewRun.py ProcessedDataSets/CLEAN/RandomSaccades/ WM 1
#Saccade accuracy
#py .\NewRun.py ProcessedDataSets/WM/RandomSaccades/ SACC
#Attack
#py .\NewRun.py ProcessedDataSets/WM/RandomSaccades/ ATTACK GWN 0.001
#NCC
#py .\NewRun.py ProcessedDataSets/WM_ATTACKED/RandomSaccades/GWN/ NCC