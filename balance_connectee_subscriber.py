#********************************************************************
#       IL FAUT CLIQUER SUR LE NOM DE L'UTILISATEUR POUR RECEVOIR
#       LA COMMANDE DE CET UTILISATEUR FAITE SUR L'AUTRE PC

#********************************************************************


from tkinter import * #importe Tkinter 
from tkinter.messagebox import * #affiche fenetres d'information
import csv #pour récupérer fichier prix_par_kilo
from tkinter import ttk #pour Treeview (récap)
import paho.mqtt.client as mqtt
import struct

fenetre = Tk() #création de la fenetre racine de l'interface
fenetre.configure(bg="navajo white")#fond de la fenetre en noir
fenetre.geometry('1900x1000')#taille de la fenetre
fenetre.title("Balance connectée") #on nomme la fenetre

#création de variables globales des variables globales
prix = 0
article2 = 0
fige_poids = 0
prix_tot_Nathan=0
prix_tot_Gabriel=0
prix_au_kg_aff = 0
utilisateur2 = 0
val_poids = 1
#***************scrollbar du treeview (récapitulatif)
scrollbar = Scrollbar(fenetre)
scrollbar.pack(side="right", fill="y")#on met le scrollbar à droite

#***************mise en place du treeview
tv = ttk.Treeview(fenetre,yscrollcommand=scrollbar.set,height=23)
tv['columns']=('Article', 'poids', 'prix_kg', 'prix')

#on défini les colonnes
tv.column('#0', width=0, stretch=NO)
tv.column('Article', anchor=CENTER, width=160)
tv.column('poids', anchor=CENTER, width=160)
tv.column('prix_kg', anchor=CENTER, width=160)
tv.column('prix', anchor=CENTER, width=160)

#on nomme les différentes colonnes du treeview
tv.heading('#0', text='', anchor=CENTER)
tv.heading('Article', text='Article', anchor=CENTER)
tv.heading('poids', text='Poids (kg)', anchor=CENTER)
tv.heading('prix_kg', text='prix par kilo (€/kg)', anchor=CENTER)
tv.heading('prix', text='Prix (€)', anchor=CENTER)
#**************fin du scrollbar du treeview (récapitulatif)

