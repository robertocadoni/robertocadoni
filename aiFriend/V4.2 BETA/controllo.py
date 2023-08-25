import openai
import re

OPENAI_API_KEY = 'YOUR_KEY_HERE'


def get_response_from_openai(prompt_text):
    print("Prompt inviato a OpenAI:", prompt_text)  # DEBUG
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt_text, max_tokens=150,
            temperature=0.5, frequency_penalty=0.5, presence_penalty=0.5)
        return response.choices[0].text
    except Exception as e:
        print("Errore durante la chiamata a OpenAI:", e)
        return None


class Controllo:
    def __init__(self, api_key, lista_azioni):
        self.api_key = api_key
        self.lista_azioni = lista_azioni
        openai.api_key = self.api_key

    def verifica_azione(self, frase_utente):
        prompt = (
            f"Considerando l'input '{frase_utente}', quale tra le seguenti azioni è più probabile che l'utente voglia eseguire? "
            f"Azioni possibili: {', '.join(self.lista_azioni)}. "
            f"Fornisci una stima accurata della probabilità per ciascuna azione o 'Nessuna azione' se nessuna corrisponde.")

        try:
            response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)
            risposta_grezza = response.choices[0].text.strip()
            #print("Risposta grezza da OpenAI:", risposta_grezza)  # DEBUG: Stampa l'output grezzo

            # Utilizza un'espressione regolare per estrarre le probabilità per ciascuna azione
            pattern = re.compile(r'(.*?):\s+(\d+)%')
            probabilita_azioni = {azione: int(prob) for azione, prob in pattern.findall(risposta_grezza)}

            azione_con_probabilita_piu_alta = max(probabilita_azioni, key=probabilita_azioni.get)
            print("Azione con probabilità più alta:", azione_con_probabilita_piu_alta,
                  probabilita_azioni[azione_con_probabilita_piu_alta])

            return azione_con_probabilita_piu_alta, probabilita_azioni[azione_con_probabilita_piu_alta]
        except Exception as e:
            print("Errore durante la chiamata a OpenAI:", e)
            return None, 0

