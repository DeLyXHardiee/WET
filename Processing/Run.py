import Filtering.CSVUtility as csvu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import Embed_watermark as ew
import Analysis.Analyze as an

def run_IDT(fileIn, fileOut, duration_threshold=30, dispersion_threshold=0.5):
    eye_tracking_data = csvu.extract_data(fileIn)
    result = idt.IDT(eye_tracking_data, duration_threshold, dispersion_threshold)
    csvu.write_data(fileOut, result)
    return result

def run_IVT(fileIn, fileOut, velocity_threshold=0):
    eye_tracking_data = csvu.extract_data(fileIn)
    result = ivt.IVT(eye_tracking_data, velocity_threshold)
    csvu.write_data(fileOut, result)
    return result

def run_embed_watermark(fileIn, fileOut):
    data = csvu.extract_data(fileIn)
    result = ew.run_watermark(data)
    csvu.write_data(fileOut, result)
    return result

og_idt_data = run_IDT('../Datasets/Reading/S_1004_S2_TEX.csv', 'out.csv')

run_embed_watermark('out.csv', 'out_watermarked.csv')

watermarked_idt_data = run_IDT('out_watermarked.csv', 'out_watermarked_out.csv')

print(an.measure_saccade_accuracy(og_idt_data, watermarked_idt_data))

og_ivt_data = run_IVT('../Datasets/Reading/S_1004_S2_TEX.csv', 'out2.csv')

run_embed_watermark('out2.csv', 'out2_watermarked.csv')

watermarked_ivt_data = run_IVT('out2_watermarked.csv', 'out2_watermarked_out2.csv')

print(an.measure_saccade_accuracy(og_ivt_data, watermarked_ivt_data))