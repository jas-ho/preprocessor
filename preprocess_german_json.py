from preprocessor import preprocess
import argparse

parser = argparse.ArgumentParser(description='Preprocess .')
parser.add_argument('input_file', metavar='in', type=str,
                   help='path to the input json-file')
parser.add_argument('output_file', metavar='out', type=str,
                   help='path to the output json-file to be created')

args = parser.parse_args()
in_file = args.input_file
out_file = args.output_file

print("Reading input from {}...\n".format(in_file))
preprocess(in_file, output_file=out_file)
print("Output written to {}.\n".format(out_file))
