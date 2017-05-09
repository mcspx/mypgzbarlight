import numpy
import zbar, zbar.misc
import zbarlight
import qrcode
from PIL import Image
import pygame.surfarray

#--gen qrcode
def genqrcodefile(xtxt):
	img = qrcode.make(xtxt)
	xfile = "img.png"
	img.save(xfile)
	return (xfile)


#--calc Barcode ImageArray
def getimg_ndarray(xpgimage):
    image_ndarray = pygame.surfarray.array3d(xpgimage)

    if len(image_ndarray.shape) == 3:
         image_ndarray = zbar.misc.rgb2gray(image_ndarray)
    return image_ndarray

#--read Barcode
def convzbar(ximg_ndarray):
	# Detect all
	scanner = zbar.Scanner()

	results = scanner.scan(ximg_ndarray)
	if results==[]:
		data0 = ""
		result0 = ("No Barcode found.")
	else:
		for result in results:
			# By default zbar returns barcode data as byte array, so decode byte array as ascii
			print(result.type, result.data.decode("ascii"), result.quality)

		data0 =  results[0].data.decode("ascii")
		result0 = ("[Q%s]  %s >> '%s'" % (results[0].quality, results[0].type,data0 ))	
	
	print (result0)
	return (result0,data0)

#--read QRcode
def convzbarlight(xfileimg):
	with open(xfileimg, 'rb') as image_file:
		ximage = Image.open(image_file)
		ximage.load()

	codes =  zbarlight.scan_codes('qrcode', ximage)
	result0 = ('QR codes: %s' % codes)
	print (result0)
	
	if not(codes == None) :
		data0 = codes
	else:
		data0 = ""
	return (result0,data0)
