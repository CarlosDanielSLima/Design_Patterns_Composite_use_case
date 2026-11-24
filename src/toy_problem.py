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
    def draw(self, nivel=0):
        # 'nivel' serve apenas para indentar a saída e mostrar a árvore.
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

    def draw(self, nivel=0):
        print("  " * nivel + f"Ponto em ({self.x}, {self.y})")


# =============================================================================
# LEAF (folha)
# Outra folha. Herda de Dot, mas continua sendo um Graphic sem filhos.
# =============================================================================
class Circle(Dot):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self, nivel=0):
        print("  " * nivel + f"Círculo em ({self.x}, {self.y}) com raio {self.radius}")


# =============================================================================
# COMPOSITE (composto)
# Também é um Graphic, mas guarda uma lista de filhos (folhas OU outros
# compostos). Ele não faz o trabalho sozinho: DELEGA para os filhos.
# =============================================================================
class CompoundGraphic(Graphic):

    def __init__(self):
        # Os filhos são referenciados pela interface Graphic, então o composto
        # não sabe (nem precisa saber) se cada filho é folha ou outro composto.
        self.children = []

    # Métodos de gerenciamento de filhos (exclusivos do Composite).
    def add(self, child: Graphic):
        self.children.append(child)

    def remove(self, child: Graphic):
        self.children.remove(child)

    def move(self, x, y):
        # DELEGAÇÃO RECURSIVA: repassa a operação para cada filho.
        # Se o filho for outro CompoundGraphic, ele repete o processo,
        # percorrendo a árvore inteira até chegar nas folhas.
        for child in self.children:
            child.move(x, y)

    def draw(self, nivel=0):
        # Mesma ideia: o composto desenha a si mesmo desenhando seus filhos.
        print("  " * nivel + "Grupo:")
        for child in self.children:
            child.draw(nivel + 1)


# =============================================================================
# CLIENT (cliente)
# Trabalha SOMENTE com a interface Graphic. Não precisa saber se está movendo
# um ponto, um círculo ou um grupo inteiro de formas.
# =============================================================================
class ImageEditor:

    def __init__(self):
        # A "tela" do editor é ela mesma um composto (raiz da árvore).
        self.all = CompoundGraphic()

    def load(self):
        self.all.add(Dot(1, 2))
        self.all.add(Circle(5, 3, 10))

    def group_selected(self, components):
        # Junta vários Graphics em um novo grupo. Como o grupo também é um
        # Graphic, ele pode entrar na árvore no lugar dos itens originais.
        group = CompoundGraphic()
        for component in components:
            group.add(component)
            self.all.remove(component)
        self.all.add(group)
        return group


if __name__ == "__main__":
    editor = ImageEditor()
    editor.load()

    print("== Estado inicial ==")
    editor.all.draw()

    # Seleciona as duas formas carregadas e agrupa.
    dot, circle = editor.all.children
    grupo = editor.group_selected([dot, circle])

    # Composto dentro de composto: adiciona um novo ponto fora do grupo.
    editor.all.add(Dot(0, 0))

    print("\n== Após agrupar e adicionar um ponto ==")
    editor.all.draw()

    # UNIFORMIDADE: a MESMA chamada move() funciona para folha e para grupo.
    print("\n== Movendo só o grupo em (+10, +10) ==")
    grupo.move(10, 10)
    editor.all.draw()

    print("\n== Movendo só a folha (ponto) em (-1, -1) ==")
    dot.move(-1, -1)
    editor.all.draw()

    print("\n== Movendo TUDO (raiz) em (+100, 0) ==")
    editor.all.move(100, 0)
    editor.all.draw()
