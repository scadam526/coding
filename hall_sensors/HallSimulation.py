# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:19:01 2023

@author: Doug
"""

%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

H1 = np.array([0.100,0.208,0.407,0.588,0.743,0.866,0.951,0.995,0.995,0.951,0.866,0.743,0.588,0.407,0.208,0.000,-0.208,-0.407,-0.588,-0.743,-0.866,-0.951,-0.995,-0.995,-0.951,-0.866,-0.743,-0.588,-0.407,-0.208,-0.100,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000])

H2 = np.array([0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.100,0.208,0.407,0.588,0.743,0.866,0.951,0.995,0.995,0.951,0.866,0.743,0.588,0.407,0.208,0.000,-0.208,-0.407,-0.588,-0.743,-0.866,-0.951,-0.995,-0.995,-0.951,-0.866,-0.743,-0.588,-0.407,-0.208,-0.100,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000])

H3 = np.array([0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.100,0.208,0.407,0.588,0.743,0.866,0.951,0.995,0.995,0.951,0.866,0.743,0.588,0.407,0.208,0.000,-0.208,-0.407,-0.588,-0.743,-0.866,-0.951,-0.995,-0.995,-0.951,-0.866,-0.743,-0.588,-0.407,-0.208,-0.100])

D = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27,27.5,28,28.5,29,29.5,30])

fig, ax = plt.subplots()
line, = ax.plot(D, H1 , lw=2)
line, = ax.plot(D, H2 , lw=2)
line, = ax.plot(D, H3 , lw=2)
ax.set_xlabel('Location (mm)')
H1Val = ax.text(0,-.50,'Test', fontsize=12, color = 'blue')
H2Val = ax.text(0,-.70,'Test', fontsize=12, color = 'orange')
H3Val = ax.text(0,-.90,'Test', fontsize=12, color = 'green')
#H1val.set_text('update') 

H1Reading = H1[np.abs(D - 15).argmin()]
H2Reading = H2[np.abs(D - 15).argmin()]
H3Reading = H3[np.abs(D - 15).argmin()]
 

fig.subplots_adjust(left=0.25, bottom=0.25)

axdist = fig.add_axes([0.25, 0.1, 0.65, 0.03]) #Add a plot axis for the distance slider to live
location_slider = Slider(
    ax=axdist,
    label='Location (mm)',
    valmin=0,
    valmax=30,
    valinit=15,
)

# Function called when slider position updates
def update(val):
    closest_value = D[np.abs(D - location_slider.val).argmin()]
    H1Reading = H1[np.abs(D - location_slider.val).argmin()]
    H2Reading = H2[np.abs(D - location_slider.val).argmin()]
    H3Reading = H3[np.abs(D - location_slider.val).argmin()]
    H1Val.set_text(H1Reading) 
    H2Val.set_text(H2Reading) 
    H3Val.set_text(H3Reading) 
        
    

# register the update function with  slider
location_slider.on_changed(update)

#plt.plot(D, H1)
#plt.plot(D, H2)

#plt.plot(D, H3)