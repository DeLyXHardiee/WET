import os
import Filtering.CSVUtility as csvu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import Embed_watermark as ew
import Analysis.Analyze as an
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
    result = idt.IDT(eye_tracking_data, duration_threshold, dispersion_threshold)
    outFile = name_file(fileIn,'IDT',IDT_location)
    csvu.write_data(outFile, result)
    return result,outFile

def run_IVT(fileIn, outFolder, velocity_threshold=0):
    eye_tracking_data = csvu.extract_data(fileIn)
    result = ivt.IVT(eye_tracking_data, velocity_threshold)
    csvu.write_data(name_file(fileIn,'IVT',outFolder), result)
    return result

def run_embed_watermark(fileIn, outFolder):
    data = csvu.extract_data(fileIn)
    result = ew.run_watermark(data)
    outFile = name_file(fileIn,'WM',outFolder)
    csvu.write_data(outFile, result)
    return result,outFile

def run_IDT_with_watermark(fileIn, duration_threshold=30, dispersion_threshold=0.5):
    original_idt_data,outFile = run_IDT(fileIn, duration_threshold, dispersion_threshold)
    _,watermarkedFile = run_embed_watermark(outFile, WIDT_location)
    watermarked_idt_data,_ = run_IDT(watermarkedFile,duration_threshold,dispersion_threshold)
    print(an.measure_saccade_accuracy(original_idt_data, watermarked_idt_data))    

def run_IVT_with_watermark(fileIn, fileOut, velocity_treshold=0):
    og_ivt_data = run_IVT(fileIn, 'out2.csv')
    run_embed_watermark('out2.csv', 'out2_watermarked.csv')
    watermarked_ivt_data = run_IVT('out2_watermarked.csv', 'out2_watermarked_out2.csv')
    print(an.measure_saccade_accuracy(og_ivt_data, watermarked_ivt_data))

def name_file(filename,analysistype,folder):
    file_name, file_extension = os.path.splitext(os.path.basename(filename))
    new_file_name = folder + file_name + '_' + analysistype + file_extension
    print("new file name : " + new_file_name)
    return folder + file_name + '_' + analysistype + file_extension

def run():
    #format example: IDT ../Datasets/Reading/S_1004_S2_TEX.csv 100 0.5
    mode = sys.argv[1]
    match mode:
        case 'IDT':
            if len(sys.argv) == 5:
                run_IDT(sys.argv[2],float(sys.argv[3]),float(sys.argv[4]))
            else:
                run_IDT(sys.argv[2])
        case 'IVT':
            if len(sys.argv) == 5:
                run_IVT(sys.argv[2],sys.argv[3],float(sys.argv[4]))
            else:
                run_IVT(sys.argv[2],sys.argv[3])
        case 'WIDT':
            if len(sys.argv) == 5:
                run_IDT_with_watermark(sys.argv[2],float(sys.argv[3]),float(sys.argv[4]))
            else:
                run_IDT_with_watermark(sys.argv[2])
        case 'WIVT':
            if len(sys.argv) == 5:
                run_IVT_with_watermark(sys.argv[2],sys.argv[3],float(sys.argv[4]))
            else:
                run_IVT_with_watermark(sys.argv[2],sys.argv[3])
run()