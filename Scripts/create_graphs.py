import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import matplotlib.font_manager as font_manager

def create_figure8A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    fern_data = fern_data[fern_data["Day of Picture"] == 18]
    fern_data["Group"] = fern_data["Fungus"] + "_" + fern_data["Inoculation time"]
    fern_data.fillna("Control", inplace=True)
    df = fern_data.groupby("Group", as_index=False).mean()

    plt.figure(figsize=(15,8))
    plt.bar(df["Group"], df["Area"])
    plt.title("Comparing to the Control", size=18)
    plt.ylabel("Fern Coverage cm$^{2}$\n18 Days after Sowing", size=18)
    
    i = 0
    values = df["Area"].values
    for value in values:
        plt.text(i,value+.1,str(round(value/values[0],1))+"x",size=18,ha='center')
        i+=1

    avg = df[df["Group"] != "Control"]["Area"].mean()
    plt.axhline(y=avg, color="Purple", ls="--")
    plt.text(0,avg+.2,"Average for all\ninoculations",
             size=18,ha='center',color="Purple")


    plt.tight_layout()
    plt.savefig(outputs + "Graphs/figure8A.png", dpi=600)

def create_figure7A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    labels = []
    values = []
    
    mask = (fern_data["Fungus"] == 'control') & (fern_data["Day of Picture"] == 18)
    labels.append("Control")
    values.append(fern_data[mask]["Area"].mean())

    mask = (fern_data["Fungus"].str[:-1] == 'NVP64') & (fern_data["Day of Picture"] == 18)
    labels.append("NVP64")
    values.append(fern_data[mask]["Area"].mean())
    
    mask = (fern_data["Fungus"].str[:-1] == 'GBAus27b') & (fern_data["Day of Picture"] == 18)
    labels.append("GBAus27b")
    values.append(fern_data[mask]["Area"].mean())

    mask = (fern_data["Inoculation time"] == 'I0') & (fern_data["Day of Picture"] == 18)
    labels.append("Inoculated T0")
    values.append(fern_data[mask]["Area"].mean())

    mask = (fern_data["Inoculation time"] == 'I7') & (fern_data["Day of Picture"] == 18)
    labels.append("Inoculated T7")
    values.append(fern_data[mask]["Area"].mean())

    mask = (fern_data["Endobacteria"] == '+') & (fern_data["Day of Picture"] == 18)
    labels.append("Endobacteria Present")
    values.append(fern_data[mask]["Area"].mean())

    mask = (fern_data["Endobacteria"] == '-') & (fern_data["Day of Picture"] == 18)
    labels.append("Endobacteria Absent")
    values.append(fern_data[mask]["Area"].mean())

    plt.figure(figsize=(15,8))
    plt.bar(labels, values)
    plt.title("Comparing to the Control", size=18)
    plt.ylabel("Fern Coverage cm$^{2}$\n18 Days after Sowing", size=18)
    i = 0
    for value in values:
        plt.text(i,value+.1,str(round(value/values[0],1))+"x",size=18,ha='center')
        i+=1

    mask = (fern_data["Fungus"] != 'control') & (fern_data["Day of Picture"] == 18)
    avg = fern_data[mask]["Area"].mean()
    plt.axhline(y=avg, color="Purple", ls="--")
    plt.text(0,avg+.2,"Average for all\ninoculations",
             size=18,ha='center',color="Purple")


    plt.tight_layout()
    plt.savefig(outputs + "Graphs/figure7A.png", dpi=600)

def show_difference(df, e_mask):
    e_top = df[e_mask]["Area"].max()
    e_bot = df[e_mask]["Area"].min()
    e_height = df[e_mask]["Area"].mean()
    e_range = e_top - e_bot
    plt.errorbar(18.5, e_height, yerr=e_range/2, color="black", capsize=10,
                 zorder=5)
    plt.text(18.75, e_height, "+" + str(round(e_top/e_bot * 100 - 100, 1)) + "%",
             va="center", zorder = 4, size=18).set_bbox({"facecolor":"white",
                                                "edgecolor":"white",
                                                "boxstyle":"square,pad=.05"})

