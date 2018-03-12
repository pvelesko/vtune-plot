import pandas as pd
import os
class VtuneCSV():
    """
        Pass a list of strings containing paths to CSV files.
        Each file name should only contain integers
            - These files will be plotted in ascending order based on filename
    """
    data = None
    names = None
    def __init__ (self, csv_list):
        self.data = []
        self.names = [os.path.basename(a).strip(".csv") for a in csv_list]
        if isinstance(csv_list, list) == False:
            csv_list = [csv_list]

        for csv_file in csv_list:
            raw_data = pd.read_csv(csv_file)
            raw_data = self.remove_empty_cols(raw_data)
            raw_data = raw_data.dropna(axis=1, how="all")
            function_col = raw_data.columns[0]
            raw_data = raw_data.set_index(function_col)
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
        a.columns = [metric]
        a = a.loc[function]
        a.index = self.names
        a.index = [int(idx) for idx in list(a.index)]
        a = a.sort_index(ascending=True)
        a.index = [str(idx) for idx in list(a.index)]
        a.index.name = function
        return a