#affichages des carrés de bases du poids/prix et du prix
label_prix_kg = Label(fenetre,text='__.__€/kg',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
label_prix_kg.place(x=820,y=200)
label_prix = Label(fenetre,text='__.__€',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
label_prix.place(x=660,y=400)

#création de deux variables qui vont servir de compteur
i=0
j=0

#création de différents tableaux pour stocker toutes les valeurs que nous allons avoir
tab_prix = [i] *50 #définit taile du tableau
tab_article = [i]*50#définit taile du tableau
tab_poids = [i]*50#définit taile du tableau
tab_prix_kg = [i]*50#définit taile du tableau
tab_prix_Nathan = [j] *50 #définit taile du tableau
tab_article_Nathan = [j]*50#définit taile du tableau
tab_poids_Nathan = [j]*50#définit taile du tableau
tab_prix_kg_Nathan = [j]*50#définit taile du tableau
tab_prix_Gabriel = [i] *50 #définit taile du tableau
tab_article_Gabriel = [i]*50#définit taile du tableau
tab_poids_Gabriel = [i]*50#définit taile du tableau
tab_prix_kg_Gabriel = [i]*50#définit taile du tableau

                    #création des fonctions
def fonction_article(param_article):
    global prix
    global article2
    global fige_poids
    global poids_recap
    global i
    global j
    global tab_prix
    global prix_au_kg_aff
    if utilisateur2 == 0 :
        showwarning('','Veuillez choisir un utilisateur') #affiche un message d'erreur si on a pas choisi d'utilisateur
    if utilisateur2 != 0 :
        fige_poids = 1
        poids_recap = val_poids
        label = Label(fenetre,text= "                             ",font = ('System',20),bg="navajo white")#efface l'article d'avant
        label.place(x=800 , y = 50)
        label = Label(fenetre,text= str(param_article),bg="navajo white",fg="black",font = ('System',20))
        label.place(x=800 , y = 50) # on affiche l'article choisi à l'endroit voulu
        article2=param_article #pour pouvoir le sortir de la fonction
        # Extraction du prix/kilo dans le fichier CSV
        fichier_csv = open("prix_par_kilo.csv", "r")# on ouvre le fichier CSV
        try :
            lecteur_csv = csv.reader(fichier_csv, delimiter=",")
            for colonne in lecteur_csv : #on cherche le prix au kilo en fonction de l'article sélectionné dans le fichier CSV
                if param_article == colonne[0]:
                    prix_au_kilo = colonne[1]
                    prix_au_kilo = float(prix_au_kilo)
                    prix = prix_au_kilo*poids_recap # cacul du prix
                    prix = round(prix,2)# on met 2 chiffres après la virgule
                    prix_au_kg_aff = prix_au_kilo
                    label_prix_kg = Label(fenetre,text=str(prix_au_kilo)+'€/kg',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
                    label_prix_kg.place(x=820,y=200)#on affiche le prix au kilo à l'endroit désiré
                    label_prix = Label(fenetre,text=str(prix)+'€',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
                    label_prix.place(x=660,y=400)#on affiche le prix à l'endroit désiré    
        finally :
            fichier_csv.close()#on ferme le fichier csv
        return prix
        return article2
        return poids_recap
        return i
        return prix_au_kg_aff

def fonction_utilisateur(utilisateur):
    global utilisateur2
    global prix_tot_Nathan
    global prix_tot_Gabriel
    global tab_article_Nathan
    global tab_poids_Nathan
    global tab_prix_kg_Nathan
    global tab_prix_Nathan
    
    label_utilisateur = Label(fenetre,text= str(utilisateur),bg="black",fg="DeepSkyBlue2",font = ('System',20))
    label_utilisateur.place(x=1500 , y = 165)#on affiche l'utilisateur qui fait la commmande.
    utilisateur2 = utilisateur#on met l'utilisateur dans une seconde variable pour pouvoir retourner l'utilisateur en cours
    tv.delete(*tv.get_children())#efface le treeview si on prend un nouvel utilisateur
       
       #on place les différentes valeurs dans le treeview
    if utilisateur2 == 'Nathan' :
        label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
        label_prix_total.place(x=1520 , y = 865)
        for j in range(50):#comme les tableaux sont de maximum 50 éléments, on fait le "for" jusqu'à 50
            if tab_article_Nathan[j] != 0 :
                tv.insert(parent='', index=j, iid=j, text='', values=(str(tab_article_Nathan[j]),str(tab_poids_Nathan[j]),str(tab_prix_kg_Nathan[j]),str(tab_prix_Nathan[j])))# pour afficher ce qu'il faut dans les colonnes du treeview
    if utilisateur2 == 'Gabriel' :
        label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
        label_prix_total.place(x=1520 , y = 865)
        for i in range(50):#comme les tableaux sont de maximum 50 éléments, on fait le "for" jusqu'à 50
            if tab_article_Gabriel[i] != 0 :
                tv.insert(parent='', index=i, iid=i, text='', values=(str(tab_article_Gabriel[i]),str(tab_poids_Gabriel[i]),str(tab_prix_kg_Gabriel[i]),str(tab_prix_Gabriel[i])))# pour afficher ce qu'il faut dans les colonnes du treeview
    return utilisateur2

def fonction_Validation(Validation):
    global utilisateur2
    global prix_tot_Nathan
    global prix_tot_Gabriel
    global article2
    global prix
    global fige_poids
    global prix_au_kg_aff
    global i
    global j
    global tab_article_Nathan
    global tab_poids_Nathan
    global tab_prix_kg_Nathan
    global tab_prix_Nathan
    global tab_article_Gabriel
    global tab_poids_Gabriel
    global tab_prix_kg_Gabriel
    global tab_prix_Gabriel
    
    if Validation == 'Validé' :
        tab_prix[i] = prix
        tab_article[i] = article2
        tab_poids[i] = val_poids
        tab_prix_kg[i] = prix_au_kg_aff #on place nos différentes valeurs dans différents tableaux pour les conserver
        
        if utilisateur2 == 'Nathan' :
            prix_tot_Nathan = prix_tot_Nathan + prix
            prix_tot_Nathan = round(prix_tot_Nathan,2)
            tab_article_Nathan[j] = article2
            tab_poids_Nathan[j] = val_poids
            tab_prix_kg_Nathan[j] = prix_au_kg_aff
            tab_prix_Nathan[j] = prix
            if j<50 : # on peut avoir maximum 50 lignes de récapilatif
                tv.insert(parent='', index=j, iid=j, text='', values=(str(tab_article_Nathan[j]),str(tab_poids_Nathan[j]),str(tab_prix_kg_Nathan[j]),str(tab_prix_Nathan[j])))# pour afficher ce qu'il faut dans les colonnes du treeview
                j=j+1 # on indente le compteur
            label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865) # on place le prix total
                
        elif utilisateur2 == 'Gabriel' :
            prix_tot_Gabriel = prix_tot_Gabriel + prix
            prix_tot_Gabriel = round(prix_tot_Gabriel,2)
            tab_article_Gabriel[i] = article2
            tab_poids_Gabriel[i] = val_poids
            tab_prix_kg_Gabriel[i] = prix_au_kg_aff
            tab_prix_Gabriel[i] = prix
            if i<50 : # on peut avoir maximum 50 lignes de récapilatif
                tv.insert(parent='', index=i, iid=i, text='', values=(str(tab_article_Gabriel[i]),str(tab_poids_Gabriel[i]),str(tab_prix_kg_Gabriel[i]),str(tab_prix_Gabriel[i])))# pour afficher ce qu'il faut dans les colonnes du treeview
                i=i+1 # on indente le compteur
            label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865) # on place le prix total
    
    if Validation == 'Annulé' :#si on clique sur le bouton annulé, on supprime la dernière ligne actuelle du treeview 
        if utilisateur2 == 'Nathan' :
            tv.delete(j-1)# supprime la dernière ligne du treeview
            prix_tot_Nathan = prix_tot_Nathan - tab_prix_Nathan[j-1]
            prix_tot_Nathan = round(prix_tot_Nathan,2)
            tab_prix_Nathan[j-1] = 0
            tab_prix_kg_Nathan[j-1] = 0
            tab_poids_Nathan[j-1] = 0
            tab_article_Nathan[j-1] = 0#on remplace la case du tableau que l'on vient d'annulé par "0"
            j=j-1#on décrémente la valeur du compteur afin de readapter le compteur
            label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865) #On place le prix total
            if j < 0 : #si on clique trop de fois sur "annuler", j ne devient pas négatif -> pas de répercussions sur tab_prix[i]
                j=0
                
        elif utilisateur2 == 'Gabriel' :
            tv.delete(i-1)# supprime la dernière ligne du treeview
            prix_tot_Gabriel = prix_tot_Gabriel - tab_prix_Gabriel[i-1]
            prix_tot_Gabriel = round(prix_tot_Gabriel,2)#on arrondi à deux chiffres après la virgule
            tab_prix_Gabriel[i-1] = 0
            tab_prix_kg_Gabriel[i-1] = 0
            tab_poids_Gabriel[i-1] = 0
            tab_article_Gabriel[i-1] = 0#on remplace la case du tableau que l'on vient d'annulé par "0"
            i=i-1#on décrémente la valeur du compteur afin de readapter le compteur
            label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865) #On place le prix total
            if i < 0 : #si on clique trop de fois sur "annuler", i ne devient pas négatif -> pas de répercussions sur tab_prix[i]
                i=0
    return i
    return j
    return prix_tot_Nathan
    return prix_tot_Gabriel
    return tab_article_Nathan
    return tab_poids_Nathan
    return tab_prix_kg_Nathan
    return tab_prix_Nathan
    return tab_article_Gabriel
    return tab_poids_Gabriel
    return tab_prix_kg_Gabriel
    return tab_prix_Gabriel
    
                    # Création des boutons fruits
