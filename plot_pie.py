from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os


# Anything less than this %value will be grouped into "tiny loops" slice
percent_cutoff = 0.05

def plot_pie(csv_path):
    """
        Plot a donut graph representing in which loops time is being spent
    """
    data = pd.read_csv(csv_path)
    time_total = data[['CPU Time']].sum()[0]
    data.insert(loc=2, column='% of Total', value=data['CPU Time']/time_total*100)
    data_cutoff = data[data['CPU Time']/time_total > percent_cutoff]
    other = data[data['CPU Time']/time_total < percent_cutoff].sum()
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


for i in range(1,len(sys.argv)):
    if (not os.path.exists(sys.argv[i])):
        print("File %s not found" % csv_name)
        quit()
    plot_pie(sys.argv[i])
    plt.show()
