# from numba import jit
# import numpy as np
import cv2

def draw_lineseg(lineseg_cords, image,color=(255,255,255), thickness=1):
	f1,f2 = lineseg_cords['f1'],lineseg_cords['f2']
	image = cv2.line(image, (f1[0],f1[1]), (f2[0],f2[1]), color, thickness)
	return(image) 

def verti_intesect(fx,x,y1,y2):
	y = fx(x)
	return(y>=y1 and y<=y2)

def hori_intersect(fy,y,x1,x2):
	x = fy(y)
	return(x>=x1 and x<=x2)

def get_fxfy(lineseg_cords):
	"""
	lineseg_cords = {f1:[x1,y1],f2:[x2,y2]}
	where f1 and f2 are the two points of the lineseg in the image
	"""
	f1,f2 = lineseg_cords['f1'],lineseg_cords['f2']
	m = ( f2[1] - f1[1] ) / ( f2[0] - f1[0] )
	c = f2[1] - ( m * f2[0] )
	def fx(x):
		return( int( (m*x) + c ) )
	def fy(y):
		return( int( (y-c) / m ) )

	return (fx,fy)

def lineseg_cross(lineseg_cords,boxes,image=None):
	"""
	input : cordinates of a line segment, list of boxes
	output: a list of boxes through which the given line segment passes
	
	lineseg_cords = {f1:[x1,y1],f2:[x2,y2]}
	where f1 and f2 are the two points of the lineseg in the image
	boxes = [[x11,y11,w1,h1], [x12,y12,w2,h2],..... [x1n,y1n,wn,hn] ]
	"""

	fx,fy = get_fxfy(lineseg_cords)

	crossers = []
	for box in boxes:
		x1,y1,x2,y2 = box[0],box[1],box[0]+box[2],box[1]+box[3]
		intersections = [ verti_intesect(fx,x1,y1,y2), hori_intersect(fy,y1,x1,x2), verti_intesect(fx,x2,y1,y2), hori_intersect(fy,y2,x1,x2) ]
		if sum(intersections)>=1:
			crossers.append(box)

	return(crossers)

	# to visualise the line segment in yellow, all boxes as green, and intersecting boxes as red

	# draw = draw_lineseg(lineseg_cords,image)
	# 	color = (0,255,0)					#default colour of box being red
	# 	if sum(intersections)>=1:			#checking if at least one edge of the box intersects
	# 		color = (0,0,255)				#colour changed to red 
			# for i in range(4):					#to visualise which individual edges of box intersected
			# 	intersection = intersections[i]
			# 	if i==0 and intersection:
			# 		cv2.line(draw,(x1,y1),(x1,y2),(0,0,255),2)
			# 	if i==2 and intersection:
			# 		cv2.line(draw,(x2,y1),(x2,y2),(0,0,255),2)
			# 	if i==1 and intersection:
			# 		cv2.line(draw,(x1,y1),(x2,y1),(0,0,255),2)
			# 	if i==3 and intersection:
			# 		cv2.line(draw,(x1,y2),(x2,y2),(0,0,255),2)
	# 	cv2.rectangle(draw,(x1,y1),(x2,y2),color,1)

	# return(draw)

	# cv2.imshow('0',draw)
	# cv2.waitKey(0)

if __name__ == '__main__':
	"""
	To visualise this algorithim
	generates a blank image,
	draws a random line segement from one edge to another
	generates random boxes in the image
	checks which boxes have the line segment passing through them
	"""
	h_im,b_im = 720,1280
	for im_num in range(20):
		image = np.zeros((h_im,b_im,3),np.uint8)
		hori_lineseg = np.random.randint(0,2)
		if hori_lineseg == 1:
			lineseg_cords = {'f1':[np.random.randint(0,20),np.random.randint(0,h_im)], 'f2':[np.random.randint(b_im- 20,b_im),np.random.randint(0,h_im)]}
		else:
			lineseg_cords = {'f1':[np.random.randint(0,b_im),np.random.randint(0,20)], 'f2':[np.random.randint(0,b_im),np.random.randint(h_im-20,h_im)]}
		boxes=[ [np.random.randint(0, b_im-50),np.random.randint(0, h_im-50),np.random.randint(10,40),np.random.randint(10,40) ] for i in range(200) ]
		image = lineseg_cross(lineseg_cords,boxes,image)
		# cv2.imwrite('0_lineseg_cross_exprmnt/{}.jpg'.format(im_num),image)