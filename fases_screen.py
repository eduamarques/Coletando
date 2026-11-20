import math
import pygame
from config import (WIDTH, FPS, FASES, BRANCO, PRETO, CINZA, CINZA_ESCURO, CREME, AMARELO_OURO, LARANJA_UI,
                    CORES_TITULO, INIT, ESCOLHA, GAME, DIFICULDADE, QUIT)
from desenho import texto, painel, estrela
from sprites import Botao
from assets import tocar_som, tocar_musica, liga_desliga_som

VELOCIDADES = {1: 'Devagar', 2: 'Rápida', 3: 'Muito rápida'}


def desenha_cadeado(window, centro):
    x = centro[0]
    y = centro[1]
    pygame.draw.arc(window, PRETO, (x - 30, y - 62, 60, 70), 0, math.pi, 10)
    corpo = pygame.Rect(x - 42, y - 30, 84, 66)
    pygame.draw.rect(window, (240, 190, 50), corpo, border_radius=10)
    pygame.draw.rect(window, PRETO, corpo, 4, border_radius=10)
    pygame.draw.circle(window, PRETO, (x, y), 9)
    pygame.draw.rect(window, PRETO, (x - 4, y, 8, 20))


def fases_screen(window, assets, dados):
    # Mostra as 3 fases. Só dá para jogar as fases já desbloqueadas.
    clock = pygame.time.Clock()
    tocar_musica(assets, 'musica_menu')
    progresso = dados['progresso']

    # Um cartão para cada fase: {'fase': 1, 'rect': ..., 'liberada': True}
    cartoes = []
    for fase in FASES:
        rect = pygame.Rect(0, 0, 280, 300)
        rect.center = (WIDTH / 2 + (fase - 2) * 340, 380)
        cartao = {'fase': fase, 'rect': rect, 'liberada': fase <= progresso['desbloqueada']}
        cartoes.append(cartao)

    botao_voltar = Botao((WIDTH / 2, 640), 260, 70, 'VOLTAR', LARANJA_UI, 34)

    state = ESCOLHA
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)

        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                liga_desliga_som(assets)
            elif botao_voltar.clicado(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                tocar_som(assets, 'clique')
                state = INIT
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for cartao in cartoes:
                    if cartao['rect'].collidepoint(event.pos):
                        if cartao['liberada']:
                            tocar_som(assets, 'clique')
                            dados['fase'] = cartao['fase']
                            if cartao['fase'] == 1:
                                state = DIFICULDADE  # pergunta a dificuldade antes da fase 1
                            else:
                                state = GAME
                            running = False
                        else:
                            tocar_som(assets, 'erro')

        # ----- Atualiza estado do jogo
        assets['fundo_externo'].update(dt)
        botao_voltar.update(dt)

        # ----- Gera saídas
        assets['fundo_externo'].draw(window)
        texto(window, 'ESCOLHA A FASE', 64, AMARELO_OURO, (WIDTH / 2, 110), contorno=4)
        mouse = pygame.mouse.get_pos()
        for cartao in cartoes:
            fase = cartao['fase']
            r = cartao['rect']
            if cartao['liberada'] and r.collidepoint(mouse):
                r = r.inflate(16, 16)  # cresce quando o mouse está em cima

            if cartao['liberada']:
                painel(window, r, CREME, 255)
                texto(window, f'FASE {fase}', 44, CORES_TITULO[fase - 1], (r.centerx, r.y + 50), contorno=3)
                for i in range(3):
                    cheia = i < progresso['estrelas'][fase]
                    estrela(window, (r.centerx + (i - 1) * 62, r.y + 130), 26, cheia)
                texto(window, f"{FASES[fase]['itens']} lixos", 26, PRETO, (r.centerx, r.y + 195))
                texto(window, f'Esteira: {VELOCIDADES[fase]}', 22, CINZA_ESCURO, (r.centerx, r.y + 232))
            else:
                painel(window, r, (190, 190, 195), 255)
                texto(window, f'FASE {fase}', 44, CINZA, (r.centerx, r.y + 50), contorno=3)
                desenha_cadeado(window, (r.centerx, r.y + 150))
                texto(window, 'Bloqueada', 26, CINZA_ESCURO, (r.centerx, r.y + 235))

        texto(window, 'Ganhe 2 estrelas para liberar a próxima fase!', 26, BRANCO, (WIDTH / 2, 560), contorno=3)
        window.blit(botao_voltar.image, botao_voltar.rect)

        pygame.display.update()

    return state
