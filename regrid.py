import argparse
import sys
import os
from textwrap import dedent
import subprocess
import tempfile
import shutil
from textwrap import dedent


def main(argv):
    description = dedent(
        """\
        Calls cdo to regrid a MERRA 2 granule to the AIRS L3 grid.
        """
    )

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("input_file", help="path to the input file")
    parser.add_argument("output_file", help="path to the output regridded file")
    parser.add_argument(
        "--type",
        default="remapcon",
        help="remap type, default remapcon",
        choices=["remapcon", "remapnn", "remapcon"],
    )
    parser.add_argument(
        "--gridfile",
        default=None,
        help="file describing output grid. Defaults to AIRS L3 grid.",
    )

    args = parser.parse_args(argv)

    temp_dir = tempfile.mkdtemp(dir=tempfile.gettempdir())

    gridfile = args.gridfile
    # If no grid file was passed in, create a temporary file with the
    # AIRS L3 grid.
    if gridfile is None:
        gridfile = os.path.join(temp_dir, "1x1grid.txt")
        with open(gridfile, "w") as f:
            f.write(
                dedent(
                    """\
                    gridtype  = lonlat
                    xsize     = 360
                    ysize     = 180
                    xfirst    = 0.5
                    xinc      = 1.0
                    yfirst    = 89.5
                    yinc      = -1.0
                """
                )
            )

    cdo_cmd = [
        "cdo",
        "-s",
        "-L",
        "-f",
        "nc4",
        f"-{args.type},{gridfile}",
        "-select,name=QV,RH,T,levidx=1,2,3,4,5,6,7,8",
        args.input_file,
        args.output_file,
    ]

    print("Executing: {}".format(" ".join(cdo_cmd)))
    try:
        subprocess.check_output(cdo_cmd)
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
