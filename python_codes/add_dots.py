import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle


img = mpimg.imread( 'CH3NH3_side_-2.5_numbers.png' ) 
fig = plt.figure() 
ax = fig.add_subplot( 1,1,1) 
sc = ax.imshow( img ) 

xx = 100
yy = 100
circ = Circle((xx,yy),10, color = "black")
ax.add_patch(circ)

plt.show() 
