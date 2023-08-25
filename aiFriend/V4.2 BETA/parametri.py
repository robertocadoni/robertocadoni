class Parametri:
    def __init__(self, nome_interlocutore=None, posizione_geografica=None):
        self.nome_interlocutore = nome_interlocutore
        self.posizione_geografica = posizione_geografica

    def set_nome_interlocutore(self, nome):
        self.nome_interlocutore = nome

    def set_posizione_geografica(self, posizione):
        self.posizione_geografica = posizione

    def get_nome_interlocutore(self):
        return self.nome_interlocutore

    def get_posizione_geografica(self):
        return self.posizione_geografica
