"""
Toy problem do padrão Composite: editor gráfico que move formas.

Baseado no exemplo de https://refactoring.guru/design-patterns/composite

Papéis do padrão neste código:
    - Component  -> Graphic          (interface comum)
    - Leaf       -> Dot, Circle      (objetos simples, sem filhos)
    - Composite  -> CompoundGraphic  (contêiner que guarda outros Graphics)
    - Client     -> ImageEditor      (usa tudo apenas pela interface Graphic)
"""

from abc import ABC, abstractmethod


# =============================================================================
# COMPONENT
# Interface comum para objetos simples (folhas) e complexos (compostos).
# É ela que permite ao cliente tratar os dois da MESMA forma.
# =============================================================================
class Graphic(ABC):

    @abstractmethod
    def move(self, x, y):
        pass

    @abstractmethod
    def draw(self):
        pass


# =============================================================================
# LEAF (folha)
# Elemento básico da árvore: não tem filhos e faz o trabalho de verdade.
# =============================================================================
class Dot(Graphic):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        # A folha executa a operação diretamente sobre si mesma.
        self.x += x
        self.y += y

    def draw(self):
        print(f"Ponto em ({self.x}, {self.y})")


# =============================================================================
# LEAF (folha)
# Outra folha. Herda de Dot, mas continua sendo um Graphic sem filhos.
# =============================================================================
class Circle(Dot):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self):
        print(f"Círculo em ({self.x}, {self.y}) com raio {self.radius}")
