from gpiozero import MCP3002 #importe librairie can de la librairie gpio
from tkinter import * #importe Tkinter 
from tkinter.messagebox import * #affiche fenetres d'information
import csv #pour récupérer fichier prix_par_kilo
from tkinter import ttk #pour Treeview (récap)
import paho.mqtt.client as mqtt
import struct

fenetre = Tk() #création de la fenetre racine de l'interface
fenetre.configure(bg="navajo white")#fond de la fenetre en couleur "crème"
fenetre.geometry('1900x1000')#taille de la fenetre
fenetre.title("Balance connectée") #titre de la fenetre
adc = MCP3002(channel=0)#déclaration du can
val_poids = StringVar()#le poids sera une chaîne de caractères variable

#Création des variables globales
prix = 0
article2 = 0
fige_poids = 0
prix_tot_Nathan=0
prix_tot_Gabriel=0
prix_au_kg_aff = 0
utilisateur2 = 0

#barre de défilement du récapitulatif
scrollbar = Scrollbar(fenetre)
scrollbar.pack(side="right", fill="y")

#Initialisation du récapitulatif
tv = ttk.Treeview(fenetre,yscrollcommand=scrollbar.set,height=23)
#déclaration des différentes colonnes
tv['columns']=('Article', 'poids', 'prix_kg', 'prix')
tv.column('#0', width=0, stretch=NO)
tv.column('Article', anchor=CENTER, width=160)
tv.column('poids', anchor=CENTER, width=160)
tv.column('prix_kg', anchor=CENTER, width=160)
tv.column('prix', anchor=CENTER, width=160)
#déclaration des titres des différentes colonnes
tv.heading('#0', text='', anchor=CENTER)
tv.heading('Article', text='Article', anchor=CENTER)
tv.heading('poids', text='Poids (kg)', anchor=CENTER)
tv.heading('prix_kg', text='prix par kilo (€/kg)', anchor=CENTER)
tv.heading('prix', text='Prix (€)', anchor=CENTER)

