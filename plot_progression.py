import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

def plot_progression(csv_paths, total_pct=True, kind="bar", cutoff=("number", 4), targets = []):
    """
        Plot either a line or a bar graph representing changes in where time
        is being spent with increasing MPI ranks
        cutoff = ("numbe", 5) or cutoff = ("percentage", 34)
    """
    net_data = pd.DataFrame()
    names = []
    for i in range(0,len(csv_paths)):
        percent_cutoff = cutoff[1]/100 # percentage of top consumer loops to display
        num_cutoff = cutoff[1] # number of loops to display
        data = pd.read_csv(csv_paths[i], index_col='Function')[['CPU Time']]
        names.append(os.path.basename(csv_paths[i]).strip(".csv"))
        time_total = data[['CPU Time']].sum()[0]
        data.insert(loc=1, column='% of Total', value=data['CPU Time']/time_total*100)

        other = pd.DataFrame(index=['Other Loops'], columns=data.columns)
        if cutoff[0] == "number":
            data_cutoff = data.iloc[0:num_cutoff, :]
            other.loc['Other Loops']  = data.iloc[num_cutoff:, :].sum()
        elif cutoff[0] == "percentage":
            data_cutoff = data[data['CPU Time']/time_total > percent_cutoff]
            other.loc['Other Loops']= data[data['CPU Time']/time_total < percent_cutoff].sum()
        else:
            sys.exit("Cutoff must be either 'number' or 'percentage'")
        data_cutoff = data_cutoff.append(other)

        #from IPython import embed; embed()
        if targets != []:
            if targets[0] == 'total':
                data_cutoff = pd.DataFrame(data.sum())
                data_cutoff.columns = ['total']
                data_cutoff = data_cutoff.transpose()
            else:
                data_cutoff = data.loc[targets]


        if total_pct == True:
            slice_this = '% of Total'
        else:
            slice_this = 'CPU Time'
        data_cutoff.rename(lambda x: x.strip("[]").replace("Loop at line ", ""))
        if i==0: # Slice out only the % of times
            net_data = data_cutoff[[slice_this]]
        else:
            net_data = pd.concat([net_data, data_cutoff[slice_this]], axis=1)

    net_data.columns = names
    sorted_names = [int(idx) for idx in names]
    sorted_names.sort()
    sorted_names = [str(idx) for idx in sorted_names]
    net_data = net_data[sorted_names] # make sure data appears in increasing order
    # Make sure that the data starts with most expensive column first
    net_data = net_data.sort_values(sorted_names[0], ascending=False)
    plot_data = net_data.transpose()
    if kind == "stack":
        ax = plt.stackplot(range(len(sorted_names)), [list(plot_data.iloc[:,a]) for a in range(len(plot_data.columns))], labels=plot_data.columns)
        plt.legend(loc="lower right")
        plt.xticks(range(len(sorted_names)), sorted_names, rotation='vertical')
        if total_pct == True:
            locs, labels = plt.yticks()
            plt.yticks(locs, ["%s%%" % a for a in locs])
            plt.ylim(0,100)
            plt.ylabel("% of Total Time")
        else:
            plt.ylabel("CPU Time(s)")
        plt.xlabel("Number of Elements")

    else:
        ax = plot_data.plot(kind=kind)
        ax.set_xticklabels(ax.get_xticklabels(), rotation='vertical')
        ax.set_xlabel("Number of Elements")
        if total_pct == True:
            ax.set_yticklabels(["%s%%" % pct for pct in ax.get_yticks()])
            ax.set_ylim(0, 75)
            ax.set_ylabel("% of Total Time")
        else:
            ax.set_ylabel("CPU Time(s)")


csv_names = []
for i in range(1,len(sys.argv)):
    if (not os.path.exists(sys.argv[i])):
        print("File %s not found" % csv_name)
        quit()
    csv_names.append(os.path.abspath(sys.argv[i]))

#plot_pie(csv_names[0])
#plot_progression(csv_names, kind="stack")
#plot_progression(csv_names, kind="line", targets = ['[Loop at line 4015 in gwce_new]', '[Outside any loop]'])
plot_progression(csv_names, kind="line", total_pct=False,targets = ['total'])
plt.show()
