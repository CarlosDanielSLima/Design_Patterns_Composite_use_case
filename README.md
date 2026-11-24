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

# 3. Aplicação do padrão Composite
A versão refatorada está em `src/composite_problem.py`; a implementação original foi mantida em `src/original_problem.py` para permitir a comparação.

- `ComponenteMilitar` define a interface comum para operações sobre um militar ou uma unidade.
- `Militar` é o componente concreto e também o Composite: mantém somente seus subordinados diretos. Um militar sem subordinados funciona como folha.
- Operações como movimento e alteração de atributos percorrem a hierarquia recursivamente. Cada militar aplica seu próprio fator de cumprimento, e as operações numéricas retornam o resultado agregado da unidade.
- `QG` continua responsável pela priorização das ordens, mas deixa de depender de listas de subordinados separadas por patente; a estrutura de comando é percorrida pela própria composição.

Para executar a demonstração, use `python src/composite_problem.py`. Ela cria uma hierarquia General–Coronel–Soldado, emite ordens conflitantes para o General e o Soldado e mostra que prevalece a ordem do superior, com o fator de cumprimento do Soldado aplicado.