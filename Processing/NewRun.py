import os

from matplotlib import pyplot as plt
import numpy as np
import Filtering.CSVUtility as csvu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import Embed_watermark as ew
import Adversary as ad
import Analyze as an
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


def name_file(filename, analysistype, folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension


analysis_modes = {
    'IVT', 'IDT', 'WM', 'AGWN', 'ARPP', 'ADEA', 'ALIA', 'ACA', 'NCC'
}

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
        if arg not in analysis_modes:
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
            while next_index < len(args) and args[next_index] not in analysis_modes:
                next_index += 1

            parameters = parse_parameters(args[i:next_index])
            print(f"Executing {mode} with parameters {parameters}")
            filename = dispatch_table[mode](context, filename, parameters)
            # Move index past the current mode and its parameters
            i = next_index
        else:
            print(f"Skipping unrecognized mode: {mode}")
            i += 1  # Move to the next potential mode

def run():
    filename = sys.argv[1]
    print(filename)
    args = sys.argv[2:]
    process_pipeline(args, filename)

run()
