from __future__ import annotations

# Constantes com as patentes
PATENTE_GENERAL = 0
PATENTE_CORONEL = 1
PATENTE_CAPITAO = 2
PATENTE_SOLDADO = 3

class QG:
    def __init__(self):
        self.militares: list[Millitary] = []

    def adicionar_militar(self, militar: Millitary) -> None:
        self.militares.append(militar)
        if militar.superior_imediato is not None:
            militar.superior_imediato.add_subordinado(militar.patente, militar)

    def executar_dia(self) -> None:
        # Resolve conflitos de ordens de cima para baixo (patente 0 -> 1 -> 2 -> 3)
        for patente_atual in range(4):
            for militar in self.militares:
                if militar.patente != patente_atual:
                    continue
                for lista in (
                    militar.generais_subordinados,
                    militar.coroneis_subordinados,
                    militar.capitaes_subordinados,
                    militar.soldados_subordinados,
                ):
                    for sub in lista:
                        sub.order.priorize_order(militar.order)

        # Executa as ordens restantes de cada militar
        for patente_atual in range(4):
            for militar in self.militares:
                if militar.patente != patente_atual:
                    continue
                v = militar.order.variacoes
                dx, dy = v["pos_x"][0], v["pos_y"][0]
                if dx is not None or dy is not None:
                    militar.move(dx or 0.0, dy or 0.0)
                if v["prontidao"][0] is not None:
                    militar.set_prontidao(v["prontidao"][0])
                if v["saciedade"][0] is not None:
                    militar.set_saciedade(v["saciedade"][0])
                if v["poder_fogo"][0] is not None:
                    militar.set_poder_fogo(v["poder_fogo"][0])
                if v["poder_defesa"][0] is not None:
                    militar.set_poder_defesa(v["poder_defesa"][0])

                # Limpa a ordem apos o dia
                militar.set_order(Order(militar))

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

    def _todos_subordinados(self) -> list[Millitary]:
        return (
            self.generais_subordinados
            + self.coroneis_subordinados
            + self.capitaes_subordinados
            + self.soldados_subordinados
        )

    def _aplicar_fator(self, valor: float, patente: int, diferencial: float) -> float:
        return valor * diferencial if patente == PATENTE_SOLDADO else valor
        
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
        self.pos_x += self._aplicar_fator(x, self.patente, self.diferencial_menor)
        self.pos_y += self._aplicar_fator(y, self.patente, self.diferencial_menor)

        soma_x, soma_y = self.pos_x, self.pos_y
        subordinados = self._todos_subordinados()

        for sub in subordinados:
            sub.pos_x += self._aplicar_fator(x, sub.patente, sub.diferencial_menor)
            sub.pos_y += self._aplicar_fator(y, sub.patente, sub.diferencial_menor)
            soma_x += sub.pos_x
            soma_y += sub.pos_y

        total = 1 + len(subordinados)
        return (soma_x / total, soma_y / total)

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
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.prontidao = max(0.0, min(100.0, self.prontidao + delta))

        soma = self.prontidao
        subordinados = self._todos_subordinados()
        for sub in subordinados:
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.prontidao = max(0.0, min(100.0, sub.prontidao + d_sub))
            soma += sub.prontidao

        return soma / (1 + len(subordinados))
    
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
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.saciedade = max(0.0, min(100.0, self.saciedade + delta))

        soma = self.saciedade
        subordinados = self._todos_subordinados()
        for sub in subordinados:
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.saciedade = max(0.0, min(100.0, sub.saciedade + d_sub))
            soma += sub.saciedade

        return soma / (1 + len(subordinados))
    
    def set_poder_fogo(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao no poder de fogo dos subordinados.
        O poder de fogo resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao no poder de fogo.

        Returns:
            float: Poder de fogo medio das tropas.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.poder_fogo = max(0.0, min(100.0, self.poder_fogo + delta))

        soma = self.poder_fogo
        subordinados = self._todos_subordinados()
        for sub in subordinados:
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.poder_fogo = max(0.0, min(100.0, sub.poder_fogo + d_sub))
            soma += sub.poder_fogo

        return soma / (1 + len(subordinados))

    def set_poder_defesa(
        self,
        fator_variacao: float
    ) -> float:
        """ Aplica um fator de variacao no poder de defesa dos subordinados.
        O poder de defesa resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao no poder de defesa.

        Returns:
            float: Poder de defesa medio das tropas.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.poder_defesa = max(0.0, min(100.0, self.poder_defesa + delta))

        soma = self.poder_defesa
        subordinados = self._todos_subordinados()
        for sub in subordinados:
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.poder_defesa = max(0.0, min(100.0, sub.poder_defesa + d_sub))
            soma += sub.poder_defesa

        return soma / (1 + len(subordinados))

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
        if patente == PATENTE_GENERAL:
            self.generais_subordinados.append(subordinado)
        elif patente == PATENTE_CORONEL:
            self.coroneis_subordinados.append(subordinado)
        elif patente == PATENTE_CAPITAO:
            self.capitaes_subordinados.append(subordinado)
        elif patente == PATENTE_SOLDADO:
            self.soldados_subordinados.append(subordinado)

        if self.superior_imediato is not None:
            self.superior_imediato.add_subordinado(patente, subordinado)

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
        if patente == PATENTE_GENERAL and subordinado in self.generais_subordinados:
            self.generais_subordinados.remove(subordinado)
        elif patente == PATENTE_CORONEL and subordinado in self.coroneis_subordinados:
            self.coroneis_subordinados.remove(subordinado)
        elif patente == PATENTE_CAPITAO and subordinado in self.capitaes_subordinados:
            self.capitaes_subordinados.remove(subordinado)
        elif patente == PATENTE_SOLDADO and subordinado in self.soldados_subordinados:
            self.soldados_subordinados.remove(subordinado)

        if self.superior_imediato is not None:
            self.superior_imediato.drop_subordinado(patente, subordinado)
    
    def set_order(
        self, 
        order: Order
    ) -> None:
        self.order = order
    
    