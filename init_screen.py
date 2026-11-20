import math
import pygame
from config import (WIDTH, HEIGHT, FPS, BRANCO, CREME, VERDE_OK, AZUL_UI, VERMELHO_ERRO, CORES_TITULO,
                    TAMANHO_ITEM, INIT, ESCOLHA, GAME, QUIT)
from desenho import fonte, texto, painel
from sprites import Botao
from assets import tocar_som, tocar_musica, liga_desliga_som


def desenha_titulo(window, tempo):
    # Título "COLETANDO" com letras coloridas pulando
    frase = 'COLETANDO'
    f = fonte(78)
    larguras = []
    largura_total = 0
    for letra in frase:
        larguras.append(f.size(letra)[0])
        largura_total += f.size(letra)[0]

    x = WIDTH / 2 - largura_total / 2
    for i in range(len(frase)):
        dy = math.sin(tempo * 4 + i * 0.5) * 8
        texto(window, frase[i], 78, CORES_TITULO[i % 5], (x + larguras[i] / 2, 78 + dy), contorno=4)
        x += larguras[i]


def init_screen(window, assets, dados):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    tocar_musica(assets, 'musica_menu')

    # Criando botões
    botao_play = Botao((300, 330), 300, 82, 'PLAY', VERDE_OK, 44)
    botao_fases = Botao((300, 440), 300, 82, 'FASES', AZUL_UI, 40)
    botao_sair = Botao((300, 550), 300, 82, 'SAIR', VERMELHO_ERRO, 40)
    all_buttons = pygame.sprite.Group()
    all_buttons.add(botao_play)
    all_buttons.add(botao_fases)
    all_buttons.add(botao_sair)

    # Lixinhos que flutuam ao redor do título: [desenho, x, y]
    decoracao = [['garrafa_pet', 250, 170], ['lata', 1030, 175], ['jornal', 150, 60],
                 ['banana', 1150, 70], ['garrafa_vidro', 455, 205]]
    tempo = 0

    state = INIT
    running = True
    while running:
        # Ajusta a velocidade do jogo. dt = segundos desde o último frame
        dt = min(clock.tick(FPS) / 1000, 0.05)

        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                liga_desliga_som(assets)
            elif botao_play.clicado(event):
                tocar_som(assets, 'clique')
                dados['fase'] = 1
                state = GAME
                running = False
            elif botao_fases.clicado(event):
                tocar_som(assets, 'clique')
                state = ESCOLHA
                running = False
            elif botao_sair.clicado(event):
                tocar_som(assets, 'clique')
                state = QUIT
                running = False

        # ----- Atualiza estado do jogo
        tempo += dt
        assets['fundo_externo'].update(dt)
        all_buttons.update(dt)

        # ----- Gera saídas
        assets['fundo_externo'].draw(window)
        for i in range(len(decoracao)):
            imagem = assets['itens'][decoracao[i][0]]
            imagem = pygame.transform.rotozoom(imagem, math.sin(tempo * 2 + i) * 15, 70 / TAMANHO_ITEM)
            rect = imagem.get_rect()
            rect.center = (decoracao[i][1], decoracao[i][2] + math.sin(tempo * 3 + i) * 8)
            window.blit(imagem, rect)

        desenha_titulo(window, tempo)
        texto(window, 'Aprenda a separar o lixo brincando!', 30, BRANCO, (WIDTH / 2, 150), contorno=3)
        painel(window, (120, 260, 360, 360), CREME, 200)
        all_buttons.draw(window)
        texto(window, 'ESC: pausar   |   M: liga/desliga o som', 20, BRANCO,
              (WIDTH - 20, HEIGHT - 14), 'bottomright', contorno=2)

        pygame.display.update()  # Mostra o novo frame para o jogador

    return state
