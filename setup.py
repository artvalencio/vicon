from setuptools import setup
setup(name='vicon',
version='0.25',
description='Package for VICON Motion Capture data analysis',
url='https://github.com/artvalencio/vicon',
author='Arthur Valencio, IC-Unicamp, RIDC NeuroMat',
author_email='arthur@liv.ic.unicamp.br',
license='MIT',
packages=['vicon'],
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires='>=3.6',
install_requires=['pandas','numpy','matplotlib'],
zip_safe=False)
