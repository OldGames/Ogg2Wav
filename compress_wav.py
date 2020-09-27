# Copyright 2020

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os, glob, argparse, logging, sys
import subprocess

OGGENC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "oggenc2.exe")

def find_files(directory, extensions):
    extensions = [x.lower() for x in extensions]
    for filename in glob.glob(os.path.join(directory, "**"), recursive = True):
        base, ext = os.path.splitext(filename)
        if ext.lower() in extensions:
            yield filename

def compress_wav(path, remove_file = False):
    command = [OGGENC_PATH, "-q-1", path]
    logging.debug('Calling: "{}"'.format(" ".join(command)))
    try: 
        subprocess.check_call(command)
        if remove_file:
            logging.debug('Deleting "{}"'.format(path))
            os.remove(path)
    except subprocess.CalledProcessError:
        error_message = 'Failed to compress "{}"'.format(path)
        logging.error(error_message)
        raise RuntimeError(error_message)


def main(parent_directory, remove_after_compress):
    try:
        for file_path in find_files(parent_directory, ['.wav']):
            compress_wav(file_path, remove_after_compress)
    except RuntimeError as e:
        sys.exit(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recursive WAV->Ogg Compressor')
    parser.add_argument('-d', '--directory', action='store', required=True, help="Parent directory containing WAV files")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('-r', '--remove', action='store_true', default=False, help="Remove WAV files after compression")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)
    
    main(args.directory, args.remove)