Bouton_pommes = Button(fenetre, text = 'Pommes',command=lambda: fonction_article('pommes'), fg= "chartreuse3", bg= "black", width=10, height=5, activeforeground="black", activebackground="chartreuse3",font = (20))
Bouton_litchis = Button(fenetre, text = 'Litchis',command=lambda: fonction_article('litchis'), fg= "pink", bg= "black", width=10, height=5, activeforeground="black", activebackground="pink",font = (20))
Bouton_clémentines = Button(fenetre, text = 'Clémentines',command=lambda: fonction_article('clémentines'), fg= "orange", bg= "black", width=10, height=5, activeforeground="black", activebackground="orange",font = (20))
Bouton_bananes = Button(fenetre, text = 'Bananes',command=lambda: fonction_article('bananes'), fg= "yellow2", bg= "black", width=10, height=5, activeforeground="black", activebackground="yellow2",font = (20))
Bouton_papayes = Button(fenetre, text = 'Papayes',command=lambda: fonction_article('papayes'), fg= "lime", bg= "black", width=10, height=5, activeforeground="black", activebackground="lime",font = (20))
Bouton_tomates = Button(fenetre, text = 'Tomates',command=lambda: fonction_article('tomates'), fg= "red3", bg= "black", width=10, height=5, activeforeground="black", activebackground="red3",font = (20))
Bouton_myrtilles = Button(fenetre, text = 'Myrtilles',command=lambda: fonction_article('myrtilles'), fg= "RoyalBlue3", bg= "black", width=10, height=5, activeforeground="black", activebackground="midnight blue",font = (20))
Bouton_figues = Button(fenetre, text = 'Figues',command=lambda: fonction_article('figues'), fg= "purple3", bg= "black", width=10, height=5, activeforeground="black", activebackground="DarkOrchid4",font = (20))
                   
                   # Création des boutons légumes
