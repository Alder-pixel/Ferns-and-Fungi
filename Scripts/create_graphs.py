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
    print(
        fern_data.groupby(
            ["Fungus", "Inoculation time", "Day of Picture"], as_index=False
        ).mean()
    )

def create_figure5A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    df = fern_data.replace(
        {
            "GBAus27b+": "GBAus27b",
            "GBAus27b-": "GBAus27b",
            "control": "None",
            "NVP64+": "NVP64",
            "NVP64-": "NVP64",
        }
    )
    df2 = df.groupby(["Fungus", "Inoculation time"], as_index=False).mean()
    df2["Name"] = df2["Fungus"] + "_" + df2["Inoculation time"]
    df2["Color"] = df2["Fungus"].replace({"GBAus27b":"Red", "NVP64":"Purple"})
    # I added the code to color by fungus type, but it looked terrible.
    df3 = df2.sort_values(by=["Inoculation time", "Fungus"])
    heights = df3["Area"].values

    plt.figure(figsize=(15,10))
    plt.bar(df3["Name"], df3["Area"])
    plt.title("Fern Growth by Fungus and Inoculation time", size=32)
    plt.xlabel("Fungi and Inoculation time", size=22)
    plt.ylabel("Average Coverage cm$^{2}$", size=22)
    plt.text(x=1,y=heights[1]+.04,size=18,ha="center",
             s="+"+str(round(100*(heights[1]/heights[0]-1),1))+"%")
    plt.text(x=3,y=heights[3]+.04,size=18,ha="center",
             s="+"+str(round(100*(heights[3]/heights[2]-1),1))+"%")
    plt.savefig(outputs + "Graphs/figure5A.png", dpi=400)


def create_figure4A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    fern_data = fern_data[fern_data["Fungus"] != "control"]
    fern_data["Inoculation day"] = fern_data["Inoculation time"].str[-1].values.astype(int)
    fern_data["Day after"] = fern_data["Day of Picture"] - fern_data["Inoculation day"]

    df = fern_data.groupby(
        ["Fungus", "Inoculation time", "Day of Picture"], as_index=False
    ).mean()

    plt.figure(figsize=(20, 10))
    # Create the masks
    m1 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I0")
    m2 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I7")
    m3 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I0")
    m4 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I7")
    m5 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I0")
    m6 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I7")
    m7 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I0")
    m8 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I7")

    # Create the plots
    plt.plot(
        df[m1]["Day after"],
        df[m1]["Area"],
        ls="-",
        color="red",
        label="GBAus27b+ I0",
        lw=5,
    )
    plt.plot(
        df[m2]["Day after"],
        df[m2]["Area"],
        ls="-",
        color="red",
        label="GBAus27b+ I7",
        lw=3,
    )
    plt.plot(
        df[m3]["Day after"],
        df[m3]["Area"],
        ls="--",
        color="red",
        label="GBAus27b- I0",
        lw=5,
    )
    plt.plot(
        df[m4]["Day after"],
        df[m4]["Area"],
        ls="--",
        color="red",
        label="GBAus27b- I7",
        lw=2,
    )
    plt.plot(
        df[m5]["Day after"],
        df[m5]["Area"],
        ls="-",
        color="purple",
        label="NVP64+ I0",
        lw=5,
    )
    plt.plot(
        df[m6]["Day after"],
        df[m6]["Area"],
        ls="-",
        color="purple",
        label="NVP64+ I7",
        lw=2,
    )
    plt.plot(
        df[m7]["Day after"],
        df[m7]["Area"],
        ls="--",
        color="purple",
        label="NVP64- I0",
        lw=5,
    )
    plt.plot(
        df[m8]["Day after"],
        df[m8]["Area"],
        ls="--",
        color="purple",
        label="NVP64- I7",
        lw=3,
    )

    plt.title("Fern Growth Measured from Inoculation", size=32)
    plt.ylabel("Area cm$^{2}$", size=22)
    plt.xlabel("Day after inoculation", size=22)
    plt.legend(prop={"size": 18})

    plt.savefig(outputs + "Graphs/figure4A.png", dpi=400)


