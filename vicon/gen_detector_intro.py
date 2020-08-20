def gen_detector_intro(filename_out,seconds,fps=30):
    ''' Generate a video of a central dot
        running for the defined number of
        seconds, and a corner rectangle
        with changing brigthness, used as
        introduction step in experiment to
        calibrate the stimulus-detector
        synchronization apparatus.

    Parameters
    ----------
    filename_out: str,
        Path and name of the MP4 video file to be created
    seconds: int,
        Length in seconds of the video file to be created
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
    scrambled_video: uses pre-processed VICON data to produce
        video of scrambled points (non-biological motion)
    central_dot: generate video of a central dot (resting interval)

    Example
    -------
    vicon.gen_detector_intro('C:\\Users\\MyUser\\Documents\\Vicon\\intro_video.mp4',15)
    '''
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg') # Needed to run on mac
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import cnames
    from matplotlib import animation
    from matplotlib import patches as patches
 
    numframes=seconds*fps

    #generate figure
    fig = plt.figure()
    plt.style.use('dark_background')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(13.66, 7.68, forward=True)
    ax = plt.axes()

    def animate(i):
        #plot the points
        ax.clear()
        ax.scatter(0.5,0.5, c='w', alpha=0.7)
        #set axis limits, removeing grid, setting background etc
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        #setting varying rectangle brightness levels for detector calibration
        if i>12*fps:
            detector=0.3
        elif i>11*fps:
            detector=0
        elif i>10*fps:
            detector=1
        else:
            detector=int(i/fps)/10
        ax.add_patch(patches.Rectangle((0.95,0.85),0.1,0.3,fill=True,fc=(detector,detector,detector),zorder=2,clip_on=False))
        #black background
        ax.patch.set_facecolor('black')
        fig.set_facecolor('black')
        plt.axis('off')
        plt.grid(b=None)

    #make animation
    ani = animation.FuncAnimation(fig, animate, frames=numframes)

    #setting up animation file
    Writer = animation.writers['ffmpeg']
    writer = animation.FFMpegWriter(fps=fps,metadata=dict(artist='NeuroMat'),bitrate=1800,extra_args=['-vcodec','libx264'])

    #save animation
    ani.save(filename_out, writer=writer)
    plt.close()
