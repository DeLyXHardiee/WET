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

reading_datasets_location = '../Datasets/Reading/'
random_datasets_location = '../Datasets/Random/'
datasets_processed_location = '../ProcessedDatasets/'
IDT_location = 'ProcessedDatasets/IDT/'
IVT_location = 'ProcessedDatasets/IVT/'
WIDT_location = 'ProcessedDatasets/WIDT/'
WIVT_location = 'ProcessedDatasets/WIVT/'
AGWN_location = 'ProcessedDatasets/AGWN/'
ADEA_location = 'ProcessedDatasets/ADEA/'
Results_location = 'Results/'

NO_VALUE = -1
IDT_MODE = 'IDT'
IVT_MODE = 'IVT'
WIDT_MODE = 'WIDT'
WIVT_MODE = 'WIVT'
AGWN_IDT_MODE = 'AGWN_IDT'
AGWN_IVT_MODE = 'AGWN_IVT'
DEA_IDT_MODE = 'DEA_IDT'
DEA_IVT_MODE = 'DEA_IVT'
RPP_IDT_MODE = 'RPP_IDT'
RPP_IVT_MODE = 'RPP_IVT'
LIA_IDT_MODE = 'LIA_IDT'
LIA_IVT_MODE = 'LIA_IVT'
CA_IDT_MODE = 'CA_IDT'
CA_IVT_MODE = 'CA_IVT'
NCC_AGWN_IVT_MODE = 'NCC_AGWN_IVT'
NCC_AGWN_IDT_MODE = 'NCC_AGWN_IDT'
NCC_ADEA_IVT_MODE = 'NCC_ADEA_IVT'
NCC_ADEA_IDT_MODE = 'NCC_ADEA_IDT'
PLOT_RESULTS_IVT_MODE = 'PLOT_RESULTS_IVT'
PLOT_RESULTS_IDT_MODE = 'PLOT_RESULTS_IDT'
DATA_GATHER_IVT = 'DATA_GATHER_IVT'
DATA_GATHER_IDT = 'DATA_GATHER_IDT'

def run_IDT(fileIn, duration_threshold, dispersion_threshold):
    eye_tracking_data = csvu.extract_data(fileIn)
    print("eye tracking data size: " + str(len(eye_tracking_data)))
    result = idt.IDT(eye_tracking_data, duration_threshold, dispersion_threshold)
    print("result size: " + str(len(result)))
    outFile = name_file(fileIn,'IDT',IDT_location)
    csvu.write_data(outFile, result)
    return result,outFile

def run_IVT(fileIn, velocity_threshold):
    eye_tracking_data = csvu.extract_data(fileIn)
    result = ivt.IVT(eye_tracking_data, velocity_threshold)
    outFile = name_file(fileIn,'IVT',IVT_location)
    csvu.write_data(outFile, result)
    return result,outFile

def run_embed_watermark(fileIn, outFolder, strength):
    data = csvu.extract_data(fileIn)
    result,watermark = ew.run_watermark(data, strength)
    outFile = name_file(fileIn,'WM',outFolder)
    csvu.write_data(outFile, result)
    return result,watermark,outFile

def run_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength):
    original_idt_data,IDTFile = run_IDT(fileIn, duration_threshold, dispersion_threshold)
    _,watermark,watermarkedFile = run_embed_watermark(IDTFile, WIDT_location, strength)
    watermarked_idt_data,_ = run_IDT(watermarkedFile,duration_threshold,dispersion_threshold)
    print(an.measure_saccade_accuracy(original_idt_data, watermarked_idt_data))    
    return watermarked_idt_data

def run_IVT_with_watermark(fileIn, velocity_treshold, strength):
    original_ivt_data,IVTFile = run_IVT(fileIn,velocity_treshold)
    _,watermark,watermarkedFile = run_embed_watermark(IVTFile, WIVT_location, strength)
    watermarked_ivt_data,_ = run_IVT(watermarkedFile,velocity_treshold)
    print(an.measure_saccade_accuracy(original_ivt_data, watermarked_ivt_data))
    return watermarked_ivt_data

