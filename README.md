# Solvr

## Inspiration
Tutorials on how to solve Rubik's cubes too often give very general algorithms on how to solve a cube from any starting state. These thus miss a great opportunity to teach children the basics of logic and deduction. Providing a step-by-step instructions *specifically* made for the cube in your hands was thus our goal, with future plans to give more complete insight on the reasoning behind each step.

## What it does
Using your webcam, we find a solution for your cube and provide you with step-by-step instructions on how to solve it by displaying a 3D virtual representation of the cube on the screen.
Simply show all faces of a cube to the webcam and let the program teach you what to do next!

## How we built it
A Unity3D app shows the cube and displays animations as to what to do next. This app is connected to a python server on which OpenCV is used to analyze images from a webcam in realtime in order to detect the state of a cube by reading colors from each face of the cube.

Our teams' Rubik's cube genius built a custom Rubik's cube solver for maximum bragging rights!

The 3D representation of the cube was taken from https://github.com/stuartsoft/RSolver

## What's next for Solvr
With a little bit more work, Solvr could be used as an educational platform for kids to learn how to solve Rubik's cubes, while gaining important logic skills! This platform could also be used to gamify the experience.
