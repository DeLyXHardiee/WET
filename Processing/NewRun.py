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
#from memory_profiler import profile
import sys

from Context import Context

reading_datasets_location = '../Datasets/Reading/'
random_datasets_location = '../Datasets/Random/'
datasets_processed_location = '../ProcessedDatasets/'
IDT_location = 'ProcessedDatasets/IDT/'
IVT_location = 'ProcessedDatasets/IVT/'
WIDT_location = 'ProcessedDatasets/WIDT/'
WIVT_location = 'ProcessedDatasets/WIVT/'
AGWN_location = 'ProcessedDatasets/AGWN/'
ALIA_location = 'ProcessedDatasets/ALIA/'
ARRP_location = 'ProcessedDatasets/RRP/'
ADEA_location = 'ProcessedDatasets/ADEA/'
ACA_location = 'ProcessedDatasets/ACA/'
Results_location = 'Results/'

def run_IVT(context, fileIn, parameters):
    eye_tracking_data = csvu.extract_data(fileIn)
    velocity_threshold = float(parameters[0])
    result = ivt.IVT(eye_tracking_data, velocity_threshold)
    outFile = name_file(fileIn, 'IVT', IVT_location)
    csvu.write_data(outFile, result)
    context.add_file('IVT', outFile)
    context.add_file('Filtering_Type', 'IVT')
    context.add_parameters('IVT_Threshold', velocity_threshold)# Save IVT result file in context
    return outFile

def run_IDT(context, fileIn, parameters):
    eye_tracking_data = csvu.extract_data(fileIn)
    duration_threshold = float(parameters[0])
    dispersion_threshold = float(parameters[1])
    result = idt.IDT(eye_tracking_data, duration_threshold, dispersion_threshold)
    outFile = name_file(fileIn,'IDT', IDT_location)
    csvu.write_data(outFile, result)
    context.add_file('IDT', outFile)
    context.add_file('Filtering_Type', 'IDT')
    context.add_parameters('Duration_Threshold', duration_threshold)
    context.add_parameters('Dispersion_Threshold', dispersion_threshold)
    return outFile

