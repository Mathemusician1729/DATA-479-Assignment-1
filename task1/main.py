# basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # create output directory if not exists
    os.makedirs("output", exist_ok=True)

    # generate random data
    data = np.random.normal(loc=50, scale=10, size=100)
    df = pd.DataFrame({"values": data})

    # compute summary statistics
    summary = df["values"].describe()
    print("="*40)
    print("Summary Statistics:")
    print(summary)
    print("="*40)

    # plot histogram
    plt.figure(figsize=(6, 4))
    plt.hist(df["values"], bins=10)
    plt.title("Histogram of Random Values")
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    # save figure
    out_path = "output/histogram.png"
    plt.savefig(out_path)
    plt.close()

    print(f"Histogram saved to: {out_path}")

if __name__ == "__main__":
    main()
