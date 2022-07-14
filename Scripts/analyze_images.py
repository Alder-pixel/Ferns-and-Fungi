import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import argparse

# The code takes me ~7 seconds per picture to run.


def find_area(directory, picture, project_directory):
    black_area = 9  # cm^2. This is a MAGIC number from me measuring the square
    # Included in the image.
    img = mpimg.imread(directory + picture)
    image_copy = img.copy()
    black_mask = np.sum(img, axis=2) < 120  # MAGIC: I looked at a histogram of
    # the brightness to choose this threshold.
    image_copy[black_mask] = 255  # Makes it white. My code fo find the green
    # values also picks up on very dark values.

    # Picks the green values pixels based on the following logic:
    # You can't both have red be more than 25% of green as well
    # as blue being more than 25% of green.
    # The mask gets inverted because there isn't a symbol for nand.
    green_mask = (1.2 * image_copy[:, :, 0] > image_copy[:, :, 1]) & (
        1.2 * image_copy[:, :, 2] > image_copy[:, :, 1]
    )
    green_mask = np.invert(green_mask)

    #  Save the images to check if they make sense.

    # Saves the image highlighting the black square the code picks up.
    plt.figure(figsize=(30, 15))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(image_copy)
    plt.savefig(
        project_directory + "Data/Output/See_black/" + picture[:-4] + "_black.png"
    )
    plt.close()

    # Sets the green values to white and the rest to black, allowing me to
    # scroll through to make sure the code is doing what it should.
    image_copy[green_mask] = 255
    image_copy[np.invert(green_mask)] = 0

    # Saves the image showing the green color the code picks up.
    plt.figure(figsize=(30, 15))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(image_copy)
    plt.savefig(
        project_directory + "Data/Output/See_green/" + picture[:-4] + "_green.png"
    )
    plt.close()

    return black_area / black_mask.sum() * green_mask.sum()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", type=str, help="Path to the projects directory")
    parser.add_argument("recreate", type=str, help="Yes to recreate, No to not")
    args = parser.parse_args()

    project_directory = args.root_dir
    recreate = args.recreate
    picture_directory = project_directory + "Data/Input/Pictures/"
    output_file = project_directory + "Data/Output/fern_growth.csv"
    if recreate == "No":
        ferndf = pd.read_csv(output_file)

    # An example ID is GBAus27b+_I0_R1_T7
    # Another example ID is control_R3_T8
    # The code below extracts the information from this format.
    growth_dict = {
        "ID": [],
        "Fungus": [],
        "Endobacteria": [],
        "Inoculation time": [],
        "Replicate Number": [],
        "Day of Picture": [],
        "Area": [],
    }
    counter = 0
    length = len(os.listdir(picture_directory))
    for picture in os.listdir(picture_directory):
        split_name = picture.split("_")
        split_name[-1] = split_name[-1][:-4]  # Removes the extension.
        if recreate == "No" and picture[:-4] in ferndf["ID"].values:
            continue
        growth_dict["ID"].append(picture[:-4])  # Removes the extension
        growth_dict["Fungus"].append(split_name[0])

        # The control group does not have an inoculation time, therefore the
        # numbers are slightly off from the inoculated samples.
        if split_name[0] == "control":
            growth_dict["Endobacteria"].append(np.nan)
            growth_dict["Inoculation time"].append(np.nan)
            growth_dict["Replicate Number"].append(split_name[1])
            growth_dict["Day of Picture"].append(int(split_name[2][1:]))
        else:
            growth_dict["Endobacteria"].append(split_name[0][-1])
            growth_dict["Inoculation time"].append(split_name[1])
            growth_dict["Replicate Number"].append(split_name[2])
            growth_dict["Day of Picture"].append(int(split_name[3][1:]))
        growth_dict["Area"].append(
            find_area(picture_directory, picture, project_directory)
        )
        counter += 1
        if counter % 5 == 0:
            print(round(counter * 100 / length, 1), "%")
    growth_df = pd.DataFrame(growth_dict)
    if recreate == "No":
        growth_df = pd.concat([ferndf, growth_df])
    print(growth_df)  # Good for checking that it actually worked
    growth_df.to_csv(output_file, index=False)