#affichages des carrés de bases du prix/kg et du prix
label_prix_kg = Label(fenetre,text='__.__€/kg',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
label_prix_kg.place(x=820,y=200)
label_prix = Label(fenetre,text='__.__€',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
label_prix.place(x=660,y=400)

#Création des tableaux où on stocke nos différentes valeurs
i=0
j=0
tab_prix = [0]*50
tab_poids = [0]*50
tab_article = [0]*50
tab_prix_kg = [0]*50
tab_prix_Nathan =  [0]*50
tab_prix_Gabriel = [0]*50
tab_poids_Nathan =  [0]*50
tab_poids_Gabriel = [0]*50
tab_article_Nathan = [0]*50
tab_article_Gabriel =[0]*50
tab_prix_kg_Nathan =  [0]*50
tab_prix_kg_Gabriel = [0]*50

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
        showwarning('','Veuillez choisir un utilisateur')
    if utilisateur2 != 0 :
        fige_poids = 1 #on stoppe le poids le temps de la manipulation
        poids_recap = val_poids
        label = Label(fenetre,text= "                             ",font = ('System',20),bg="navajo white")#on "efface" l'ancien article sélectionné
        label.place(x=800 , y=50)
        label = Label(fenetre,text= str(param_article),bg="navajo white",fg="black",font = ('System',20))#on dit quel article est sélectionné
        label.place(x=800 , y = 50)
        article2=param_article #pour pouvoir le sortir de la fonction
        
        #Extraction du prix/kilo dans le fichier CSV
        fichier_csv = open("prix_par_kilo.csv", "r")
        try :
            lecteur_csv = csv.reader(fichier_csv, delimiter=",")
            for colonne in lecteur_csv :
                if param_article == colonne[0]:
                    prix_au_kilo = float(colonne[1])
                    prix = prix_au_kilo*poids_recap # cacul du prix
                    prix = round(prix,2)# on affiche  2 chiffres après la virgule
                    prix_au_kg_aff = prix_au_kilo
                    label_prix_kg = Label(fenetre,text=str(prix_au_kilo)+'€/kg',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
                    label_prix_kg.place(x=820,y=200)
                    label_prix = Label(fenetre,text=str(prix)+'€',fg ='red', bg ='white', width=15, height=3,font = ('System',20))
                    label_prix.place(x=660,y=400)
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
    global tab_article_Gabriel
    global tab_poids_Gabriel
    global tab_prix_kg_Gabriel
    global tab_prix_Gabriel
    
    label_utilisateur = Label(fenetre,text= str(utilisateur),bg="black",fg="DeepSkyBlue2",font = ('System',20))
    label_utilisateur.place(x=1500 , y = 165)
    utilisateur2 = utilisateur
    tv.delete(*tv.get_children())#On efface le récapitulatif
    
    #On affiche le prix total puis on place nos 4 variables (article, poids, prix au kg, prix) dans le tableau récaputilatif
    if utilisateur2 == 'Nathan' :
        label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
        label_prix_total.place(x=1520 , y = 865)
        for j in range(50):
            if tab_article_Nathan[j] != 0 :
                tv.insert(parent='', index=j, iid=j, text='', values=(str(tab_article_Nathan[j]),str(tab_poids_Nathan[j]),str(tab_prix_kg_Nathan[j]),str(tab_prix_Nathan[j])))#On affiche ce qu'il faut dans les colonnes du récapitulatif
    #On affiche le prix total puis on place nos 4 variables (article, poids, prix au kg, prix) dans le tableau récaputilatif
    if utilisateur2 == 'Gabriel' :
        label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
        label_prix_total.place(x=1520 , y = 865)
        for i in range(50):
            if tab_article_Gabriel[i] != 0 :
                tv.insert(parent='', index=i, iid=i, text='', values=(str(tab_article_Gabriel[i]),str(tab_poids_Gabriel[i]),str(tab_prix_kg_Gabriel[i]),str(tab_prix_Gabriel[i])))#On affiche ce qu'il faut dans les colonnes du récapitulatif
    return utilisateur2
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
    
def fonction_Validation(Validation):
    global utilisateur2
    global article2
    global prix
    global i
    global j
    global fige_poids
    global prix_tot_Nathan
    global prix_tot_Gabriel
    global prix_au_kg_aff
    global tab_prix
    global tab_article
    global tab_poids
    global tab_prix_kg
    global compteur
    global tab_article_Nathan
    global tab_poids_Nathan
    global tab_prix_kg_Nathan
    global tab_prix_Nathan
    global tab_article_Gabriel
    global tab_poids_Gabriel
    global tab_prix_kg_Gabriel
    global tab_prix_Gabriel
    
    if Validation == 'Validé' :
        #On place nos valeurs dans les tableaux appropriés
        tab_prix[i] = prix
        tab_article[i] = article2
        tab_poids[i] = val_poids
        tab_prix_kg[i] = prix_au_kg_aff
        #Protocole mqtt      
        article_encode = article2.encode()#l'encodage permet d'envoyer un string au correspondant
        utilisateur_encode = utilisateur2.encode()
        message_encode=struct.pack('12sfff7s', article_encode, val_poids, prix_au_kg_aff, prix, utilisateur_encode) #Permet d'envoyer article+poids... au correspondant
        client.publish('Balance_poids_prix', message_encode, qos=0, retain=False)#publit le message au topic
        
        if utilisateur2 == 'Nathan' :
            prix_tot_Nathan = prix_tot_Nathan + prix
            prix_tot_Nathan = round(prix_tot_Nathan,2)
            tab_article_Nathan[j] = tab_article[i]
            tab_poids_Nathan[j] = tab_poids[i]
            tab_prix_kg_Nathan[j] = tab_prix_kg[i]
            tab_prix_Nathan[j] = tab_prix[i]
            if j<50 : #On peut avoir maximum 50 lignes de récapilatif
                tv.insert(parent='', index=j, iid=j, text='', values=(str(tab_article_Nathan[j]),str(tab_poids_Nathan[j]),str(tab_prix_kg_Nathan[j]),str(tab_prix_Nathan[j])))#On affiche ce qu'il faut dans les colonnes du récapitulatif
                j=j+1 #On indente
            label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865)
            
        elif utilisateur2 == 'Gabriel' :
            prix_tot_Gabriel = prix_tot_Gabriel + prix
            prix_tot_Gabriel = round(prix_tot_Gabriel,2)
            tab_article_Gabriel[i] = tab_article[i]
            tab_poids_Gabriel[i] = tab_poids[i]
            tab_prix_kg_Gabriel[i] = tab_prix_kg[i]
            tab_prix_Gabriel[i] = tab_prix[i]
            if i<50 : #On peut avoir maximum 50 lignes de récapilatif
                tv.insert(parent='', index=i, iid=i, text='', values=(str(tab_article_Gabriel[i]),str(tab_poids_Gabriel[i]),str(tab_prix_kg_Gabriel[i]),str(tab_prix_Gabriel[i])))#On affiche ce qu'il faut dans les colonnes du récapitulatif
                i=i+1 #On indente
            label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865)
    
    if Validation == 'Annulé' :
        if utilisateur2 == 'Nathan' :
            tv.delete(j-1)#Supprime la dernière ligne du récapitulatif
            prix_tot_Nathan = prix_tot_Nathan - tab_prix_Nathan[j-1]
            prix_tot_Nathan = round(prix_tot_Nathan,2)
            #On réinitialise les dernières valeurs de nos 4 tableaux
            tab_prix_Nathan[j-1] = 0
            tab_prix_kg_Nathan[j-1] = 0
            tab_poids_Nathan[j-1] = 0
            tab_article_Nathan[j-1] = 0
            j=j-1
            label_prix_total = Label(fenetre,text= str(prix_tot_Nathan)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865)
            if j < 0 :#Le compteur d'une liste ne peut pas être négatif
                j=0
                
        elif utilisateur2 == 'Gabriel' :
            tv.delete(i-1)#Supprime la dernière ligne du récapitulatif
            prix_tot_Gabriel = prix_tot_Gabriel - tab_prix_Gabriel[i-1]
            prix_tot_Gabriel = round(prix_tot_Gabriel,2)
            #On réinitialise les dernières valeurs de nos 4 tableaux
            tab_prix_Gabriel[i-1] = 0
            tab_prix_kg_Gabriel[i-1] = 0
            tab_poids_Gabriel[i-1] = 0
            tab_article_Gabriel[i-1] = 0
            i=i-1
            label_prix_total = Label(fenetre,text= str(prix_tot_Gabriel)+' €         ',bg="navajo white",fg="black",font = ('System',20))
            label_prix_total.place(x=1520 , y = 865)
            if i < 0 :#Le compteur d'une liste ne peut pas être négatif
                i=0

    fige_poids = 0#Le poids pourra varier une fois la manipulation effectuée
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

def UpdateEverySecond():#Fonction pour actualiser le poids récupéré
    global val_poids
    global fige_poids
    if fige_poids == 0 : #On actualise en continu le poids
        val_poids=(adc.value-val_init)/0.17 #On divise par 0.17 (valeur au repos)
        val_poids=round(val_poids,3)
        if val_poids < 0 :#Le poids ne peut pas être négatif
            val_poids = 0
    
    Label_poids.config(text= str(val_poids) + ' Kg')
    fenetre.after(1000, UpdateEverySecond) #Actualisation de la fonction toutes les secondes

def on_connect(client, userdata, flags, rc):#Vérifie connection pour mqtt
    print(f"Connected with result code {rc}")#Code rc=0 : conection réussie ; sinon connection échouée

client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883)#On se connecte au réseau local
client.loop_start() #Début de la boucle MQTT