def create_figure3A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data["Group"] = fern_data["Fungus"] + "_" + fern_data["Inoculation time"]
    fern_data.fillna("Control", inplace=True)
    df1 = fern_data.groupby(["Group", "Replicate Number"], as_index=False).mean()

    m1 = df1["Replicate Number"] == "R1"
    m2 = df1["Replicate Number"] == "R2"
    m3 = df1["Replicate Number"] == "R3"
    m4 = df1["Replicate Number"] == "R4"

    plt.figure(figsize=(15, 5))
    plt.scatter(df1[m1]["Group"], df1[m1]["Area"], color="black", label="Replicate 1-3")
    plt.scatter(df1[m2]["Group"], df1[m2]["Area"], color="black")
    plt.scatter(df1[m3]["Group"], df1[m3]["Area"], color="black")
    plt.scatter(
        df1[m4]["Group"],
        df1[m4]["Area"],
        color="red",
        marker="x",
        s=90,
        label="Replicate 4",
    )

    plt.legend()
    plt.xlabel("Group", size=22)
    plt.ylabel("Avg Coverage cm$^{2}$", size=22)
    plt.title("Replicate 4 was dropped", size=22)

    plt.savefig(outputs + "Graphs/figure3A.png", dpi=400)


def create_figure2A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    df1 = fern_data.fillna("Control")
    df2 = df1.groupby("Endobacteria", as_index=False).mean()
    df2.replace({"+": "Present", "-": "Absent"}, inplace=True)
    plt.figure(figsize=(20, 7.5))
    plt.subplot(1, 3, 1)
    plt.bar(df2["Endobacteria"], df2["Area"])
    plt.xlabel("Endobacteria Status", size=22)
    plt.ylabel("Average Coverage cm$^{2}$", size=22)
    plt.ylim([0, 6.25])  # MAGIC: Will need to change as more data comes in.

    df3 = df1.groupby("Inoculation time", as_index=False).mean()
    df3.replace({"I0": "Day 0", "I7": "Day 7", "Control": "Never"}, inplace=True)
    plt.subplot(1, 3, 2)
    plt.bar(df3["Inoculation time"], df3["Area"])
    plt.xlabel("Time of Inoculation", size=22)
    # plt.ylabel("Average Coverage cm$^{2}$", size=22)
    plt.ylim([0, 6.25])  # MAGIC: Will need to change as more data comes in.

    df4 = df1.replace(
        {
            "GBAus27b+": "GBAus27b",
            "GBAus27b-": "GBAus27b",
            "control": "None",
            "NVP64+": "NVP64",
            "NVP64-": "NVP64",
        }
    )
    df4 = df4.groupby("Fungus", as_index=False).mean()
    plt.subplot(1, 3, 3)
    plt.bar(df4["Fungus"], df4["Area"])
    plt.xlabel("Plates Inoculated With", size=22)
    plt.ylim([0, 6.25])  # MAGIC: Will need to change as more data comes in.

    plt.suptitle("Effect of different factors on fern growth rate", size=32)
    plt.savefig(outputs + "Graphs/figure2A.png", dpi=400)


def create_figure1A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]

    df1 = fern_data.groupby(
        ["Inoculation time", "Day of Picture"], as_index=False
    ).mean()
    m1 = df1["Inoculation time"] == "I0"
    m2 = df1["Inoculation time"] == "I7"
    df2 = fern_data.replace(
        {
            "GBAus27b+": "GBAus27b",
            "GBAus27b-": "GBAus27b",
            "NVP64+": "NVP64",
            "NVP64-": "NVP64",
        }
    )
    df2 = df2.groupby(["Fungus", "Day of Picture"], as_index=False).mean()
    m3 = df2["Fungus"] == "GBAus27b"
    m4 = df2["Fungus"] == "NVP64"
    df3 = fern_data.replace(
        {
            "GBAus27b+": "+",
            "GBAus27b-": "-",
            "NVP64+": "+",
            "NVP64-": "-",
        }
    )
    df3 = df3.groupby(["Fungus", "Day of Picture"], as_index=False).mean()
    m5 = df3["Fungus"] == "+"
    m6 = df3["Fungus"] == "-"
    m7 = df3["Fungus"] == "control"

    plt.figure(figsize=(20, 10))
    plt.plot(
        df1[m1]["Day of Picture"],
        df1[m1]["Area"],
        color="Blue",
        ls="-",
        lw=3,
        label="Inoculated T0",
    )
    plt.plot(
        df1[m2]["Day of Picture"],
        df1[m2]["Area"],
        color="Blue",
        ls="--",
        lw=3,
        label="Inoculated T7",
    )
    plt.plot(
        df2[m3]["Day of Picture"],
        df2[m3]["Area"],
        color="Green",
        ls="-",
        lw=3,
        label="GBAus27b",
    )
    plt.plot(
        df2[m4]["Day of Picture"],
        df2[m4]["Area"],
        color="Green",
        ls="--",
        lw=3,
        label="NVP64",
    )
    plt.plot(
        df3[m5]["Day of Picture"],
        df3[m5]["Area"],
        color="Goldenrod",
        ls="-",
        lw=3,
        label="With Endobacteria",
    )
    plt.plot(
        df3[m6]["Day of Picture"],
        df3[m6]["Area"],
        color="Goldenrod",
        ls="--",
        lw=3,
        label="Without Endobacteria",
    )
    plt.plot(
        df3[m7]["Day of Picture"],
        df3[m7]["Area"],
        color="black",
        ls="-",
        lw=3,
        label="Control",
    )

    plt.title("Fern Growth Among Different Groups", size=32)
    plt.ylabel("Area cm$^{2}$", size=22)
    plt.xlabel("Day after sowing", size=22)
    plt.legend(prop={"size": 18})

    plt.savefig(outputs + "Graphs/figure1A.png", dpi=400)


