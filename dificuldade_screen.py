# Mateus
import pygame
from config import (WIDTH, FPS, FASES, DIFICULDADES, ORDEM_DIFICULDADES, BRANCO, PRETO, CINZA_ESCURO, CREME,
                    AMARELO_OURO, LARANJA_UI, INIT, GAME, QUIT, DIFICULDADE)
from desenho import texto, painel, lampada
from sprites import Botao
from assets import tocar_som, tocar_musica, liga_desliga_som


def calcula_ajudas(ajudas_da_fase, dificuldade):
    # Devolve quantas ajudas a criança vai ter na fase, de acordo com a dificuldade:
    #   fácil = todas, médio = metade, difícil = nenhuma
    if dificuldade == 'facil':
        return ajudas_da_fase
    elif dificuldade == 'medio':
        return ajudas_da_fase // 2
    else:
        return 0


def dificuldade_screen(window, assets, dados):
    # Pergunta a dificuldade antes de começar a fase 1
    clock = pygame.time.Clock()
    tocar_musica(assets, 'musica_menu')

    ajudas_da_fase = FASES[1]['ajudas']

    # Um cartão para cada dificuldade: {'chave': 'facil', 'rect': ...}
    cartoes = []
    for i in range(len(ORDEM_DIFICULDADES)):
        rect = pygame.Rect(0, 0, 300, 300)
        rect.center = (WIDTH / 2 + (i - 1) * 360, 370)
        cartao = {'chave': ORDEM_DIFICULDADES[i], 'rect': rect}
        cartoes.append(cartao)

    botao_voltar = Botao((WIDTH / 2, 640), 260, 70, 'VOLTAR', LARANJA_UI, 34)

    state = DIFICULDADE
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
                        tocar_som(assets, 'clique')
                        dados['dificuldade'] = cartao['chave']
                        state = GAME
                        running = False

        # ----- Atualiza estado do jogo
        assets['fundo_externo'].update(dt)
        botao_voltar.update(dt)

        # ----- Gera saídas
        assets['fundo_externo'].draw(window)
        texto(window, 'ESCOLHA A DIFICULDADE', 64, AMARELO_OURO, (WIDTH / 2, 110), contorno=4)
        mouse = pygame.mouse.get_pos()
        for cartao in cartoes:
            info = DIFICULDADES[cartao['chave']]
            r = cartao['rect']
            if r.collidepoint(mouse):
                r = r.inflate(16, 16)  # cresce quando o mouse está em cima

            painel(window, r, CREME, 255)
            texto(window, info['nome'], 48, info['cor'], (r.centerx, r.y + 55), contorno=3)

            # uma lâmpada para cada ajuda da fase: acesa = a criança vai ter essa ajuda
            ajudas = calcula_ajudas(ajudas_da_fase, cartao['chave'])
            for i in range(ajudas_da_fase):
                x = r.centerx + (i - (ajudas_da_fase - 1) / 2) * 60
                lampada(window, (int(x), r.y + 140), i < ajudas, 1.3)

            if ajudas == 1:
                frase = '1 ajuda por fase'
            elif ajudas == 0:
                frase = 'Sem ajudas'
            else:
                frase = f'{ajudas} ajudas por fase'
            texto(window, frase, 26, PRETO, (r.centerx, r.y + 210))
            texto(window, info['descricao'], 22, CINZA_ESCURO, (r.centerx, r.y + 250))

        texto(window, 'As ajudas explicam em qual lixeira vai cada lixo.', 26, BRANCO, (WIDTH / 2, 560),
              contorno=3)
        window.blit(botao_voltar.image, botao_voltar.rect)

        pygame.display.update()

    return state
# Fim Mateus
