# ***Heavy Ordnance***
## **Projeto Realizado por:**

### Daniel Fernandes (a22202501) e David Mendes (a22203255)

1. *Daniel Fernandes* (a22202501)
     - Game Render processes
     - Cannon, Bullet and Ship Classes
     - Colisions and Sprites
     - GameScreen Ui
2. *David Mendes* (a22203255)
     - Main, Leaderboard e auxiliary functions
     - StartScreen, GameoverScreen e LeaderboardScreen UI
     - Code Integration
     - Markdown

------------------------------    
## **Desenvolvimento**


## O projeto é constituído por 4 ficheiros de código, vários ficheiros de imagens e um ficheiro de texto onde se guarda a pontuação:
 - Main.py: Este ficheiro agrupa as funções de cada Ecrã para uma melhor leitura das diversas etapas do jogo.
 - auxiliary_functions.py: Este ficheiro contem algumas funções auxiliares ao funcionamento de certas partes do código.
 - Ui.py: Define os diversos Ecrãs de jogo (StartScreen, GameScreen, GameoverScreen, LeaderboardScreen) e contém a função que inicializa o pygame.
 - Boat_and_cannon.py: Define as Clases, sprites e colisões reacionados aos barcos, canhão e balas bem como todos os processos diretamente relacionados.
 - Leaderboard.txt: Contém o top 10 de todas as pontuações introduzidas bem como as respetivas iniciais.


### **Referências**
https://realpython.com/pygame-a-primer/
-Consultado para a construção do jogo usando sprites.

https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
-Consultado para a rotação de sprites.

Consultamos o código do jogo do professor Andrade de onde retirámos a idea de utilizar a livraria pygame.math.Vector2 para guardar posições e velocidades.

O Código referente ao Leaderboard, Gameover e Start foi retirado do projeto anterior chamado Comets. Ainda assim, foi necessário adaptar essas funções a este projeto.