#Mise du tare
val_init=adc.value
val_poids.set(val_init)

#Création des boutons fruits
Bouton_pommes = Button(fenetre, text = 'Pommes',command=lambda: fonction_article('pommes'), fg= "chartreuse3", bg= "black", width=10, height=5, activeforeground="black", activebackground="chartreuse3",font = (20))
Bouton_litchis = Button(fenetre, text = 'Litchis',command=lambda: fonction_article('litchis'), fg= "pink", bg= "black", width=10, height=5, activeforeground="black", activebackground="pink",font = (20))
Bouton_clémentines = Button(fenetre, text = 'Clémentines',command=lambda: fonction_article('clémentines'), fg= "orange", bg= "black", width=10, height=5, activeforeground="black", activebackground="orange",font = (20))
Bouton_bananes = Button(fenetre, text = 'Bananes',command=lambda: fonction_article('bananes'), fg= "yellow2", bg= "black", width=10, height=5, activeforeground="black", activebackground="yellow2",font = (20))
Bouton_papayes = Button(fenetre, text = 'Papayes',command=lambda: fonction_article('papayes'), fg= "lime", bg= "black", width=10, height=5, activeforeground="black", activebackground="lime",font = (20))
Bouton_tomates = Button(fenetre, text = 'Tomates',command=lambda: fonction_article('tomates'), fg= "red3", bg= "black", width=10, height=5, activeforeground="black", activebackground="red3",font = (20))
Bouton_myrtilles = Button(fenetre, text = 'Myrtilles',command=lambda: fonction_article('myrtilles'), fg= "RoyalBlue3", bg= "black", width=10, height=5, activeforeground="black", activebackground="midnight blue",font = (20))
Bouton_figues = Button(fenetre, text = 'Figues',command=lambda: fonction_article('figues'), fg= "purple3", bg= "black", width=10, height=5, activeforeground="black", activebackground="DarkOrchid4",font = (20))

