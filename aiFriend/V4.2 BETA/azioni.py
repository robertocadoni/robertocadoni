import sys

lista_azioni = ["chiudi l'app", "richiesta informazioni", "calcolo matematico", "manda un'email"]

def chiudi_app():
    #conferma = input("Sei sicuro di voler chiudere l'applicazione? (y/n): ")
    #if conferma.lower() == 'y':
        print("Chiusura dell'applicazione...")
        sys.exit()
    #else:
        #print("Chiusura annullata.")

funzioni_corrispondenti = {
     "Chiudi l'app": chiudi_app,
}
