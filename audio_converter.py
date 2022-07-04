from pathlib import Path
import sys
import os
from common import *
from pydub import AudioSegment 

VERSION = "0.11"
TITLE = f'Relicta Audio Converter v{VERSION}\nCreated by Astra'
LOGGER_FILE = "log.txt"
OUTPUT_FOLDER = "audio_output"
FILE_REG = ["*.wav","*.mp3",]

def main():
    to_convert = sys.argv[1]

    # check for path
    if not IsPathExists(to_convert):
        input("Error. This path doesn't exist.")
        return

    # path collection
    working_dir = os.path.dirname(os.path.realpath(__file__))
    root = os.path.dirname(to_convert)
    logger = os.path.join(root,LOGGER_FILE)
    to_output = os.path.join(working_dir,OUTPUT_FOLDER)
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
        pathname, extension = os.path.splitext(save_path)
        pathname = FilterFileName(pathname,'()\",\'')
        MakeDirsIfNotExist(pathname)
        segment = AudioSegment.from_file(path,format=extension[1:])
        segment = segment.set_channels(1)
        segment.export(os.path.join(pathname + ".ogg"),format='ogg')
        i += 1
        DrawProgress(TITLE, i, len(paths), 40, errors)
    DrawComplete()

if __name__ == '__main__':
    main()