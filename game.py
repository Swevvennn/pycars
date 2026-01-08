import pygame

class Pycars:
    """Road to beyond"""    
    #---Ecran d'affichage du jeu
    w = 1800
    h = 1000
    screen = pygame.display.set_mode((w,h))
    def __init__(self):
        """Initialisation des éléments du jeu"""
        #---Listes des sprites

        #############################################################################
        ##### Les sprites sont neutralisés pour transporter moins de fichiers.  #####
        ##### Certaines variables, attributs et/ou méthodes sont donc inutiles. #####
        ##### Des éléments ne sont pas neutralisés même si ils sont inutiles    #####
        ##### Pour cette version du jeu.                                        #####
        #############################################################################

        ####################### Erreur OS ###########################
        ##### Sur des OS de types MACOS/LINUX, changez les "\" en "/" #####
        ##### Sur des OS de types WINDOWS, changez les "/" en "\"  #####
        #############################################################

        self.spriteL =   [pygame.image.load('img/spriteLeft-1.png').convert_alpha(),
                          pygame.image.load('img/spriteLeft-2.png').convert_alpha()]
        self.spriteP =   [pygame.image.load('img/spritePlayer-1.png').convert_alpha(),
                          pygame.image.load('img/spritePlayer-2.png').convert_alpha()]
        self.spriteR =   [pygame.image.load('img/spriteRight-1.png').convert_alpha(),
                          pygame.image.load('img/spriteRight-2.png').convert_alpha()]

        #---Elements visibles
        self.player = Voiture('red',Vecteur(Pycars.w//8,Pycars.h//2+Pycars.h//24),Vecteur(0,0),0, 12,self.spriteP,(160,100))
        self.Route = Decor((50,50,50),Vecteur(0,Pycars.h//6),(Pycars.w,Pycars.h//3*2))
        self.Ligne = Decor('white',Vecteur(0,Pycars.h//2),(Pycars.w,10))
        self.Ldp = []
        for j in range(2):
            for i in range(10):
                t = Decor('white',Vecteur((Pycars.w//40)+(Pycars.w//10)*i,(Pycars.h//3)+((Pycars.h//3)*j)),(Pycars.w//20,10))
                self.Ldp.append(t)
        self.LDV = [Traffic(Vecteur(-9,0),4000,self.spriteR,Vecteur(0,Pycars.h//2 + Pycars.h//6 + Pycars.h//24)), #Voie du bas-bas
                    Traffic(Vecteur(-6,0),10000,self.spriteR,Vecteur(0,Pycars.h//2 + Pycars.h//24)), #Voie du bas-haut
                    Traffic(Vecteur(-12,0),6000,self.spriteL,Vecteur(0,Pycars.h//2 - Pycars.h//3 + Pycars.h//24)), #Voie du haut-haut
                    Traffic(Vecteur(-15,0),14000,self.spriteL,Vecteur(0,Pycars.h//2- Pycars.h//6 + Pycars.h//24))] #Voie du haut-bas
        #---Elements pour le bon fonctionnement du jeu
        #Objet clock pour permettre un déplacement fluide du joueur (cf. ligne 141)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.acceleration = 1
        #Mise à jour du meilleur score
        try:
            with open('score.txt','r') as f:
                self.best = f.read()
        except FileNotFoundError:
            with open('score.txt', 'w') as f:
                f.write("0")
                self.best = 0
        #Création des polices pour le texte
        self.Tfont = pygame.font.SysFont('ArialBlack', 100)
        #Création des variables pour le score et le menu
        self.mode = 0
        self.NG = 0
        self.last_score = 0
        self.s = 0
        #Création de variable de débug
        #self.nVoitures = 0
        pygame.mixer.music.load('music/home.mp3')

    def changer_mode(self,mode : int):
        """Change de mode"""
        if mode == 0:
            #---MàJ du score de la partie précédante
            self.last_score = self.score
            #---MàJ du meilleur score
            f = open('score.txt','r')
            if self.score > float(f.read()):
                self.best = self.score
                f.close()
                f = open('score.txt','w')
                f.write(str(self.score))
            f.close()
            #---Retire les voitures restante
            for V in self.LDV:
                while V.ajout != 0:
                    V.nouvelle_voiture()
                    #self.nVoitures+=1
                    #print("il y a",str(self.nVoitures),"voitures maintenant")
                while len(V.ldv)!=0:
                    V.retirer()
                    #self.nVoitures-=1
                    #print("il y a",str(self.nVoitures),"voitures maintenant")
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/home.mp3')
            pygame.mixer.music.play(-1, 0, 5000)
            self.mode = 0
        elif mode == 1:
            #print("Initialisation")
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/ride.mp3')
            pygame.display.set_caption('Pycars - Playing   Record : '+str(self.best))
            self.NG = pygame.time.get_ticks()
            self.LDV[0].ajouter(4)
            self.LDV[1].ajouter(2)
            self.LDV[2].ajouter(3)
            self.LDV[3].ajouter(1)
            self.player.pos = Vecteur(Pycars.w//8,Pycars.h//2+Pycars.h//24)
            pygame.mixer.music.play(-1, 0, 10000)
            #print("Starting")
            self.mode = 1
        self.Ldp = []
        for j in range(2):
            for i in range(10):
                t = Decor('white',Vecteur((Pycars.w//40)+(Pycars.w//10)*i,(Pycars.h//3)+((Pycars.h//3)*j)),(Pycars.w//20,10))
                self.Ldp.append(t)

    def run(self):
        """Fonctionnement du jeu"""
        if self.mode ==0:
            #---Remplissage de l'écran d'une couleur en RGB pour écraser la frame précédante
            Pycars.screen.fill((25,150,25))
            #---Affichage du fond du menu
            self.Route.trace()
            self.Ligne.trace()
            for e in self.Ldp:
                e.trace()
            #---Affichage des textes
            #Titre du jeu
            self.affichage_texte((Pycars.w / 2, 50), "PyCars", self.Tfont)
            #Score de la dernière partie
            self.affichage_texte((Pycars.w/4,200),"Last run : "+str(self.last_score))
            #Meilleur score
            self.affichage_texte((Pycars.w*3/4,200),"Best Score : "+str(self.best))
            #Comment lancer la partie
            self.affichage_texte((Pycars.w/2,750), "Press p to play")
            #---Changement du titre de la page
            pygame.display.set_caption('Pycars - Home menu')
            #---Détection du lancement de la partie
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                self.changer_mode(1)
            #---Rafraichissement de l'affichage
            pygame.display.flip()
        elif self.mode == 1:
            self.s+=1
            #---MàJ de l'affichage du décor
            #Supression de la frame précédent
            Pycars.screen.fill((25,150,25))
            #Affichage du décor
            self.Route.trace()
            self.Ligne.trace()
            #Défilement des pointilliers
            for e in self.Ldp:
                e.defile(self.acceleration)
                if e.pos.x == -e.tal[0]:
                    e.pos.x = Pycars.w
            #Animation du joueur
            self.player.avance(self.s)
            #---MàJ du score
            self.score = round((pygame.time.get_ticks() - self.NG)/500,1)
            self.acceleration = 0.5+(4.5/(1+1.005**(-(self.score-300))))
            #---Affichge des différents textes
            self.affichage_texte((Pycars.w/2,10),"Score : "+str(self.score))
            self.affichage_texte((Pycars.w/4,100),"Last run : "+str(self.last_score))
            self.affichage_texte((Pycars.w*3/4,100),"Best Score : "+str(self.best))
            #---Système de déplacement du joueur inspiré du tuto pygame
            dt = self.clock.tick(60) / 1000
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_z] or keys[pygame.K_UP]) and self.player.pos.y > Pycars.h//6:
                    self.player.pos.y -= 300*dt
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.player.pos.y < Pycars.h - Pycars.h//6 - Pycars.h//10:
                    self.player.pos.y += 300*dt
            #---Controle des voitures
            for voie in self.LDV:
                voie.defilement(self.s, self.acceleration)
                #Ajout de voitures
                if voie.ajout > 0 and pygame.time.get_ticks() - voie.last >= voie.cd:
                    voie.nouvelle_voiture()
                    #self.nVoitures+=1
                    #print("il y a",str(self.nVoitures),"voitures maintenant")
                #Test du contact
                if self.player.contact(voie):
                    #Retour au menu home et remise à zéro
                    self.changer_mode(0)
        #Rafraichissement du décor
        pygame.display.flip()

    def affichage_texte(self, pos : tuple[int,int], content : str, font = 0):
        if font == 0:
            font = pygame.font.SysFont('ArialBlack', 50)
        text = font.render(content,True,"white")
        text_pos = text.get_rect(centerx = pos[0], y = pos[1])
        Pycars.screen.blit(text,text_pos)

class Decor:
    """Classe pour tracer les éléments du décors en forme de rectangle"""
    def __init__(self,couleur : tuple[int,int,int] | str ,position : tuple[int,int] ,taille : tuple[int,int] = (180,100)):
        """Définit la couleur du rectagle, sa position et sa taille"""
        self.pos = position
        self.col = couleur
        self.tal = taille

    def trace(self):
        """Dessine l'élément voulu sur l'écran"""
        pygame.draw.rect(Pycars.screen,self.col,(self.pos.x,self.pos.y,self.tal[0],self.tal[1]))

    def defile(self, acceleration):
        """Déplace l'élément du décor voulu, vers la gauche"""

        ##### Utilisé seulement pour les pointillés #####
        
        self.pos.x -= (self.tal[0]//8)*acceleration
        self.trace()
        if self.pos.x+self.tal[0]<=0:
            self.pos.x = Pycars.w

class Vecteur:
    """vecteur de déplacement"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __str__(self):
        """Affiche les coordonnées d un vecteur comme en mathématique (2,5) par exemple"""
        return "("+str(self.x)+","+str(self.y)+")"
    
    def __mul__(self,val):
        """Multiplie les coordonnées d'un vecteur avec un entier et renvoie un vecteur"""
        return Vecteur(self.x*val,self.y*val)
    
    def __add__(self,v):
        """Ajoute les coordonnées de deux vecteurs et renvoie un vecteur"""
        return Vecteur(self.x+v.x,self.y+v.y)

class Anime:
    """Classe permettant de faire apparaitre une animation sur la hitbox des voitures"""
    def __init__(self, liste : list, scale:int):
        """Initialisation des variables pour enregistrer les différents éléments de l'animation et changer de sprite fluidement"""
        #---Liste de sprite - - - - - Voir constant.py en cas de problème
        self.liste = liste
        #---Echelle pour afficher le sprite correctement
        self.scale = scale
        #---Indice permettant de récupérer le bon sprite dans self.liste
        self.n = 0

    def set_image(self, sprite, width : int = 32, height : int = 32):
        """Mise en place du sprite à taille voulue"""

        ######## Fonction inspirée du tuto youtube de "Coding With Russ" #########

        #---Création de l'écran pour faire aparaitre la sprite
        image = pygame.Surface((width,height)).convert_alpha()
        #---Mise en place d'un fond vert pour séparer le fond de l'écran avec le sprite
        image.fill('green')
        #---Affichage du sprite ur l'écran
        image.blit(sprite, (0,0))
        #---Mise à l'échelle de l'écran pour mettre à l'échelle le sprite
        image = pygame.transform.scale(image,(width*self.scale,height*self.scale))
        #---Soustraction de la couleur verte sur l'écran
        image.set_colorkey('green')
        #---Renvoi de l'écran avec le sprite à léchelle et sur fond transparent
        return image

    def animation(self, s : int, pos : object):
        """Changement de sprite pour une animation agréable avec s la variable qui controle le temps écoulé et pos la positoin de la voiture"""

        ##### Fonction initialement créée pour animer aussi le décor ######

        #---Test à intervalle régulière
        if s%(72//len(self.liste)) == 0:
            #---Changement de sprite
            self.n = (self.n+1)%len(self.liste)
        #---Affichage du sprite sur l'écran de jeu
        Pycars.screen.blit(self.set_image(self.liste[self.n]), (pos.x-8*self.scale,pos.y-10*self.scale))
    
class Voiture(Decor):
    """Classe des voitures"""
    def __init__(self,couleur,position,vitesse,cooldown,scale, liste = [],taille = (180,100)):
        Decor.__init__(self,couleur,position,taille)
        self.vit=vitesse
        self.cd=cooldown
        self.sprite = Anime(liste,scale)
        
    def __str__(self):
        """affiche les informations de la voiture"""
        return "Voiture à la vitesse "+str(self.vit)+" et aux coordonnées "+str(self.pos)
    
    def avance(self,s,acceleration = 1):
        """Déplace la voiture"""
        #---MàJ de la position
        self.pos = self.pos+self.vit*acceleration
        #self.trace()
        self.sprite.animation(s,self.pos)

    def hitbox(self,taille = (180,100)):
        """Renvoi une liste de tuple contenant les coordonnées de chaque point de la hitbox"""
        UL = (self.pos.x,self.pos.y)
        UR = (self.pos.x+taille[0],self.pos.y)
        DL = (self.pos.x,self.pos.y+taille[1])
        DR = (self.pos.x+taille[0],self.pos.y+taille[1])
        return [UL,UR,DL,DR]
    
    def contact(self,voie):
        """Test pour chaque voiture dans la voie si l'un des angles de la voitures et dans la hitbox de l'une d'entre elles"""
        
        ##### Utilisé uniquement pour self.player dans la classe pycars #####
        
        for v in voie.ldv:
            for i in range(4):
                if v.hitbox()[0][0] <= self.hitbox(self.tal)[i][0] and self.hitbox(self.tal)[i][0] <= v.hitbox()[3][0] and v.hitbox()[0][1] <= self.hitbox(self.tal)[i][1] and self.hitbox(self.tal)[i][1] <= v.hitbox()[3][1]:
                    return True
        return False
      

class Traffic:
    """Classe des voitures à éviter sur 1 voie"""
    i = 0
    def __init__(self,vitesse,cooldown,sprite,position = Vecteur(Pycars.w//2,Pycars.h//2)):
        #Liste des sprites des voitures de la voie
        self.sprite = sprite
        #liste de voitures
        self.ldv = []
        #Vitesse des voitures sur la voie
        self.vit = vitesse
        #Position de départ des voitures de la voie
        self.pos = position
        #Délai de réaparition entre 2 voitures, en ms
        self.cd = cooldown
        #Nombre de voiture restantes à ajouter à la fin du délai
        self.ajout = 0
        #Instant où la dernière voiture a été créée
        self.last = pygame.time.get_ticks()
        #Numéro de la voie pour séparer celles du haut de clles du bas
        self.i = Traffic.i
        Traffic.i+=1
        
    def __str__(self):
        """Affiche les voitures d'une voie"""
        t = "La classe Traffic"+str(self.voie)+" contient :"
        for v in self.ldv:
            t+='/n'
            t+=str(v)
        return t
        
    def ajouter(self,n):
        """Ajoute une voiture sur la voie"""
        self.ajout+=n

    def retirer(self):
        """Supprime une voiture de la voie"""
        self.ldv.pop(0)

    def defilement(self,s,acceleration):
        """Déplace les voitures et les fait réapparaitre"""
        for v in self.ldv:
            #Avance chaque voiture dans la voie
            v.avance(s,acceleration)
            #---Vérification si si a voiture n'est pas sortie de l'écran
            if v.pos.x+v.tal[0] <= 0:
                self.retirer()
                self.ajouter(1)
            elif v.pos.x-v.tal[0] >= Pycars.w:
                self.retirer()
                self.ajouter(1)

    def nouvelle_voiture(self):
        """Ajoute une nouvelle voiture à la liste de voitures"""
        self.last = pygame.time.get_ticks()
        #Créé une instance de la classe voiture
        v = Voiture('blue',Vecteur(Pycars.w,self.pos.y),self.vit,self.cd,12,self.sprite)
        #Ajoute la voiture à la liste de voiture
        self.ldv.append(v)
        self.ajout-=1

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
running = True

print("Made w/ heart by Swevvenn\nThanks for playing PyCars - Road to Beyond")

#---Création du jeu et de toute les variables nécessaires
J = Pycars()

#---Boucle de jeu
while running:
    #---Jeu en cours
    J.run()
    #---Fermeture de la fenêtre avec la croix
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#print("score",score)
#print("Closing window")
pygame.quit()