def preprocess(filename_in,filename_out,center=None):
    '''Reads a CSV file from VICON Motion Capture and
    creates a new CSV file only with the trajectories,
    changing to another reference frame (mean, rotating)
    if convenient.

    Parameters
    ----------
    filename_in: str,
        Path and name of the original CSV from the VICON
        acquisition
    filename_out: str,
        Path and name of the VICON CSV file to be generated
        after processing
    center: str, optional
        The option to re-reference the viewing perspective:
        options:
            center='shoulder': sets the view along the
                neck-shoulder axis, hence transforming
                a walk around the room to a walk on a
                treadmill
            center='mean': changes the axis origin to the
                mean, hence centralizing the acquisition data
                in the screen
            center=None: no effect (default)

    Returns
    -------
    (none) (output file is saved in the specified filename_out)

    See Also
    --------
    make_video: uses pre-processed VICON data to generate
        video of the movement at specified viewing angle
    scrambled_video: uses pre-processed VICON data to produce
        video of scrambled points (non-biological motion)
    central_dot: generate video of a central dot (resting interval)

    Example
    -------
    vicon.preprocess('C:\\Users\\MyUser\\Documents\\Vicon\\acquisition.csv',
        'C:\\Users\\MyUser\\Documents\\Vicon\\preprocessed.csv',center='shoulders')
    '''
    import numpy as np
    import pandas as pd

    #reading data
    file = pd.read_csv(filename_in,header=None,sep='\n')
    i=file[file[0]=='Trajectories']
    skip_lines=i.index[0]+3
    idx_data=pd.read_csv(filename_in,skiprows=skip_lines+1,nrows=1)
    data = pd.read_csv(filename_in,skiprows=skip_lines+3,header=None)
    data.columns=idx_data.columns

    numframes=len(data.index)
    xdata=data.filter(['X','X.1','X.2','X.3','X.4','X.5','X.6','X.7','X.8','X.9','X.10','X.11','X.12','X.13','X.14','X.15','X.16','X.17','X.18','X.19'],axis=1)
    ydata=data.filter(['Y','Y.1','Y.2','Y.3','Y.4','Y.5','Y.6','Y.7','Y.8','Y.9','Y.10','Y.11','Y.12','Y.13','Y.14','Y.15','Y.16','Y.17','Y.18','Y.19'],axis=1)
    zdata=data.filter(['Z','Z.1','Z.2','Z.3','Z.4','Z.5','Z.6','Z.7','Z.8','Z.9','Z.10','Z.11','Z.12','Z.13','Z.14','Z.15','Z.16','Z.17','Z.18','Z.19'],axis=1)

    theta=np.zeros(numframes)
    if center=='shoulder':
        #coordinate translation to X5 (neck)
        print("axis translation")
        for i in range(numframes):
            xdata.loc[i]=xdata.loc[i]-xdata.loc[i,'X.4']
            ydata.loc[i]=ydata.loc[i]-ydata.loc[i,'Y.4']
            zdata.loc[i]=zdata.loc[i]-zdata.loc[i,'Z.4']
            if i%100==0:
                print("frames done:"+str(i))

        #coordinate rotation around z-axis to X6 (left shoulder) direction
        print("axis rotation")
        for i in range(numframes):
            #calulate new axis angle
            if np.absolute(ydata.loc[i,'Y.6'])<10:
                theta[i]=np.pi/2
            else:
                theta[i]=np.arctan(-xdata.loc[i,'X.6']/(ydata.loc[i,'Y.6'])) #1st and 4th quadrant
            if i>0:
                if (theta[i]<=0 and theta[i-1]>=0) and theta[i-1]<np.pi: #2nd quadrant
                    theta[i]=np.pi-np.absolute(theta[i])
                elif theta[i]>0 and (theta[i-1]>=3 and theta[i]<=1.6): #3rd quadrant
                    theta[i]=np.pi+theta[i]
            #coordinate rotation
            theta2[i]=-theta[i]
            a , b = xdata.loc[i].values*np.cos(theta2[i])-ydata.loc[i].values*np.sin(theta2[i]) , xdata.loc[i].values*np.sin(theta2[i])+ydata.loc[i].values*np.cos(theta2[i])
            xdata.loc[i] , ydata.loc[i] = a , b
            #display progress    
            if i%100==0:
                print("frames done:"+str(i))
    elif center=='mean':
        #coordinate translation to mean
        print("axis translation")
        for i in range(numframes):
            xdata.loc[i]=xdata.loc[i]-xdata.loc[i].mean()
            ydata.loc[i]=ydata.loc[i]-ydata.loc[i].mean()
            zdata.loc[i]=zdata.loc[i]-zdata.loc[i].mean()
            if i%100==0:
                print("frames done:"+str(i))
    else:
        pass

    #making new csv
    print("saving file")
    newdata=pd.concat([xdata,ydata,zdata],axis=1)
    newdata.to_csv(filename_out,index=False)
    print("done")
