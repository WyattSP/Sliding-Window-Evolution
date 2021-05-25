# Sliding Window Evolution
Models of evolution towards adaptive optimums using a simple sliding window implementation of gradient descent.

Each major version release will add a layer of complexity to the models. 

## Current Release

* v 0.0.1

Simple gradient descent implemented using a sliding window

Model requires the usuage of two functions. The first creates the surface to run gradient descent, the second is the actual implementation.
Provided is an example with the required code.

To run the model:

1) Open a new command window


2) Set working directory to folder containing 3d_sliding_descent.py


3) Create your surface

> python 3d_window_descent.py square_surface


Input parameters for square_surface:

    array_size: Length of square array to create. Default set to 1000.
    
    plot: Plot surface using plotly. Default False.
    

4) Run the model

> python 3d_window_descent.py iter_movement 10 20 10 False True

Input parameters for square_surface:

    runs: Number of individuals moving across the adaptive surface.
    
    steps: The number of steps each individual will take. Default set to 10.
    
    step_size: The distance of each step. Default set to 1.
    
    plot_all: Default False. Shows animated plot of individuals in QT window. Recommend set to False if large number of runs chosen. Steps plotted every 0.005s.
    
    save_plot: Default True. Saves .png animation to working directory of individuals movement on surface.
    

Outputs are saved into your working directory as individual files.

* square surface returns surface.npy
* iter_movement returns evolution_surface.png 

surface.npy must exist in your working directory for iter_movement to run.
