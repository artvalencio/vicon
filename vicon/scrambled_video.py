def scrambled_video(filename_in,filename_out,links=None,scrambletype='pairwise',
                    framerange=None,fps=30,detector=None):

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
    links: 2D list, 2D tuple, None, 'original', optional
        The pairs showing which VICON points should be linked
        with a line. (default: 'original', i.e. same as humanoid)
    scrambledtype: str, optional
        The type of scrambling to be adopted. Options:
            'scrambled': simple scrambling of the original
                positions, constraining only at the initial
                frame. May lead to slightly larger motion
                area than original video
            'constrained': scrambling contraining the points
                at all frames to the limits defined by the
                original video
            'pairwise': pairwise scrambling of positions,
                following procedure by Kim et al (2015)
                doi:10.1167/15.11.13 (default)              
    framerange: int, list (2 elements), tuple (2 elements), optional
        Range of frames from the input file to be used to
        generate the video
    fps: int, optional
        Frames per second of the generated video. (default=30)
    detector: float(0-1), None, optional
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
    central_dot: generate video of a central dot (resting interval)

    Example
    -------
    vicon.scrambled_video('C:\\Users\\MyUser\\Documents\\Vicon\\pre_processed.csv',
        'C:\\Users\\MyUser\\Documents\\Vicon\\scrambled.mp4',framerange=[500,2500])
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
    import mpl_toolkits.mplot3d.art3d as art3d

    #function to scramble the data points
    def calc_scrambled(x,y,z):
        xlims=(x.loc[0].max(),x.loc[0].min())
        ylims=(y.loc[0].max(),y.loc[0].min())
        zlims=(z.loc[0].max(),z.loc[0].min())
        x0=np.random.uniform(xlims[0],xlims[1],len(x.columns))
        y0=np.random.uniform(ylims[0],xlims[1],len(y.columns))
        z0=np.random.uniform(zlims[0],xlims[1],len(z.columns))
        for i in range(len(x.index)): #updating trajectory
            x.loc[i]=x.loc[i]-x0
            y.loc[i]=y.loc[i]-y0
            z.loc[i]=z.loc[i]-z0
        return x,y,z
        
    #function to do the constrained scrambling method
    def calc_constrained(x,y,z):
        xlims,ylims,zlims=(x.values.min(),x.values.max()),(y.values.min(),y.values.max()),(z.values.min(),z.values.max()) #defining constraint limits
        x0=np.random.uniform(xlims[0],xlims[1],len(x.columns))#defining random initial positions
        y0=np.random.uniform(ylims[0],xlims[1],len(y.columns))
        z0=np.random.uniform(zlims[0],xlims[1],len(z.columns))
        for i in range(20):#defining new random initial positions if passed constraint limit at any moment
            while xlims[0]>(x.iloc[:,i].values+x0[i]).min() and (x.iloc[:,i].values+x0[i]).max()<=xlims[1]:
                x0[i]=np.random.uniform(xlims[0],xlims[1])
            while ylims[0]>(y.iloc[:,i]+y0[i]).min() and (y.iloc[:,i]+y0[i]).max()<=ylims[1]:
                y0[i]=np.random.uniform(ylims[0],ylims[1])
            while zlims[0]>(z.iloc[:,i]+z0[i]).min() and (z.iloc[:,i]+z0[i]).max()<=zlims[1]:
                z0[i]=np.random.uniform(zlims[0],zlims[1])
        for i in range(len(x.index)): #updating trajectory
            x.loc[i]=x.loc[i]-x0
            y.loc[i]=y.loc[i]-y0
            z.loc[i]=z.loc[i]-z0
        return x,y,z
    
    #function to do the pairwise scrambling method
    def calc_pairwise(x,y,z):
        x_centroid=x.mean()
        y_centroid=y.mean()
        z_centroid=z.mean()
        pairs=[[0,2],[1,3],[6,7],[8,9],[10,11],[12,13],[14,15],[16,17],[4,18],[5,19]] #4 first are arms, next 4 are legs, final 2 are head/shoulder 
        #scrambling pairs according to rules defined in the paper
        pair_idx=list(range(10))
        np.random.shuffle(pair_idx)
        for i in range(10):
            if i<4:
                if pair_idx[i]<4:
                    np.random.shuffle(pair_idx[i:])
            elif i<8:
                if 4<=pair_idx[i]<8:
                    np.random.shuffle(pair_idx[i:])
        new_pairs=[]
        for i in range(10):
            new_pairs.append([pairs[pair_idx[i]][1],pairs[pair_idx[i]][0]])
        #defining which PLD points switch with which
        switch_idx=[]
        for i in range(len(new_pairs)):
            switch_idx.append([pairs[i][0],new_pairs[i][0]])
            switch_idx.append([pairs[i][1],new_pairs[i][1]])
        #calculating the displacement vectors to maintain the same centroids
        x_displacement=np.zeros(20)
        y_displacement=np.zeros(20)
        z_displacement=np.zeros(20)
        switch_idx2=[]
        for i in range(20):#sorting according to origin PLD
            for j in range(20):
                if switch_idx[j][0]==i:
                    switch_idx2.append([switch_idx[j][0],switch_idx[j][1]])
                    break
        for i in range(20):
            x_displacement[i]=x_centroid[switch_idx2[i][1]]-x_centroid[switch_idx2[i][0]]
            y_displacement[i]=y_centroid[switch_idx2[i][1]]-y_centroid[switch_idx2[i][0]]
            z_displacement[i]=z_centroid[switch_idx2[i][1]]-z_centroid[switch_idx2[i][0]]
        #updating trajectory
        for i in range(len(x.index)): #updating trajectory
            x.loc[i]=x.loc[i]+x_displacement
            y.loc[i]=y.loc[i]+y_displacement
            z.loc[i]=z.loc[i]+z_displacement
        return x,y,z         

    #definition of links between point-light displays, forming arms, legs, head etc
    if type(links)==list or type(links)==tuple:
        pass
    elif links==None:
        links=[]
    else:
        links=((0,2),(0,4),(1,2),(1,3),(4,5),(4,10),(5,6),(5,18),(5,20),(6,7),(6,14),(7,8),(8,9),(10,11),(10,14),(11,12),(12,13),(14,15),(15,16),(16,17),(18,19),(19,5))

    #function to check if a pair is linked or not
    def islinked(n1,n2):
        for i in range(len(links)):
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

    #calculate the data limits
    x_max=xdata.max(axis=1)
    x_min=xdata.min(axis=1)
    y_max=ydata.max(axis=1)
    y_min=ydata.min(axis=1)
    z_max=zdata.max(axis=1)
    z_min=zdata.min(axis=1)
        
    #calculate the axis limits
    a=max(np.absolute(xdata.min().min()),np.absolute(xdata.max().max()))
    xmin,xmax=-(a+100),a+100
    b=max(np.absolute(ydata.min().min()),np.absolute(ydata.max().max()))
    ymin,ymax=-(b+100),b+100
    c=max(np.absolute(zdata.min().min()),np.absolute(zdata.max().max()))
    zmin,zmax=-c,c

    if scrambletype=='scrambled':
        xdata,ydata,zdata=calc_scrambled(xdata,ydata,zdata)
    elif scrambletype=='pairwise':
        xdata,ydata,zdata=calc_pairwise(xdata,ydata,zdata)
    else:
        xdata,ydata,zdata=calc_constrained(xdata,ydata,zdata)

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
        ax.scatter(xline,yline,zline, c='w', alpha=0.7)
        #plot the sticks
        for name1 in range(20):
            for name2 in range(20):
                if islinked(name1,name2):
                    x=(xdata.iloc[i,name1],xdata.iloc[i,name2])
                    y=(ydata.iloc[i,name1],ydata.iloc[i,name2])
                    z=(zdata.iloc[i,name1],zdata.iloc[i,name2])
                    ax.plot(x,y,z,'w-',alpha=0.5)
        ax.view_init(0,0)
        
        #set axis limits, removeing grid, setting background etc
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)
        ax.set_zlim(zmin,zmax)
        if detector!=None:
            p = patches.Rectangle((xmax+180,zmax+500),100,1000,fill=True,fc=(detector,detector,detector),zorder=2,clip_on=False)
            ax.add_patch(p)
            art3d.pathpatch_2d_to_3d(p, z=0, zdir="x")         
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
