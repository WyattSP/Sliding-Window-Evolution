#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:44:17 2021

@author: wyattpetryshen
"""
import fire
import matplotlib.pyplot as plt
from random import randrange
import numpy as np
import plotly.graph_objects as go
import plotly
import os
import time

#Boundary array function
def min_dims(row_val,col_val,w_size,arr):
    max_row = arr.shape[0]
    max_col = arr.shape[1]
    row_val = row_val
    col_val = col_val
    w_size = w_size
    global colmin, rowmin
    #Row truncation for minimum array index
    if row_val < w_size:
        if abs(row_val-0) < abs(row_val-max_row):
            Cr = row_val - w_size
            rowmin = int(row_val-w_size-Cr)
        elif abs(row_val-0) > abs(row_val-max_row):
            Cr = row_val - w_size
            rowmin = int(row_val-w_size+Cr)
    elif row_val >= w_size:
        rowmin = int(center[0]-w_size)
    #Column truncations for minimum array index
    if col_val < w_size:
        if abs(col_val-0) < abs(col_val-max_col):
            CC = col_val - w_size
            colmin = int(col_val-w_size-CC)
        elif abs(col_val-0) > abs(col_val-max_col):
            CC = col_val - w_size
            colmin = int(col_val-w_size+CC)
    elif col_val >= w_size:
        colmin = int(col_val-w_size)
    return rowmin, colmin

def sliding_window(array,window_size,start):
    global center
    arr = array #Set input array
    window_size = window_size #Size of moving window
    center = start #Starting point, first randomly assigned, then uses last move
    #Screen if window min row and col values outside array dimensions
    rowmin, colmin = min_dims(center[0],center[1],window_size,arr)
    #Everything below will iterate through number of steps
    #Set Center
    window_vals = arr[int(rowmin):int(center[0]+window_size+1),int(colmin):int(center[1]+window_size+1)]
    cent_val = arr[center[0],center[1]]
    window_index = np.empty_like(window_vals,dtype='int,int')
    #Fills in index values
    for idx, i in enumerate(np.arange(colmin,colmin+window_index.shape[1])):
        for idx2, j in enumerate(np.arange(rowmin,rowmin+window_index.shape[0])):
            window_index[idx2,idx] = (j,i)
        #Calculate vectors for array
    vectors = window_vals-cent_val
        #Find index for min value,this index refers you to window_index
    try:
        if len(np.argwhere(vectors == np.min(vectors))) > 1:
            #print('Pick random high value')
            new_center = np.argwhere(vectors == np.min(vectors))[randrange(0,len(np.argwhere(vectors == np.min(vectors))))]
        else:
            new_center = np.argwhere(vectors == np.min(vectors))[0]
    except: 
        print(center)
        new_center = np.argwhere(vectors == np.min(vectors))[0]
    #Find new center
    return window_index[new_center[0],new_center[1]]


#Simple gradiant descent with a sliding window. It really likes to get stuck in local minimums
def gradient_descent_3d(array,x_start,y_start,steps=10,step_size=1,plot=True):
    # Initial point to start gradient descent at
    x_start = x_start
    y_start = y_start
    array = array
    steps = steps
    step_size = step_size
    
    step = (x_start,y_start)
    vals = array[step[0],step[1]]

    # Store each step taken in gradient descent in a list
    step_history = []
    step_history.append(step)
    step_vals = []
    step_vals.append(vals)
    
    # Plot 2D representation of array with startng point as a red marker
    if plot:
        fig, ax = plt.subplots()
        CS = ax.contour(np.arange(0,array.shape[0]), np.arange(0,array.shape[1]),array,
                    levels = 25, linewidths = 0.25)
        ax.clabel(CS, inline=True, fontsize=5)
        ax.set_title('Adaptive Surface')
        plt.plot(y_start,x_start,'ro')
    current_x = x_start
    current_y = y_start

    # Loop through specified number of steps of gradient descent to take
    for i in range(steps):
        prev_x = current_x
        prev_y = current_y
        center = (prev_x,prev_y)
        #Find next step
        step = sliding_window(array,step_size,center)
        vals = array[step[0],step[1]]
        # Update current point to now be the next point after stepping
        current_x, current_y = (step[0],step[1])
        #Record step
        step_history.append(step)
        step_vals.append(vals)
        
        # Plot each step taken as a black line to the current point nominated by a red marker
        if plot:
            plt.plot([prev_y,current_y],[prev_x,current_x],'k-')
            plt.plot(current_y,current_x,'ro')
            
        # If step is to the same location as previously, this infers convergence and end loop
        if prev_y == current_y and prev_x == current_x:
            print(f"Converged in {i} steps")
            break
    return step_vals,step_history


class Core_Functions(object):
    
    #Create square 3D surface
    def square_surface(self, array_size = 1000, plot = False):
        '''
        Creates adaptive surface

        Parameters
        ----------
        array_size : TYPE, int
            DESCRIPTION. The default is 1000. int value specifies square dimensions of surface. Must be single value.
        plot : TYPE, boolean
            DESCRIPTION. The default is False. Plots surface.

        Returns
        -------
        new_surface : TYPE, array
            DESCRIPTION. Input array for iter_movement function

        '''
        N = array_size
        # the x and y coordinate of the center point
        center_arr = (N - 1) / 2
        # the coordinates of the square array
        row, col = np.ogrid[:N, :N]
        # N - distance gives the result
        new_surface = N/2 - np.maximum(np.abs(row - center_arr), np.abs(col - center_arr))
        for i in np.arange(1,new_surface.shape[1]-1):
            for j in range(new_surface.shape[0]):
                if new_surface[j,i] == 0:
                    new_surface[j,i] = 0
                elif new_surface[j,i] >= 0:
                    new_surface[j,i] = -new_surface[j,i]
                elif new_surface[j,i] <= 0:
                    new_surface[j,i] = new_surface[j,i]
        if plot:
            sh_0, sh_1 = new_surface.shape
            x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)

            topo = go.Figure(data=[go.Surface(z=new_surface, x=x, y=y)])
            topo.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
            plotly.offline.plot(topo)
            
        np.save('surface.npy',new_surface)
        return new_surface
    
    #Iterate through many runs
    def iter_movement(self, runs, steps=10,step_size=1,plot_all=False,save_plot=True):
        '''
        Models a specified number of individuals to move towards the lowest point on the surface
    
        Parameters
        ----------
        runs : TYPE int
            DESCRIPTION. Number of individuals to evolve on surface
        steps : TYPE, int
            DESCRIPTION. The default is 10. Number of steps each individual will take per run.
        step_size : TYPE, int
            DESCRIPTION. The default is 1. Vector length between each step.
        plot_all : TYPE, boolean
            DESCRIPTION. The default is False. Animated plot of individuals on surface. Set to False for large number of runs.
        save_plot : TYPE, boolean
            DESCRIPTION. The default is True. Save model to .png file in working directory

        Returns
        -------
        TYPE .png
            DESCRIPTION. Returns .png file of model

        '''
        # Initial point to start gradient descent at
        path  = os.getcwd()
        array = np.load(path + '/surface.npy')
        steps = steps
        step_size = step_size
        runs = runs
        color=iter(plt.cm.rainbow(np.linspace(0,1,runs)))
        #Initiates plot
        fig, ax = plt.subplots()
        CS = ax.contour(np.arange(0,array.shape[0]), np.arange(0,array.shape[1]),array,levels = 25, linewidths = 0.25)
        ax.clabel(CS, inline=True, fontsize=5)
        ax.set_title('Adaptive Surface')
        #Iterates through runs
        for k in range(runs):
                c = next(color)
                x_start = randrange(0,array.shape[0]-1)
                y_start = randrange(0,array.shape[1]-1)
                vals_t, step_t = gradient_descent_3d(array,x_start,y_start,steps=steps,step_size=step_size,plot=False)
                x_steps = [i[0] for i in step_t]
                y_steps = [i[1] for i in step_t]
                next_x = x_steps[0]
                next_y = y_steps[0]
                plt.plot(next_y,next_x,'ro',c=c, marker = "d")
                for i in np.arange(1,len(x_steps)-1):
                    past_x = next_x
                    past_y = next_y
                    next_x = x_steps[i]
                    next_y = y_steps[i]
                    plt.plot([past_y,next_y],[past_x,next_x],'k-', c='black')
                    plt.plot(next_y,next_x,'ro', c=c, marker = "o")
                    if plot_all:
                        plt.pause(0.005)
        if save_plot:
            plt.savefig('evolution_surface.png')
        plt.show()
        return print('All finished!')
    
    
    #Main looping function to iterate through runs
    def ind_evol(self, name, runs, steps=10, step_size=10, plot_model = False, plot_rate = 0.05):
        '''
        Evolution towards optima calculated at each step
    
        Parameters
        ----------
        name : TYPE, str
            Name of saved surface, must be a string.
        runs : TYPE, int
            Select number of individuals to include in analysis.
        steps : TYPE, int
            The default is 10. Number of steps individual will take.
        step_size : TYPE, int
            The default is 10. Size of each step.
        plot_model: TYPE, Boolean
            Plots model runs
        plot_rate: TYPE, numeric
            Rate to update plot for each run. For large run values suggest very small vales. Default = 0.05 seconds.
    
        Returns
        -------
        Steps Taken: TYPE Array
            Array of steps taken by each individual. m X n array correspounds to steps (row) X runs (column)
        Step Values: TYPE Array
            Array of values for each step towards the optima. Demensions are the same as Steps Taken array.
    
        '''
        start_time = time.time()
        
        name = name
        path  = os.getcwd()
        array = np.load(path + '/surface.npy')
        step_size = step_size
        steps = steps
        runs = runs
        plot_rate = plot_rate
        
        if runs > 10 and plot_model:
            print("Warning: Plotting large runs will take a long time")
        
        #Initalize starting point for each run
        run_vals = [] #Save starting ooints
        
        #Initiates plot
        if plot_model:
            fig, ax = plt.subplots()
            CS = ax.contour(np.arange(0,array.shape[0]), np.arange(0,array.shape[1]),array,levels = 25, linewidths = 0.25)
            ax.clabel(CS, inline=True, fontsize=5)
            ax.set_title('Adaptive Surface')
            
            color=iter(plt.cm.rainbow(np.linspace(0,1,runs))) #set colors
        
        #Save all values from steps in array
        master_arr_steps = np.empty((steps+1,runs),dtype='int,int')
        master_arr_vals = np.empty((steps+1,runs),dtype='int')
        color_list = []
        for j in range(runs): #5 will be replaced with runs
            x_start = randrange(0,array.shape[0]-1)
            y_start = randrange(0,array.shape[1]-1)
            run_vals.append((x_start,y_start))
            
            if plot_model:
                c = next(color)
                color_list.append(c)
                
                plt.plot(y_start,x_start,'ro',c=c, marker = "d")
            
        master_arr_steps[0] = run_vals
        master_arr_vals[0] = np.zeros(runs)
            
        for i in np.arange(1,steps+1): #Iterate number of steps for each run
                
            new_vals = []
            new_step = []
        
            for idx2, j in enumerate(master_arr_steps[i-1]): #Iterates each individual run per step
                
                prev_x = j[0]
                prev_y = j[1]
                center = (prev_x,prev_y)
                step = sliding_window(array,step_size,center)
                vals = array[step[0],step[1]]
                # Update current point to now be the next point after stepping
                current_x, current_y = (step[0],step[1])
                #Record step
                new_step.append(step) #local
                new_vals.append(vals) #local
                
                past_x = prev_x
                past_y = prev_y
                
                next_x = current_x
                next_y = current_y
                
                if plot_model:
                    plt.plot([past_y,next_y],[past_x,next_x],'k-', c='black')
                    plt.plot(next_y,next_x,'ro', c=color_list[idx2], marker = "o")
                    plt.pause(plot_rate)
                
            master_arr_steps[i] = new_step #global
            master_arr_vals[i] = new_vals #global
        
        if plot_model:
            plt.savefig('Ind_evol.png')
            
        save_name_steps = name + '_steps.npy'
        save_name_values = name + '_values.npy'
        np.save(save_name_steps,master_arr_steps)
        np.save(save_name_values,master_arr_vals)
        print("--- Model run time %s seconds ---" % (time.time() - start_time))
            
        return master_arr_steps,master_arr_vals
                
if __name__ == '__main__':
    core_functions = Core_Functions()
    fire.Fire(core_functions)           
                                