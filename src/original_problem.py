from __future__ import annotations
from random import random
from copy import deepcopy

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

    def executar_dia(self) -> list:
        old_orders = []
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

                old_orders.append(deepcopy(militar))
                # Limpa a ordem apos o dia
                militar.set_order(Order.random_order(militar, probability=0.25))
        
        return old_orders

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

    @classmethod
    def random_order(cls, millitary: Millitary, probability: float=0.5) -> Order:
        order = cls(millitary)
        for each_col_fator_variacao in order.variacoes.keys():
            # Probabilidade de probability de alterar o campo nulo
            if random() <= probability:
                order.variacoes[each_col_fator_variacao][0] = 50 - random()*100
        
        return order


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
        self.order: Order      = Order.random_order(self, probability=0.25)
        
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

    def move(self, x: float, y: float) -> None:
        """ Move a si mesmo e todos os subordinados 
        na direcao do vetor (x, y).
        
        Args:
            x (float): Movimento no eixo x.
            y (float): Movimento no eixo y.
        """
        self.pos_x += self._aplicar_fator(x, self.patente, self.diferencial_menor)
        self.pos_y += self._aplicar_fator(y, self.patente, self.diferencial_menor)

        for sub in self._todos_subordinados():
            sub.pos_x += self._aplicar_fator(x, sub.patente, sub.diferencial_menor)
            sub.pos_y += self._aplicar_fator(y, sub.patente, sub.diferencial_menor)

    def set_prontidao(self, fator_variacao: float) -> None:
        """ Aplica um fator de variacao na prontidao de si e dos subordinados.
        A prontidao resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na prontidao.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.prontidao = max(0.0, min(100.0, self.prontidao + delta))

        for sub in self._todos_subordinados():
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.prontidao = max(0.0, min(100.0, sub.prontidao + d_sub))

    def set_saciedade(self, fator_variacao: float) -> None:
        """ Aplica um fator de variacao na saciedade de si e dos subordinados.
        A saciedade resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao na saciedade.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.saciedade = max(0.0, min(100.0, self.saciedade + delta))

        for sub in self._todos_subordinados():
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.saciedade = max(0.0, min(100.0, sub.saciedade + d_sub))

    def set_poder_fogo(self, fator_variacao: float) -> None:
        """ Aplica um fator de variacao no poder de fogo de si e dos subordinados.
        O poder de fogo resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao no poder de fogo.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.poder_fogo = max(0.0, min(100.0, self.poder_fogo + delta))

        for sub in self._todos_subordinados():
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.poder_fogo = max(0.0, min(100.0, sub.poder_fogo + d_sub))

    def set_poder_defesa(self, fator_variacao: float) -> None:
        """ Aplica um fator de variacao no poder de defesa de si e dos subordinados.
        O poder de defesa resultante de cada um eh limitada entre 0 e 100.

        Args:
            fator_variacao (float): Fator de variacao no poder de defesa.
        """
        delta = self._aplicar_fator(fator_variacao, self.patente, self.diferencial_menor)
        self.poder_defesa = max(0.0, min(100.0, self.poder_defesa + delta))

        for sub in self._todos_subordinados():
            d_sub = self._aplicar_fator(fator_variacao, sub.patente, sub.diferencial_menor)
            sub.poder_defesa = max(0.0, min(100.0, sub.poder_defesa + d_sub))

    def get_posicao(self) -> tuple[float, float]:
        """Retorna a posicao (x, y) do centroide de si e dos subordinados."""
        subordinados = self._todos_subordinados()
        soma_x = self.pos_x + sum(sub.pos_x for sub in subordinados)
        soma_y = self.pos_y + sum(sub.pos_y for sub in subordinados)
        total = 1 + len(subordinados)
        return (soma_x / total, soma_y / total)

    def get_prontidao(self) -> float:
        """Retorna a prontidao media de si e dos subordinados."""
        subordinados = self._todos_subordinados()
        soma = self.prontidao + sum(sub.prontidao for sub in subordinados)
        return soma / (1 + len(subordinados))

    def get_saciedade(self) -> float:
        """Retorna a saciedade media de si e dos subordinados."""
        subordinados = self._todos_subordinados()
        soma = self.saciedade + sum(sub.saciedade for sub in subordinados)
        return soma / (1 + len(subordinados))

    def get_poder_fogo(self) -> float:
        """Retorna o poder de fogo medio de si e dos subordinados."""
        subordinados = self._todos_subordinados()
        soma = self.poder_fogo + sum(sub.poder_fogo for sub in subordinados)
        return soma / (1 + len(subordinados))

    def get_poder_defesa(self) -> float:
        """Retorna o poder de defesa medio de si e dos subordinados."""
        subordinados = self._todos_subordinados()
        soma = self.poder_defesa + sum(sub.poder_defesa for sub in subordinados)
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
    


def print_arvore_ordens(militares: list[Millitary]) -> None:
    conjunto_militares = set(militares)
    filhos: dict[Millitary | None, list[Millitary]] = {}

    for militar in militares:
        superior = militar.superior_imediato
        chave_pai = superior if superior in conjunto_militares else None
        filhos.setdefault(chave_pai, []).append(militar)

    def _formatar_variacoes(ordem: Order) -> str:
        itens = [
            f"{aspecto} = {valor:.2f}" if isinstance(valor, float) else f"{aspecto} = {valor}"
            for aspecto, (valor, _) in ordem.variacoes.items()
            if valor is not None
        ]
        return "{" + ", ".join(itens) + "}"

    def _print_no(militar: Millitary, prefixo: str = "", eh_raiz: bool = True, eh_ultimo: bool = True) -> None:
        texto = f"{militar.patente} {_formatar_variacoes(militar.order)}"

        if eh_raiz:
            print(texto)
            novo_prefixo = ""
        else:
            conector = "└───── " if eh_ultimo else "├───── "
            print(f"{prefixo}{conector}{texto}")
            novo_prefixo = prefixo + ("       " if eh_ultimo else "│      ")

        subordinados = filhos.get(militar, [])
        for i, sub in enumerate(subordinados):
            _print_no(
                sub,
                prefixo=novo_prefixo,
                eh_raiz=False,
                eh_ultimo=(i == len(subordinados) - 1),
            )

    for raiz in filhos.get(None, []):
        _print_no(raiz)