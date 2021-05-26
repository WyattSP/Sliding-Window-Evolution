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

* Two model arguments for this version:

> python 3d_window_descent.py iter_movement 10 20 10 False True

Input parameters for iter_movement:

    runs: Number of individuals moving across the adaptive surface.
    
    steps: The number of steps each individual will take. Default set to 10.
    
    step_size: The distance of each step. Default set to 1.
    
    plot_all: Default False. Shows animated plot of individuals in QT window. Recommend set to False if large number of runs chosen. Steps plotted every 0.005s.
    
    save_plot: Default True. Saves .png animation to working directory of individuals movement on surface.
    

> python 3d_window_descent.py ind_evol 'Test_Model' 10 20 10 True 0.05

Input parameters for ind_evol:

    name: Name of saved output files.

    runs: Number of individuals moving across the adaptive surface.
    
    steps: The number of steps each individual will take. Default set to 10.
    
    step_size: The distance of each step. Default set to 1.
    
    plot_model: Default False. Shows animated plot of individuals in QT window. Recommend set to False if large number of runs chosen. Steps plotted every 0.005s.
    
    plot_rate: Default 0.05. For large number of runs choose low values for plot_rate.
    

Outputs are saved into your working directory as individual files.

* square surface returns surface.npy
* iter_movement returns evolution_surface.png 
* ind_evol returns two numpy files, one of the steps taken in each run, and the other of step values. Plot can also be optionaly saved.

surface.npy must exist in your working directory for iter_movement to run.
