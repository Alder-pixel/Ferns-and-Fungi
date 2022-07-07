import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def display_data(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")

    # Drop the fourth replicate. Almost all of my fourth replicates dried up,
    # either due to being positioned near the front or being poured earlier.
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]

    print(fern_data)
    print(fern_data.groupby("Fungus").mean())
    print(fern_data.groupby("Inoculation time").mean())
    print(fern_data.groupby(["Fungus", "Inoculation time",
                             "Day of Picture"], as_index=False).mean())

def create_figure1(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    df = fern_data.groupby(["Fungus", "Inoculation time",
                            "Day of Picture"], as_index = False).mean()
    df2 = fern_data.groupby(["Fungus"], as_index = False).mean()

    plt.figure(figsize=(20,10))

    # Create the masks
    print("Before first mask")
    m1 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I0")
    print("After first mask")
    m2 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I7")
    m3 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I0")
    m4 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I7")
    m5 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I0")
    m6 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I7")
    m7 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I0")
    m8 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I7")

    # Create the plots
    plt.plot(df[m1]["Day of Picture"], df[m1]["Area"], ls="-", alpha=1,
             color="red", label="GBAus27b+ I0")
    plt.plot(df[m2]["Day of Picture"], df[m2]["Area"], ls="-", alpha=.7,
             color="red", label="GBAus27b+ I7")
    plt.plot(df[m3]["Day of Picture"], df[m3]["Area"], ls="--", alpha=1,
             color="red", label="GBAus27b- I0")
    plt.plot(df[m4]["Day of Picture"], df[m4]["Area"], ls="--", alpha=.7,
             color="red", label="GBAus27b- I7")
    plt.plot(df[m5]["Day of Picture"], df[m5]["Area"], ls="-", alpha=1,
             color="purple", label="NVP64+ I0")
    plt.plot(df[m6]["Day of Picture"], df[m6]["Area"], ls="-", alpha=.7,
             color="purple", label="NVP64+ I7")
    plt.plot(df[m7]["Day of Picture"], df[m7]["Area"], ls="--", alpha=1,
             color="purple", label="NVP64- I0")
    plt.plot(df[m8]["Day of Picture"], df[m8]["Area"], ls="--", alpha=.7,
             color="purple", label="NVP64- I7")
    plt.legend()

    plt.savefig(outputs + "figure1.png", dpi=400)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=str, help="Path to the raw data")
    parser.add_argument("outputs", type=str, help="Path to the results")
    args = parser.parse_args()
    inputs = args.inputs
    outputs = args.outputs

    display_data(inputs, outputs)
    create_figure1(inputs, outputs)
