import pandas as pd
import matplotlib.pyplot as plt

project_directory = "/home/alder/Documents/research/ferns_and_fungi/Ferns-and-Fungi/"
fern_data = pd.read_csv(project_directory + "Data/Output/fern_growth.csv")

print(fern_data.groupby("Replicate Number").mean())
print(fern_data.groupby("Fungus").mean())
