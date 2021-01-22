import sys
import argparse
from textwrap import dedent

import matplotlib

# prevent x11 stuff
matplotlib.use("Agg")

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.cm as cm


def main(argv):
    description = dedent(
        """\
        Plots a MERRA 3-D variable as a map at a specified pressure level.
        """
    )

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("input_file", help="path to the input MERRA file")
    parser.add_argument("output_file", help="path to the output png files")
    parser.add_argument("variable", help="name of the variable to plot")
    parser.add_argument("level_num", type=int, help="index of the pressure level")

    args = parser.parse_args(argv)
    dataset = xr.open_dataset(args.input_file)

    plot_level(dataset, args.variable, args.level_num, args.output_file)


def plot_level(dataset, variable, level_num, out_file, cmap_name="RdBu_r"):
    """
    Plots variable in dataset at level level_num to out_file using cmap_name
    colormap.
    """

    # get just the level number we want. The dimensions are:
    # time (only one value)
    # pressure level
    # latitude and longitude
    subset = dataset[variable][0, level_num, :, :]
    # figure out range for plot
    min_val = subset.min()
    max_val = subset.max()

    # Create axes with the projection we want
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Plot the variable
    subset.plot.contourf(
        ax=ax,
        levels=np.linspace(min_val, max_val, 15),
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"fraction": 0.02, "label": subset.units},  # make the colorbar fit
        cmap=cm.get_cmap(cmap_name),
    )

    level_str = "{}={} {}".format(
        dataset["lev"].long_name,
        dataset["lev"].to_masked_array()[level_num],
        dataset["lev"].units,
    )
    t = dataset["time"].to_masked_array()[0]
    time_str = str(np.datetime_as_string(t, unit="h")).replace("T", " ")

    plt.title(subset.long_name + "\n{}, {}".format(level_str, time_str))

    ax.coastlines()

    plt.savefig(out_file)


if __name__ == "__main__":
    main(sys.argv[1:])
