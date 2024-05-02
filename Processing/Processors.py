import math
import os
import random

from matplotlib import pyplot as plt
import numpy as np
import Filtering.CSVUtility as csvu
import Filtering.JSONUtility as jsonu
import Filtering.BINUtility as binu
import Filtering.IDT as idt
import Filtering.IVT as ivt
import W_Trace_Watermark as ew
import Adversary as ad
import Analyze as an
import random
from memory_profiler import profile
import sys
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.clean_path = "ProcessedDatasets/CLEAN/"
        self.clean_attacked_path = "ProcessedDatasets/CLEAN_ATTACKED/"
        self.wm_path = "ProcessedDatasets/WM/"
        self.wm_attacked_path = "ProcessedDatasets/WM_ATTACKED/"
        self.analysis_path = "ProcessedDatasets/ANALYSIS/"
        self.context_file = "context.json"
        self.current_context = jsonu.extract_context(current_directory + self.context_file)

    def get_data_name(self):
        return self.current_context["Dataset"] + "/"

    def process_data(self):
        raise NotImplementedError

    def create_new_context(self):
        raise NotImplementedError

    def create_target_directory(self):
        raise NotImplementedError

class IVTProcessor(DataProcessor):
    def __init__(self, current_directory):
        super().__init__(current_directory)
        self.target_directory = self.create_target_directory()
        self.velocities = self._load_velocities()


    def process_data(self):
        files = csvu.list_csv_files_in_directory(self.current_directory)
        for file in files:
            data = csvu.extract_data(self.current_directory + file)
            velocity = self.velocities[file]
            data = ivt.IVT(data, velocity)
            csvu.write_data(self.target_directory + file, data)
        return self.target_directory

    def create_new_context(self):
        new_context = {}
        files = csvu.list_csv_files_in_directory(self.current_directory)
        for file in files:
            new_context[file] = ivt.find_best_threshold(csvu.extract_data(self.current_directory + file))
        new_context["Dataset"] = self.current_context["Dataset"]
        jsonu.write_context_to_json(new_context, self.target_directory + self.context_file)

    def _load_velocities(self):
        if not jsonu.file_exists(self.target_directory, self.context_file):
            self.create_new_context()
        velocities = jsonu.extract_context(self.target_directory + self.context_file)
        return velocities

    def create_target_directory(self):
        return self.clean_path + self.get_data_name()

class WMProcessor(DataProcessor):
    def __init__(self, old_directory, strength):
        super().__init__(old_directory)
        self.strength = strength
        self.velocities = self._load_velocities()
        self.target_directory = self.create_target_directory()

    def process_data(self):
        files = csvu.list_csv_files_in_directory(self.current_directory)
        for file in files:
            data = csvu.extract_data(self.current_directory + file)
            velocity = self.velocities[file]
            data, watermark = ew.run_watermark(data, self.strength)
            data = ivt.IVT(data, velocity)
            csvu.write_data(self.target_directory + file, data)
        self.create_new_context()
        return self.target_directory

    def create_new_context(self):
        context = {
            "Dataset": self.current_context["Dataset"],
            "WM_ID": random.randint(1, 1000000),
            "WM_strength": self.strength,
            "filter_context_path": self.current_directory + self.context_file
        }
        jsonu.write_context_to_json(context, self.target_directory + self.context_file)

    def _load_velocities(self):
        return jsonu.extract_context(self.current_directory + self.context_file)

    def create_target_directory(self):
        return self.wm_path + self.get_data_name()

class AttackProcessor(DataProcessor):
    def __init__(self, current_directory, attack_type, strength):
        super().__init__(current_directory)
        self.attack_type = attack_type
        self.strength = strength
        self.velocities = self._load_velocities()
        self.target_directory = self.create_target_directory()

    def process_data(self):
        files = csvu.list_csv_files_in_directory(self.current_directory)
        for file in files:
            data = csvu.extract_data(self.current_directory + file)
            attack_function = getattr(ad, f"{self.attack_type}_attack")
            data = attack_function(data, self.strength)
            velocity = self.velocities[file]
            data = ivt.IVT(data, velocity)
            csvu.write_data(self.target_directory + file, data)
        self.create_new_context()
        return self.target_directory

    def _load_velocities(self):
        context = jsonu.extract_context(self.current_directory + self.context_file)
        velocities = jsonu.extract_context(context["filter_context_path"])
        return velocities

    def create_new_context(self):
        context = jsonu.extract_context(self.current_directory + self.context_file)
        context = {
            "Dataset": self.current_context["Dataset"],
            "WM_ID": context["WM_ID"],
            "Attack_type": self.attack_type,
            "Strength": self.strength,
            "filter_context_path": context["filter_context_path"],
            "WM_strength": self.current_context["WM_strength"]
        }
        jsonu.write_context_to_json(context, self.target_directory + self.context_file)

    def create_target_directory(self):
        return self.wm_attacked_path + self.get_data_name() + self.attack_type + "/"