def create_figure6A(inputs, outputs):
    fern_data = pd.read_csv(outputs + "fern_growth.csv")
    fern_data = fern_data[fern_data["Replicate Number"] != "R4"]
    
    plt.figure(figsize=(13,13))
    plt.suptitle("Effect of different factors on fern growth rate", size=28)

    # First examine endobacteria status
    plt.subplot(3,2,1)
    plt.grid(axis='y')
    plt.title("Endobacteria", size=18)
    plt.ylabel("Fern Coverage cm$^{2}$", size=18)
    df1 = fern_data.replace({"+":"Present","-":"Absent"}).groupby(
        ["Endobacteria", "Day of Picture"],as_index=False).mean()
    m1 = df1["Endobacteria"] == "Present"
    m2 = df1["Endobacteria"] == "Absent"
    plt.plot(df1[m1]["Day of Picture"], df1[m1]["Area"], ls="-", color="Black",
            label="Present")
    plt.plot(df1[m2]["Day of Picture"], df1[m2]["Area"], ls="--",
             color="Black", label="Absent")
    plt.legend()
    """
    plt.xlim([None, 19])
    e_mask = (df1["Day of Picture"] == 18)
    show_difference(df1, e_mask)
    """

    # Second, examine time of inoculation
    plt.subplot(3,2,2)
    plt.grid(axis='y')
    plt.title("Time of Inoculation", size=18)
    df2 = fern_data.groupby(["Inoculation time", "Day of Picture"],
                            as_index=False).mean()
    m3 = df2["Inoculation time"] == "I0"
    m4 = df2["Inoculation time"] == "I7"
    plt.plot(df2[m3]["Day of Picture"], df2[m3]["Area"], lw=5, color="Black",
             label="Inoculated T0")
    plt.plot(df2[m4]["Day of Picture"], df2[m4]["Area"], lw=2, color="Black",
             label="Inoculated T7")
    plt.legend()

    plt.xlim([None, 19])
    e_mask = (df2["Day of Picture"] == 18)
    show_difference(df2, e_mask)

    # Third, examine type of fungus
    plt.subplot(3,2,3)
    plt.grid(axis='y')
    plt.title("Fungus", size=18)
    plt.ylabel("Fern Coverage cm$^{2}$", size=18)
    df3 = fern_data.copy()
    df3 = df3[df3["Fungus"] != "control"]
    df3["Fungus"] = df3["Fungus"].str[:-1]
    df3 = df3.groupby(["Fungus", "Day of Picture"], as_index=False).mean()
    m5 = df3["Fungus"] == "GBAus27b"
    m6 = df3["Fungus"] == "NVP64"
    plt.plot(df3[m5]["Day of Picture"], df3[m5]["Area"], color="Red",
             label="GBAus27b")
    plt.plot(df3[m6]["Day of Picture"], df3[m6]["Area"], color="Purple",
             label="NVP64")
    plt.legend()

    plt.xlim([None, 19])
    e_mask = (df3["Day of Picture"] == 18)
    show_difference(df3, e_mask)

    # Fourth, fungus + inoculation
    plt.subplot(3,2,4)
    plt.grid(axis='y')
    plt.title("Fungus + Time of Inoculation", size=18)
    df4 = fern_data.copy()
    df4["Fungus"] = df4["Fungus"].str[:-1]
    df4 = df4.groupby(["Fungus", "Inoculation time", "Day of Picture"],
                      as_index=False).mean()
    m7 = (df4["Fungus"] == "GBAus27b") & (df4["Inoculation time"] == "I0")
    m8 = (df4["Fungus"] == "GBAus27b") & (df4["Inoculation time"] == "I7")
    m9 = (df4["Fungus"] == "NVP64") & (df4["Inoculation time"] == "I0")
    m10 = (df4["Fungus"] == "NVP64") & (df4["Inoculation time"] == "I7")
    plt.plot(df4[m7]["Day of Picture"], df4[m7]["Area"], color="Red", lw=5,
             label="GBAus27b I0")
    plt.plot(df4[m8]["Day of Picture"], df4[m8]["Area"], color="Red", lw=2,
            label="GBAus27b I7")
    plt.plot(df4[m9]["Day of Picture"], df4[m9]["Area"], color="Purple", lw=5,
            label="NVP64 I0")
    plt.plot(df4[m10]["Day of Picture"], df4[m10]["Area"], color="Purple",
             lw=2, label="NVP64 I7")
    plt.legend()

    plt.xlim([None, 19])
    e_mask = (df4["Inoculation time"] == "I7") & (df4["Day of Picture"] == 18)
    show_difference(df4, e_mask)
    e_mask = (df4["Inoculation time"] == "I0") & (df4["Day of Picture"] == 18)
    show_difference(df4, e_mask)

    # Fifth, Endobacteria and Fungus
    plt.subplot(3,2,5)
    plt.grid(axis='y')
    plt.title("Endobacteria + Fungus", size=18)
    plt.xlabel("Days after Sowing", size=18)
    plt.ylabel("Fern Coverage cm$^{2}$", size=18)
    df5 = fern_data.copy()
    df5["Fungus"] = df5["Fungus"].str[:-1]
    df5 = df5.groupby(["Fungus", "Endobacteria", "Day of Picture"],
                      as_index=False).mean()
    m11 = (df5.Fungus == "GBAus27b") & (df5.Endobacteria == "+")
    m12 = (df5.Fungus == "GBAus27b") & (df5.Endobacteria == "-")
    m13 = (df5.Fungus == "NVP64") & (df5.Endobacteria == "+")
    m14 = (df5.Fungus == "NVP64") & (df5.Endobacteria == "-")
    plt.plot(df5[m11]["Day of Picture"], df5[m11]["Area"], color="Red", ls="-",
            label="GBAus27b+")
    plt.plot(df5[m12]["Day of Picture"], df5[m12]["Area"], color="Red",
             ls="--", label="Gbaus27b-")
    plt.plot(df5[m13]["Day of Picture"], df5[m13]["Area"], color="Purple",
             ls="-", label="NVP64+")
    plt.plot(df5[m14]["Day of Picture"], df5[m14]["Area"], color="Purple",
             ls="--", label="NVP64-")
    plt.legend()

    # All factors: Fungus, Endobacteria, Inoculation time
    plt.subplot(3,2,6)
    plt.grid(axis='y')
    plt.title("All factors", size=18)
    plt.xlabel("Days after Sowing", size=18)
    df6 = fern_data.copy()
    df6["Fungus"] = df6["Fungus"].str[:-1]
    df6 = df6.groupby(["Fungus", "Endobacteria", "Inoculation time", "Day of Picture"],
                      as_index=False).mean()
    m1 = (df6["Fungus"] == "GBAus27b") & (df6["Endobacteria"] == "+") & (df6["Inoculation time"] == "I0")
    m2 = (df6["Fungus"] == "GBAus27b") & (df6["Endobacteria"] == "-") & (df6["Inoculation time"] == "I0")
    m3 = (df6["Fungus"] == "GBAus27b") & (df6["Endobacteria"] == "+") & (df6["Inoculation time"] == "I7")
    m4 = (df6["Fungus"] == "GBAus27b") & (df6["Endobacteria"] == "-") & (df6["Inoculation time"] == "I7")
    m5 = (df6["Fungus"] == "NVP64") & (df6["Endobacteria"] == "+") & (df6["Inoculation time"] == "I0")
    m6 = (df6["Fungus"] == "NVP64") & (df6["Endobacteria"] == "-") & (df6["Inoculation time"] == "I0")
    m7 = (df6["Fungus"] == "NVP64") & (df6["Endobacteria"] == "+") & (df6["Inoculation time"] == "I7")
    m8 = (df6["Fungus"] == "NVP64") & (df6["Endobacteria"] == "-") & (df6["Inoculation time"] == "I7")
    plt.plot(df6[m1]["Day of Picture"], df6[m1]["Area"], color="Red", ls="-",
             lw=5, label="GABaus27b+ I0")
    plt.plot(df6[m2]["Day of Picture"], df6[m2]["Area"], color="Red", ls="--",
             lw=5, label="GBAus27b- I0")
    plt.plot(df6[m3]["Day of Picture"], df6[m3]["Area"], color="Red", ls="-",
             lw=2, label="GBAus27b+ I7")
    plt.plot(df6[m4]["Day of Picture"], df6[m4]["Area"], color="Red", ls="--",
             lw=2, label="GBAus27b- I7")
    plt.plot(df6[m5]["Day of Picture"], df6[m5]["Area"], color="Purple",
             ls="-", lw=5, label="NVP64+ I0")
    plt.plot(df6[m6]["Day of Picture"], df6[m6]["Area"], color="Purple",
             ls="--", lw=5, label="NVP64- I0")
    plt.plot(df6[m7]["Day of Picture"], df6[m7]["Area"], color="Purple",
             ls="-", lw=2, label="NVP64+ I7")
    plt.plot(df6[m8]["Day of Picture"], df6[m8]["Area"], color="Purple",
             ls="--", lw=2, label="NVP64- I7")
    df7 = fern_data.copy()
    df7 = df7[df7["Fungus"] == "control"]
    df7 = df7.groupby(["Day of Picture"], as_index=False).mean()
    plt.plot(df7["Day of Picture"], df7["Area"], color="Black", ls=":",
             label="Control", lw=2)

    plt.legend() 

    plt.tight_layout()
    plt.savefig(outputs + "Graphs/figure6A.png", dpi=600)

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

    plt.figure(figsize=(15,6))
    plt.bar(df3["Name"], df3["Area"])
    plt.title("Fern Growth by Fungus and Inoculation time", size=32)
    plt.xlabel("Fungi and Inoculation time", size=22)
    plt.ylabel("Average Coverage cm$^{2}$", size=22)
    plt.text(x=1,y=heights[1]+.04,size=16,ha="center",
             s="+"+str(round(100*(heights[1]/heights[0]-1),1))+"%")
    plt.text(x=3,y=heights[3]+.04,size=16,ha="center",
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
    
    plt.figure(figsize=(15, 7*5.46/5.84))
    plt.scatter(df1[m1]["Group"], df1[m1]["Area"], color="black", label="Replicate 1-3")
    plt.scatter(df1[m2]["Group"], df1[m2]["Area"], color="black")
    plt.scatter(df1[m3]["Group"], df1[m3]["Area"], color="black")
    
    """
    plt.scatter(
        df1[m4]["Group"],
        df1[m4]["Area"],
        color="red",
        marker="x",
        s=90,
        label="Replicate 4",
    )
    """
    # plt.legend()
    plt.xlabel("Group", size=22)
    plt.ylabel("Avg Coverage cm$^{2}$", size=22)
    plt.title("Growth of Every Replicate", size=22)
    plt.xticks(fontsize=22, rotation=30)
    plt.tight_layout()
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

    # Find and set the font to times new roman.
    for font in font_manager.findSystemFonts(fontpaths=None,
                                                        fontext='ttf'):
        if font.split("/")[-1] in ["NotoColorEmoji.ttf"]:
            continue
        font_manager.fontManager.addfont(font)
    plt.rcParams['font.family'] = 'Times New Roman'

    #create_figure1(inputs, outputs)
    #create_figure2(inputs, outputs)
    #create_figure1A(inputs, outputs)
    #create_figure2A(inputs, outputs)
    #create_figure3A(inputs, outputs)
    #create_figure4A(inputs, outputs)
    #create_figure5A(inputs, outputs)
    create_figure6A(inputs, outputs)
    create_figure7A(inputs, outputs)
    create_figure8A(inputs, outputs)
