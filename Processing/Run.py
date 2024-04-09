import os

from matplotlib import pyplot as plt
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
Results_location = 'Results/'
#NCC_AGWN_IVT_Results_location = 

IDT_MODE = 'IDT'
IVT_MODE = 'IVT'
WIDT_MODE = 'WIDT'
WIVT_MODE = 'WIVT'
AGWN_IDT_MODE = 'AGWN_IDT'
AGWN_IVT_MODE = 'AGWN_IVT'
NCC_AGWN_IVT_MODE = 'NCC_AGWN_IVT'
NCC_AGWN_IDT_MODE = 'NCC_AGWN_IDT'
PLOT_RESULTS_MODE = 'PLOT_RESULTS'

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

def name_file(filename,analysistype,folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension

def plot_results(filename,dictionary,axis):
    results = []
    data = csvu.extract_data(filename)
    for tuple in data:
        for index, value in dictionary.items():
            if tuple[index] != value:
                continue
        results.append(tuple)
    SD = []
    S = []
    NCC = []
    for i in results:
        SD.append(i[-3])
        S.append(i[-2])
        NCC.append(i[-1])
    plt.figure()
    if axis == 'SD':
        plt.scatter(SD, NCC, color='blue')
        plt.xlabel('SD')
        plt.ylabel('NCC')
    elif axis == 'S':
        plt.scatter(S, NCC, color='blue')
        plt.xlabel('S')
        plt.ylabel('NCC')
    plt.title('Strength = ' + str(dictionary[2]))
    plt.grid(True)
    plt.show()    

def run():
    #format example: IDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: WIDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: IVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03
    #format example: WIVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03 
    mode = sys.argv[1]
    filename = sys.argv[2]
    velocity_threshold = 0.05
    strength = 0.0003
    dispersion_threshold = 0.5
    duration_threshold = 100
    standard_deviation = 0.001
    if len(sys.argv) > 3:
        if 'IVT' in mode:
            velocity_threshold = float(sys.argv[3])
            if len(sys.argv) > 4:
                strength = float(sys.argv[4])
            if len(sys.argv) > 5:
                standard_deviation = float(sys.argv[5])
        if 'IDT' in mode:
            duration_threshold = float(sys.argv[3])
            if len(sys.argv) > 4:
                dispersion_threshold = float(sys.argv[4])
            if len(sys.argv) > 5:
                strength = float(sys.argv[5])
            if len(sys.argv) > 6:
                standard_deviation = float(sys.argv[6])
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
    elif mode == PLOT_RESULTS_MODE:
        dictionary = {
            0: duration_threshold,
            1: dispersion_threshold,
            2: strength,
        }
        filename = Results_location + 'NCC_AGWN_IDT.csv'
        plot_results(filename,dictionary,'SD')

run()