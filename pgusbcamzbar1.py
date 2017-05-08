#!usr/bin/python3
# -*- coding: utf-8 -*-
# pygame.camera +streaming +zbar +zbarlight

import sys,time,numpy
import pygame.camera, pygame.surfarray
from pygame.locals import *
from PIL import Image
import zbar, zbar.misc
import zbarlight

DEVICE0 = '/dev/video0'
CAMW,CAMH = 320,240
SIZE0 = (CAMW*2,CAMH+20)
SIZECAM = (CAMW,CAMH)
FILEPATH = '/home/pi/scr/'
xcolor =[(255,255,0),(0,0,255),(0,0,0)]

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

#--main loop
def camstream():
	pygame.init()
	pygame.display.set_caption("อ่าน BARCODE & QRCODE จาก กล้องเว็บแคม USB")
	display = pygame.display.set_mode(SIZE0, 0,24)

	f01 = pygame.font.Font("Garuda-Bold.ttf",12)  

	pygame.camera.init()
	camera = pygame.camera.Camera(DEVICE0, SIZECAM)
	camera.start()
	surfcam = pygame.surface.Surface(SIZECAM,depth=24)

	FPS = 25   
	clock = pygame.time.Clock()
	running = True
	while running:
		camera.get_image(surfcam)
		display.blit(surfcam, (0,0))
	
		xrect1 = pygame.Rect(0, CAMH, CAMW, 20)
		pygame.draw.rect(display, xcolor[0], xrect1)
		msgcam = "คลิกซ้าย..อ่าน BARCODE   คลิกขวา..อ่าน QRCODE"
		display.blit(f01.render(msgcam,True,xcolor[1]),(10,CAMH))

		pygame.display.flip()

		for event in pygame.event.get():
			#event quit
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_q:
				running = False
			
			elif event.type == pygame.MOUSEBUTTONDOWN :
			#[1=Lclick 3=Rclick  2=Mclick  4=ScrUp 5=ScrDN]
				if (event.button == 1): #event zbar
					ximgndarray = getimg_ndarray(surfcam)
					xrtns = convzbar(ximgndarray)
				if (event.button == 3): #event zbarlight
					xfile = 'filecam.png'
					pygame.image.save(surfcam,xfile)
					xrtns = convzbarlight(xfile)
					
				display.blit(surfcam, (CAMW,0))
				xrect2 = pygame.Rect(CAMW, CAMH, CAMW, 20)
				pygame.draw.rect(display, xcolor[2], xrect2)
				msgzbar = xrtns[0]
				display.blit(f01.render(msgzbar,True,xcolor[0]),(CAMW+10,CAMH))

		pygame.display.flip()
		clock.tick(FPS)

	camera.stop()
	pygame.quit()
	return

if __name__ == '__main__':
	camstream()
	sys.exit(0)
