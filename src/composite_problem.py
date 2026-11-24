from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator


PATENTE_GENERAL = 0
PATENTE_CORONEL = 1
PATENTE_CAPITAO = 2
PATENTE_SOLDADO = 3

ATRIBUTOS_LIMITADOS = {
    "prontidao",
    "saciedade",
    "poder_fogo",
    "poder_defesa",
}


class ComponenteMilitar(ABC):
    """Interface comum para um militar isolado ou para uma unidade hierárquica."""

    @abstractmethod
    def mover(self, x: float, y: float) -> tuple[float, float]:
        """Move o componente e retorna o centroide da unidade."""

    @abstractmethod
    def alterar_atributo(self, atributo: str, variacao: float) -> float:
        """Altera um atributo do componente e de seus subordinados."""


class Ordem:
    def __init__(
        self,
        militar: Militar,
        pos_x: float | None = None,
        pos_y: float | None = None,
        prontidao: float | None = None,
        saciedade: float | None = None,
        poder_fogo: float | None = None,
        poder_defesa: float | None = None,
    ) -> None:
        patente = militar.patente
        self.variacoes: dict[str, tuple[float | None, int]] = {
            "pos_x": (pos_x, patente),
            "pos_y": (pos_y, patente),
            "prontidao": (prontidao, patente),
            "saciedade": (saciedade, patente),
            "poder_fogo": (poder_fogo, patente),
            "poder_defesa": (poder_defesa, patente),
        }

    def priorizar_ordem(self, nova_ordem: Ordem) -> None:
        for atributo, (novo_valor, nova_patente) in nova_ordem.variacoes.items():
            if novo_valor is None:
                continue

            valor, patente = self.variacoes[atributo]
            if valor is None or patente > nova_patente:
                self.variacoes[atributo] = (None, nova_patente)


class Militar(ComponenteMilitar):
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
        superior_imediato: Militar | None = None,
    ) -> None:
        self.patente = patente
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.prontidao = prontidao
        self.saciedade = saciedade
        self.poder_fogo = poder_fogo
        self.poder_defesa = poder_defesa
        self.diferencial_menor = diferencial_menor
        self.superior_imediato = superior_imediato
        self.subordinados: list[Militar] = []
        self.order = Ordem(self)

    def adicionar_subordinado(self, subordinado: Militar) -> None:
        if subordinado is self or subordinado in self.subordinados:
            raise ValueError("O subordinado já está nesta unidade ou é o próprio militar.")
        if self in subordinado.descendentes():
            raise ValueError("A hierarquia não pode conter ciclos.")
        if subordinado.superior_imediato not in (None, self):
            raise ValueError("O militar já possui outro superior imediato.")
        subordinado.superior_imediato = self
        self.subordinados.append(subordinado)

    def remover_subordinado(self, subordinado: Militar) -> None:
        self.subordinados.remove(subordinado)
        subordinado.superior_imediato = None

    def descendentes(self) -> Iterator[Militar]:
        for subordinado in self.subordinados:
            yield subordinado
            yield from subordinado.descendentes()

    def _aplicar_fator(self, valor: float) -> float:
        return (
            valor * self.diferencial_menor
            if self.patente == PATENTE_SOLDADO
            else valor
        )

    def _mover_e_contar(self, x: float, y: float) -> tuple[float, float, int]:
        self.pos_x += self._aplicar_fator(x)
        self.pos_y += self._aplicar_fator(y)
        soma_x, soma_y, total = self.pos_x, self.pos_y, 1

        for subordinado in self.subordinados:
            sub_x, sub_y, sub_total = subordinado._mover_e_contar(x, y)
            soma_x += sub_x
            soma_y += sub_y
            total += sub_total

        return soma_x, soma_y, total

    def mover(self, x: float, y: float) -> tuple[float, float]:
        soma_x, soma_y, total = self._mover_e_contar(x, y)
        return soma_x / total, soma_y / total

    def _alterar_atributo_e_contar(
        self, atributo: str, variacao: float
    ) -> tuple[float, int]:
        valor_atual = getattr(self, atributo)
        novo_valor = valor_atual + self._aplicar_fator(variacao)
        setattr(self, atributo, max(0.0, min(100.0, novo_valor)))
        soma, total = getattr(self, atributo), 1

        for subordinado in self.subordinados:
            sub_soma, sub_total = subordinado._alterar_atributo_e_contar(
                atributo, variacao
            )
            soma += sub_soma
            total += sub_total

        return soma, total

    def alterar_atributo(self, atributo: str, variacao: float) -> float:
        if atributo not in ATRIBUTOS_LIMITADOS:
            raise ValueError(f"Atributo inválido para alteração: {atributo}")

        soma, total = self._alterar_atributo_e_contar(atributo, variacao)
        return soma / total

    def set_order(self, order: Ordem) -> None:
        self.order = order


class QG:
    def __init__(self) -> None:
        self.militares: list[Militar] = []

    def adicionar_militar(self, militar: Militar) -> None:
        if militar in self.militares:
            raise ValueError("O militar já foi cadastrado no QG.")
        self.militares.append(militar)
        if militar.superior_imediato is not None:
            militar.superior_imediato.adicionar_subordinado(militar)

    def executar_dia(self) -> None:
        hierarquia = sorted(self.militares, key=lambda militar: militar.patente)

        for militar in hierarquia:
            for subordinado in militar.descendentes():
                subordinado.order.priorizar_ordem(militar.order)

        for militar in hierarquia:
            variacoes = militar.order.variacoes
            dx = variacoes["pos_x"][0]
            dy = variacoes["pos_y"][0]
            if dx is not None or dy is not None:
                militar.mover(dx or 0.0, dy or 0.0)

            for atributo in ATRIBUTOS_LIMITADOS:
                variacao = variacoes[atributo][0]
                if variacao is not None:
                    militar.alterar_atributo(atributo, variacao)

            militar.set_order(Ordem(militar))


def demonstrar() -> None:
    qg = QG()
    general = Militar(0, 0, 0, 80, 80, 60, 60, 1.0)
    coronel = Militar(1, 0, 0, 80, 80, 60, 60, 1.0, general)
    soldado = Militar(3, 0, 0, 80, 80, 60, 60, 0.5, coronel)

    for militar in (general, coronel, soldado):
        qg.adicionar_militar(militar)

    general.set_order(Ordem(general, pos_x=2))
    soldado.set_order(Ordem(soldado, pos_x=6))
    qg.executar_dia()

    for nome, militar in (
        ("General", general),
        ("Coronel", coronel),
        ("Soldado", soldado),
    ):
        print(f"{nome}: posicao=({militar.pos_x:.1f}, {militar.pos_y:.1f})")


if __name__ == "__main__":
    demonstrar()
