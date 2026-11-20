import math
import random
import pygame
from config import (WIDTH, HEIGHT, FPS, TOTAL_FASES, BRANCO, AMARELO_OURO, AZUL_UI, ORDEM_LIXEIRAS,
                    INIT, PARABENS, QUIT)
from desenho import texto, painel, escurecer_tela, estrela, lixeira
from sprites import Botao, Particula, LixoCaindo
from dados import ITENS_FACEIS, ITENS_DIFICEIS
from assets import tocar_som, tocar_musica, liga_desliga_som


def parabens_screen(window, assets, dados):
    # Animação final: confete, lixeiras dançando e chuva de lixinhos
    clock = pygame.time.Clock()
    tocar_musica(assets, 'musica_menu')
    tocar_som(assets, 'vitoria')

    todos_confetes = pygame.sprite.Group()
    lixos_caindo = pygame.sprite.Group()
    for i in range(14):
        lixos_caindo.add(LixoCaindo(assets, ITENS_FACEIS + ITENS_DIFICEIS))
    botao_menu = Botao((WIDTH / 2, 425), 300, 70, 'MENU', AZUL_UI, 34)

    # total de estrelas conquistadas em todas as fases
    total_estrelas = 0
    for fase in dados['progresso']['estrelas']:
        total_estrelas += dados['progresso']['estrelas'][fase]

    tempo = 0
    state = PARABENS
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
            elif tempo > 1.5 and botao_menu.clicado(event):
                tocar_som(assets, 'clique')
                state = INIT
                running = False

        # ----- Atualiza estado do jogo
        tempo_anterior = tempo
        tempo += dt
        assets['fundo_externo'].update(dt)
        botao_menu.update(dt)
        # chuva constante de confete vindo do topo
        for i in range(3):
            todos_confetes.add(Particula(random.uniform(0, WIDTH), -10, velocidade=120, gravidade=160, vida=4.5))
        # explosão de fogos de vez em quando (a cada 1/1.2 segundos)
        if int(tempo * 1.2) != int(tempo_anterior * 1.2):
            x = random.uniform(200, 1080)
            y = random.uniform(120, 300)
            for i in range(40):
                todos_confetes.add(Particula(x, y, velocidade=500, vida=1.4))
            tocar_som(assets, 'estrela')
        todos_confetes.update(dt)
        lixos_caindo.update(dt)

        # ----- Gera saídas
        assets['fundo_externo'].draw(window)
        lixos_caindo.draw(window)
        escurecer_tela(window, 70)
        painel(window, (230, 40, 820, 440), (40, 60, 90), 170, 30, 0)

        # título que entra crescendo e depois pulsa
        entrada = min(1.0, tempo * 1.5)
        pulso = 1 + math.sin(tempo * 5) * 0.05
        texto(window, 'Parabéns!', int(110 * entrada * pulso), AMARELO_OURO, (WIDTH / 2, 125), contorno=6)
        if tempo > 0.6:
            texto(window, 'Você aprendeu a reciclar um lixo!', 46, BRANCO, (WIDTH / 2, 230), contorno=4)
        if tempo > 1.0:
            texto(window, f'Estrelas conquistadas: {total_estrelas} de {3 * TOTAL_FASES}', 30, BRANCO,
                  (WIDTH / 2, 295), contorno=3)
            for i in range(3 * TOTAL_FASES):
                estrela(window, (WIDTH / 2 + (i - 4) * 50, 345), 20, i < total_estrelas, math.sin(tempo * 3 + i) * 0.2)
        if tempo > 1.5:
            window.blit(botao_menu.image, botao_menu.rect)

        # lixeiras dançando em fila
        largura_espaco = WIDTH / (len(ORDEM_LIXEIRAS) + 1)
        for i in range(len(ORDEM_LIXEIRAS)):
            balanco = abs(math.sin(tempo * 6 + i * 0.9))
            r = pygame.Rect(0, 0, 130, 150)
            r.midbottom = (largura_espaco * (i + 1), HEIGHT - 10 - balanco * 30)
            lixeira(window, r, ORDEM_LIXEIRAS[i], balanco)

        todos_confetes.draw(window)

        pygame.display.update()

    return state
