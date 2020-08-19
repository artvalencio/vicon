def make_video(filename_in,filename_out,elevation_angle=0,azimuth_angle=0,framerange=None,fps=30,edgetype='edge'):
    ''' Uses pre-processed VICON data to
        generate a video of the motion at
        a specified viewing angle

    Parameters
    ----------
    filename_in: str,
        Path and name of the preprocessed CSV from the VICON
        acquisition (see vicon.preprocess function)
    filename_out: str,
        Path and name of the MP4 video file to be created
    elevation_angle: float, optional
        Elevation (height) viewing angle, in degrees. (default=0)
    azimuth_angle: float, optional
        Azimuth (sideways) viewing angle, in degrees. (default=0)
    framerange: int, list (2 elements), tuple (2 elements), optional
        Range of frames from the input file to be used to
        generate the video
    fps: int, optional
        Frames per second of the generated video. (default=30)
    edgetype: 'edge', None
        Specifies if edges between the PLD dots are to be
        included or not. (default='edge')
    
    Returns
    -------
    (none) (output video is saved in the specified filename_out)

    See Also
    --------
    preprocess: reads a CSV file from VICON Motion Capture and
        creates a new CSV file only with the trajectories,
        changing to another reference frame, if convenient
    scrambled_video: uses pre-processed VICON data to produce
        video of scrambled points (non-biological motion)
    central_dot: generate video of a central dot (resting interval)

    Example
    -------
    vicon.make_video('C:\\Users\\MyUser\\Documents\\Vicon\\pre_processed.csv',
        'C:\\Users\\MyUser\\Documents\\Vicon\\video.mp4',framerange=[500,2500])
    '''
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg') # Needed to run on mac
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import cnames
    from matplotlib import animation


    #definition of links between point-light displays, forming arms, legs, head etc
    if edgetype==None:
        links=[]
    else:
        links=((0,1),(0,2),(0,4),(1,2),(1,3),(4,5),(4,10),(5,6),(5,18),(5,20),(6,7),(6,14),(7,8),(8,9),(10,11),(10,14),(11,12),(12,13),(14,15),(15,16),(16,17),(18,19),(19,5))

    #function to check if a pair is linked or not
    def islinked(n1,n2):
        for _ in range(len(links)):
            if (n1,n2)==(links[i][0],links[i][1]):
                        return True
        return False

    #read data
    if type(framerange)==int:
        data = pd.read_csv(filename_in, nrows=framerange)
    if type(framerange)==list or type(framerange)==tuple:
        columnnames=pd.read_csv(filename_in, nrows=1)
        data = pd.read_csv(filename_in, skiprows=framerange[0], nrows=framerange[1]-framerange[0], header=None)
        data.columns=columnnames.columns
    else:
        data = pd.read_csv(filename_in)  
    xdata=data.filter(['X','X.1','X.2','X.3','X.4','X.5','X.6','X.7','X.8','X.9','X.10','X.11','X.12','X.13','X.14','X.15','X.16','X.17','X.18','X.19'],axis=1)
    ydata=data.filter(['Y','Y.1','Y.2','Y.3','Y.4','Y.5','Y.6','Y.7','Y.8','Y.9','Y.10','Y.11','Y.12','Y.13','Y.14','Y.15','Y.16','Y.17','Y.18','Y.19'],axis=1)
    zdata=data.filter(['Z','Z.1','Z.2','Z.3','Z.4','Z.5','Z.6','Z.7','Z.8','Z.9','Z.10','Z.11','Z.12','Z.13','Z.14','Z.15','Z.16','Z.17','Z.18','Z.19'],axis=1)
    
    numframes=len(data.index)

    #calculate the axis limits
    a=max(np.absolute(xdata.min().min()),np.absolute(xdata.max().max()))
    xmin,xmax=-(a+100),a+100
    b=max(np.absolute(ydata.min().min()),np.absolute(ydata.max().max()))
    ymin,ymax=-(b+100),b+100
    c=max(np.absolute(zdata.min().min()),np.absolute(zdata.max().max()))
    zmin,zmax=-c,c

    #generate figure
    fig = plt.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(13.66, 7.68, forward=True)
    ax = plt.axes(projection='3d')

    print("generating animation")

    def animate(i):
        xline=xdata.loc[i]
        yline=ydata.loc[i]
        zline=zdata.loc[i]
        #plot the points
        ax.clear()
        ax.scatter3D(xline, yline,zline, c='w', alpha=0.7)
        #plot the sticks
        for name1 in range(20):
            for name2 in range(20):
                if islinked(name1,name2):
                    x=(xdata.iloc[i,name1],xdata.iloc[i,name2])
                    y=(ydata.iloc[i,name1],ydata.iloc[i,name2])
                    z=(zdata.iloc[i,name1],zdata.iloc[i,name2])
                    ax.plot3D(x,y,z,'w-',alpha=0.5)
        ax.view_init(elevation_angle,azimuth_angle)
        
        #set axis limits, removeing grid, setting background etc
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)
        ax.set_zlim(zmin,zmax)
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
