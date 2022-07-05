import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import argparse


def find_area(directory, picture, project_directory):
    black_area = 9  # cm^2. This is a magic number from me measuring the square
    # Included in the image.
    img = mpimg.imread(directory + picture)
    image_copy = img.copy()
    black_mask = np.sum(img, axis=2) < 120
    image_copy[black_mask] = 255

    green_mask = (1.25 * image_copy[:, :, 0] > image_copy[:, :, 1]) & (
        1.25 * image_copy[:, :, 2] > image_copy[:, :, 1]
    )
    green_mask = np.invert(green_mask)

    #  Save the images to check if they make sense.
    plt.figure(figsize=(30, 15))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(image_copy)
    plt.savefig(
        project_directory + "Data/Output/See_black/" + picture[:-4] + "_black.png"
    )
    plt.close()

    image_copy[green_mask] = 255
    image_copy[np.invert(green_mask)] = 0
    plt.figure(figsize=(30, 15))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(image_copy)
    plt.savefig(
        project_directory + "Data/Output/See_green/" + picture[:-4] + "_green.png"
    )
    plt.close()

    return 9 / black_mask.sum() * green_mask.sum()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", type=str, help="Path to the projects directory")
    args = parser.parse_args()

    project_directory = args.root_dir
    picture_directory = project_directory + "Data/Input/Pictures/"

    growth_dict = {
        "ID": [],
        "Fungus": [],
        "Endobacteria": [],
        "Inoculation time": [],
        "Replicate Number": [],
        "Day of Picture": [],
        "Area": [],
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
        growth_dict["Area"].append(
            find_area(picture_directory, picture, project_directory)
        )

    growth_df = pd.DataFrame(growth_dict)
    print(growth_df)
    growth_df.to_csv(project_directory + "Data/Output/fern_growth.csv")
