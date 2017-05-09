#!usr/bin/python3
# -*- coding: utf-8 -*-
# pygame.camera +streaming +zbar +zbarlight +qrcode genimage

import sys,time
import pygame.camera
from pygame.locals import *

from myzbar import *
import pygame_textinput

DEVICE0 = '/dev/video0'
CAMW,CAMH = 320,240
SIZE0 = (CAMW*2,CAMH*2+40)
SIZECAM = (CAMW,CAMH)
FILEPATH = '/home/pi/scr/'
xcolor =[(255,255,0),(0,0,255),(0,0,0)]



#--main loop
def camstream():
	pygame.init()
	pygame.display.set_caption("อ่าน BARCODE & QRCODE จาก กล้องเว็บแคม USB")
	display = pygame.display.set_mode(SIZE0, 0,24)

	f01 = pygame.font.Font("Garuda-Bold.ttf",12)  

	textinput = pygame_textinput.TextInput( 
				font_family='',
				font_size=25, 
				text_color=xcolor[0],
				cursor_color=xcolor[0])

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

		events = pygame.event.get()
		for event in events:
			#event quit
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_q:
				running = False

			#gen qrcode image
			elif event.type == KEYDOWN and event.key == K_F1:
				xqrtext = textinput.get_text()
				ximgfile = genqrcodefile(xqrtext)
				imgqr = pygame.image.load(ximgfile)
				imgqr = pygame.transform.scale(imgqr,(CAMW,CAMH))
				display.blit(imgqr,(CAMW,CAMH+20))
				
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
		
		#input QRcode textin
		xrect2 = pygame.Rect(0, CAMH+20, CAMW, 20)
		pygame.draw.rect(display, xcolor[1], xrect2)
		textinput.update(events)
		display.blit(textinput.get_surface(), (0,CAMH+20))

		pygame.display.flip()
		clock.tick(FPS)

	camera.stop()
	pygame.quit()
	return

if __name__ == '__main__':
	camstream()
	sys.exit(0)
