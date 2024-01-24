import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from tkinter import *
from PIL import Image, ImageTk
import imutils
import random
import threading
import time
import pygame

resultadoSuma=0
fingersTotal=0


def start(): #aquesta funció s'inicialitza al premer el botó INICIAR
    iniciar.place_forget() #fem desapareixer el botó INICIAR
    finalizar.place(x=530, y=635) #apareix el botó finalitzar en aquestes coordenades
    cap = cv.VideoCapture(0) #creem un objecte anomenat cap que agafara la informació de la primera webcam (0)
    detector = HandDetector(detectionCon=0.8, maxHands=2) #configurem com detectem les mans 
    width, height = 640, 480 #establim les l'ample i alçada de la pantalla de la webcam
    cap.set(3, width) 
    cap.set(4, height)
    
    numRandomGenerator()
    
    

    def videoLoop(): #aquesta funció estarà en constant funcionament actualitzant-se cada fotograma
        global fingersTotal
        while True:
            success, img = cap.read() #fa una captura del que capta la camara, y diu si s'ha pogut fer o no a "success", es podria prescindir de "success" realment
            #Aqui em sortia la webcam de color blau y no vaig trobar
            #una altra solució que aguesta. (CHAT GPT) 
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            ##############################
            im = Image.fromarray(img_rgb) #agafa la imatge convertida RGB de adalt i la transforma en un objecte Pillow (que permet tractar les imatges)
            imtk = ImageTk.PhotoImage(image=im) #convertim la imatge pillow en una imatge per tkinter (PhotoImage) perque el pugui mostrar

            labelVideo.imgtk = imtk 
            labelVideo.configure(image=imtk) #el widget anomenat labelVideo mostra el objecte PhotoImage (la imatge convertida recentment a objecte de TK)
            #ara ja tenim el "video" integrat al label de tk que alhora esta integrat dins de la finestra i queda tot en 1


            hands, success = detector.findHands(img_rgb, draw=False) #detectem mans, posem la opcio que no dibuixi res

            if hands: #en cas de que detecti hands (es un array)
                hand1 = hands[0] #asignem la primera posició a la primera i unica ma que hi ha
                fingers1 = detector.fingersUp(hand1) #amb fingers up sabem els dits que están pujats.
                #EXEMPLE: si aixequem nomes el polze com si fesim "like", fingers1 seria =[1,0,0,0,0] on 1 es el dit aixecat i 0 baixat
                fingersTotal = sum(fingers1) #amb sum es poden sumar tots els valors de un array
                checkerSuma(fingersTotal,resultadoSuma) #executa la funcio que comproba si els dits aixecats coincideixen amb el resultat de la suma, el resultat de la suma s'obte a la linea
                if len(hands) == 2:
                    hand2 = hands[1] #s'asigna una altra ma etc com adalt
                    fingers2 = detector.fingersUp(hand2)
                    fingersTotal = sum(fingers1) + sum(fingers2)
                    checkerSuma(fingersTotal,resultadoSuma)
            else:
                fingersTotal=0 #si no hi ha cap ma en comptes de quedarse amb l'ultim valor es reseteja a 0

#podria executar videoLoop() tal cual pero no funcionaria, gracies a Thread podem executar tasques en segon pla en python mentres s'executa una altra funció
    thread = threading.Thread(target=videoLoop) #creem un objecte Thread i especifiquem la funció que executarem a target
    thread.start()


def numRandomGenerator():
    global resultadoSuma #global per modificar el parametre a fora també
    num1 = random.randint(1, 9) 
    num2 = random.randint(1, 10 - num1) #generem 2 numeros que no sumin 10 entre ells 2
    '''
    pygame.mixer.init()
    num1Sound = pygame.mixer.Sound("audio/"+str(num1)+".mp3")
    pygame.mixer.init()
    num2Sound = pygame.mixer.Sound("audio/"+str(num2)+".mp3")
    num1Sound.play()
    num2Sound.play()
    '''
    resultadoSuma = num1 + num2 #asignem la suma
    labelSuma.config(text=str(num1) + " + " + str(num2) + "?") #cambiem aquest widget de TK que serveix per mostrar la suma al nubol de la esquerra      

def checkerSuma(fingersTotal,resultadoSuma): #pasem parametres
    if fingersTotal==resultadoSuma: #si els dits aixecats coincideixen amb el resultat de la suma
        correcte("audio/"+str(resultadoSuma)+".mp3") #tinc una carpeta amb els audios de cada numero. ex: 1.mp3, llavors pasem un string anomenat com la ruta a una funció que s'executa quan els numeros coincideixen
        numRandomGenerator() #generem una altra suma   

def correcte(audio):#li arriba el string que conté la ruta
    labelGreen.pack() #mostra una pantalla verda per indicar que el resultat es correcte
    pygame.mixer.init() #inicialitza el pygame tot lo relacionat amb el so
    correct = pygame.mixer.Sound("audio/correct.mp3") #creem l'objecte de so
    num = pygame.mixer.Sound(audio) #aqui igual pero amb la ruta pasada segons el numero correcte
    correct.play() #executem el so
    num.play()
    pantalla.after(500, hideGreen) #als 500ms executem la funció que treu la pantalla verda
    

def hideGreen():
    labelGreen.pack_forget() #pantalla verda fora

def end():
    pantalla.quit() #aquesta funció s'executa quan premem finalizar al boto vermell
    
# TKINTER 
thread = None
pantalla = Tk() #creem objecte
pantalla.title("SUMAVENTURA APREN A SUMAR INTERACTIVAMENT") #titol de la finestra
pantalla.geometry("1280x720") #dimensions de la finestra
pantalla.resizable(width=False, height=False) #fem que no es pogui moure

imatge = PhotoImage(file="img/fondo.png") #ruta del fons de pantalla
background = Label(image=imatge, borderwidth=0, highlightthickness=0) #parametres de configuració
background.place(x=0, y=0, relwidth=1, relheight=1) #on va colocada la imatge

imgIniciar = PhotoImage(file="img/iniciar.png")
iniciar = Button(pantalla, text="", image=imgIniciar, height="52", width="198", command=start, borderwidth=0, highlightthickness=0)
iniciar.place(x=530, y=635)

imgFinalizar = PhotoImage(file="img/finalizar.png")
finalizar = Button(pantalla, text="", image=imgFinalizar, height="52", width="198", command=end, borderwidth=0, highlightthickness=0 )

labelVideo = Label(pantalla, borderwidth=0, highlightthickness=0) #aquesta es la label on es mostra la webcam
labelVideo.place(x=296, y=116) 


labelSuma = Label(pantalla, foreground="white", font=('Helvetica', 42)) #label que mostra la suma, no es pot posar amb el fons transparent sense subrayar
labelSuma.place(x=95, y=355)

imgGreen = Image.new("RGBA", (1280, 720), (0, 255, 0, 128)) #pantalla verda, tot hi haverhi intentat que fos una mica transparent, no ha funcionat, está en RGBA i al canal alfa assignat el valor 128
imagenGreen = ImageTk.PhotoImage(imgGreen)
labelGreen = Label(pantalla, image=imagenGreen)

pantalla.mainloop() #manté la finestra en execució fins que es tenqui
