class proceso(object):

    def __init__(self, id, rafaga, llegada, color):
        self.id = id
        self.rafaga = rafaga
        self.llegada = llegada
        self.rafagatmp = rafaga
        self.espera = 0
        self.retorno = 0
        self.finalizacion = 0
        self.color = color


