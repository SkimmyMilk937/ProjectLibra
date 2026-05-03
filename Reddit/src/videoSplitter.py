import moviepy
import os
import math
from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip

if __name__ == "__main__":
    dir = os.getcwd()
    videos = os.listdir(f"{dir}/morgs/videos")
    for video in videos:
        time = 0
        with VideoFileClip(f"{dir}/morgs/videos/{video}") as instance:
            while(math.floor((int(instance.duration/60))) > (time/60 +1)):
                new = instance.subclip(time, time+60)
                new.write_videofile(f"{dir}/morgs/clips/{str(time) + video}", codec='libx264')
                time += 60