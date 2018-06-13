
from rplidar import RPLidar
import numpy as np
from os import sys
import cv2
import math
import copy

PORT_NAME = 'COM4'

data = []
arcdata = []

def run(path):
	'''Main function'''
	lidar = RPLidar(PORT_NAME)
	outfile = open(path, 'w')
	
	try:
		print('Recording measurments... Press Crl+C to stop.')
		for measurment in lidar.iter_measurments():
			line = '\t'.join(str(v) for v in measurment) 
			outfile.write(line + '\n')
			words = line.split('\t')
			word = float(words[2])    
			data.append(word)
	except KeyboardInterrupt:
		print('Stoping.')
		'''i = 1
		for mess in data: 
			if  mess < 50:
				print("value number {} is {}".format(i, mess) )   
			i += 1''' 
  
	lidar.stop()
	lidar.disconnect()	
	outfile.close()
	np.save(path, np.array(data))

def angle_btwpoints():

	count = 0
	length = 0
	temp = []
	arr = []

	for value in data:


		if count < 2 and length < len(data):
			temp.append(value)
			count += 1		
			length += 1	

		elif len(temp) == 2:
			arr = copy.copy(temp)		
			arcdata.append(np.arctan(temp))
			count = 1
			arr.pop(0)
			temp = copy.copy(arr)
			arr = []
					

		else:
			break		

			
def distance_btwpoints():

	arcdiff = np.diff(arcdata)

	

#	statements to display the 'arcdata' values on the screen

	print(" values are: ")	
	k =1
	for out in arcdiff:	

		print("value {} '->' {}".format( k, out) ) 
		k += 1

	print("end") 	

if __name__ == '__main__':
			
	run(sys.argv[1])  	
	print(angle_btwpoints())
	print(distance_btwpoints())																												