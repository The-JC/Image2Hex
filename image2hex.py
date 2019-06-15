import numpy as np
import math
import imageio

bwtreshhold = 127 # Threshold for Grayscale to BW conversion
byte_length = 16 # Default byte length

# Convert RGB Color to grayscale color
def rgb2gray(rgb):
	r,g,b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
	return gray 

# Fill up last byte with zeros
def fillupLastByte(b, byte_length):
	while len(b[len(b)-1]) < byte_length:
		b[len(b)-1]+='0'
	return b

# Convert RGB Images to 1bit per pixel hex
def convertImage2Hex(img, bwtreshhold, byte_length):
	img = rgb2gray(img) # Convert Color image into grayscale
	#height, width = img # Read image dimensions

	# Convert grayscale into black&white
	# Compress Pixels to 1 bit pack them together to bytes
	# Stored as Strings
	hexstring = []
	i=0
	for line in img:
		for pixel in line:
			byte = math.floor(i/byte_length)
			i+=1
			if len(hexstring) <= byte:
				hexstring.append("")
			
			if pixel > bwtreshhold:
				hexstring[byte]+='1'
			else:
				hexstring[byte]+='0'

	hexstring = fillupLastByte(hexstring, byte_length)

	# Convert binary String into Hex string
	output_bytes = []
	for b in hexstring:
		output_bytes.append("{0:#0{1}x}, ".format(int(b, 2),6))

	return output_bytes

if __name__ == '__main__':
	import sys

	input_file = ''
	output_file = ''
	bit_length = 16

	if len(sys.argv) == 2:
		input_file = sys.argv[1]
		output_file = input_file + '.txt'
	elif len(sys.argv) == 3:
		input_file = sys.argv[1]
		bit_length = sys.argv[2]
		output_file = input_file + '.txt'
	elif len(sys.argv) == 4:
		input_file = sys.argv[1]
		output_file = sys.argv[2]
		bit_length = sys.argv[3]
	else:
		print("Usage: py image2hex.py [Input File] ([Byte_length])")
		exit()

	print("Converting Image...")
	img = imageio.imread(input_file)

	output_bytes = convertImage2Hex(img, bwtreshhold, byte_length)

	with open(output_file, "w") as f:
		f.write(''.join(output_bytes))
	print("\nConversion compplete \nFile: " + output_file)