#Création des boutons légumes
Bouton_champignons = Button(fenetre, text = 'Champignons',command=lambda: fonction_article('champignons'), fg= "NavajoWhite3", bg= "black", width=10, height=5, activeforeground="black", activebackground="NavajoWhite3",font = (20))
Bouton_carottes = Button(fenetre, text = 'Carottes',command=lambda: fonction_article('carottes'), fg= "DarkOrange1", bg= "black", width=10, height=5, activeforeground="black", activebackground="DarkOrange1",font = (20))
Bouton_poireaux = Button(fenetre, text = 'Poireaux',command=lambda: fonction_article('poireaux'), fg= "forest green", bg= "black", width=10, height=5, activeforeground="black", activebackground="forest green",font = (20))
Bouton_poivrons = Button(fenetre, text = 'Poivrons',command=lambda: fonction_article('poivrons'), fg= "red2", bg= "black", width=10, height=5, activeforeground="black", activebackground="red2",font = (20))
Bouton_radis= Button(fenetre, text = 'Radis',command=lambda: fonction_article('radis'), fg= "deep pink", bg= "black", width=10, height=5, activeforeground="black", activebackground="deep pink",font = (20))
Bouton_panais = Button(fenetre, text = 'Panais',command=lambda: fonction_article('panais'), fg= "navajo white", bg= "black", width=10, height=5, activeforeground="black", activebackground="navajo white",font = (20))
Bouton_choux_rouge = Button(fenetre, text = 'Choux Rouge',command=lambda: fonction_article('choux rouge'), fg= "magenta4", bg= "black", width=10, height=5, activeforeground="black", activebackground="magenta4",font = (20))
Bouton_courgettes = Button(fenetre, text = 'Courgettes',command=lambda: fonction_article('courgettes'), fg= "dark green", bg= "black", width=10, height=5, activeforeground="black", activebackground="dark green",font = (20))

