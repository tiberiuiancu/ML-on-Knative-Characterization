# Experiment code and analysis notebooks for my BSc. thesis

### Repository structure

#### Experiment code

The folder `experiment-code` contains the code used to run the experiments in the thesis. 
- `Dockerfile`: packages the code, images and files
- `dates.csv`: contains a one day sample of the arrival time of events to the model server
- `images`: sample images to send to the model sever for prediction
- `request.py`: the script that runs the experiments

#### Data analysis
The directory `analysis` contains data analysis of the monitored models.
- `analysis/trends.ipynb`: used in the background section
- `analysis/trace-exploration.ipynb`: plots inference request duration, and event arrival times
- `analysis/metrics-exploration.ipynb`: CPU and memory usage plots

#### Experiment analysis
The directory `experiments` contains the data analysis of the experiments ran with `experiment-code`.
- `experiments/analysis.ipynb` contains the code and plots used in the report

### Data download

There are two datasets produced during this research, hosted on Zenodo. The first of the two artifacts was used during exploratory data analysis, while the second was collected from the experiments we ran. The jupyter notebooks used for analysis rely on these datasets to be downloaded to the right location:

1. download the two dataset files used in data analysis from [Zenodo](https://zenodo.org/record/8104182) and place them in the folder `analysis/data/processed`.

2. download the two dataset files used in the experiment analysis from [Zenodo](https://zenodo.org/record/8104192) and place them in the folder `experiments/data/processed`.

### How to run

1. make sure to have valid Python 3 and R installations
2. install jupyter notebook with 
```bash
pip install jupyter notebook
```
3. install the R kernel for jupyter
```R
install.packages('IRkernel')
IRkernel::installspec()
```
4. clone this repository and `cd` into the root folder
5. start jupyter notebook; now you may run the analysis notebooks
```bash
jupyter notebook
```
