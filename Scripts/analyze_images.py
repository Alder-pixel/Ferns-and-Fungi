import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

def find_area(directory, picture):
    return 0


project_directory = "/home/alder/Documents/research/ferns_and_fungi/Ferns-and-Fungi/"
picture_directory = project_directory + "Data/Input/Pictures"

growth_dict = {
    "ID": [],
    "Fungus": [],
    "Endobacteria": [],
    "Inoculation time" : [],
    "Replicate Number" : [],
    "Day of Picture" : [],
    "Area" : []
}
for picture in os.listdir(picture_directory):
    split_name = picture.split("_")
    split_name[-1] = split_name[-1][:-4]

    growth_dict["ID"].append(picture[:-4])
    growth_dict["Fungus"].append(split_name[0])

    if split_name[0] == "control":
       growth_dict["Endobacteria"].append(np.nan)
       growth_dict["Inoculation time"].append(np.nan)
       growth_dict["Replicate Number"].append(split_name[1])
       growth_dict["Day of Picture"].append(int(split_name[2][-1]))
    else:
       growth_dict["Endobacteria"].append(split_name[0][-1])
       growth_dict["Inoculation time"].append(split_name[1])
       growth_dict["Replicate Number"].append(split_name[2])
       growth_dict["Day of Picture"].append(int(split_name[3][-1]))
    growth_dict["Area"].append(find_area(picture_directory, picture))

growth_df = pd.DataFrame(growth_dict)
print(growth_df)
