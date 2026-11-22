# Eduardo
import math
import pygame
# Eduardo: AMARELO_OURO foi acrescentado para o aviso de novo recorde
from config import (WIDTH, FPS, TOTAL_FASES, ESTRELAS_PARA_PASSAR, PRETO, CINZA_ESCURO, CREME, AMARELO_OURO,
                    VERDE_OK, VERMELHO_ERRO, AZUL_UI, LARANJA_UI, INIT, GAME, RESULTADO, PARABENS, QUIT)
from desenho import texto, painel, escurecer_tela, estrela
from sprites import Botao, Particula
from progresso import calcula_estrelas, registra_resultado
from assets import tocar_som, tocar_musica, liga_desliga_som

INTERVALO_ESTRELA = 0.6  # segundos entre o aparecimento de cada estrela


def centro_estrela(i):
    return (WIDTH / 2 + (i - 1) * 130, 270)


def resultado_screen(window, assets, dados):
    # Mostra quantas estrelas o jogador ganhou e se passou de fase
    clock = pygame.time.Clock()

    fase = dados['fase']
    acertos = dados['acertos']
    total = dados['total']
    estrelas = calcula_estrelas(acertos, total)
    passou = estrelas >= ESTRELAS_PARA_PASSAR
    # Eduardo
    # Guarda o recorde ANTES de registrar, senão ele já estaria trocado pelo novo
    recorde_antigo = dados['progresso']['recordes'][fase]
    novo_recorde = dados['pontos'] > recorde_antigo
    registra_resultado(dados['progresso'], fase, estrelas, dados['pontos'])
    recorde = dados['progresso']['recordes'][fase]

    tocar_musica(assets, 'musica_menu')
    if passou:
        tocar_som(assets, 'vitoria')
    else:
        tocar_som(assets, 'derrota')

    # O botão da esquerda muda conforme o resultado
    if passou and fase < TOTAL_FASES:
        acao = 'proxima'
        botao_principal = Botao((WIDTH / 2 - 170, 600), 310, 74, 'PRÓXIMA FASE', VERDE_OK, 30)
    elif passou:
        acao = 'parabens'
        botao_principal = Botao((WIDTH / 2 - 170, 600), 310, 74, 'CONTINUAR', VERDE_OK, 30)
    else:
        acao = 'repetir'
        botao_principal = Botao((WIDTH / 2 - 170, 600), 310, 74, 'TENTAR DE NOVO', LARANJA_UI, 30)
    botao_menu = Botao((WIDTH / 2 + 170, 600), 310, 74, 'MENU', AZUL_UI, 30)
    all_buttons = pygame.sprite.Group()
    all_buttons.add(botao_principal)
    all_buttons.add(botao_menu)

    todas_particulas = pygame.sprite.Group()
    tempo = 0
    estrelas_mostradas = 0
    # Eduardo
    # o confete do recorde sai uma vez só, depois que as estrelas aparecem
    confete_recorde_feito = False
    tempo_confete_recorde = 0.8 + estrelas * INTERVALO_ESTRELA + 0.3

    state = RESULTADO
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
            elif botao_principal.clicado(event):
                tocar_som(assets, 'clique')
                if acao == 'proxima':
                    dados['fase'] = fase + 1
                    state = GAME
                elif acao == 'repetir':
                    state = GAME
                else:
                    state = PARABENS
                running = False
            elif botao_menu.clicado(event):
                tocar_som(assets, 'clique')
                state = INIT
                running = False

        # ----- Atualiza estado do jogo
        tempo += dt
        assets['fundo_interno'].update(dt)
        all_buttons.update(dt)
        # as estrelas ganhas aparecem uma de cada vez, com som e confete
        if estrelas_mostradas < estrelas and tempo > 0.8 + estrelas_mostradas * INTERVALO_ESTRELA:
            centro = centro_estrela(estrelas_mostradas)
            for i in range(35):
                todas_particulas.add(Particula(centro[0], centro[1], velocidade=420))
            estrelas_mostradas += 1
            tocar_som(assets, 'estrela')
        # Eduardo
        # explosão de confete em volta do aviso de novo recorde
        if novo_recorde and not confete_recorde_feito and tempo > tempo_confete_recorde:
            for i in range(45):
                todas_particulas.add(Particula(WIDTH / 2 + 150, 420, velocidade=450))
            tocar_som(assets, 'estrela')
            confete_recorde_feito = True
        todas_particulas.update(dt)

        # ----- Gera saídas
        assets['fundo_interno'].draw(window)
        escurecer_tela(window, 120)
        painel(window, (240, 60, 800, 600), CREME, 250, 26, 5)
        if passou:
            texto(window, f'Fase {fase} concluída!', 56, VERDE_OK, (WIDTH / 2, 130), contorno=3)
        else:
            texto(window, 'Quase lá!', 56, LARANJA_UI, (WIDTH / 2, 130), contorno=3)

        for i in range(3):
            if i < estrelas_mostradas:
                # a estrela "salta" para dentro ao aparecer
                idade = tempo - (0.8 + i * INTERVALO_ESTRELA)
                escala = min(1.0, 0.3 + idade * 4) + max(0, 0.25 - abs(idade - 0.2))
                estrela(window, centro_estrela(i), int(52 * escala), True)
            else:
                estrela(window, centro_estrela(i), 52, False)

        texto(window, f'Você acertou {acertos} de {total} lixos', 34, PRETO, (WIDTH / 2, 375))
        # Eduardo
        # Mostra a pontuação junto com o recorde da fase
        if novo_recorde:
            texto(window, f"Pontuação: {dados['pontos']}", 30, AZUL_UI, (WIDTH / 2 - 110, 420))
            if confete_recorde_feito:
                # o tamanho do texto aumenta e diminui para o aviso "pulsar"
                tamanho = 30 + int(3 * math.sin(tempo * 6))
                texto(window, 'NOVO RECORDE!', tamanho, AMARELO_OURO, (WIDTH / 2 + 150, 420), contorno=3)
        else:
            texto(window, f"Pontuação: {dados['pontos']}   •   Recorde: {recorde}", 30, AZUL_UI, (WIDTH / 2, 420))
        if passou and fase < TOTAL_FASES:
            texto(window, 'Muito bem! Você passou de fase!', 28, VERDE_OK, (WIDTH / 2, 480))
        elif passou:
            texto(window, 'Você completou todas as fases!', 28, VERDE_OK, (WIDTH / 2, 480))
        else:
            texto(window, 'Você precisa de 2 estrelas para passar. Tente de novo!', 28, VERMELHO_ERRO, (WIDTH / 2, 480))
        if total == 10:
            regra = '10 acertos = 3 estrelas  •  8 ou 9 = 2  •  4 a 7 = 1'
        else:
            regra = '15 acertos = 3 estrelas  •  12 a 14 = 2  •  6 a 11 = 1'
        texto(window, regra, 20, CINZA_ESCURO, (WIDTH / 2, 525))

        all_buttons.draw(window)
        todas_particulas.draw(window)

        pygame.display.update()

    return state
