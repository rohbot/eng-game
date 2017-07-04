import pygame
import time
import os
import serial
import sys
import RPi.GPIO as GPIO
#import pyttsx

def shutdown(channel):
	logfile = open('shutdown.log', 'a')
	logfile.write(str(time.time()) + " shutting down\n")
	logfile.close()
	#os.system('flite -t "System Shutdown"')
	print 'Shutdown'
	pygame.quit()
	time.sleep(1)	
	os.system('sudo shutdown -h now')
	sys.exit()
	
def setup():
    print "Shutdown script"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(12, GPIO.OUT)
    GPIO.add_event_detect(14, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
    GPIO.output(12, GPIO.HIGH)

setup()



strPort1 = '/dev/ttyACM0'




WIDTH = 1280
HEIGHT = 700

IMG_WIDTH = 400
IMG_HEIGHT = 500

L_WIDTH = ((WIDTH / 2) - 400) / 2 + 50
R_WIDTH = L_WIDTH + (WIDTH / 2) - 220

images = []


path = "/home/pi/eng-game/assets/"
#path = "/home/roh/biji-biji/pintar/eng-game/assets/"

# Show logo
BASE_CMD = "sudo fbi -T 1 --noverbose -a "
#path = "assets/"
cmd = BASE_CMD + path + "bb.jpg"
os.system(cmd)


ser = serial.Serial(strPort1, 9600)


global counting, start_time, r_counter, l_counter, screen

for i in range(10):
	fn = path + 'ENG0' + str(i) + '.png'
	images.append(pygame.image.load(fn))


img = {'start':pygame.image.load(path + "ENGST.png"),
		'ready':pygame.image.load(path + "ENGGR.png"),
		'finish':pygame.image.load(path + "ENGFN.png"),
		'logo':pygame.image.load(path + "bb.jpg"),
		'game-bg': pygame.transform.scale(pygame.image.load(path + "ENGBG.png"),(WIDTH,HEIGHT)),
		'wait': pygame.transform.scale(pygame.image.load(path + "ENGRP.png"),(WIDTH,HEIGHT)),
		'success': pygame.image.load(path + "ENGCG.png"),
		'tryagain': pygame.image.load(path + "ENGTA.png"),
		'code': pygame.image.load(path + "ENGSC.png"),
		'code2': pygame.image.load(path + "ENGSC_2.png"),

		}


# img_start = pygame.image.load(path + "ENGRP.jpg")
# img_start = pygame.transform.scale(img_start,(1280,720))

# img_ready = pygame.image.load(path + "ENGGR.jpg")
# img_ready = pygame.transform.scale(img_ready,(1280,720))

# img_logo = pygame.image.load(path + "bb.jpg")
# img_logo = pygame.transform.scale(img_logo,(1280,720))



#screen.fill((255, 255, 255))

counting = False
won = False

def show_image(imag):
	global screen
	screen.fill((255, 255, 255))
	screen.blit(img[imag], (0, 0))
	pygame.display.flip()


def start_counter(duration):
	global screen
	r_counter = duration % 10
	duration /= 10
	l_counter = duration % 10
	print duration, l_counter, r_counter  
	counting = True
	l_image = images[l_counter]
	r_image = images[r_counter]

	start_time = time.time()

def waiting():
	#print 'Waiting'
	show_image('wait')

def showReady(line):
	global screen
	if line[2] == "R":
		print 'show ready' 
		show_image('ready')

	if line[2] == "S":
		print 'show start' 
		show_image('start')
		# screen.fill((255, 255, 255))
		# screen.blit(images[2], (0, 0))
		# pygame.display.flip()
	elif line[2] == "F": 
		show_image('finish')
		
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
	#print line


def showResult(line):
	if line[2] == "S":
		show_image('success') 
		# screen.fill((255, 255, 255))
		# screen.blit(img_ready, (0, 0))
		# pygame.display.flip()

	if line[2] == "T":
		print 'Trying again'
		show_image('tryagain') 
		# screen.fill((255, 255, 255))
		# screen.blit(img_ready, (0, 0))
		# pygame.display.flip()
	if line[2] == "C":
		show_image('code')
		time.sleep(10) 
		show_image('code2')
		time.sleep(10) 

		
	

def showLogo():
	screen.fill((255, 255, 255))
	screen.blit(img_logo, (0, 0))
	pygame.display.flip()



#showLogo()
#waiting()
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
show_image('logo')
#
#waiting()
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

		if line[0] == 'P':
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
	


