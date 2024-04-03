import os
import Filtering.CSVUtility as csvu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import Embed_watermark as ew
import Processing.Filtering.Analyze as an
import sys

reading_datasets_location = '../Datasets/Reading/'
random_datasets_location = '../Datasets/Random/'
datasets_processed_location = '../ProcessedDatasets/'
IDT_location = 'ProcessedDatasets/IDT/'
IVT_location = 'ProcessedDatasets/IVT/'
WIDT_location = 'ProcessedDatasets/WIDT/'
WIVT_location = 'ProcessedDatasets/WIVT/'

def run_IDT(fileIn, duration_threshold=30, dispersion_threshold=0.5):
    eye_tracking_data = csvu.extract_data(fileIn)
    print("eye tracking data size: " + str(len(eye_tracking_data)))
    result = idt.IDT(eye_tracking_data, duration_threshold, dispersion_threshold)
    print("result size: " + str(len(result)))
    outFile = name_file(fileIn,'IDT',IDT_location)
    csvu.write_data(outFile, result)
    return result,outFile

def run_IVT(fileIn, velocity_threshold=0):
    eye_tracking_data = csvu.extract_data(fileIn)
    result = ivt.IVT(eye_tracking_data, velocity_threshold)
    outFile = name_file(fileIn,'IVT',IVT_location)
    csvu.write_data(outFile, result)
    return result,outFile

def run_embed_watermark(fileIn, outFolder):
    data = csvu.extract_data(fileIn)
    result = ew.run_watermark(data)
    outFile = name_file(fileIn,'WM',outFolder)
    csvu.write_data(outFile, result)
    return result,outFile

def run_IDT_with_watermark(fileIn, duration_threshold=30, dispersion_threshold=0.5):
    original_idt_data,IDTFile = run_IDT(fileIn, duration_threshold, dispersion_threshold)
    _,watermarkedFile = run_embed_watermark(IDTFile, WIDT_location)
    watermarked_idt_data,_ = run_IDT(watermarkedFile,duration_threshold,dispersion_threshold)
    print(an.measure_saccade_accuracy(original_idt_data, watermarked_idt_data))    

def run_IVT_with_watermark(fileIn, velocity_treshold=0):
    original_ivt_data,IVTFile = run_IVT(fileIn,velocity_treshold)
    _,watermarkedFile = run_embed_watermark(IVTFile, WIVT_location)
    watermarked_ivt_data,_ = run_IVT(watermarkedFile,velocity_treshold)
    print(an.measure_saccade_accuracy(original_ivt_data, watermarked_ivt_data))

def name_file(filename,analysistype,folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension

def run():
    #format example: IDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: WIDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    #format example: IVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03
    #format example: WIVT ../Datasets/Reading/S_1004_S2_TEX.csv 0.03 
    mode = sys.argv[1]
    match mode:
        case 'IDT':
            if len(sys.argv) == 5:
                run_IDT(sys.argv[2],float(sys.argv[3]),float(sys.argv[4]))
            else:
                run_IDT(sys.argv[2])
        case 'IVT':
            if len(sys.argv) == 4:
                run_IVT(sys.argv[2],float(sys.argv[3]))
            else:
                run_IVT(sys.argv[2])
        case 'WIDT':
            if len(sys.argv) == 5:
                run_IDT_with_watermark(sys.argv[2],float(sys.argv[3]),float(sys.argv[4]))
            else:
                run_IDT_with_watermark(sys.argv[2])
        case 'WIVT':
            if len(sys.argv) == 4:
                run_IVT_with_watermark(sys.argv[2],float(sys.argv[3]))
            else:
                run_IVT_with_watermark(sys.argv[2])

run()