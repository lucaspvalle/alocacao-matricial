# otimizacao-alocacao

Este projeto foi desenvolvido para auxiliar a tomada de decisão em um problema de alocação de membros nas áreas e projetos de uma organização estudantil (OE).

A OE segue uma estrutura matricial, na qual o membro participa simultaneamente de times de uma área (Gestão de Pessoas, Financeiro, Projetos e Marketing) e de um projeto de impacto social.

Para isso, os membros respondem um formulário, preenchendo o interesse com uma escala de 1 à 4 com a sua preferência em relação às áreas e aos projetos em que desejam participar.
A escala é dada em:

1. Gostaria muito de participar deste time
2. Gostaria de participar deste time, embora não seja a minha primeira opção
3. Não me incomodaria de participar deste time
4. Não gostaria de participar deste time

A função objetivo busca, portanto, encontrar o mínimo valor da soma dos coeficientes de interesses, com valores de 1 a 4.

Para evitar os membros de serem alocados em times indesejados, substituiram-se os coeficientes 3 e 4 da matriz de interesses por valores suficientemente grandes para que a máquina evite a seleção destes.

Com estes dados em mão, podemos modelar o problema com variáveis de decisão binárias do tipo "Pessoa 1 (Área 1, Projeto 1)", sendo 1 caso a Pessoa seja alocado na Área 1 e Projeto 1, 0 caso contrário.

Além disso, as restrições do modelo são:

* O membro deverá participar de apenas um projeto e de uma área
* As áreas e projetos possuem restrições de quantidades máximas e mínimas de membros a serem alocadas em seus times
* Alguns membros podem desejar continuar no time em que já estavam no semestre passado. Desta forma, o modelo deve manter a alocação destes membros específicos
* Alguns times podem optar por ficar fora da estrutura matricial. Neste sentido, os membros deste time não participam de uma área e projeto, e sim apenas de um destes

Por fim, o projeto se mostrou extremamente eficaz para a organização estudantil, uma vez que reduziu um processo de decisão complicado e demorado, uma vez que tomava dias de dedicação da Presidência, encarregada do processo, para a uma resolução imediata e com muito mais qualidade.
