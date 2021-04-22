# SightWalk

## Reasoning

There are 12 million blind and visually impaired individuals in the U.S. and only 2% of visually impaired individuals in
the U.S. work with guide dogs.
We made this project in order to prototype the use of easily accessible navigation software.
Our code can identify sides, help people stay on the sidewalk and avoid obstacles.
We made this project for FIRST's Innovation Challenge and we hope we can encourage more FIRST Teams to contribute 
to open source code.

## Detection Demo
Our code uses AI in order to detect people and locate what side the sidewalk is on.
This can be clearly seen in the gif:

![](assets/Sidewalk_Demo.gif)

## Blind Navigation Code Diagram

![](assets/Code_Diagram.png)

## Design
![](assets/Design.png)

## Physical Build
![](assets/Physical_Build.jpg)

## Using the code
1. Install dependencies with `pip install -r `[`requirements.txt`](requirements.txt)
2. Build darknet as per the instructions in the darknet_builder folder
3. Build pangolin in the uoip_pangolin folder within display_3d as per the github.com/uoip/pangolin.git install instructions
4. Run process_runner.py

## File Description

[process_runner.py](process_runner.py) manages all sub tasks.

[sidewalk_classification.py](sidewalk_classification) manages and provides sidewalk state inference.

[detector.py](person_automobile_sign_detection/detector.py) manages and provides object localization inferences.

[detection.py](person_automobile_sign_detection/detection.py) models a detection tracked through time

[capturer.py](capturer.py) handles getting images from the camera

[display.py](display.py) handles displaying those images onto the visualization tool

[feedback](feedback/) handles feedback to Jetson Xavier NX (waist vibration and audio cues)

## Future Plans

TODO:
* [ ] Convert to phone application
* [ ] Add more capabilities such as more sidewalk states, when to turn, when it is safe to cross the street, etc.
* [ ] Adding GPS + ML in order to make it easier to get to the destination
* [ ] Add more aids such as text recognition
* [ ] Monocular point slam

## How to contribute
1. Create a fork of this repository on github
1. Clone the fork you made ``git clone https://github.com/GITHUB-ACCOUNT-NAME/blind-navigation.git``
2. Make a new branch with a descriptive name
3. Make your changes and test them
4. Submit a pull request with a list of changes

## Acknowledgements
* Darknet (Yolov4), Pangolin (3d Opengl Visualizer), Pygame(2D SDL Visualizer), Tensorflow, Opencv

Create an issue if you have any questions

By Paly Robotics

![](assets/Logo.png)
