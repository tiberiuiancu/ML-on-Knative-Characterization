# Experiment code and analysis notebooks for my BSc. thesis

## Experiment code

The folder `experiment-code` contains the code used to run the experiments in the thesis. 
- `Dockerfile`: packages the code, images and files
- `dates.csv`: contains a one day sample of the arrival time of events to the model server
- `images`: sample images to send to the model sever for prediction
- `request.py`: the script that runs the experiments

## Data analysis
The directory `analysis` contains data analysis of the monitored models.
- `analysis/trends.ipynb`: used in the background section
- `analysis/trace-exploration.ipynb`: plots inference request duration, and event arrival times
- `analysis/metrics-exploration.ipynb`: CPU and memory usage plots

## Experiment analysis
The directory `experiments` contains the data analysis of the experiments ran with `experiment-code`.
- `experiments/analysis.ipynb` contains the code and plots used in the report