def run_AGWN_on_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength, standard_deviation):
    idt_watermarked = run_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength)
    attacked_data = ad.gaussian_white_noise_attack(idt_watermarked,standard_deviation)
    outFile = name_file(fileIn,'WM_AGWN_IDT',AGWN_location)
    csvu.write_data(outFile, attacked_data)
    return idt_watermarked, attacked_data

def run_AGWN_on_IVT_with_watermark(fileIn, velocity_treshold, strength, standard_deviation):
    ivt_watermarked = run_IVT_with_watermark(fileIn, velocity_treshold, strength)
    attacked_data = ad.gaussian_white_noise_attack(ivt_watermarked,standard_deviation)
    outFile = name_file(fileIn,'WM_AGWN_IVT',AGWN_location)
    csvu.write_data(outFile, attacked_data)
    return ivt_watermarked, attacked_data

def run_NCC_AGWN_IVT(filename, velocity_threshold, strength, standard_deviation):
    original_data = csvu.extract_data(filename)
    ivt_watermarked, attacked_data = run_AGWN_on_IVT_with_watermark(filename, velocity_threshold, strength, standard_deviation)
    noise_watermark = ew.unrun_watermark(attacked_data, original_data, strength)
    watermark = ew.unrun_watermark(ivt_watermarked, original_data, strength)
    result = an.normalized_cross_correlation(noise_watermark, watermark)
    result_file = name_file('NCC','AGWN_IVT',Results_location) + '.csv'
    values = [ velocity_threshold,strength,standard_deviation,result ]
    csvu.append_result(result_file,values)

def run_NCC_AGWN_IDT(filename, duration_threshold, dispersion_threshold, strength, standard_deviation):
    original_data = csvu.extract_data(filename)
    ivt_watermarked, attacked_data = run_AGWN_on_IDT_with_watermark(filename,duration_threshold, dispersion_threshold, strength, standard_deviation)
    noise_watermark = ew.unrun_watermark(attacked_data, original_data, strength)
    watermark = ew.unrun_watermark(ivt_watermarked, original_data, strength)
    result = an.normalized_cross_correlation(noise_watermark, watermark)
    result_file = name_file('NCC','AGWN_IDT',Results_location) + '.csv'
    values = [ duration_threshold, dispersion_threshold, strength, standard_deviation, result ]
    csvu.append_result(result_file,values)

def run_ADEA_on_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength, attack_strength):
    idt_watermarked = run_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength)
    attacked_data = ad.DEA_attack(idt_watermarked,attack_strength)
    outFile = name_file(fileIn,'WM_ADEA_IDT',ADEA_location)
    csvu.write_data(outFile, attacked_data)
    return idt_watermarked, attacked_data

def run_NCC_ADEA_IDT(filename, duration_threshold, dispersion_threshold, strength, attack_strength):
    original_data = csvu.extract_data(filename)
    idt_watermarked, attacked_data = run_ADEA_on_IDT_with_watermark(filename,duration_threshold, dispersion_threshold, strength, attack_strength)
    noise_watermark = ew.unrun_watermark(attacked_data, original_data, strength)
    watermark = ew.unrun_watermark(idt_watermarked, original_data, strength)
    result = an.normalized_cross_correlation(noise_watermark, watermark)
    result_file = name_file('NCC','ADEA_IDT',Results_location) + '.csv'
    values = [ duration_threshold, dispersion_threshold, strength, attack_strength, result ]
    csvu.append_result(result_file,values)

def run_ADEA_on_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength, attack_strength):
    idt_watermarked = run_IDT_with_watermark(fileIn, duration_threshold, dispersion_threshold, strength)
    attacked_data = ad.DEA_attack(idt_watermarked,attack_strength)
    outFile = name_file(fileIn,'WM_ADEA_IDT',ADEA_location)
    csvu.write_data(outFile, attacked_data)
    return idt_watermarked, attacked_data

