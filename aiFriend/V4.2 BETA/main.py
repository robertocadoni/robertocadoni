from speech_processing import process_speech
from controllo import get_response_from_openai, Controllo
from gtts import gTTS
import pygame
import time
from azioni import lista_azioni, funzioni_corrispondenti
from parametri import Parametri

# Creazione dell'istanza dei parametri
parametri = Parametri()
parametri.set_nome_interlocutore("Roberto")
parametri.set_posizione_geografica("Roma")

OPENAI_API_KEY = 'YOUR_KEY_HERE'
AUDIO_FILE1 = "risposta1.mp3"
AUDIO_FILE2 = "risposta2.mp3"
MAX_HISTORY_LENGTH = 500

def continue_conversation():
    pygame.mixer.init()
    continue_chat = True
    conversation_history = ""
    use_first_file = True
    first_prompt = True

    controllo = Controllo(api_key=OPENAI_API_KEY, lista_azioni=lista_azioni)

    while continue_chat:
        text = process_speech()
        if text is None:
            continue
        conversation_history += "Utente: " + text + "\n"

        azione, probabilita = controllo.verifica_azione(text)

        if azione == "Nessuna azione":
            print("Nessuna azione corrispondente rilevata.")
        elif probabilita >= 80:
            print(f"Esecuzione dell'azione: {azione} con probabilità {probabilita}%")
            funzione_corrispondente = funzioni_corrispondenti.get(azione)
            if funzione_corrispondente:
                funzione_corrispondente()
            else:
                print(f"Nessuna funzione corrispondente trovata per l'azione: {azione}")
        else:
            print(f"Azione non identificata o probabilità troppo bassa ({probabilita}%)")

        if len(conversation_history) > MAX_HISTORY_LENGTH:
            conversation_history = "...\n" + conversation_history[-MAX_HISTORY_LENGTH:]

        # Utilizzo dei parametri nella conversazione
        nome_interlocutore = parametri.get_nome_interlocutore()
        posizione_geografica = parametri.get_posizione_geografica()

        if first_prompt:
            # Preparazione del prompt con la cronologia della conversazione
            prompt_with_history = conversation_history
            prompt_with_history += f"\nNome dell'interlocutore: {nome_interlocutore if nome_interlocutore else 'Non specificato'}"
            prompt_with_history += f"\nPosizione geografica: {posizione_geografica if posizione_geografica else 'Non specificata'}"
            prompt_with_history += f"\nRispondi svolgendo il ruolo di assistente personale, sii professionale."
            first_prompt = False
        else:
            prompt_with_history = conversation_history

        #prompt_with_history += f"\nWARNING: I dati sopracitati vanno usati nella risposta solo se inerenti alla domanda"
        prompt_with_history += f"\nAssistente: "

        # Chiamata a OpenAI con il prompt
        risposta_gpt = get_response_from_openai(prompt_with_history)

        if risposta_gpt is None:
            print("Errore nella ricezione della risposta.")
            continue

        print("Risposta GPT:", risposta_gpt)
        conversation_history += "Assistente: " + risposta_gpt + "\n"

        try:
            tts = gTTS(text=risposta_gpt, lang='it', slow=False)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            current_audio_file = AUDIO_FILE1 if use_first_file else AUDIO_FILE2
            tts.save(current_audio_file)
            pygame.mixer.music.load(current_audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            use_first_file = not use_first_file
        except Exception as e:
            print("Errore durante la conversione o riproduzione dell'audio:", e)

if __name__ == "__main__":
    continue_conversation()