def create_figure1(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    df = fern_data.groupby(
        ["Fungus", "Inoculation time", "Day of Picture"], as_index=False
    ).mean()
    df2 = fern_data.groupby(["Fungus", "Day of Picture"], as_index=False).mean()

    plt.figure(figsize=(20, 10))

    # Create the masks
    m1 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I0")
    m2 = (df["Fungus"] == "GBAus27b+") & (df["Inoculation time"] == "I7")
    m3 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I0")
    m4 = (df["Fungus"] == "GBAus27b-") & (df["Inoculation time"] == "I7")
    m5 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I0")
    m6 = (df["Fungus"] == "NVP64+") & (df["Inoculation time"] == "I7")
    m7 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I0")
    m8 = (df["Fungus"] == "NVP64-") & (df["Inoculation time"] == "I7")
    m9 = df2["Fungus"] == "control"

    # Create the plots
    plt.plot(
        df[m1]["Day of Picture"],
        df[m1]["Area"],
        ls="-",
        color="red",
        label="GBAus27b+ I0",
        lw=5,
    )
    plt.plot(
        df[m2]["Day of Picture"],
        df[m2]["Area"],
        ls="-",
        color="red",
        label="GBAus27b+ I7",
        lw=3,
    )
    plt.plot(
        df[m3]["Day of Picture"],
        df[m3]["Area"],
        ls="--",
        color="red",
        label="GBAus27b- I0",
        lw=5,
    )
    plt.plot(
        df[m4]["Day of Picture"],
        df[m4]["Area"],
        ls="--",
        color="red",
        label="GBAus27b- I7",
        lw=2,
    )
    plt.plot(
        df[m5]["Day of Picture"],
        df[m5]["Area"],
        ls="-",
        color="purple",
        label="NVP64+ I0",
        lw=5,
    )
    plt.plot(
        df[m6]["Day of Picture"],
        df[m6]["Area"],
        ls="-",
        color="purple",
        label="NVP64+ I7",
        lw=2,
    )
    plt.plot(
        df[m7]["Day of Picture"],
        df[m7]["Area"],
        ls="--",
        color="purple",
        label="NVP64- I0",
        lw=5,
    )
    plt.plot(
        df[m8]["Day of Picture"],
        df[m8]["Area"],
        ls="--",
        color="purple",
        label="NVP64- I7",
        lw=3,
    )
    plt.plot(
        df2[m9]["Day of Picture"],
        df2[m9]["Area"],
        ls=":",
        color="black",
        label="Control",
        lw=3,
    )

    plt.grid(axis='y')
    plt.title("Fern Growth Among Different Groups", size=32)
    plt.ylabel("Area cm$^{2}$", size=22)
    plt.xlabel("Day after sowing", size=22)
    plt.legend(prop={"size": 18})

    plt.savefig(outputs + "Graphs/figure1.png", dpi=400)


def create_figure2(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    fern_data.fillna("none", inplace=True)
    df = fern_data.groupby("Endobacteria", as_index=False).mean()

    plt.figure(figsize=(7.5, 7.5))
    plt.bar(["With Endobacteria", "Without Endobacteria", "Control"], df["Area"])
    plt.ylabel("Area cm$^{2}$", size=18)
    plt.xlabel("Endobacteria Status", size=18)
    plt.title("Effect of Fungus Endobacteria on Fern Growth", size=22)
    plt.savefig(outputs + "Graphs/figure2.png", dpi=400)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=str, help="Path to the raw data")
    parser.add_argument("outputs", type=str, help="Path to the results")
    args = parser.parse_args()
    inputs = args.inputs
    outputs = args.outputs

    create_figure1(inputs, outputs)
    create_figure2(inputs, outputs)
    create_figure1A(inputs, outputs)
    create_figure2A(inputs, outputs)
    create_figure3A(inputs, outputs)
    create_figure4A(inputs, outputs)
    create_figure5A(inputs, outputs)
