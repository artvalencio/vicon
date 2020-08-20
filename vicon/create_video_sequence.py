def create_video_sequence(path_to_vicon_files,preprocessed_vicon_filenames,video_seq_name):
    ''' Creates a video sequence of visual
        stimulii for Neuroscience experiment

    -----------
    Parameters:
        path_to_vicon_files: str,
            The path to where the preprocessed Vicon
            files are saved
        preprocessed_vicon_filenames: list of str,
            The names of the preprocessed Vicon files 
        video_seq_name: str,
            The name of the video file to be generated

    -----------
    Output:
        (none) (video file to be save at Vicon folder)
    
    -----------
    Description:

    The experiment design consists of 3 blocks
    with 10 stimulus each, 5 of which are
    biological (vicon.make_video), and the other
    5 non-biological (vicon.scrambled_video). The
    stimulus last for 30s.

    Each stimulus is separated from the next by
    a short rest of 3 seconds. Each block is
    separated from the next by a longer rest of
    15s. The resting intervals consist of a
    fixed point at the center of the screen.

    The experiment begins with a rest of 15s,
    where is calibrated a fast-response light
    detector used for synchronization of the
    EEG data with the stimulus presentation.
    
    '''

    #going to folder where vicon files are stored
    import os
    import numpy as np
    import vicon
    os.chdir(path_to_vicon_files)
    os.mkdir("temp")

    #defining order of stimulus within sequence blocks
    video_seq=np.empty((11,3))
    for i in range(3):
        seq=np.array([0]*5+[1]*5)
        np.random.shuffle(seq)
        seq=np.append(seq,2)
        video_seq[:,i]=seq
    
    #preparing the videos
    names='file temp\\\\intro.mp4\n'
    vicon.gen_detector_intro('temp\\intro.mp4',15)
    vicon.central_dot('temp\\rest3s.mp4',3,detector=0.3)
    vicon.central_dot('temp\\rest15s.mp4',15,detector=0.3)
    
    for j in range(3):
        for i in range(11):
            if video_seq[i,j]==1:
                walk=np.random.randint(1,len(preprocessed_vicon_filenames))
                walk_name=preprocessed_vicon_filenames[walk-1]
                with open(walk_name) as f:
                    n_lines=sum(1 for line in f)
                filename_out='temp\\\\'+'video'+str(j)+f'{i:03}'+'.mp4'
                names+="file "+filename_out+"\n"
                startframe=np.random.randint(300,n_lines-30*31)
                vicon.make_video(walk_name,filename_out,
                                 framerange=[startframe,startframe+30*30],
                                 edgetype=None,axislims=(800,800,1200))
            elif video_seq[i,j]==0:
                walk=np.random.randint(1,len(preprocessed_vicon_filenames))
                walk_name=preprocessed_vicon_filenames[walk-1]
                with open(walk_name) as f:
                    n_lines=sum(1 for line in f)
                filename_out='temp\\\\'+'video'+str(j)+f'{i:03}'+'.mp4'
                names+="file "+filename_out+"\n" 
                startframe=np.random.randint(300,n_lines-30*31)
                vicon.scrambled_video(walk_name,filename_out,
                                 framerange=[startframe,startframe+30*30],
                                 detector=1,scrambletype='constraint',
                                      axislims=(800,800,1200),detector_loc=(1350,1400))
            if i<10:
                names+='file temp\\\\rest3s.mp4\n'
            if video_seq[i,j]==2:
                names+='file temp\\\\rest15s.mp4\n'
            
    #generating ffmpeg join videos command
    f=open('videonames.txt','w')
    f.write(names)
    f.close()
    command="ffmpeg -f concat -safe 0 -i videonames.txt -c copy " + video_seq_name
    
    #calling ffmpeg via command prompt
    #(it's much faster to use it via cmd than within Python)
    #(fill the part inside " ")
    fullstr='cmd /c "' + command + ' && del /q temp && rmdir /q temp && del /q videonames.txt"'
    os.system(fullstr)
