# Lung Vasculature Analysis

## Introduction
Features: Python, Pandas, Numpy, Matplotlib

This project was to analyze mice lung vasculature labeled with gold nanoparticles. 3D tomography was acquired from Zeiss Xradia. I used Amira to segment targeted regions by combining a series of background subtraction, edge detection, and manual labeling. Filament analysis was then applied by using built-in auto-skeletonization to extract the backbone of lung vasculature and its diameter. 

## Repository
* `core`:
    * `filamentanalysis.py`: label branches
    * `fileop.py`: io control
    * `mkplot.py`: generate plots
    * `msxml.py`: convert .xml files to .csv files
* `test`: test files
* `archive_2018`: previous codes
* `par`: 
    `lung_file_idx.csv`: file information    
* `main.ipynb`: main file for jupyter notebook
* `main.py`: main file for jupyter notebook in .py file. Support Vscode Python package 
* `README.md`: readme file

## Instruction 
1. Clone the repository
2. Create a directory for data storage
3. Make a subfolder called 'raw' and copy the .xml files. 
4. Copy `par` folder to the data folder
5. rename *.xml by adding index in the begin of the filename
    * for example: FOR7-DFF-Hypoxia.xml -> 17_FOR7-DFF-Hypoxia.xml. Index is based on `lung_file_idx.csv`
    * update the column of `data_filename` in `lung_file_idx.csv`
6. Run `main.ipynb`
7. Specify the directory of workspace
8. Run through the code and generate histograms:
    1. histo/length/*.png: frequency - length (µm)
    2. histo/thickness/*.png: frequency - thickness (µm)
    3. histo_summary/length.png: histogram in line plot style
    4. histo_summary/thickness.png: histogram in line plot style

![](/figures/lung_vasculature.png)

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.