class NCCProcessor(DataProcessor):
    def __init__(self, old_directory):
        super().__init__(old_directory)
        self.analysis_type = "NCC"
        self.target_directory = self.create_target_directory()
        self.analysis = {}


    def process_data(self):
        current_files = csvu.list_csv_files_in_directory(self.current_directory)
        clean_files = csvu.list_csv_files_in_directory(self.clean_path + self.get_data_name())
        wm_files = csvu.list_csv_files_in_directory(self.wm_path + self.get_data_name())
        wm_context = jsonu.extract_context(self.wm_path + self.get_data_name() + self.context_file)
        for i in range(0, len(current_files)):
            print("NCC performed on: " + current_files[i])
            att_data = csvu.extract_data(self.current_directory + current_files[i])
            clean_data = csvu.extract_data(self.clean_path + self.get_data_name() + clean_files[i])
            wm_data = csvu.extract_data(self.wm_path + self.get_data_name() + wm_files[i])
            real_wm = ew.unrun_watermark(wm_data, clean_data, wm_context["WM_strength"])
            att_wm = ew.unrun_watermark(att_data, clean_data, wm_context["WM_strength"])
            self.analysis[current_files[i]] = an.normalized_cross_correlation(real_wm, att_wm)
            print("Mean NCC: " + str(self.analysis[current_files[i]]))
        self.create_new_context()
        return self.target_directory

    def create_new_context(self):
        wm_context = jsonu.extract_context(self.wm_path + self.get_data_name() + self.context_file)
        new_context = {
            "Dataset": self.current_context["Dataset"],
            "Directory 1": self._get_truth_folder(),
            "Directory 2": self.current_directory,
            "Analysis": "NCC",
            "Scores": self.analysis,
            "Mean_score": np.mean(list(self.analysis.values())),
            "Attack_type": self.current_context["Attack_type"],
            "Attack_strength": self.current_context["Strength"],
            "WM_strength": wm_context["WM_strength"]
        }
        jsonu.write_context_to_json(new_context, self.target_directory + "context.json")

    def _get_truth_folder(self):
        return self.wm_path + self.get_data_name() + "/"

    def create_target_directory(self):
        return self.analysis_path + self.analysis_type + "/"

class NCCProcessorWithLength(DataProcessor):
    def __init__(self, old_directory, slize_size):
        super().__init__(old_directory)
        self.analysis_type = "NCCL"
        self.slize_size = int(slize_size)
        self.target_directory = self.create_target_directory()
        self.analysis = {}


    def process_data(self):
        current_files = csvu.list_csv_files_in_directory(self.current_directory)
        clean_files = csvu.list_csv_files_in_directory(self.clean_path + self.get_data_name())
        wm_files = csvu.list_csv_files_in_directory(self.wm_path + self.get_data_name())
        wm_context = jsonu.extract_context(self.wm_path + self.get_data_name() + self.context_file)
        for i in range(0, len(current_files)):
            att_data = csvu.extract_data(self.current_directory + current_files[i])
            clean_data = csvu.extract_data(self.clean_path + self.get_data_name() + clean_files[i])
            wm_data = csvu.extract_data(self.wm_path + self.get_data_name() + wm_files[i])
            real_wm = ew.unrun_watermark(wm_data, clean_data, wm_context["WM_strength"])
            att_wm = ew.unrun_watermark(att_data, clean_data, wm_context["WM_strength"])
            ncc_values = []
            mean_ncc = 0
            for start_idx in range(0, len(wm_data), self.slize_size):
                end_idx = min(start_idx + self.slize_size, len(wm_data))
                # Extract a slice from the real watermark
                real_wm_slice = real_wm[start_idx:end_idx]
                # Extract the corresponding slice from the attacked data
                att_wm_slice = att_wm[start_idx:end_idx]
                # Compute NCC for the current slice pair
                ncc_slice = an.normalized_cross_correlation(real_wm_slice, att_wm_slice)
                # Append the NCC value to the list
                ncc_values.append(ncc_slice)
            # Compute the mean NCC value across all slices
                mean_ncc = np.mean(ncc_values)
                self.analysis[current_files[i]] = mean_ncc
            print("NCC performed on: " + current_files[i])
            print("Mean NCC: " + str(mean_ncc))
        self.create_new_context()
        return self.target_directory

    def create_new_context(self):
        wm_context = jsonu.extract_context(self.wm_path + self.get_data_name() + self.context_file)
        new_context = {
            "Dataset": self.current_context["Dataset"],
            "Analysis": "NCC",
            "Scores": self.analysis,
            "Mean_score": np.mean(list(self.analysis.values())),
            "Attack_type": self.current_context["Attack_type"],
            "Attack_strength": self.current_context["Strength"],
            "WM_strength": wm_context["WM_strength"]
        }
        jsonu.write_context_to_json(new_context, self.target_directory + "context.json")


    def create_target_directory(self):
        return self.analysis_path + self.analysis_type + "/"

