import argparse

from formulation_one import FormulationOne
from formulation_three import FormulationThree


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument relative to the input image
parser.add_argument("-f", "--file", help="Path to the input image")

# Read arguments from command line
args = parser.parse_args()

f_one = FormulationOne(args.file)
img = f_one.get_image()
print(img)
print(type(img))
print(img.shape)
