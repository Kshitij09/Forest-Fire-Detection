import cv2
import os
import logging
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", required=True, type=str,
                    help="path to input video file")
parser.add_argument("-o", "--output", required=True, type=str,
                    help="output directory for frames extracted")
parser.add_argument("-i", "--interval", required=True, type=int,
                    help="Frame extraction interval")

if __name__ == '__main__':
    args = vars(parser.parse_args())

    video = cv2.VideoCapture(args["video"])
    folder_name = Path(args["video"]).name.split(".")[0]
    try:
        dir = os.path.join(args["output"], folder_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
    except IOError as e:
        print(e)

    output = args["output"]
    interval = args["interval"]
    i = 0
    print("[INFO] starting capture, press 'q' to quit")
    while True:
        ret, frame = video.read()

        if frame is None:
            break

        cv2.imshow('frame', frame)
        filename = f"frame-{i}.png"
        path = os.path.sep.join([output, folder_name, filename])
        logging.info(f"Saving {path}")

        if i % interval == 0:
            cv2.imwrite(path, frame)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break

        i += 1

    video.release()
