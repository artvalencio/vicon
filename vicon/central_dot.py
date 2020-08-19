def central_dot(filename_out,seconds,fps=30,detector=None):
    ''' Generate a video of a central dot
        running for the defined number of
        seconds, typically used as resting
        interval for visual experiments

    Parameters
    ----------
    filename_out: str,
        Path and name of the MP4 video file to be created
    seconds: int,
        Length in seconds of the video file to be created
    fps: int, optional
        Frames per second of the generated video. (default=30)
    detector: float (0-1), None, optional
        If a light detector will be used, creates a corner
        with brightness provided by the user (0-1).
        Otherwise, detector is set to None and no corner
        is drawn
    
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

    Example
    -------
    vicon.central_dot('C:\\Users\\MyUser\\Documents\\Vicon\\rest_video.mp4',
        15,detector=0.7)
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
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(13.66, 7.68, forward=True)
    ax = plt.axes()

    print("generating animation")

    def animate(i):
        #plot the points
        ax.clear()
        ax.scatter(0.5,0.5, c='w', alpha=0.7)
        #set axis limits, removeing grid, setting background etc
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        if detector!=None:
            ax.add_patch(patches.Rectangle((0.95,0.85),0.1,0.3,fill=True,fc=(detector,detector,detector),zorder=2,clip_on=False))
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