def run_ADEA_on_IVT_with_watermark(fileIn, velocity_threshold, strength, attack_strength):
    ivt_watermarked = run_IVT_with_watermark(fileIn, velocity_threshold, strength)
    attacked_data = ad.DEA_attack(ivt_watermarked,attack_strength)
    outFile = name_file(fileIn,'WM_ADEA_IVT',ADEA_location)
    csvu.write_data(outFile, attacked_data)
    return ivt_watermarked, attacked_data

def run_NCC_ADEA_IVT(filename, velocity_threshold, strength, attack_strength):
    original_data = csvu.extract_data(filename)
    ivt_watermarked, attacked_data = run_ADEA_on_IVT_with_watermark(filename, velocity_threshold, strength, attack_strength)
    result = NCC_helper(attacked_data, ivt_watermarked, original_data,strength)
    result_file = name_file('NCC','ADEA_IVT',Results_location) + '.csv'
    values = [ velocity_threshold, strength, attack_strength, result ]
    csvu.append_result(result_file,values)

def NCC_helper(attacked_data, watermarked_data, original_data, strength):
    noise_watermark = ew.unrun_watermark(attacked_data, original_data, strength)
    watermark = ew.unrun_watermark(watermarked_data, original_data, strength)
    result = an.normalized_cross_correlation(noise_watermark, watermark)

