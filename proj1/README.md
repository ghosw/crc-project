# NetworkX
## CLUSTERING COEFFICIENT
### COMPUTING IT
```bash
python3 clustering.py <N> <N_SAMPLES>
```
where N is the number of nodes for BA and DMS, and N_SAMPLES is the number of samples to run for computing clustering coefficent before averaging it 
### PLOTTING IT 
```bash
python3 clustering_graph.py <N> <SHOW_ALL_BA_VALUES>
```
where N is the number of nodes for BA and DMS (files to load and plot), and SHOW_ALL_BA_VALUES is a boolean to show all BA values for the clustering coefficient
### BA AND DMS LINES ONLY
```bash
python3 lines.py
```
This is currently hardcoded for the following N valued files for BA and DMS: [10, 10^2, 10^3, 10^4,`10^5, 10^6]. Unfortunately the file for 10^6 was not included in the code due to its large size (>100mb). If you need the file for 10^6, be warned it takes 20+ mins with 10 samples to compute.

## DEGREE DISTRIBUTION
### COMPUTING AND PLOTTING IT
```bash
python3 degree_dist.py
```
This is currently hardcoded for 10^6 nodes with its specific cutoff points.

# GraphTool
## Compute graph metrics and distributions
```bash
python3 graph_analyser <MIN_N> <MAX_N> <STEP> <N_SAMPLES>
```
Compute graph metrics and distributions for graphs with nodes between MIN_N and MAX_N, 
at each time step add STEP nodes to the graphs. In each step compute metrics and
distributions for N_SAMPLES graphs.

## Plot graph metrics
```bash
python3 plot_metrics.py
```