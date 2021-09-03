from threading import *
import threading
from time import *


fourchettes = [1]*5


class Philosophe:
    def __init__(self, nom,id):
        self.nom = nom
        self.id = id
        self.etat = "PENSER"
    def setEtat(self, etat):
        self.etat = etat

    def manger(self):
        print(f"{self.nom} a commencé à manger ....")
        sleep(2)
        print(f"{self.nom} a terminé de manger ...")

    def penser(self):
        print(f"{self.nom} est en train de penser ...")
        sleep(5)
        print(f"{self.nom} a faim ...")

        

def philosophe(p):
    global fourchettes
    print(f"{p.nom} s'est assit à la table ...")
    p.penser()
    while(True):
        if(fourchettes[p.id] == fourchettes[(p.id+1)%5] == 1):
            fourchettes[p.id] = 0
            fourchettes[(p.id+1)%5] = 0
            p.manger()
            fourchettes[p.id] = 1
            fourchettes[(p.id+1)%5] = 1
            break
        else:
            print(f"{p.nom} attend toujours")
            sleep(3)

        

#Les solutions du cours avec 5 philosophes


voltaire = Philosophe("Voltaire",4)
aristote = Philosophe("Aristote",3)
sartre = Philosophe("Sartre",2)
nietzsche = Philosophe("Nietzsche",1)
socrate = Philosophe("Socrate",0)

Philosophes = [socrate,nietzsche,sartre,aristote,voltaire]







### Debut de la première solution
def solution_naïve():
    global Philosophes
    threads = list()
    for p in Philosophes:
        pThread = Thread(target=philosophe,args=(p,))
        threads.append(pThread)
        pThread.start()
    # pour que le processus père attend les threads avant de continuer son execution
    for t in threads:
        t.join()
###Fin


### Debut de la deuxième solution
def philosophe4(p):
    global fourchettes
    print(f"{p.nom} s'est assit à la table ...")
    p.penser()
    while(True):
        if(fourchettes[p.id] == fourchettes[(p.id+1)%5] == 1):
            fourchettes[(p.id+1)%5] = 0
            fourchettes[p.id] = 0
            p.manger()
            fourchettes[p.id] = 1
            fourchettes[(p.id+1)%5] = 1
            break
        
        else:
            print(f"{p.nom} attend toujours")
            sleep(3)




def solution2():
    global Philosophes
    threads = list()
    for p in Philosophes:
        if(p.id == 4):
            pThread = Thread(target=philosophe4,args=(p,))
            threads.append(pThread)
            pThread.start()
        else:
            pThread = Thread(target=philosophe,args=(p,))
            threads.append(pThread)
            pThread.start()
        pThread.join()
    for t in threads:
        t.join()
###Fin





### Debut de la Troisième solution
chaise = 4
def philosophe_chaise(p):
    global fourchettes
    global chaise
    while(True):
        if(chaise > 0):
            chaise -= 1
            print(f"{p.nom} s'est assit à la table ...")
            p.penser()
            while(True):
                if(fourchettes[p.id] == fourchettes[(p.id+1)%5] == 1):
                    fourchettes[p.id] = 0
                    fourchettes[(p.id+1)%5] = 0
                    p.manger()
                    fourchettes[p.id] = 1
                    fourchettes[(p.id+1)%5] = 1
                    chaise += 1
                    break
                else:
                    print(f"{p.nom} attend toujours")
                    sleep(3)
            break


def solution3():
    global Philosophes
    threads = list()
    for p in Philosophes:
        
        pThread = Thread(target=philosophe_chaise,args=(p,))
        threads.append(pThread)
        pThread.start()
        
    for t in threads:
        t.join()
###Fin




### Debut de la Quatrième solution
sema_philo = [0]*5
mutex = 1


def philosophe_etat(p):
    p.setEtat("MANGE")
    p.manger()
                
               

def test_manger(p, threads):
    global Philosophes
    global sema_philo
    global mutex
    if(Philosophes[(p.id+1)%5].etat != "MANGE" and Philosophes[(p.id-1)%5].etat != "MANGE" and p.etat == "A FAIM"):
        #Prend les fourchettes et 
        threads[p.id].start()
        sema_philo[p.id] = 1
        mutex += 1

        #Poser les fourchettes
        if(mutex == 1):
            mutex -= 1
            p.setEtat("PENSER")
            test_manger(Philosophes[(p.id+1)%5], threads)
            test_manger(Philosophes[(p.id-1)%5], threads)
            mutex += 1

    elif(p.etat == "A FAIM"):
        print(f"{p.nom} est toujours en attente !! ")

def solution4():
    global mutex
    global Philosophes
    global sema_philo
    threads = list()
    for p in Philosophes:
        print(f"{p.nom} s'est assit à la table ...")
        pThread = Thread(target=philosophe_etat,args=(p,))
        threads.append(pThread)
    while(sema_philo.count(0) > 0):
        for p in Philosophes:
            if(mutex == 1):
                mutex -= 1
                p.penser()
                p.setEtat("A FAIM")
                test_manger(p, threads)
                
            
        for t in threads:
            t.join()


### Fin




def menu():
    print("1..... Solution Naïve")
    print("2..... Solution 2")
    print("3..... Solution 3")
    print("4..... Solution 4")
    print("5..... Quitter")


def main():
    print("!!! Bienvenu au diner des philosophes !!!")
    choice = 0
    while(choice != 5):
        menu()
        choice = int(input("> "))
        if(choice == 1): 
            solution_naïve()
        elif(choice == 2):
            solution2()
        elif(choice == 3):
            solution3()
        elif(choice == 4):
            solution4()
        elif(choice == 5):
            print("Au revoir !!!")
        else:
            print("Veuillez saisir un choix valide")
        if(choice != 5): print("Processus terminer !!!!")
    
if __name__ == '__main__':
    
    main()
