import argparse

from formulation_two import FormulationTwo
from formulation_one import FormulationOne
from formulation_three import FormulationThree

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument relative to the input image
parser.add_argument("-l", "--lambda_val", help="Lambda value")
parser.add_argument("-i", "--iterations", help="Number of iterations for the algorithm")

# Read arguments from command line
args = parser.parse_args()

try:
    lambda_val = float(args.lambda_val)
except TypeError:
    lambda_val = 0.05

try:
    iterations = int(args.iterations)
except TypeError:
    iterations = 10

# f_one = FormulationOne(lambda_val=lambda_val, iterations=iterations, video_path='../vids/taxi.mpg')
# f_one.run()
# f_two = FormulationTwo()
# f_two.run('../imgs/spring.png', 15, 25, 3)
f_three = FormulationThree()
for i in range(1, 21):
    f_three.run(f'../imgs/camera_calibration/Image{i}.tif')
