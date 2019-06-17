# Lung Vasculature Analysis

* `core`:
    * `filamentanalysis.py`: label branches
    * `fileop.py`: io control
    * `mkplot.py`: generate plots
    * `msxml.py`: convert .xml files to .csv files
* `test`: test files
* `archive_2018`: previous codes
* `main.ipynb`: main file for jupyter notebook
* `main.py`: main file for jupyter notebook in .py file. Support Vscode Python package 
* `README.md`: readme file

Instruction: 
1. Clone the repository
2. Run `main.ipynb`
3. Specify the directory of workspace and folders storaging raw data
4. Run through the code to generate histograms:
    1. histo/length/*.png: frequency - length (µm)
    2. histo/thickness/*.png: frequency - thickness (µm)
    3. histo_summary/length.png: histogram in line plot style
    4. histo_summary/thickness.png: histogram in line plot style
    

    
    