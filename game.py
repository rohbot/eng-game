import pygame
import time
import os
import serial
import sys
strPort1 = '/dev/ttyACM0'
strPort2 = '/dev/ttyACM1'

ser = serial.Serial(strPort1, 9600)



WIDTH = 1280
HEIGHT = 720

IMG_WIDTH = 400
IMG_HEIGHT = 500

L_WIDTH = ((WIDTH / 2) - 400) / 2 
R_WIDTH = L_WIDTH + (WIDTH / 2)

images = []

path = "/home/pi/eng-game/assets/"
#path = "/home/roh/biji-biji/pintar/eng-game/assets/"


BASE_CMD = "sudo fbi -T 1 --noverbose -a "
#path = "assets/"


global counting, start_time, r_counter, l_counter

for i in range(10):
	fn = path + 'ENG0' + str(i) + '.png'
	images.append(pygame.image.load(fn))

img = {'start':"ENGRP.jpg",
		'ready':"ENGGR.jpg",
		'1':"ENG01.jpg",
		'2':"ENG02.jpg",
		'3':"ENG03.jpg",
		'cycle': "ENGCY.jpg",
		'logo':"bb.jpg",
		'game-bg': "ENGBG.jpg",
		'ms': "ENGMS.jpg",
		'cg': "ENGCG.jpg",
		'ta': "ENGTA.jpg",
		'sc': "ENGSC.jpg",
		}

img_start = pygame.image.load(path + "ENGRP.jpg")
img_start = pygame.transform.scale(img_start,(1280,720))

img_ready = pygame.image.load(path + "ENGGR.jpg")
img_ready = pygame.transform.scale(img_ready,(1280,720))

img_logo = pygame.image.load(path + "bb.jpg")
img_logo = pygame.transform.scale(img_logo,(1280,720))


pygame.init()



screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
done = False
clock = pygame.time.Clock()

screen.fill((255, 255, 255))

counting = False
won = False


def start_counter(duration):
	r_counter = duration % 10
	duration /= 10
	l_counter = duration % 10
	print duration, l_counter, r_counter  
	counting = True
	l_image = images[l_counter]
	r_image = images[r_counter]

	start_time = time.time()

def waiting():
	screen.fill((255, 255, 255))
	screen.blit(img_start, (0, 0))
	pygame.display.flip()


def showReady(line):
	if line[2] == "R": 
		show_image('2')
		# screen.fill((255, 255, 255))
		# screen.blit(images[2], (0, 0))
		# pygame.display.flip()
	elif line[2] == "S": 
		show_image('1')
		
		# screen.fill((255, 255, 255))
		# screen.blit(images[1], (0, 0))
		# pygame.display.flip()
	elif line[2] == "G": 
		show_image('0')
		# screen.fill((255, 255, 255))
		# screen.blit(images[1], (0, 0))
		# pygame.display.flip()
		
	else:
		duration = int(line[2:].strip())
		r_counter = duration % 10
		duration /= 10
		l_counter = duration % 10
		print duration, l_counter, r_counter  
		counting = True
		l_image = images[l_counter]
		r_image = images[r_counter]

		screen.fill((255, 255, 255))
		screen.blit(l_image, (L_WIDTH, 50))
		screen.blit(r_image, (R_WIDTH, 50))
		pygame.display.flip()
	


def showResult(line):
	if line[2] == "C": 
		screen.fill((255, 255, 255))
		screen.blit(img_ready, (0, 0))
		pygame.display.flip()
	
def show_image(imag):
	cmd = BASE_CMD + path + img[imag]
	os.system(cmd)

def showLogo():
	screen.fill((255, 255, 255))
	screen.blit(img_logo, (0, 0))
	pygame.display.flip()



#showLogo()
			
#waiting()

show_image('logo')
waiting()
while 1:
	try:
		line = ser.readline().strip()
		print line

		if line[0] == 'W':
			print 'Waiting'
			won = False
			waiting()

			
		if line[0] == 'C':
			showReady(line)	

		if line[0] == 'D':
			showResult(line)	

	except KeyboardInterrupt:
		raise
	except:
		e = sys.exc_info()[0]

		print "something messed up", e



while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			done = True
			start_counter(30)
		
	
	if time.time() - start_time > 1:
		r_counter -= 1
		if r_counter < 0:
			r_counter = 9
			l_counter -=1
		
		if l_counter < 0:
			l_counter = 0
			r_counter = 0
			counting = False
		
		l_image = images[l_counter]
		r_image = images[r_counter]

		screen.fill((255, 255, 255))


		screen.blit(l_image, (L_WIDTH, 50))
	
		screen.blit(r_image, (R_WIDTH, 50))

		pygame.display.flip()
		
		start_time = time.time()
	


