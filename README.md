# Influence of Data Fusion on Uncertainty of DNNs

This repository contains experiments for studying how different multimodal data fusion strategies affect the uncertainty behavior of deep neural networks in remote sensing segmentation tasks.
## Repository structure

- [dfc18_experiment.ipynb](dfc18_experiment.ipynb) — notebook for the experiment on the DFC2018 dataset.
- [mdas_experiment.ipynb](mdas_experiment.ipynb) — notebook for the experiment on the MDAS dataset.
- [pre_processing](pre_processing/preprocessing.py) — pipelines for preprocessing the data

## What this project does

The code is designed around remote sensing image segmentation with multiple modalities such as:
- hyperspectral imagery (HSI),
- multispectral imagery (MSI),
- RGB imagery,
- synthetic aperture radar (SAR),
- digital surface models (DSM).

The experiments compare different fusion strategies:
- no fusion,
- early fusion,
- middle fusion,
- late fusion.

The notebooks also compute uncertainty maps and related metrics to evaluate model confidence.

## Requirements

This project relies on Python with the following libraries:
- PyTorch
- NumPy
- rasterio
- albumentations

You may also need Jupyter Notebook or JupyterLab to run the notebooks.

## Setup

1. Clone the repository.
2. Create a Python environment and install the required dependencies.
3. Open the desired notebook or run the preprocessing script.
4. Replace the placeholder data paths in the scripts and notebooks with your local dataset paths.

## Data preparation

The preprocessing scripts expect large geospatial raster files and save them as patch-based .npy files.

- [pre_processing/preprocessing.py](pre_processing/preprocessing.py) prepares multispectral, SAR, RGB, DSM, and mask data.
- [pre_processing/preprocessing_hsi.py](pre_processing/preprocessing_hsi.py) prepares hyperspectral patches separately because the HSI data is very large.

The scripts currently contain placeholder values such as `IMAGE_PATH = ...` and `save_path = ...`. These must be replaced with your actual local paths before running them.

## Running the experiments

1. Download and prepare the dataset using the preprocessing scripts.
2. Open [dfc18_experiment.ipynb](dfc18_experiment.ipynb) or [mdas_experiment.ipynb](mdas_experiment.ipynb).
3. Update the dataset paths in the notebook cells.
4. Run the cells in order to train the models and evaluate fusion strategies.


