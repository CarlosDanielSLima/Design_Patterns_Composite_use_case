# Design_Patterns_Composite_use_case
Código destinado a estudar o padrão de projeto de software **Composite**, demonstrando sua motivação, seu 
funcionamento e sua aplicação na melhoria de uma implementação existente. 

# Problema real: Cadeia de Comando Militar
Um quartel, composto por militares de diferentes patentes, possui uma hierarquia de comando muito bem definida, onde um militar de patente $n$ obedece as ordens de todos os $n$ superiores, de $0$ a $n$. (Usaremos o índice numérico para fins de simplificação do problema).

Simultaneamente, um militar pode receber ordens de vários tipos e possivelmente contraditórias. Cada tipo de ordem altera um aspecto diferente do pelotão.

Em caso de contradições, um militar deve optar por seguir a regra do maior superior possível. Nesse caso de uso, consideramos que um militar de categoria alta, por mais alta que seja, não pode mandar nos subordinados de um de seus pares, evitando conflitos de poder dentro do QG.

Cada militar possui:
- Patente;
- Posição (x, y);
- Prontidão (0%-100%);
- Saciedade (0%-100%);
- Poder de fogo;
- Poder de defesa.

Os militares podem possuir as seguintes patentes:
- General;
- Coronel;
- Capitão;
- Soldado.

# 1. Implementação Original
Ignorando o padrão Composite, implementamos uma classe Militar. A patente $i$, com $i \in (0, 1, 2)$, possui uma lista para cada patente subordinada $j$, $j \in [i+1, n]$ (A patente Soldado, $i=3$, não possui subordinados).

Cada vez que um militar adiciona um subordinado, passa para o seu superior imediato e adiciona esse novo subordinado à lista de subordinados da respectiva patente no objeto do superior.

Cada ordem executada pelo militar é passada para cada uma das listas, sendo executada por cada patente de subordinados, agregando os resultados ao final.

Os soldados, por não terem nem experiência nem subordinados, são mais desleixados para cumprir regras. Por isso, é aplicado um fator de redução à qualquer ordem recebida (diminuir a variação no movimento ou na saciedade, por exemplo).

Para viabilizar a solução de conflitos de ordens entre superiores, a classe QG, que realiza a criação e alocação de militares, além de passar os dias, também irá garantir a execução das ordens seguindo a hieráriquia: Cada militar irá carregar a ordem que irá executar no dia, sobrescrevendo ordens conflitantes dos subordinados e executando a sua própria. Portanto, para garantir que a priorização de ordens dos militares de mais alta patente, é necessário que esses sejam os primeiros a executar suas ordens, sobrescrevendo ordens conflitantes dos subordinados.

<!-- O código está completo, funcional e suficientemente elaborado para evidenciar problemas de design que justifiquem a aplicação do padrão. -->
<!-- Explicar o contexto, o funcionamento e as responsabilidades dos principais componentes. 
Executar o programa, demonstrando seu funcionamento. 
Identificar problemas concretos de design na implementação. 
Localizar e explicar os trechos de código responsáveis pelos problemas 
identificados, demonstrando suas consequências para a manutenção, evolução ou extensão do software. 
Explicar por que o padrão escolhido é pertinente aos problemas apresentados.  -->

# 2. Explicação do padrão: Toy Problem (editor gráfico)
Baseado no exemplo do [Refactoring Guru](https://refactoring.guru/design-patterns/composite): um editor gráfico onde o usuário pode mover formas simples (pontos, círculos) ou **grupos** de formas, que podem conter outros grupos.

**Problema:** sem o padrão, o cliente precisaria saber se está lidando com uma forma simples ou com um grupo (e grupos dentro de grupos), espalhando `if`/`isinstance` pelo código para mover cada coisa de um jeito.

**Participantes** (em [src/toy_problem.py](src/toy_problem.py)):
| Papel | Classe | Responsabilidade |
|---|---|---|
| Component | `Graphic` | Interface comum (`move`, `draw`) para folhas e compostos |
| Leaf | `Dot`, `Circle` | Fazem o trabalho de verdade; não têm filhos |
| Composite | `CompoundGraphic` | Guarda filhos (`add`/`remove`) e **delega** `move`/`draw` a eles recursivamente |
| Client | `ImageEditor` | Usa tudo apenas via `Graphic`, sem distinguir folha de grupo |

**Vantagens:** o cliente trata objetos simples e compostos de forma uniforme; novas formas podem ser adicionadas sem alterar o cliente nem o composto (Open/Closed); árvores de qualquer profundidade funcionam com a mesma chamada.

**Limitações:** a interface comum precisa fazer sentido para todos os elementos (pode ficar genérica demais); fica difícil restringir que tipos de filhos um composto aceita; `add`/`remove` existem só no composto, então o cliente precisa saber que tem um grupo para montá-lo.

**Como executar:**
```bash
python src/toy_problem.py
```
