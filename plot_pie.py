import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

# Anything less than this %value will be grouped into "tiny loops" slice
def plot_pie(csv_path,percent_cutoff = 0.05):
    """
        Plot a donut graph representing in which loops time is being spent
    """
    data = pd.read_csv(csv_path)
    
    time_total = data[['CPU Time']].sum()[0]
    
    time_ratio = data['CPU Time']/time_total
    
    data.insert(loc=2, column='% of Total', value=time_ratio*100)
    data_cutoff = data[time_ratio > percent_cutoff]
    other = data[time_ratio < percent_cutoff].sum()
    
    other['Function'] = 'Tiny Loops'
    data_cutoff = data_cutoff.append(other, ignore_index=True).sort_values(by='CPU Time', ascending=False)
    func_times = data_cutoff[['Function', '% of Total']]
    labels=func_times['Function']
    labels_trim= labels.map(lambda x: x.strip("[]").replace("Loop at line ", ""))
    
    #pie = plt.pie(func_times['% of Total'], labels=labels_trim, autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    pie = plt.pie(func_times['% of Total'], autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    plt.legend(pie[0], labels_trim, loc="best")

    #draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.75,color='white', fc='white',linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

if __name__ == "__main__":

    l_exit = set(filter(os.path.exists, sys.argv))
    l_no_exit = set(sys.argv) - l_exit
    if l_no_exit:
        print(f"Files {l_no_exit} do not exist. Will not be printed", file=sys.stderr)
    
    for path in l_exit:
        plot_pie(path)
        plt.show()