def run_embed_watermark(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    strength = float(parameters[0])
    result, watermark = ew.run_watermark(data, strength)
    if context.has_file('IVT'):
        outFile = name_file(fileIn, 'WM', WIVT_location)
        result = ivt.IVT(result, context.get_parameters('IVT_Threshold'))
    else:
        outFile = name_file(fileIn, 'WM', WIDT_location)
        result = idt.IDT(result, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    csvu.write_data(outFile, result)
    context.add_file('WM', outFile)  # Save watermarked file in context
    context.add_parameters('WM_Strength', strength)  # Save watermark strength in context
    return outFile

def run_AGWN(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    std = float(parameters[0])
    attacked_data = ad.gaussian_white_noise_attack(data, std)
    if context.has_file('IVT'):
        attacked_data = ivt.IVT(attacked_data, context.get_parameters('IVT_Threshold'))
    else:
        attacked_data = idt.IDT(attacked_data, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    outFile = name_file(fileIn, 'AGWN', AGWN_location)
    csvu.write_data(outFile, attacked_data)
    context.add_file('AGWN', outFile)
    context.add_file('Attack_Type', 'AGWN')
    context.add_parameters('Attack_Strength', std)
    return outFile

def run_ADEA(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    strength = float(parameters[0])
    attacked_data = ad.DEA_attack(data, strength)
    if context.has_file('IVT'):
        attacked_data = ivt.IVT(attacked_data, context.get_parameters('IVT_Threshold'))
    else:
        attacked_data = idt.IDT(attacked_data, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    outFile = name_file(fileIn, 'ADEA', ADEA_location)
    csvu.write_data(outFile, attacked_data)
    context.add_file('ADEA', outFile)
    context.add_file('Attack_Type', 'ADEA')
    context.add_parameters('Attack_Strength', strength)
    return outFile

def run_ARRP(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    theta = float(parameters[0])
    attacked_data = ad.RRP_attack(data, theta)
    if context.has_file('IVT'):
        attacked_data = ivt.IVT(attacked_data, context.get_parameters('IVT_Threshold'))
    else:
        attacked_data = idt.IDT(attacked_data, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    outFile = name_file(fileIn, 'ARRP', ARRP_location)
    csvu.write_data(outFile, attacked_data)
    context.add_file('ARRP', outFile)
    context.add_file('Attack_Type', 'ARRP')
    context.add_parameters('Attack_Strength', theta)
    return outFile

def run_ALIA(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    num_insertions = float(parameters[0])
    attacked_data = ad.LIA_attack(data, num_insertions)
    if context.has_file('IVT'):
        attacked_data = ivt.IVT(attacked_data, context.get_parameters('IVT_Threshold'))
    else:
        attacked_data = idt.IDT(attacked_data, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    outFile = name_file(fileIn, 'ALIA', ALIA_location)
    csvu.write_data(outFile, attacked_data)
    context.add_file('ALIA', outFile)
    context.add_file('Attack_Type', 'ALIA')
    context.add_parameters('Attack_Strength', num_insertions)
    return outFile

def run_ACA(context, fileIn, parameters):
    data = csvu.extract_data(fileIn)
    num_removals = float(parameters[0])
    attacked_data = ad.CA_attack(data, num_removals)
    if context.has_file('IVT'):
        attacked_data = ivt.IVT(attacked_data, context.get_parameters('IVT_Threshold'))
    else:
        attacked_data = idt.IDT(attacked_data, context.get_parameters('Duration_Threshold'), context.get_parameters('Dispersion_Threshold'))
    outFile = name_file(fileIn, 'ACA', ALIA_location)
    csvu.write_data(outFile, attacked_data)
    context.add_file('ACA', outFile)
    context.add_file('Attack_Type', 'ACA')
    context.add_parameters('Attack_Strength', num_removals)
    return outFile

def run_NCC(context, fileIn, parameters):
    original_data = []
    watermarked_data = []
    attacked_data = []
    original_data = csvu.extract_data(context.get_file(context.get_file('Filtering_Type')))
    watermarked_data = csvu.extract_data(context.get_file('WM'))
    attack_type = context.get_file('Attack_Type')
    attacked_data = csvu.extract_data(context.get_file(attack_type))
    strength = context.get_parameters('WM_Strength')
    noise_watermark = ew.unrun_watermark(attacked_data, original_data, strength)
    watermark = ew.unrun_watermark(watermarked_data, original_data, strength)
    result = an.normalized_cross_correlation(noise_watermark, watermark)
    print(result)
    result_file = name_file('NCC', 'AGWN_IVT', Results_location) + '.csv'
    values = [strength, result]
    csvu.append_result(result_file, values)

def ensure_parameter(context, key, prompt_message):
    """
    Ensures that a parameter is available in the context. If not, prompts the user to enter it.

    Args:
        context (Context): The context object where parameters are stored.
        key (str): The key for the parameter in the context.
        prompt_message (str): The message to display when asking the user for input.

    Returns:
        The value of the parameter, either from the context or input by the user.
    """
    # Check if the key exists in the context
    if not context.has_parameter(key):
        # Key does not exist, ask the user for input
        value = input(prompt_message + ": ")
        try:
            # Attempt to convert the input to a float if possible
            value = float(value)
        except ValueError:
            # If conversion to float fails, keep it as string (or handle differently)
            pass
        # Store the newly obtained value in the context
        context.add_parameters(key, value)
    else:
        # Retrieve the existing value from the context
        value = context.get_parameters(key)

    return value


def name_file(filename, analysistype, folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension


dispatch_table = {
    'IVT': run_IVT,
    'IDT': run_IDT,
    'WM': run_embed_watermark,
    'AGWN': run_AGWN,
    'ADEA': run_ADEA,
    'ARPP': run_ARRP,
    'ALIA': run_ALIA,
    'ACA': run_ACA,
    'NCC': run_NCC
}


def parse_parameters(args):
    # Check if the mode contains parameters, meaning args must be 2 or more in length,
    # since the mode is also included.
    if len(args) < 1:
        return []
    ordered_mode_parameters = []
    # Iterate through each argument
    for arg in args[1:]:
        if arg not in dispatch_table:
            ordered_mode_parameters.append(float(arg))
    return ordered_mode_parameters

def process_pipeline(args, filename):
    context = Context()
    i = 0
    while i < len(args):
        mode = args[i]
        if mode in dispatch_table:

            # Move to the next element after mode to start capturing parameters
            next_index = i + 1

            # Find the next mode start to limit parameter parsing
            while next_index < len(args) and args[next_index] not in dispatch_table:
                next_index += 1

            parameters = parse_parameters(args[i:next_index])
            print(f"Executing {mode} with parameters {parameters}")
            filename = dispatch_table[mode](context, filename, parameters)

            # Move index past the current mode and its parameters
            i = next_index
        else:
            print(f"Skipping unrecognized mode: {mode}")
            i += 1  # Move to the next potential mode

def IVT_all(directory, new_directory):
    filter_context = "context.json"
    files = csvu.list_csv_files_in_directory(directory)
    velocities = {}
    if jsonu.file_exists(new_directory, filter_context):
        velocities = jsonu.extract_context(new_directory + filter_context)
    else:
        jsonu.create_empty_json(new_directory, filter_context)
        for file in files:
            velocities[file] = ivt.find_best_threshold(csvu.extract_data(directory + file))
        jsonu.write_context_to_json(velocities, new_directory + filter_context)

    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)


def WM_all(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    velocities = jsonu.extract_context(directory + "context.json")
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data, watermark = ew.run_watermark(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": random.randint(1, 1000000),
        "WM_strength": strength,
        "filter_context_path": directory + "context.json"
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

#IVT_all("../Datasets/Reading/", "ProcessedDatasets/Reading/IVT/CLEAN/")

def AGWN_all_WM(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    context = jsonu.extract_context(directory + "context.json")
    velocities = jsonu.extract_context(context["filter_context_path"])
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ad.gaussian_white_noise_attack(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": context["WM_ID"],
        "Attack_type": "AGWN",
        "AGWN_strength": strength,
        "filter_context_path": context["filter_context_path"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

def DEA_all_WM(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    context = jsonu.extract_context(directory + "context.json")
    velocities = jsonu.extract_context(context["filter_context_path"])
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ad.DEA_attack(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": context["WM_ID"],
        "Attack_type": "DEA",
        "DEA_strength": strength,
        "filter_context_path": context["filter_context_path"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

def RRP_all_WM(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    context = jsonu.extract_context(directory + "context.json")
    velocities = jsonu.extract_context(context["filter_context_path"])
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ad.RRP_attack(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": context["WM_ID"],
        "Attack_type": "RRP",
        "RRP_strength": strength,
        "filter_context_path": context["filter_context_path"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

def LIA_all_WM(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    context = jsonu.extract_context(directory + "context.json")
    velocities = jsonu.extract_context(context["filter_context_path"])
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ad.LIA_attack(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": context["WM_ID"],
        "Attack_type": "LIA",
        "LIA_strength": strength,
        "filter_context_path": context["filter_context_path"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")


def CA_all_WM(directory, new_directory, strength):
    files = csvu.list_csv_files_in_directory(directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    context = jsonu.extract_context(directory + "context.json")
    velocities = jsonu.extract_context(context["context_path"])
    for file in files:
        data = csvu.extract_data(directory + file)
        velocity = velocities[file]
        data = ad.CA_attack(data, strength)
        data = ivt.IVT(data, velocity)
        csvu.write_data(new_directory + file, data)
    context = {
        "WM_ID": context["WM_ID"],
        "Attack_type": "CA",
        "CA_strength": strength,
        "filter_context_path": context["filter_context_path"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

def run_NCC_on_attack(clean_directory, WM_directory, attacked_directory, new_directory):
    clean_files = csvu.list_csv_files_in_directory(clean_directory)
    WM_files = csvu.list_csv_files_in_directory(WM_directory)
    attacked_files = csvu.list_csv_files_in_directory(attacked_directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    WM_context = jsonu.extract_context(WM_directory + "context.json")
    attack_context = jsonu.extract_context(attacked_directory + "context.json")
    scores = {}
    for i in range(0, len(clean_files)):
        print("Performing NCC for: " + clean_files[i])
        clean_data = csvu.extract_data(clean_directory + clean_files[i])
        WM_data = csvu.extract_data(WM_directory + WM_files[i])
        attacked_data = csvu.extract_data(attacked_directory + attacked_files[i])
        original_wm = ew.unrun_watermark(WM_data, clean_data, WM_context["WM_strength"])
        attacked_wm = ew.unrun_watermark(attacked_data, clean_data, WM_context["WM_strength"])
        ncc_score = an.normalized_cross_correlation(original_wm, attacked_wm)
        scores[clean_files[i]] = ncc_score

    context = {
        "Analysis": "NCC",
        "Scores": scores,
        "Mean_score": np.mean(list(scores.values())),
        "Attack_type": attack_context["Attack_type"],
        "Attack_strength": attack_context[attack_context["Attack_type"] + "_strength"],
        "WM_strength": WM_context["WM_strength"]
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

def run_saccade_accuracy(first_directory, second_directory, new_directory):
    first_files = csvu.list_csv_files_in_directory(first_directory)
    second_files = csvu.list_csv_files_in_directory(second_directory)
    if not jsonu.file_exists(new_directory, "context.json"):
        jsonu.create_empty_json(new_directory, "context.json")
    scores = {}
    for i in range(0, len(first_files)):
        print("Performing Saccade Accuracy for: " + first_files[i])
        first_data = csvu.extract_data(first_directory + first_files[i])
        second_data = csvu.extract_data(second_directory + second_files[i])
        sa_score = an.measure_saccade_accuracy(first_data, second_data)
        scores[first_files[i]] = sa_score

    context = {
        "First_directory_context": jsonu.extract_context(first_directory + "context.json"),
        "Second_directory": jsonu.extract_context(second_directory + "context.json"),
        "Analysis": "Saccade Accuracy",
        "Scores": scores,
        "Mean_score": np.mean(list(scores.values())),
    }
    jsonu.write_context_to_json(context, new_directory + "context.json")

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


#IVT_all("../Datasets/Reading/" ,"ProcessedDatasets/CLEAN/Reading/")
#WM_all("ProcessedDatasets/CLEAN/Reading/", "ProcessedDatasets/WM/Reading/", 1)
#AGWN_all_WM("ProcessedDatasets/WM/Reading/", "ProcessedDatasets/WM_ATTACKED/Reading/GWN/", 0.001)

#run_NCC_on_attack("ProcessedDatasets/CLEAN/Reading/", "ProcessedDatasets/WM/Reading/", "ProcessedDatasets/WM_ATTACKED/Reading/GWN/", "ProcessedDatasets/ANALYSIS/")
run_saccade_accuracy("ProcessedDatasets/CLEAN/Reading/", "ProcessedDatasets/WM/Reading/", "ProcessedDatasets/ANALYSIS/")