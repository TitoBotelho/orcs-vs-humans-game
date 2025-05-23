# Jogo Orcs vs. Humans


<div align="center">
<img src="https://github.com/user-attachments/assets/3ed97600-6ef1-48c9-adc1-861417ecdc32" width="700px" />
</div>


## Visão Geral
Orcs vs. Humans é um jogo roguelike onde o jogador controla um personagem que interage com orcs em um ambiente dinâmico. O jogo possui animações de sprites tanto para o jogador quanto para os orcs, além de efeitos sonoros e música de fundo.

## Estrutura do Projeto
```
Orcs vs. Humans
├── src
│   ├── main.py          # Lógica principal do jogo, incluindo animações, movimentação e interações do jogador e dos orcs.
├── assets
│   ├── sounds           # Diretório com os arquivos de som usados no jogo.
│   ├── images           # Diretório com as imagens dos sprites do jogo.
│   └── music            # Diretório com as músicas de fundo do jogo.
├── requirements.txt     # Lista de dependências necessárias para o projeto.
└── README.md            # Documentação do projeto.
```

## Instruções de Instalação
1. Clone o repositório para sua máquina local.
2. Navegue até o diretório do projeto.
3. Instale as dependências listadas em `requirements.txt` (se necessário).
4. Execute o jogo com o comando:
   ```
   pgzrun src/main.py
   ```

## Detalhes da Jogabilidade
- O jogador pode se mover pela tela usando as teclas `W`, `A`, `S` e `D`.
- O jogador pode atacar os orcs clicando com o botão esquerdo do mouse.
- Cada vez que um orc é derrotado, dois novos orcs aparecem na área do jogo.
- O jogo possui um menu principal com opções para iniciar o jogo, alternar a música e sair.

## Melhorias Futuras
- Adicionar novos recursos ao jogo, como power-ups, diferentes tipos de inimigos e fases.

## Agradecimentos
- Agradecimentos especiais aos criadores dos sprites e arquivos de som utilizados no jogo.
