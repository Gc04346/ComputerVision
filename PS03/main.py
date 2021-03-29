import argparse

from formulation_one import FormulationOne


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument relative to the input image
parser.add_argument("-f", "--file", help="Path to the input image")

# Read arguments from command line
args = parser.parse_args()

f_one = FormulationOne(args.file, 130)
f_one.execute()