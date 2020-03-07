import os
from uuid import uuid4
from imutils.paths import list_files
from argparse import ArgumentParser
from pathlib import Path
import shutil
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("-s", "--source", required=True,
                    help="Source directory")

if __name__ == '__main__':
    args = vars(parser.parse_args())

    source_path = str(args["source"])
    dest_path = str(source_path) + "-agg"
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    files = list(map(lambda x: str(x), list_files(args["source"])))
    for file_path in tqdm(files,maxinterval=len(files)):
        p = Path(file_path)
        new_name = str(uuid4().hex) + p.suffix
        new_path = str(dest_path) + "/" + new_name
        while os.path.exists(new_path):
            new_name = str(uuid4().hex) + p.suffix
            new_path = str(dest_path) + "/" + new_name
        shutil.copy(file_path, new_path)
