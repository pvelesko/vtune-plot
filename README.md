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


### Prerequisites

Python 2.7  
Matplotlib - graphics  
Pandas - data handling  
Numpy - data handling  
