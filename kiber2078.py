import pygame, sys, time
from pygame.locals import *
from random import *
import ctypes
from winsound import Beep


MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, 'Управление: r - сброс, z - откат, стрелочки - двигать. Приятной игры :)', 'Кибер2078 Зуевской Н., Ефимов М. 11Т2', 0)

flag = 1
proigral = open('lose.mp3')


balli = 0
standart = 2
razmerdoski = 4

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(proigral)

scr = pygame.display.set_mode((470, 510), 0, 32)
pygame.display.set_caption("Кибер2078 Зуевской Н., Ефимов М. 11Т2")

font = pygame.font.SysFont("Arial", 56)
ballifont = pygame.font.SysFont("Arial", 50)
postext = [[(20, 38), (20, 148), (20, 258), (20, 368)], [(130, 38), (130, 148), (130, 258), (130, 368)], [(240, 38), (240, 148), (240, 258), (240, 368)], [(350, 38), (350, 148), (350, 258), (350, 368)]]
posklet = [[(20, 20, 100, 100), (20, 130, 100, 100), (20, 240, 100, 100), (20, 350, 100, 100)], [(130, 20, 100, 100), (130, 130, 100, 100), (130, 240, 100, 100), (130, 350, 100, 100)], [(240, 20, 100, 100), (240, 130, 100, 100), (240, 240, 100, 100), (240, 350, 100, 100)], [(350, 20, 100, 100), (350, 130, 100, 100), (350, 240, 100, 100), (350, 350, 100, 100)]]
tablitsa = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
otmenaoper = []

def main(zapushen = False):

	if not zapushen:
		novayakletka()
		novayakletka()

	rendertabl()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if proverkadvig() == True:
				if event.type == KEYDOWN:
					if strelka(event.key):
						rotations = napravlenie(event.key)

						otmena()

						for i in range(0, rotations):
							povorottabl()

						if mojnodvigat():
							dvigaem()
							soed()
							novayakletka()

						for j in range(0, (4 - rotations) % 4):
							povorottabl()

						rendertabl()
			else:
				vsyo()

			if event.type == KEYDOWN:
				global razmerdoski

				if event.key == pygame.K_r:
					sbros()

				if 50 < event.key and 56 > event.key:
					razmerdoski = event.key - 48
					sbros()

				if event.key == pygame.K_z:
					otmena2()

		pygame.display.update()

def cvet(x):
    cveta = [(255, 255, 255), (255, 0, 255), (128, 0, 128), (255, 0, 0), (128, 0, 0), (255, 255, 0), (128, 128, 0), (0, 255, 0), (0, 128, 0), (0, 255, 255), (0, 128, 128)]
    if x == 0:
        return cveta[0]
    elif x == 2:
        return cveta[1]
    elif x == 4:
        return cveta[2]
    elif x == 8:
        return cveta[3]
    elif x == 16:
        return cveta[4]
    elif x == 32:
        return cveta[5]
    elif x == 64:
        return cveta[6]
    elif x == 128:
        return cveta[7]
    elif x == 256:
        return cveta[8]
    elif x == 512:
        return cveta[9]
    elif x == 1024:
        return cveta[10]
    elif x == 2048:
        return cveta[11]
    elif x > 2048:
        return cveta[0]

def rendertabl():
    global tablitsa, scr, tsveta, posklet, font, balli, ballifont
    scr.fill((0, 0, 0))
    Beep(500, 50)
    ballitxt = ballifont.render("Баллы: " + str(balli), 1, (255, 255, 255))
    scr.blit(ballitxt, (25, 450))
    for i in range(4):
        for j in range(4):
            t = tablitsa[i][j]
            pygame.draw.rect(scr, cvet(t), posklet[i][j])
            te = font.render(str(t), False, (255, 255, 255))
            scr.blit(te, postext[i][j])

