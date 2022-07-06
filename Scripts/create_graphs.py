import pandas as pd
import matplotlib.pyplot as plt
import argparse

def display_data(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")

    # Drop the fourth replicate. Almost all of my fourth replicates dried up,
    # either due to being positioned near the front or being poured earlier.
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]

    print(fern_data)
    print(fern_data.groupby("Fungus").mean())
    print(fern_data.groupby("Inoculation time").mean())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=str, help="Path to the raw data")
    parser.add_argument("outputs", type=str, help="Path to the results")
    args = parser.parse_args()
    inputs = args.inputs
    outputs = args.outputs

    display_data(inputs, outputs)

