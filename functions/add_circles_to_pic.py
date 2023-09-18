import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle

picture = "CH3NH3_side_-2.5_numbers.png"
x_list_values = [270, 455, 370, 380]
y_list_values = [160, 155, 210, 390]
colors_list = ["orange", "orange", "black", "purple"]
size_list = [20, 20, 25, 35]

def add_circles(picture, x_list_values, y_list_values, colors_list, size_list):
	img = mpimg.imread(picture)
	fig = plt.figure() 
	ax = fig.add_subplot( 1,1,1) 
	sc = ax.imshow( img )
	for i in range(0, len(x_list_values)):
		xx = x_list_values[i]
		yy = y_list_values[i]
		circ = Circle((xx,yy), size_list[i], color = colors_list[i])
		ax.add_patch(circ)
	plt.axis('off')
	fig.savefig('out.png', bbox_inches='tight', pad_inches=0, dpi=300)
	plt.show() 

add_circles(picture, x_list_values, y_list_values, colors_list, size_list)
