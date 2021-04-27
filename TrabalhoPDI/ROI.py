import cv2
import easygui
import unicodedata
from Save import _save_file_dialogs
import os
# Inicializa a lista com os pontos de referencia
refPt = []

def makeRectangle(event, x, y, flags, param):
	global refPt
	# Se o botão esquerdo por clicado duas vezes. pega as coordenadas x e y
	if event == cv2.EVENT_LBUTTONDBLCLK:
		# 64 é usado para ser a image 128x128
		x1 = x - 64
		y1 = y - 64
		x2 = x + 64
		y2 = y + 64
		refPt = [(x1, y1), (x2, y2)]
		# Desenha um retângulo em volta da região de interesse
		cv2.rectangle(image, refPt[0], refPt[1], (255, 0, 0), 2)
		cv2.imshow("Região de interesse", image)

def getRoi(filepath):
	global image
	global clone
	image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
	clone = image.copy()
	cv2.namedWindow("Imagem", cv2.WINDOW_AUTOSIZE)
	cv2.setMouseCallback("Imagem", makeRectangle)
	while True:
		# Mostra a imagem e espera a tecla ser pressionada
		cv2.imshow("Imagem", image)
		key = cv2.waitKey(1) & 0xFF
		# Se 'r' for pressionada, reseta a imagem
		if key == ord("r"):
			image = clone.copy()
		# Se 'c' for pressionado, para o loop
		elif key == ord("c"):
			break
	# Se houver mais de dois pontos de referencia, corta a imagem
	if len(refPt) == 2:
		roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]	
		return roi
		