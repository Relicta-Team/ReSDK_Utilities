from pathlib import Path
import sys
import os
from common import *

VERSION = "0.1"
TITLE = f'Relicta Audio Converter v{VERSION}\nCreated by Astra'
LOGGER_FILE = "log.txt"
OUTPUT_FOLDER = "audio_output"
FILE_REG = ["*.wav",".mp3",]

def main():
    to_convert = sys.argv[1]

    # check for path
    if not IsPathExists(to_convert):
        input("Error. This path doesn't exist.")
        return

    # path collection
    root = os.path.dirname(to_convert)
    logger = os.path.join(root,LOGGER_FILE)
    to_output = os.path.join(root,OUTPUT_FOLDER)
    paths = CollectFilePaths(to_convert,FILE_REG)

    # delete logger if exists
    DeleteFileIfExists(logger)

    # check if folder contains images
    if(len(paths) == 0):
        input(f'Error. This folder doesn\'t contain {FILE_REG} files.')
        return

    # process images
    i = 0
    errors = 0
    DrawProgress(TITLE, i, len(paths), 40, errors)
    for path in paths:
        p = Path(path)
        rel = p.relative_to(to_convert)
        save_path = os.path.join(to_output,rel)    
        MakeDirsIfNotExist(save_path)

    DrawComplete()

if __name__ == '__main__':
    main()