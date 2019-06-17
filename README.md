# Lung Vasculature Analysis

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
    

    
    