class QG:
    pass

class Order:
    def __init__(
        self, 
        millitary: Millitary,
        pos_x: float=None,
        pos_y: float=None,
        prontidao: float=None,
        saciedade: float=None,
        poder_fogo: float=None,
        poder_defesa: float=None,
    ):
        patente   = millitary.patente
        self.variacoes = {
            "pos_x": [pos_x, patente],
            "pos_y": [pos_y, patente],
            "prontidao": [prontidao, patente],
            "saciedade": [saciedade, patente],
            "poder_fogo": [poder_fogo, patente],
            "poder_defesa": [poder_defesa, patente],
        }
    
    def priorize_order(
        self,
        new_order: Order
    ) -> None:
        # Se a ordem prioritaria altera um aspecto que tambem esta na ordem atual, remove a 
        # alteracao da ordem atual mantendo somente na ordem prioritaria para evitar duplicacao
        for each_aspecto, (novo_valor, nova_patente) in new_order.variacoes.items():
            if novo_valor is None:
                continue
            
            valor, patente = self.variacoes.get(each_aspecto, [None, -1]) # -1 para ignorar aspectos fora dos previstos
            if (valor is None) or (patente > nova_patente):
                self.variacoes[each_aspecto] = [None, nova_patente]



class Millitary:
    def __init__(
        self,
        patente: int, 
        pos_x: float,
        pos_y: float,
        prontidao: float,
        saciedade: float,
        poder_fogo: float,
        poder_defesa: float,
        diferencial_menor: float,
        superior_imediato: Millitary
    ):
        self.patente      = patente
        self.pos_x        = pos_x
        self.pos_y        = pos_y
        self.prontidao    = prontidao
        self.saciedade    = saciedade
        self.poder_fogo   = poder_fogo
        self.poder_defesa = poder_defesa
        
        self.diferencial_menor = diferencial_menor
        self.superior_imediato = superior_imediato
        self.order: Order      = Order(self)
        
        self.generais_subordinados = []
        self.coroneis_subordinados = []
        self.capitaes_subordinados = []
        self.soldados_subordinados = []
        
    def move(
        self,
        x: float,
        y: float
    ) -> tuple[float, float]:
        """ Move a si mesmo e todos os subordinados na direcao
        do vetor (x, y).
        Agrega as posicoes de todos os subordinados, obtendo e
        retornando o centroide ao final.

        Args:
            x (float): Movimento no eixo x.
            y (float): Movimento no eixo y.

        Returns:
            tuple[float, float]: Posicao (x, y) do centroide das tropas.
        """
        pass

    def set_prontidao(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao na prontidao dos subordinados.
        A prontidao resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na prontidao.

        Returns:
            float: Prontidao media das tropas.
        """
        pass
    
    def set_saciedade(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao na saciedade dos subordinados.
        A saciedade resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na saciedade.

        Returns:
            float: Saciedade media das tropas.
        """
        pass
    
    def set_poder_fogo(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao na poder de fogo dos subordinados.
        A poder de fogo resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na poder de fogo.

        Returns:
            float: Poder de fogo medio das tropas.
        """
        pass

    def set_poder_defesa(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao na poder de defesa dos subordinados.
        A poder de defesa resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na poder de defesa.

        Returns:
            float: Poder de defesa medio das tropas.
        """
        pass

    def add_subordinado(
        self, 
        patente: int, 
        subordinado: Millitary
    ) -> None:
        """ Adiciona um novo subordinado na lista corresponte a sua patente.
        Passa recursivamente sobre os superiores imediatos do militar atual, 
        adicionando o subordinado as suas listas.

        Args:
            patente (int): Patente do novo subordinado.
            subordinado (Millitary): Objeto do novo subordinado.
        """
        pass

    def drop_subordinado(
        self, 
        patente: int, 
        subordinado: Millitary
    ) -> None:
        """ Remove um novo subordinado na lista corresponte a sua patente.
        Passa recursivamente sobre os superiores imediatos do militar atual, 
        removendo o subordinado as suas listas.

        Args:
            patente (int): Patente do novo subordinado.
            subordinado (Millitary): Objeto do novo subordinado.
        """
        pass
    
    def set_order(
        self, 
        order: Order
    ) -> None:
        self.order = order
    
    
    