Bouton_champignons = Button(fenetre, text = 'Champignons',command=lambda: fonction_article('champignons'), fg= "NavajoWhite3", bg= "black", width=10, height=5, activeforeground="black", activebackground="NavajoWhite3",font = (20))
Bouton_carottes = Button(fenetre, text = 'Carottes',command=lambda: fonction_article('carottes'), fg= "DarkOrange1", bg= "black", width=10, height=5, activeforeground="black", activebackground="DarkOrange1",font = (20))
Bouton_poireaux = Button(fenetre, text = 'Poireaux',command=lambda: fonction_article('poireaux'), fg= "forest green", bg= "black", width=10, height=5, activeforeground="black", activebackground="forest green",font = (20))
Bouton_poivrons = Button(fenetre, text = 'Poivrons',command=lambda: fonction_article('poivrons'), fg= "red2", bg= "black", width=10, height=5, activeforeground="black", activebackground="red2",font = (20))
Bouton_radis= Button(fenetre, text = 'Radis',command=lambda: fonction_article('radis'), fg= "deep pink", bg= "black", width=10, height=5, activeforeground="black", activebackground="deep pink",font = (20))
Bouton_panais = Button(fenetre, text = 'Panais',command=lambda: fonction_article('panais'), fg= "navajo white", bg= "black", width=10, height=5, activeforeground="black", activebackground="navajo white",font = (20))
Bouton_choux_rouge = Button(fenetre, text = 'Choux Rouge',command=lambda: fonction_article('choux rouge'), fg= "magenta4", bg= "black", width=10, height=5, activeforeground="black", activebackground="magenta4",font = (20))
Bouton_courgettes = Button(fenetre, text = 'Courgettes',command=lambda: fonction_article('courgettes'), fg= "dark green", bg= "black", width=10, height=5, activeforeground="black", activebackground="dark green",font = (20))

Bouton_utilisateur_Nathan = Button(fenetre, text = 'Nathan',command=lambda: fonction_utilisateur('Nathan'), fg= "DeepSkyBlue2", bg= "black", width=10, height=5, activeforeground="black", activebackground="DeepSkyBlue2",font = (20))
Bouton_utilisateur_Gabriel = Button(fenetre, text = 'Gabriel',command=lambda: fonction_utilisateur('Gabriel'), fg= "DeepSkyBlue2", bg= "black", width=10, height=5, activeforeground="black", activebackground="DeepSkyBlue2",font = (20))

Bouton_Valider = Button(fenetre, text = 'Valider',command=lambda: fonction_Validation('Validé'), fg= "black", bg= "chartreuse2", width=10, height=5, activeforeground="black", activebackground="chartreuse3",font = (20))
Bouton_Annuler = Button(fenetre, text = 'Annuler',command=lambda: fonction_Validation('Annulé'), fg= "gold", bg= "red2", width=10, height=5, activeforeground="gold", activebackground="red3",font = (20))

                    #Positionnement des boutons
Bouton_bananes.place(x=10,y=40)
Bouton_clémentines.place(x=10,y=145)
Bouton_figues.place(x=10,y=250)
Bouton_litchis.place(x=10,y=355)
Bouton_myrtilles.place(x=10,y=460)
Bouton_papayes.place(x=10,y=565)
Bouton_pommes.place(x=10,y=670)
Bouton_tomates.place(x=10,y=775)

Bouton_carottes.place(x=170,y=40)
Bouton_champignons.place(x=170,y=145)
Bouton_choux_rouge.place(x=170,y=250)
Bouton_courgettes.place(x=170,y=355)
Bouton_panais.place(x=170,y=460)
Bouton_poireaux.place(x=170,y=565)
Bouton_poivrons.place(x=170,y=670)
Bouton_radis.place(x=170,y=775)

Bouton_utilisateur_Nathan.place(x=1675,y=5)
Bouton_utilisateur_Gabriel.place(x=1540,y=5)

Bouton_Valider.place(x=630,y=700)
Bouton_Annuler.place(x=830,y=700)

                    #création d'un label "poids"
Label_poids = Label(fenetre,text=str(val_poids) + ' Kg', fg ='red', bg ='white', width=15, height=3,font = ('System',20))
Label_poids.place(x=500,y=200)

                    #création label "fruits"
