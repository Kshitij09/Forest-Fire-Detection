import os
import argparse
from imutils.paths import list_images
import numpy as np
from shutil import copyfile
from numpy import random
from pathlib import Path, PosixPath

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

def train_test_split(data_root, dest, test_size=.1):
    try:    
        os.makedirs(dest,exist_ok=True)

        train_dir, test_dir = dest + "/train", dest + "/test"
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)
        for label in os.listdir(data_root):
            os.makedirs(dest + "/train/" + label, exist_ok=True)
            os.makedirs(dest + "/test/" + label, exist_ok=True)
            all_images = list(map(str,get_files(Path(f"{data_root}/{label}"), image_types)))
            total_examples = len(all_images)
            print(f"Class: {label}")
            print(f"Total examples: {total_examples}")
            
            random.shuffle(all_images)
            
            test_length = int(total_examples * test_size)
            train_length = total_examples - test_length
            
            train_set, test_set = all_images[:train_length], all_images[-test_length:]

            print(f"Train examples: {train_length}")
            for file in train_set:
                dest_path = os.path.sep.join(
                    [dest, "train", label, Path(file).name])
                copyfile(file, str(dest_path))

            print(f"Test examples: {test_length}")
            for file in test_set:
                dest_path = os.path.sep.join(
                    [dest, "test", label, Path(file).name])
                copyfile(file, str(dest_path))
            print()

    except OSError:
        print("Unable to create directories")
        return


# credits: fastai
def get_files(path: Path, extensions: [str]=None):
    "Return list of files in `path` that have a suffix in `extensions`; optionally `recurse`."
    f = [o.name for o in os.scandir(path) if o.is_file()]
    res = _get_files(path, path, f, extensions)
    return res

def _get_files(parent, p, f, extensions, raw:bool=False):
    p = Path(p)#.relative_to(parent)
    if isinstance(extensions,str): extensions = [extensions]
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    res = [p/o for o in f if not o.startswith('.')
           and (extensions is None or f'.{o.split(".")[-1].lower()}' in low_extensions)]
    return res

def _get_files_raw(parent, p, f, extensions, raw:bool=False):
    p = Path(p)#.relative_to(parent)
    if isinstance(extensions,str): extensions = [extensions]
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    res = [p/o for o in f if not o.startswith('.')
           and (extensions is None or f'.{o.split(".")[-1].lower()}'.startswith(tuple(low_extensions)) if raw else f'.{o.split(".")[-1].lower()}' in extensions)]
    return res


def rename(l: [PosixPath]):
    for p in l:
        new_name = p.suffix.split('?')[0]
        new_p = Path(f'{p.parent}/{p.stem}{new_name}')
        # print(f'{p} --> {new_p}')
        os.rename(p,new_p)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", required=True,
                    help="Source directory of data")
parser.add_argument("-d", "--dest", required=True,
                    help="Destination Directory for split")
parser.add_argument("-t", "--test", default=0.2,
                    help="Test split ratio")

if __name__ == '__main__':
    args = vars(parser.parse_args())
    train_test_split(args["source"], args["dest"], float(args["test"]))





# rename(get_files(Path('samples/sunset-2'), image_types, raw=True))
# len(get_files(Path('samples/sunset-2'), image_types))
# rename(len(get_files(Path('samples/smoke'), image_types)))
# len(get_files(Path('samples/smoke'), image_strange))