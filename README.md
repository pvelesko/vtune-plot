# Plotting Suite for Intel® Vtune Amplifier™

A set of python scripts to assist in generating publication style plots from CSV data produced by Vtune.

## Getting Started

### Plotting a pie chart showing where time is being spent
First, collect data using Vtune.  
Advanced hotspots is recommended to include individual loops rather than just functions.  

```
amplxe-cl --collect advanced-hotspots -r vtune_ah -- ./myexe
```

Generate a CSV report.  
```
amplxe-cl --report -report-output advanced-hotspots.csv -format csv -csv-delimiter comma -r vtune_ah
```

Plot  
```
python plot_pie.py advanced-hotspots.csv
```

An example CSV is included.  
```
python plot_pie.py ./data/advanced-hotspots.csv
```
![Image](./examples/advanced-hotspots-pie.png)

### Plotting a bar graph showing the changes in distribution of where time is spent
Generate data at different # of MPI ranks and generate CSV reports.  
Name each CSV report how you'd like it to appear on the final plot.  
This can be useful for plotting strong scaling or a serial application with increasing domain size.  
Using this information you can determine which loops/functions are sensitive to domain size.

Plotting all the functions/loops would be too busy so instead data is cutoff either at % of total time or  
by total # of functions/loops to be displayed.

This example was generated by running increasingly large grids. The CSVs were named based on the resulting domain size.  

Plot
```
python plot_progression.py ./data/progression/*.csv
```
![Image](./examples/progression.png)


### Prerequisites

Python 2.7  
Matplotlib - graphics  
Pandas - data handling  
Numpy - data handling  
