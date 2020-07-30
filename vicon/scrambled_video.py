import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # Need to use in order to run on mac
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

def scrambled_video(filename_in,filename_out,framerange=None,fps=30):
    ''' Uses pre-processed VICON data to generate a
        video of scrambled points (non-biological motion)

    Parameters
    ----------
    filename_in: str,
        Path and name of the preprocessed CSV from the VICON
        acquisition (see vicon.preprocess function)
    filename_out: str,
        Path and name of the MP4 video file to be created
    framerange: int, list (2 elements), tuple (2 elements), optional
        Range of frames from the input file to be used to
        generate the video
    fps: int, optional
        Frames per second of the generated video. (default=30)
    
    Returns
    -------
    (none) (output video is saved in the specified filename_out)

    See Also
    --------
    preprocess: reads a CSV file from VICON Motion Capture and
        creates a new CSV file only with the trajectories,
        changing to another reference frame, if convenient
    make_video: uses pre-processed VICON data to generate
        video of the movement at specified viewing angle

    Example
    -------
    vicon.scrambled_video('C:\\Users\\MyUser\\Documents\\Vicon\\pre_processed.csv',
        'C:\\Users\\MyUser\\Documents\\Vicon\\scrambled_video.mp4',framerange=[500,2500])
    '''
    pass