def name_file(filename,analysistype,folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension

def plot_results(filename,dictionary,axis):
    results = []
    data = csvu.extract_results(filename)
    #Go through tuple and make sure each entry has the same values as dictionary for each variable.
    #This is used to filter out which data points to do analysis on. Leave entries in dictionary blank if you wish to include them regardless of value.
    #IDT: DUT,DIT,S,SD,NCC
    #IVT: VT,S,SD,NCC
    print(dictionary.items())
    for tuple in data:
        invalid = False
        for index, value in dictionary.items():
            if (tuple[index] != value) & (value != None):
                invalid = True
                continue
        if not invalid:
            results.append(tuple)
    SD = []
    S = []
    NCC = []
    for i in results:
        S.append(i[-3])
        SD.append(i[-2])
        NCC.append(i[-1])
    plt.figure()
    print(axis)
    if axis == 'SD':
        plt.scatter(SD, NCC, color='blue')
        plt.xlabel('SD')
        plt.ylabel('NCC')
        if 'IDT' in filename:
            plt.title('Strength = ' + str(dictionary[2]))
        elif 'IVT' in filename:
            plt.title('Strength = ' + str(dictionary[1]))
    elif axis == 'S':
        plt.scatter(S, NCC, color='blue')
        plt.xlabel('S')
        plt.ylabel('NCC')
        if 'IDT' in filename:
            plt.title('Standard deviation = ' + str(dictionary[3]))
        if 'IVT' in filename:
            plt.title('Standard deviation = ' + str(dictionary[2]))    
    plt.grid(True)
    plt.show()    

def run():
    #format example: IDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: WIDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: IVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03
    #format example: WIVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03 

    #plot format: py Run.py PLOT_MODE FILE ALGORITHMPARAMETERS(DUT,DIT,VT) STRENGTH STANDARD_DEVIATION AXIS
    #-1 MEANS INCLUDE ALL
    #plot format example: py Run.py PLOT_RESULTS_AGWN_IVT Results/NCC_AGWN_IVT.csv -1 -1 0.001 S
    mode = sys.argv[1]
    filename = sys.argv[2]
    if 'PLOT' not in mode:
        velocity_threshold = 0.05
        strength = 0.0003
        attack_strength = 0.0003
        dispersion_threshold = 0.5
        duration_threshold = 100
        standard_deviation = 0.001
    axis = 'SD'
    if len(sys.argv) > 3:
        if 'IVT' in mode:
            if sys.argv[3] != NO_VALUE:
                velocity_threshold = float(sys.argv[3])
            if (len(sys.argv) > 4) & (sys.argv[4] != NO_VALUE):
                strength = float(sys.argv[4])
            if (len(sys.argv) > 5) & (sys.argv[5] != NO_VALUE):
                standard_deviation = float(sys.argv[5])
            if 'PLOT' in mode:
                if (len(sys.argv) > 6) & (sys.argv[6] != NO_VALUE):
                    axis = sys.argv[6]
        if 'IDT' in mode:
            duration_threshold = float(sys.argv[3])
            if (len(sys.argv) > 4) & (sys.argv[4] != NO_VALUE):
                dispersion_threshold = float(sys.argv[4])
            if (len(sys.argv) > 5) & (sys.argv[5] != NO_VALUE):
                strength = float(sys.argv[5])
            if 'AGWN' in mode:
                if (len(sys.argv) > 6) & (sys.argv[6] != NO_VALUE):
                    standard_deviation = float(sys.argv[6])
            elif 'ADEA' in mode:
                if (len(sys.argv) > 6) & (sys.argv[6] != NO_VALUE):
                    attack_strength = float(sys.argv[6])
            if 'PLOT' in mode:
                if (len(sys.argv) > 7) & (sys.argv[7] != NO_VALUE):
                    axis = sys.argv[7]
    print(mode)
    if mode == IDT_MODE:
        run_IDT(filename, duration_threshold, dispersion_threshold)
    elif mode == IVT_MODE:
        run_IVT(filename, velocity_threshold)
    elif mode == WIDT_MODE:
        run_IDT_with_watermark(filename, duration_threshold, dispersion_threshold, strength)
    elif mode == WIVT_MODE:
        run_IVT_with_watermark(filename, velocity_threshold, strength)
    elif mode == AGWN_IDT_MODE:
        run_AGWN_on_IDT_with_watermark(filename, duration_threshold, dispersion_threshold, strength, standard_deviation)
    elif mode == AGWN_IVT_MODE:
        run_AGWN_on_IVT_with_watermark(filename, velocity_threshold, strength, standard_deviation)
    elif mode == NCC_AGWN_IVT_MODE:
        run_NCC_AGWN_IVT(filename, velocity_threshold, strength, standard_deviation)
    elif mode == NCC_AGWN_IDT_MODE:
        run_NCC_AGWN_IDT(filename, duration_threshold, dispersion_threshold, strength, standard_deviation)
    elif mode == NCC_ADEA_IVT_MODE:
        run_NCC_ADEA_IVT(filename, velocity_threshold, strength, attack_strength)
    elif mode == NCC_ADEA_IDT_MODE:
        run_NCC_ADEA_IDT(filename, duration_threshold, dispersion_threshold, strength, attack_strength)
    elif mode == PLOT_RESULTS_IDT_MODE:
        dictionary = {
            0: duration_threshold if duration_threshold != -1 else None,
            1: dispersion_threshold if dispersion_threshold != -1 else None,
            2: strength if strength != -1 else None,
            3: standard_deviation if standard_deviation != -1 else None,
        }
        plot_results(filename,dictionary,axis)
    elif mode == PLOT_RESULTS_IVT_MODE:
        dictionary = {
            0: velocity_threshold if velocity_threshold != -1 else None,
            1: strength if strength != -1 else None,
            2: standard_deviation if standard_deviation != -1 else None,
        }
        plot_results(filename,dictionary,axis)
    elif mode == DATA_GATHER_IVT:
        start_value = 0.1
        end_value = 1
        interval = 0.1
        strengths = np.arange(start_value, end_value + interval, interval)#[0.0003,0.005,0.0495,1]
        standard_deviations = [0.001,0.01,0.05,0.1]
        for i in strengths:
            for j in standard_deviations:
                run_NCC_AGWN_IVT(filename,velocity_threshold,i,j)
    elif mode == DATA_GATHER_IDT:
        strengths = [0.0003,0.005,0.0495,1]
        standard_deviations = [0.001,0.01,0.05,0.1]
        for i in strengths:
            for j in standard_deviations:
                run_NCC_AGWN_IDT(filename, duration_threshold, dispersion_threshold,i,j)
run()