#Création des boutons utilisateurs
Bouton_utilisateur_Nathan = Button(fenetre, text = 'Nathan',command=lambda: fonction_utilisateur('Nathan'), fg= "DeepSkyBlue2", bg= "black", width=10, height=5, activeforeground="black", activebackground="DeepSkyBlue2",font = (20))
Bouton_utilisateur_Gabriel = Button(fenetre, text = 'Gabriel',command=lambda: fonction_utilisateur('Gabriel'), fg= "DeepSkyBlue2", bg= "black", width=10, height=5, activeforeground="black", activebackground="DeepSkyBlue2",font = (20))

#Création des boutons de validation
Bouton_Valider = Button(fenetre, text = 'Valider',command=lambda: fonction_Validation('Validé'), fg= "black", bg= "chartreuse2", width=10, height=5, activeforeground="black", activebackground="chartreuse3",font = (20))
Bouton_Annuler = Button(fenetre, text = 'Annuler',command=lambda: fonction_Validation('Annulé'), fg= "gold", bg= "red2", width=10, height=5, activeforeground="gold", activebackground="red3",font = (20))

#Positionnement des boutons fruits
Bouton_bananes.place(x=10,y=40)
Bouton_clémentines.place(x=10,y=145)
Bouton_figues.place(x=10,y=250)
Bouton_litchis.place(x=10,y=355)
Bouton_myrtilles.place(x=10,y=460)
Bouton_papayes.place(x=10,y=565)
Bouton_pommes.place(x=10,y=670)
Bouton_tomates.place(x=10,y=775)

#Positionnement des boutons légumes
Bouton_carottes.place(x=170,y=40)
Bouton_champignons.place(x=170,y=145)
Bouton_choux_rouge.place(x=170,y=250)
Bouton_courgettes.place(x=170,y=355)
Bouton_panais.place(x=170,y=460)
Bouton_poireaux.place(x=170,y=565)
Bouton_poivrons.place(x=170,y=670)
Bouton_radis.place(x=170,y=775)

#Positionnement des boutons utilisateurs
Bouton_utilisateur_Nathan.place(x=1675,y=5)
Bouton_utilisateur_Gabriel.place(x=1540,y=5)

#Positionnement des boutons de validation
Bouton_Valider.place(x=630,y=700)
Bouton_Annuler.place(x=830,y=700)

#Création des cadres de texte
label_article = Label(fenetre,text="Articles en cours : ",bg="navajo white",fg="black" , font = ('System',20))
label_utilisateur = Label(fenetre,text="Utilisateur en cours : ",bg="black",fg="DeepSkyBlue2" , font = ('System',20))
label_recap = Label(fenetre,text="Récapitulatif de la commande",bg="navajo white" ,fg="black" ,width=30, height=2, font = ('System',20))
label_prix_tot = Label(fenetre,text="Prix total = ",bg="navajo white" ,fg="black" ,width=10, height=2, font = ('System',20))

#Positionnement des cadres de texte
label_article.place(x=800 , y=5)
label_utilisateur.place(x=1500 , y=120)
label_recap.place(x=1220 , y=247)
label_prix_tot.place(x=1300 , y=850)

#Création label "poids"
Label_poids = Label(fenetre, fg ='red', bg ='white', width=15, height=3,font = ('System',20))
Label_poids.place(x=500,y=200)

#Création label "fruits"
Label_fruits = Label(fenetre, text ="Fruits", bg ='navajo white', fg ='black',font = ('System',20))
Label_fruits.place(x=35,y=5)

#Création label "légumes"
Label_legumes = Label(fenetre, text ="Légumes", bg ='navajo white', fg ='black',font = ('System',20))
Label_legumes.place(x=172,y=5)

tv.place(x=1160,y=350) #On place le treeview (récapitulatif)
scrollbar.config(command=tv.yview) #Appel de la scrollbar (barre de défilement)

UpdateEverySecond() #Actualise la valeur du poids

fenetre.mainloop()#On démarre la boucle Tkinter