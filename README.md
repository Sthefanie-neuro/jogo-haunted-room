# Haunted Room 👻💎

### Um jogo de sobrevivência e coleta em uma caverna assombrada, desenvolvido com Python e Pygame Zero.

![GIF da jogabilidade de Haunted Room](https-github-com-Sthefanie-neuro-jogo-haunted-room-blob-main-gameplay-gif-raw-true.gif)
> *Nota: Substitua o link acima pelo GIF da sua jogabilidade!*

---

## 📜 Sobre o Jogo

**Haunted Room** é um jogo de arena no estilo *roguelike* onde você controla um aventureiro preso em uma sala mal-assombrada. Seu objetivo é simples, mas desafiador: colete todas as gemas preciosas para destravar a passagem para o próximo nível, tudo isso enquanto desvia de hordas de monstros que se tornam mais rápidos e numerosos a cada sala que você conquista.

Este projeto foi criado como um desafio de desenvolvimento, utilizando um conjunto limitado de tecnologias para focar na lógica de jogo, animação de sprites e jogabilidade.

---

## ✨ Funcionalidades Principais

* **Animação Detalhada:** Herói e inimigos possuem animações de sprite para movimento e estado ocioso, criando um mundo mais vivo.
* **Inimigos Variados:** Enfrente 4 tipos de monstros, cada um com um padrão de movimento único (aleatório, perseguidor, etc.).
* **Níveis Progressivos:** A dificuldade aumenta a cada nível, com mais inimigos e maior velocidade.
* **Power-up de Velocidade:** Coletar uma gema concede um bônus temporário de velocidade para ajudar na fuga.
* **Menu Completo:** Um menu principal com opções para iniciar o jogo, controlar a música/sons e sair.
* **Sistema de Recordes:** O jogo salva sua maior pontuação (gemas coletadas) localmente.

---

## 🎮 Como Jogar

* **Movimento:** Use as **Setas do Teclado** para mover o personagem.
* **Objetivo:** Colete todas as 5 gemas em cada sala.
* **Fuga:** Após coletar todas as gemas, corra para a **passagem na extremidade direita da tela** para avançar para o próximo nível.
* **Cuidado:** Não toque nos inimigos!

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando apenas as seguintes tecnologias, conforme os requisitos do desafio:

* **Python:** A linguagem de programação principal.
* **Pygame Zero:** Um framework para iniciantes construído sobre o Pygame, facilitando a criação de jogos.
* **Bibliotecas Padrão:** `math`, `random`, `os`, `glob`.

---

## 🚀 Como Executar o Projeto Localmente

