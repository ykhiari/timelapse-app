# imports
import cv2
import os
import time
import signal
import sys
from datetime import datetime
import argparse

# define a parser for the script arguments
parser = argparse.ArgumentParser()
parser.add_argument("--output",required=True,help="location to store the images.")
parser.add_argument("--delay",type=float,default=4.0,help="delay between every stored image")
args = vars(parser.parse_args())

# helper functions
def handler(signum, frame):
    print("The program has been stopped after you pressed 'ctrl+c'")
    sys.exit(0)

# initiate the signal handler
signal.signal(signal.SIGINT,handler)

# define a video capture object
vc = cv2.VideoCapture(0)

# define a counter to name the images
count = 0

# setup the output directory name
timeformat = "%Y-%m-%d-%H%M"
outputDir = os.path.join(args["output"],datetime.now().strftime(timeformat))
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# starting the program
print("Starting the timelapse program...")
print("Please press 'ctrl+c' or press 'q' if you want to stop the program.")
while(True):
    # capture video frames
    ret, frame = vc.read()
    # display the video
    cv2.imshow("frame",frame)
    # add tag to the image
    tag = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame,tag,(10,frame.shape[0]-10),cv2.FONT_HERSHEY_DUPLEX,0.35,(0,0,255),1)
    # define a path and a name to the image
    image_path = os.path.join(outputDir,f"{str(count).zfill(16)}.jpg")
    # store the image in output directory
    cv2.imwrite(image_path,frame)
    # define a quitting button 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    # delay the next image storage
    time.sleep(args["delay"])
    # increment the counter to name the next image
    count += 1

# release the video capture object
vc.release()
# destroy all the windows
cv2.destroyAllWindows()
