# SightWalk

![](assets/JetsonCase.png)

## Project Description

### Goal: Aiding blind users in the goal of safe outdoor exercise without the assistance of guides

SightWalk is an entirely open source visual assistance and sidewalk navigation device that helps visually-impaired individuals navigate outdoor environments. SightWalk uses neural network models that detect objects, such as people, cars, bikes, street signs, and more, and a set of custom trained deep neural network models to provide relevant & specific sidewalk state space information. At the moment, we have 2 custom models: a sidewalk shift classification model and a turn classification model. The shift classification model determines an individual’s position relative to a sidewalk as a classification NN problem which can be used to provide feedback on which direction the blind user should move to get back onto the sidewalk given that they have drifted onto the road (a common and potentially fatal situation faced by blind individuals when navigating their outdoor environments). The turn classification model can determine if there is a junction point up ahead, and if so, what direction the sidewalk is leading the blind user. While the user is walking, the discreet "button camera" paired with the waist-mounted Jetson Xavier computer uses these convolutional NN models for blind-user position evaluation. This evaluation outputed by the program then interfaces with the visually-impared user using 2 feedback modalities: audio and vibratory. 


## Detection Demo

[![youtube link](assets/Youtube.png)](https://www.youtube.com/watch?v=xqhnR9QOT2w)


## Physical Build

Discreet Camera            | Computer Housing
:-------------------------:|:-------------------------:
![](assets/DesignV2Camera.png)  |  ![](assets/DesignV2Worn.png)

## Technical Details: A More In-Depth Explanation
The button camera as shown above takes a live video stream of the surroundings of the blind individual upon which important data can be extrapolated. 

In order to determine the sidewalk shift state and the sidewalk turn state, we trained 2 custom convolutional neural networks. The CNN models use Resnet and VGG architecture respectively and were trained on custom datasets of over 5000 images taken by the Paly Robotics team. Both models have around 95% verification accuracy at the moment. 

In order to identify obstacles such as cars, people, vehicles, stop signs, street lights, and other unseen hazards such as fire hydrants, we trained a YOLOV4-Tiny CNN model on the COCO image dataset. In order to track objects through frames, we wrote a custom tracking algorithm which can take the model’s inferences and associate detections through multiple frames (doing extra false positive and false negative detection removals simultaneously). We ended up with a highly accurate object detection pipeline as shown in the demo video. With the ability to id each object and associate objects in movement, we have access to the temporal movement history of all objects which allow us to calculate the movemement direction vector of the object which can be used to predict possible collisions that may occur. Since only objects likely to come into collision with the blind user are relevant feedbackthat is acted upon, this allows us to filter out important and unimportant object locationary information as to not overload the auditory feedback modality. We also use this information for a lightweight intersection safety detector which can evaluate if there are no moving cars at an intersection based on the movement direction vectors of all the vehicles in the scene.

In order to interact with the user, we also have a set of vibration motors which allow for dynamic steering of the course of the blind individual, useful for providing more immediate and abrupt feedback. An ambient sound pass-through earbud set is used for higher resolution outputs such as object detection data.

Our demo video showcases the above features on top of our visualization tools. Most recently, we have worked on the development of the 3d viewing tool using OpenGL as shown in the beginning of the video which allows us to navigate around frames and view the three-dimensional movement direction vectors of detected objects.

We also have been prototyping a navigation system that can take in audio input specifying the wanted location, search for the location in a place database, use gps to find the current location, generate a route or trajectory, and then follow the trajectory. A prototype of this is attached in the above video.

## Blind Navigation Code Diagram

![](assets/Code_Diagram.png)

## Using the code
1. Install dependencies with `pip install -r `[`requirements.txt`](requirements.txt)
2. Build darknet as per the instructions in the darknet_builder folder or the github.com/AlexeyAB/darknet.git install instructions
3. Build pangolin in the uoip_pangolin folder within display_3d as per the github.com/uoip/pangolin.git install instructions
4. Run process_runner.py

## File Description

[process_runner.py](process_runner.py) manages all sub tasks.

[sidewalk_classification.py](sidewalk_classification) manages and provides sidewalk shift state inference.

[turn_classification.py](sidewalk_classification) manages and provides sidewalk turn state inference.

[detector.py](person_automobile_sign_detection/detector.py) manages and provides object localization inferences.

[detection.py](person_automobile_sign_detection/detection.py) models a detection tracked through time

[capturer.py](capturer.py) handles getting images from the camera

[display.py](display.py) handles displaying those images onto the 2d and 3d visualization tool

[feedback](feedback/) handles feedback to Jetson Xavier NX (waist vibration and audio cues)



## Future Plans

TODO:
* [ ] Convert to phone application
* [ ] Adding GPS + ML in order to make it easier to get to the destination
* [ ] Add more aids such as text recognition
* [ ] Monocular point slam

## Open Source & How to contribute

SightWalk is entirely open source, meaning all software, CAD designs, and image datasets are public. Public availability of projects are often the most effective way of fostering community growth onto a project and the continued improvement of a piece of tech. We heavily encourage anyone who is interested in participating to contribute!

1. Create a fork of this repository on github
2. Clone the fork you made ``git clone https://github.com/GITHUB-ACCOUNT-NAME/blind-navigation.git``
3. Download models and place them in the appropriate folders <br> [Model Download Link](https://drive.google.com/file/d/1AinPk80U0Euq6phM6UEneZsE8TIypnoy/view?usp=sharing)
4. Make a new branch with a descriptive name
5. Implement the new feature
6. Write test cases showing the robustness of the feature against multiple test cases and edge cases.
7. Submit a pull request detailing all changes made.

## Image Dataset Link

[Sidewalk Position Determination Dataset](https://drive.google.com/file/d/1hT2aOikyk8xYNjPstqaAtFY1kt-81E8O/view?usp=sharing)

We custom collected this dataset housing the images that would respectively indicate if an individual was left, right, or middle of the sidewalk. It has been weighted for training purposes with a left: 1000, right: 1000, middle: 1150 split. Augmentation has been preperformed on the data. 

Create a pull request with a zip file of the new images and a google drive link if you have more images to add!

## Acknowledgements
* Darknet (Yolov4), Pangolin (3d Opengl Visualizer), Pygame(2D SDL Visualizer), Tensorflow, Opencv

Create an issue if you have any questions

By Paly Robotics

![](assets/Logo.png)