Label_fruits = Label(fenetre, text ="Fruits", bg ='navajo white', fg ='black',font = ('System',20))
Label_fruits.place(x=35,y=5)

                    #création label "légumes"
Label_legumes = Label(fenetre, text ="Légumes", bg ='navajo white', fg ='black',font = ('System',20))
Label_legumes.place(x=172,y=5)

                    #Création et positionnement des cadres textes
label_article = Label(fenetre,text="Articles en cours : ",bg="navajo white",fg="black" , font = ('System',20))
label_utilisateur = Label(fenetre,text="Utilisateur en cours : ",bg="black",fg="DeepSkyBlue2" , font = ('System',20))
label_recap = Label(fenetre,text="Récapitulatif de la commande",bg="navajo white" ,fg="black" ,width=30, height=2, font = ('System',20))
label_prix_tot = Label(fenetre,text="Prix total = ",bg="navajo white" ,fg="black" ,width=10, height=2, font = ('System',20))
label_article.place(x=800 , y = 5)
label_utilisateur.place(x=1500 , y = 120)
label_recap.place(x=1220 , y = 247)
label_prix_tot.place(x=1300 , y = 850)

tv.place(x=1160,y=350) # on place le treeview
scrollbar.config(command=tv.yview) # appel de la scrollbar

#******************************************mqtt***********************************************************************************************
#fonction pour se connecter à la Raspberry
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")# si rc=5 alors erreur de connexion
    client.subscribe("Balance_poids_prix")#on se connecte au sujet "Balance_poids_prix"

#création de 4 tableaux pour mise en forme des valeurs récupérées par mqtt
tab_article_mqtt = 50*[0]
tab_poids_mqtt = 50*[0]
tab_prix_kilo_mqtt = 50*[0]
tab_prix_mqtt = 50*[0]

compteur_mqtt=0 #création d'un compteur pour la fonction ci-dessous

#fonction pour décoder les messages reçus et les afficher comme il faut dans le récapitulatif
def on_message(client, userdata, msg):
    global j
    global i
    global prix_tot_Nathan
    global prix_tot_Gabriel
    message = struct.unpack('12sfff7s' ,msg.payload)#on convertit le message reçu en une liste de 4 éléments
    article_décodé = message[0].decode()#on décode l'article reçu
    article = article_décodé.rstrip('\x00')#on met en forme l'article (on enlève les espaces inutiles à la fin)
    poids = round(message[1],3)#on arrondit et passe en string le poids récupéré
    prix_kilo = round(message[2],2)#on arrondit et passe en string le prix au kilo récupéré
    prix = round(message[3],2)#on arrondit et passe en string le prix récupéré
    utilisateur_décodé = message[4].decode()#on décode l'article reçu
    utilisateur_mqtt = utilisateur_décodé.rstrip('\x00')#on met en forme l'article (on enlève les espaces inutiles à la fin)
    if utilisateur_mqtt == 'Nathan':
        tab_article_Nathan[j]=article
        tab_poids_Nathan[j]=poids
        tab_prix_kg_Nathan[j]=prix_kilo
        tab_prix_Nathan[j]=prix
        prix_tot_Nathan = prix_tot_Nathan + prix
        prix_tot_Nathan = round(prix_tot_Nathan, 2)
        j = j + 1 # compteur pour mettre les valeurs dans des tableaux

    if utilisateur_mqtt == 'Gabriel':
        tab_article_Gabriel[i]=article
        tab_poids_Gabriel[i]=poids
        tab_prix_kg_Gabriel[i]=prix_kilo
        tab_prix_Gabriel[i]=prix
        prix_tot_Gabriel = prix_tot_Gabriel + prix
        prix_tot_Gabriel = round(prix_tot_Gabriel, 2)#on arrondi à deux chiffres après la virgule
        i = i + 1 # compteur pour mettre les valeurs dans des tableaux

    return j
    return i
    return prix_tot_Nathan
    return prix_tot_Gabriel
    return compteur_mqtt
    return tab_article_mqtt
    return tab_prix_kilo_mqtt
    return tab_prix_mqtt
    return tab_poids_mqtt

client = mqtt.Client()
client.connect("148.60.45.70", 1883)# on se connecte à l'adresse IP indiquée(c'est celle de notre Raspberry)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()#boucle qui permet de faire fonctionner le protocole MQTT

fenetre.mainloop()# On démarre la boucle Tkinter, qui s'interompt si on ferme la fenêtre

#fin du programme...





