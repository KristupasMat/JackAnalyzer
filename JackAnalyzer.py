import sys
import os
from classes.JackTokenizer import JackTokenizer
from classes.CompilationEngine import CompilationEngine


# takes input - can be single file or a directory, must end with .jack
# output - file name .xml

# Steps
# 1. Creates a JackTokenizer from fileName.jack
# 2. Creates a Compilation engine and passes the tokenizer and the output file for the given .jack file

arg_length = len(sys.argv)

if arg_length < 2:
    print('Missing the input file')
    sys.exit()
elif arg_length > 2:
    print('Too many arguments')
    sys.exit()

input_file = sys.argv[1]

if os.path.isdir(input_file):
    # Find all .jack files in the given directory and create xml output file for each one 

    # return a list of full paths to input, output files for every .jack file 
    jack_files = [
      {
        'input_file_path': os.path.join(input_file, f), 
        'output_file_path': os.path.join(input_file, f.replace('.jack', 'My.xml'))
      } for f in os.listdir(input_file) if f.endswith('.jack')
    ]

elif os.path.isfile(input_file) and input_file.endswith('.jack'):
    jack_files = [{
      'input_file_path': input_file, 
      'output_file_path': os.path.join(input_file.replace('.jack', 'My.xml'))
    }]
else:
    print('Input file has wrong file extension. Prove a file with .jack extension')
    sys.exit()

def main():

    for jack_file in jack_files:
      tokenizer = JackTokenizer(jack_file['input_file_path'])
      CompilationEngine(tokenizer, jack_file['output_file_path'])


main()
print('Done')
