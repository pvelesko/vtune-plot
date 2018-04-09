#!/usr/bin/env python
import pandas as pd
import os
class VtuneCSV():
    """
        Pass a list of strings containing paths to CSV files.
        If each file name contains only integers
            - These files will be aranged in ascending order based on filename
        else:
            - These files will be aranged in the order they're passed in through CLI
    """
    data = None
    names = None
    def __init__ (self, csv_list):
        self.data = []
        self.names = [os.path.basename(a).strip(".csv") for a in csv_list]
        if isinstance(csv_list, list) == False:
            csv_list = [csv_list]

        for csv_file in csv_list:
            raw_data = pd.read_csv(csv_file, error_bad_lines=False)
            raw_data = self.remove_empty_cols(raw_data)
            raw_data = raw_data.dropna(axis=1, how="all")
            function_col = raw_data.columns[0]
            raw_data = raw_data.set_index(function_col)
            if (' [Unknown stack frame(s)]') in raw_data:
                raw_data = raw_data.drop(' [Unknown stack frame(s)]')
            raw_data = raw_data.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))
            raw_data = raw_data.groupby(raw_data.index, sort=False).first()
            self.data.append(raw_data)

    def remove_empty_cols(self, raw_data):
        empties = (raw_data.iloc[:,:].sum() != 0)
        raw_data = raw_data.iloc[:,list(empties)]
        return raw_data

    def get_frame(self, function, metric):
        a= pd.DataFrame()
        for td in self.data:
            a = pd.concat([a, td[metric]])

        a = a.loc[function]
        if len(self.data) > 1:
            a.columns = [metric]
            a.index = self.names
            try:
                a.index = [int(idx) for idx in list(a.index)]
                a = a.sort_index(ascending=True)
                a.index = [str(idx) for idx in list(a.index)]
            except ValueError:
                a.index = self.names
        a.index.name = function
        return a

if __name__ == "__main__":
    import sys
    from IPython import embed
    assert(len(sys.argv) > 1)
    csv = VtuneCSV(sys.argv[1:])
    index_list = list(csv.data[0].index)
    column_list = list(csv.data[0].columns)
    print("************************************************")
    print("Possibe Loops/Functions\n")
    print("************************************************")
    for a in index_list:
        print(a)
    print("************************************************")
    print("Possibe Metrics")
    print("************************************************")
    for a in column_list:
        print(a)
    embed()
