#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 07:27:36 2023

@author: fsoylu
"""
import numpy as np
import pandas as pd
import nibabel as nib
import tkinter as tk
from tkinter import filedialog

def select_files(title="Select files", filetypes=(("NIfTI files", "*.nii"), ("all files", "*.*"))):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title=title, filetypes=filetypes)
    return list(file_paths)

def extract_gmv_for_subjects():
    """
    Takes segmented GM images for each participant, extracts GMV values from ROIs, 
    and returns them in a pandas DataFrame.
    """

    def extract_gmv_for_roi(img_paths, roi_path):
        roi_img = nib.load(roi_path)
        roi_data = roi_img.get_fdata()
        
        vals = []

        for img_path in img_paths:
            img = nib.load(img_path)
            img_data = img.get_fdata()
            imgvs = abs(np.linalg.det(img.affine))
            img_data = img_data * roi_data
            val = np.sum(img_data) * imgvs / 1000
            vals.append(val)

        return vals



    roi_mask_paths = select_files(title="Select all ROI files to extract values for")
    subject_img_paths = select_files(title="Select the image files for each participant")
    
    # Data structure to store GMV values for each subject and ROI
    data = {"ImageNumber": list(range(1, len(subject_img_paths) + 1))}

    for roi_path in roi_mask_paths:
        roi_name = roi_path.split('/')[-1].split('.')[0]
        gmv_values = extract_gmv_for_roi(subject_img_paths, roi_path)
        gmv_values = np.round(gmv_values, 4)
        data[roi_name] = gmv_values

    # Create a DataFrame and return
    df = pd.DataFrame(data)
    return df

# Usage example
df = extract_gmv_for_subjects()
df.to_csv("ROI_extracted_GMV.csv", index=False)
