import pandas as pd

data = pd.read_excel("./eventdata.xlsx")
data = data['GPS포인트집합']
data.dropna(how="all", inplace=True)
data.reset_index(drop=True, inplace=True)
data = data.head(10)
print(data)
data.to_excel("pre_data_test.xlsx")