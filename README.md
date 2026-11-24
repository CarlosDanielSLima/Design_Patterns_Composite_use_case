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