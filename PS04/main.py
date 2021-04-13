import argparse
from formulation_one import FormulationOne

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

f_one = FormulationOne(lambda_val=lambda_val, iterations=iterations, video_path='../vids/taxi.mpg')
f_one.run()