def vsyo():
        global balli, flag
        if flag == 1:
            pygame.mixer.music.play()
            flag = 0
        else:
            flag = 1
        scr.fill((0, 0, 0))
        la = ballifont.render("Провал!", 1, (255,255,255))
        la2 = ballifont.render("Баллы:" + str(balli), 1, (255,255,255))
        la3 = font.render("Нажмите [r]", 1, (255,255,255))
        la4 = font.render("для начала игры", 1, (255,255,255))
        scr.blit(la, (10, 10))
        scr.blit(la2, (10, 110))
        scr.blit(la3, (10, 210))
        scr.blit(la4, (10, 260))

def otmena2():
	if len(otmenaoper) > 0:
		mat = otmenaoper.pop()

		for i in range(0, razmerdoski ** 2):
			tablitsa[floor(i / razmerdoski)][i % razmerdoski] = mat[i]

		global balli
		balli = mat[razmerdoski ** 2]

		rendertabl()

def novayakletka():
	count = 0
	for i in range(0, razmerdoski):
		for j in range(0, razmerdoski):
			if tablitsa[i][j] == 0:
				count += 1

	k = floor(random() * razmerdoski * razmerdoski)

	while tablitsa[floor(k / razmerdoski)][k % razmerdoski] != 0:
		k = floor(random() * razmerdoski * razmerdoski)

	tablitsa[floor(k / razmerdoski)][k % razmerdoski] = 2

def floor(n):
	return int(n - (n % 1))

def dvigaem():
	for i in range(0, razmerdoski):
		for j in range(0, razmerdoski - 1):
			while tablitsa[i][j] == 0 and sum(tablitsa[i][j:]) > 0:
				for k in range(j, razmerdoski - 1):
					tablitsa[i][k] = tablitsa[i][k + 1]
				tablitsa[i][razmerdoski - 1] = 0

def soed():
	global balli

	for i in range(0, razmerdoski):
		for k in range(0, razmerdoski - 1):
				if tablitsa[i][k] == tablitsa[i][k + 1] and tablitsa[i][k] != 0:
					tablitsa[i][k] = tablitsa[i][k] * 2
					tablitsa[i][k + 1] = 0
					balli += tablitsa[i][k]
					dvigaem()

def sbros():
	global balli
	global tablitsa

	balli = 0
	scr.fill((0, 0, 0))

	tablitsa = [[0 for i in range(0, razmerdoski)] for j in range(0, razmerdoski)]

	main()

def proverkadvig():
	for i in range(0, razmerdoski ** 2):
		if tablitsa[floor(i / razmerdoski)][i % razmerdoski] == 0:
			return True

	for i in range(0, razmerdoski):
		for j in range(0, razmerdoski - 1):
			if tablitsa[i][j] == tablitsa[i][j + 1]:
				return True
			elif tablitsa[j][i] == tablitsa[j + 1][i]:
				return True
	return False

def povorottabl():
	for i in range(0, int(razmerdoski/2)):
		for k in range(i, razmerdoski- i - 1):
			t1 = tablitsa[i][k]
			t2 = tablitsa[razmerdoski - 1 - k][i]
			t3 = tablitsa[razmerdoski - 1 - i][razmerdoski - 1 - k]
			t4 = tablitsa[k][razmerdoski - 1 - i]

			tablitsa[razmerdoski - 1 - k][i] = t1
			tablitsa[razmerdoski - 1 - i][razmerdoski - 1 - k] = t2
			tablitsa[k][razmerdoski - 1 - i] = t3
			tablitsa[i][k] = t4

def mojnodvigat():
	for i in range(0, razmerdoski):
		for j in range(1, razmerdoski):
			if tablitsa[i][j-1] == 0 and tablitsa[i][j] > 0:
				return True
			elif (tablitsa[i][j-1] == tablitsa[i][j]) and tablitsa[i][j-1] != 0:
				return True

	return False

def napravlenie(k):
	if k == pygame.K_UP:
		return 0
	elif k == pygame.K_DOWN:
		return 2
	elif k == pygame.K_LEFT:
		return 1
	elif k == pygame.K_RIGHT:
		return 3

def strelka(k):
	return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

		
def lin():
	mat = []

	for i in range(0, razmerdoski ** 2):
		mat.append(tablitsa[floor(i / razmerdoski)][i % razmerdoski])

	mat.append(balli)

	return mat

def otmena():
	otmenaoper.append(lin())


main()