class AttackAnalysisProcessor(DataProcessor):
    def __init__(self, current_directory, attack_type, strength):
        self.attack_processor = AttackProcessor(current_directory, attack_type, strength)

    def process_data(self):
        attacked_data_directory = self.attack_processor.process_data()
        ncc_processor = NCCProcessor(attacked_data_directory)
        ncc_processor.process_data()
        saccade_processor = SaccadeProcessor(attacked_data_directory)
        saccade_processor.process_data()
        csvu.append_result("Results/NCC_AT_AV.csv",(self.attack_processor.attack_type, self.attack_processor.strength, 
                                                    np.mean(list(ncc_processor.analysis.values())), 
                                                    np.mean(list(saccade_processor.analysis.values())), 
                                                    np.mean(list(saccade_processor.degrees.values())), 
                                                    np.mean(list(saccade_processor.rms.values()))))
        
class SaccadeProcessor(DataProcessor):
    def __init__(self, current_directory):
        super().__init__(current_directory)
        self.analysis_type = "SACC"
        self.target_directory = self.create_target_directory()
        self.analysis = {}
        self.degrees = {}
        self.rms = {}

    def process_data(self):
        current_files = csvu.list_csv_files_in_directory(self.current_directory)
        truth_files = csvu.list_csv_files_in_directory(self._get_truth_folder())
        for i in range(0, len(current_files)):
            data = csvu.extract_data(self.current_directory + current_files[i])
            truth = csvu.extract_data(self._get_truth_folder() + truth_files[i])
            self.analysis[current_files[i]] = an.measure_saccade_accuracy(data, truth)
            print("SACC performed on: " + current_files[i])
            print("SACC accuracy: " + str(self.analysis[current_files[i]]))
            self.degrees[current_files[i]] = an.measure_degrees_of_visual_angle(data,truth)
            self.rms[current_files[i]] = an.measure_rms_precision(data)
        self.create_new_context()
        #csvu.append_result("Results/SaccadeAccuracies.csv",(self.current_context['WM_strength'],np.mean(list(self.analysis.values())),np.mean(list(self.degrees.values())),np.mean(list(self.rms.values()))))
        return self.target_directory

    def create_new_context(self):
        new_context = {
            "Directory 1": self._get_truth_folder(),
            "Directory 2": self.current_directory,
            "Analysis": self.analysis_type,
            "Scores": self.analysis,
            "Mean_score": np.mean(list(self.analysis.values())),
            "Degrees": self.degrees,
            "Mean_degrees": np.mean(list(self.degrees.values())),
            "RMS": self.rms,
            "Mean_RMS": np.mean(list(self.rms.values())),
            "WM_strength": self.current_context['WM_strength']
        }
        jsonu.write_context_to_json(new_context, self.target_directory + "context.json")

    def _get_truth_folder(self):
        return self.clean_path + self.get_data_name() + "/"

    def create_target_directory(self):
        return self.analysis_path + self.analysis_type + "/"