Para rodar o jogo em sua máquina, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Sthefanie-neuro/jogo-haunted-room.git](https://github.com/Sthefanie-neuro/jogo-haunted-room.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd jogo-haunted-room
    ```

3.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    *Ative o ambiente:*
    * No Windows: `venv\Scripts\activate`
    * No Linux/Mac: `source venv/bin/activate`

4.  **Instale as dependências:**
    ```bash
    pip install pgzero
    ```

5.  **Execute o jogo:**
    ```bash
    pgzrun main.py
    ```

---

## ✒️ Autora

Desenvolvido com ❤️ por **Sthefanie**.

---

## 💖 Créditos e Agradecimentos

Este jogo não seria possível sem os incríveis recursos criados pela comunidade.

### Imagens Geradas por IA
As imagens de fundo foram criadas com o auxílio de IA, utilizando os seguintes prompts:

> **caverna_background:** *Arte pixel, em vista de cima, de um mapa de masmorra para um jogo estilo roguelike. O piso é composto por lajes de pedra quadradas, em tons de cinza e bege, formando uma grade perfeita. As paredes, que emolduram a área, são de rocha bruta escura, quase preta, com detalhes marrons e uma textura irregular. No canto superior direito, há uma plataforma elevada, feita de madeira clara com um padrão de tábuas na diagonal. A passagem escura ao lado da plataforma é uma área de transição para o próximo nível. A iluminação é sombria e dramática, com um gradiente escuro nas bordas que concentra a luz no centro do mapa, simulando a iluminação de uma caverna.*

> **menu_background:** *Uma visão de cima da tela de 'Menu Principal' de um jogo roguelike, projetada em estilo pixel art. A cena se passa na entrada de uma masmorra escura e amaldiçoada, reminiscente do ambiente visto na tela de 'Fim de Jogo'. O chão é feito de ladrilhos de pedra rachados em tons de cinza e marrom. As paredes da masmorra são ásperas e escuras, com detalhes em pedra desgastada. No centro da imagem, um personagem herói masculino com cabelo espetado castanho e roupas escuras está em posição de combate, de frente para a entrada da masmorra, segurando uma espada com uma lâmina prateada brilhante e punho marrom. Seus olhos demonstram coragem e prontidão. A entrada da masmorra é um arco de pedra escura, com sombras profundas onde os inimigos estão parcialmente escondidos; pares de olhos brilhantes e ameaçadores espreitam nas sombras: amarelos, roxos e verde-azulados, pertencentes aos fantasmas e ao morcego, similares em estilo aos inimigos da tela de 'Fim de Jogo', mas menos visíveis. Não há texto na imagem.*

> **game_over:** *Uma visão de cima da tela de 'Fim de Jogo' de um jogo roguelike. A cena se passa em uma masmorra escura e amaldiçoada. O chão é feito de ladrilhos de pedra rachados, e as paredes são ásperas e escuras. No centro, um personagem herói masculino com cabelo espetado castanho e roupas escuras está derrotado, deitado de costas com os braços e pernas ligeiramente afastados. Sua espada está no chão ao lado dele, significando a derrota. Ao seu redor, estão os inimigos do jogo: vários fantasmas distintos em pixel art com diferentes esquemas de cores - um fantasma espectral marrom-acinzentado com olhos amarelos brilhantes, um fantasma com uma aura escura e olhos roxos vibrantes, e um fantasma cinza-azulado adornado com chamas espectrais verde-azuladas - e uma pequena criatura voadora semelhante a um morcego, com corpo e asas vermelhos e laranjas e olhos amarelos. Os fantasmas e o morcego têm expressões sinistras e ameaçadoras, celebrando a derrota do herói. O estilo geral é pixel art, semelhante a jogos roguelike clássicos. Não há texto na imagem.*

### Assets Visuais
* **Herói:** [Free Swordsman 1–3 Level Pixel Top-Down Sprite Character (Level 2)](https://craftpix.net/freebies/free-swordsman-1-3-level-pixel-top-down-sprite-character-pack/) por craftpix.
* **Wraith (Inimigo):** [Free Wraith Tiny Style 2D Sprites](https://craftpix.net/freebies/free-wraith-tiny-style-2d-sprites/) por craftpix.
* **Bat (Inimigo):** Criado por [Bagzie](https://opengameart.org/users/bagzie) no OpenGameArt.
* **Ícones do Menu:** [Game Icons](https://kenney.nl/assets/game-icons) por Kenney.
* **Fonte:** [Creepster](https://fonts.google.com/specimen/Creepster) por Google Fonts.

### Áudio
* **Música de Fundo:** [fast-epic-108427](https://pixabay.com/music/build-up-scenes-fast-epic-108427/) no Pixabay.
* **Som de Colisão:** [Sound Design Elements Impact SFX PS 037](https://pixabay.com/sound-effects/sound-design-elements-impact-sfx-ps-037-321219/) no Pixabay.
* **Som de Level Up:** [Arcade UI 6](https://pixabay.com/no/sound-effects/arcade-ui-6-229503/) por floraphonic no Pixabay.
* **Som de Coleta de Gema:** [arcade-ui-7-229506](https://pixabay.com/sound-effects/arcade-ui-7-229506/) por floraphonic no Pixabay.

* **Música de Fundo:** [fast-epic-108427](https://pixabay.com/music/build-up-scenes-fast-epic-108427/) no Pixabay.
* **Som de Colisão:** [Sound Design Elements Impact SFX PS 037](https://pixabay.com/sound-effects/sound-design-elements-impact-sfx-ps-037-321219/) no Pixabay.
* **Som de Level Up:** [Arcade UI 6](https://pixabay.com/no/sound-effects/arcade-ui-6-229503/) por floraphonic no Pixabay.
* **Som de Coleta de Gema:** [arcade-ui-7-229506](https://pixabay.com/sound-effects/arcade-ui-7-229506/) por floraphonic no Pixabay.
