import speech_recognition as sr

def process_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascolto... Parla quando sei pronto.")
        while True:
            try:
                audio = recognizer.listen(source)  # Aumenta il timeout se necessario
                text = recognizer.recognize_google(audio, language='it-IT')
                if text:  # Se viene rilevato un input vocale
                    print("Hai detto:", text)
                    return text
            except sr.UnknownValueError:
                continue  # Continua ad ascoltare se non viene rilevato nulla di sensato
            except sr.RequestError:
                print("Impossibile ottenere i risultati; controlla la connessione Internet.")
                return None