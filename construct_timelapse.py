# imports
import cv2
import os
import progressbar
import argparse
from glob import glob


# define an argument parser for the script
parser = argparse.ArgumentParser()
parser.add_argument("--imgloc",required=True,help="the location of the images.")
parser.add_argument("--fps",type=int,default=30,help="frame per second")
args = vars(parser.parse_args())

# define the video writer codec object
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
writer = None

# define the video file name and path
video_name = f"{args['imgloc'].split(os.path.sep)[-1]}.avi"
video_path = os.path.join(args["imgloc"],video_name)
if os.path.exists(video_path):
    print("[warning] file exists and will be overwritten.")


# helper function
def get_number(imagepath) -> int:
    """helper function to get the image number from the path

    Args:
        imagepath (string): image path

    Returns:
        int: the image number.
    """
    return int(imagepath.split(os.path.sep)[-1][:-4])

def get_image_paths(outputdir) -> list:
    """get the list of image paths sorted by their number.

    Args:
        outputdir (string): the path of the image location.

    Returns:
        list: list of the sorted image paths.
    """
    unsorted_img_list = glob(os.path.join(outputdir,"*.jpg"))
    return sorted(unsorted_img_list,key=get_number)

# construct the list of images
list_images = get_image_paths(args["imgloc"])

# set up a progress bar
widget = [["Building Video: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]]
pbar = progressbar.ProgressBar(maxval=len(list_images), widget=widget).start()

# video construction process
print("Building the video...")
for i,img_path in enumerate(list_images):
    # read the image
    frame = cv2.imread(img_path)
    # initialize the writer if not
    if writer is None:
        (h,w) = frame.shape[:2]
        writer = cv2.VideoWriter(video_path,fourcc,args["fps"],(w,h),True)
    # write the image in the writer
    writer.write(frame)
    # update the progressbar
    pbar.update(i)

print("Cleaning...")
writer.release()
pbar.finish()

