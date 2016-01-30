#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
    from Tkinter import  *
import socket
import argparse


parser = argparse.ArgumentParser(description='wipbox client')
parser.add_argument('--ip', nargs=1, help='adresse ip')
parser.add_argument('--port', type=int, help='numero de port')
args = parser.parse_args()

serveur_ip = ""
if(args.ip is not None):
    serveur_ip = args.ip
serveur_port = 1111
if(args.port is not None):
    serveur_port = args.port

print "adress " + serveur_ip + "[" + str(serveur_port) + "]" 


#Définition de la taille de l ecran et du stock
stock=10
limite=4
largeur =800
hauteur=600
taille=largeur/(stock+1)
niveau =0

#initialisation de la fenêtre
fenetre = Tk()
fenetre.title('K3X8')
fenetre.resizable(0,0)
try:
    canvas = Canvas(fenetre, width=largeur, height=hauteur, background='black')
    photo = PhotoImage(file="/Users/lemairec/wipbox/ntn.png")
    canvas.create_image(0, 0, anchor=NW, image=photo)
except:
    print "load img fail"
k=niveau
marqueur=canvas.create_oval(taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5,fill='yellow')

#dessin du tableau
i=0
for i in range(stock+1):
    if i<limite:
        couleur='green'
    elif i==limite:
        couleur='orange'
    elif i>limite:
        couleur='red'
    canvas.create_rectangle(taille*i,hauteur/2-taille/2,taille*(i+1),hauteur/2+taille/2, fill=couleur,outline='white')
    canvas.create_text(taille*(0.5+i),hauteur/2,justify=CENTER,text=i,font="arial 18 bold")
canvas.pack()


def send_niveau(niveau):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serveur_ip, serveur_port))
    s.send("niveau " + str(niveau))

#Détection du clic, de la position et positionnement d'un symbole
def touche(event):
    if hauteur/2-taille/2<event.y<hauteur/2+taille/2:
        # Capturer la case qui a été cliquée
        k=int(event.x/taille)
        print(k)
        canvas.coords(marqueur,taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5)
        niveau=k
        send_niveau(niveau)
canvas.bind("<Button-1>", touche)
fenetre.mainloop()
