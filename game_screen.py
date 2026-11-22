import math
import random
import pygame
# Mateus
from config import (WIDTH, HEIGHT, FPS, FASES, LIXEIRAS, ORDEM_LIXEIRAS, PONTOS_ACERTO, ESTEIRA_X_FIM,
                    BRANCO, PRETO, CINZA, CINZA_ESCURO, CREME, AMARELO_OURO, VERDE_OK, VERMELHO_ERRO,
                    AZUL_UI, LARANJA_UI, DIFICULDADES, INIT, GAME, RESULTADO, QUIT)
# Fim Mateus
from dados import CONJUNTOS
from desenho import texto, texto_paragrafo, quebrar_linhas, fonte, painel, escurecer_tela, lampada
from sprites import Botao, Lixo, Lixeira, Particula, TextoFlutuante
from cenarios import Esteira
# Mateus
from dificuldade_screen import calcula_ajudas
# Fim Mateus
from assets import tocar_som, tocar_musica, pausar_musica, continuar_musica, liga_desliga_som

# Regras da partida:
# * cada fase tem um número fixo de lixos (10, 10 e 15);
# * soltar na lixeira errada ou deixar cair da esteira conta como erro;
# * clicar (sem arrastar) num lixo mostra uma ajuda e PAUSA o jogo
# Mateus
#   (fácil = 2 ajudas por fase, médio = 1, difícil = nenhuma;
#   rever a ajuda de um mesmo lixo não gasta outra);
# Fim Mateus
# * ESC pausa o jogo.

# Estados da partida
CONTAGEM = 0  # contagem 3, 2, 1, JÁ!
JOGANDO = 1
DICA = 2  # janela de ajuda aberta (jogo parado)
PAUSA = 3  # menu de pausa (ESC)
FIM = 4  # todos os lixos já foram separados

ELOGIOS = ['Muito bem!', 'Isso aí!', 'Arrasou!', 'Perfeito!', 'Mandou bem!', 'Show!']
DISTANCIA_CLIQUE = 10  # se o mouse andar menos que isso, foi um clique (e não um arraste)


def distancia(ponto1, ponto2):
    dx = ponto1[0] - ponto2[0]
    dy = ponto1[1] - ponto2[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def sorteia_lixos(lista_lixos, quantidade):
    # Sorteia lixos sem repetir nenhum
    copia = lista_lixos[:]
    random.shuffle(copia)
    return copia[:quantidade]


def volta_para_esteira(lixo, todos_lixos):
    # Coloca o lixo de volta na esteira (quando é solto fora das lixeiras)
    lixo.estado = 'esteira'
    if lixo.x < 40:
        lixo.x = 40
    if lixo.x > ESTEIRA_X_FIM - 20:
        lixo.x = ESTEIRA_X_FIM - 20
    lixo.y = lixo.y_base
    lixo.atualiza_imagem()
    todos_lixos.add(lixo)


def registra_erro(partida, lixo, mensagem, lixeira_por_chave, todos_efeitos):
    partida['sequencia'] = 0
    partida['resultados'].append(False)
    lixeira_por_chave[lixo.lixeira_certa].destaque = 2.2  # a lixeira certa pisca
    partida['mensagem'] = mensagem
    partida['tempo_mensagem'] = 3.0
    todos_efeitos.add(TextoFlutuante('X', (lixo.x, lixo.y - 40), VERMELHO_ERRO, 46, 0.8))


def avalia(partida, lixo, lixeira, lixeira_por_chave, assets, todos_efeitos):
    # Confere se o lixo foi para a lixeira certa e dá a recompensa ou a explicação
    certa = lixeira_por_chave[lixo.lixeira_certa]
    if lixeira == certa:
        partida['sequencia'] += 1
        ganho = PONTOS_ACERTO + 20 * (partida['sequencia'] - 1)  # bônus por acertos seguidos
        partida['pontos'] += ganho
        partida['acertos'] += 1
        partida['resultados'].append(True)
        boca = lixeira.boca()
        lixo.voar_para(boca)
        lixeira.pulo = 0.5
        tocar_som(assets, 'acerto')
        for i in range(28):
            todos_efeitos.add(Particula(boca[0], boca[1], velocidade=380, vida=0.9))
        todos_efeitos.add(TextoFlutuante(random.choice(ELOGIOS), (boca[0], boca[1] - 70), VERDE_OK, 34))
        todos_efeitos.add(TextoFlutuante(f'+{ganho}', (boca[0], boca[1] - 30), AMARELO_OURO, 30))
    else:
        nome_certa = LIXEIRAS[certa.chave]['nome']
        mensagem = f"Ops! {lixo.dados['nome']} vai no {nome_certa}."
        registra_erro(partida, lixo, mensagem, lixeira_por_chave, todos_efeitos)
        lixo.voar_para(certa.boca())
        lixeira.tremor = 0.5
        tocar_som(assets, 'erro')


def pede_ajuda(partida, lixo, assets, todos_efeitos):
    # Devolve True se a janela de ajuda deve abrir
    if lixo.ajuda_vista:
        pass  # rever uma ajuda já usada não gasta outra
    elif partida['ajudas'] > 0:
        partida['ajudas'] -= 1
        lixo.ajuda_vista = True
    else:
        tocar_som(assets, 'erro')
        # Mateus
        if partida['ajudas_total'] == 0:
            mensagem = 'Sem ajudas no modo difícil!'
        else:
            mensagem = 'Acabaram as ajudas!'
        todos_efeitos.add(TextoFlutuante(mensagem, (lixo.x, lixo.y - 60), LARANJA_UI, 28))
        # Fim Mateus
        return False
    tocar_som(assets, 'dica')
    return True


def solta_proximo_lixo(partida, info, esteira, todos_lixos, assets, dt):
    # Coloca um novo lixo no começo da esteira quando houver espaço
    if len(partida['fila']) == 0:
        return
    partida['distancia_spawn'] += esteira.velocidade * dt
    esteira_vazia = True
    for lixo in todos_lixos:
        if lixo.estado == 'esteira':
            esteira_vazia = False
    if partida['distancia_spawn'] >= info['espacamento'] or (esteira_vazia and partida['distancia_spawn'] > 80):
        todos_lixos.add(Lixo(assets, partida['fila'].pop(), -40))
        partida['distancia_spawn'] = 0


# ----------------------------------------------------------------------------- desenhos

def desenha_hud(window, fase, info, partida):
    # Painel da esquerda: fase, pontuação e progresso
    painel(window, (16, 66, 380, 170), CREME, 235)
    texto(window, f'Fase {fase}', 40, AZUL_UI, (36, 76), 'topleft', contorno=2)
    # Eduardo
    # Recorde no canto direito do painel. Quando a criança passa dele,
    # a pontuação fica laranja e aparece o aviso "Recorde!"
    if partida['recorde'] > 0 and partida['pontos'] > partida['recorde']:
        texto(window, f"Pontuação: {partida['pontos']}", 28, LARANJA_UI, (36, 128), 'topleft')
        texto(window, 'Recorde!', 22, LARANJA_UI, (378, 132), 'topright', contorno=1)
    else:
        texto(window, f"Pontuação: {partida['pontos']}", 28, PRETO, (36, 128), 'topleft')
        texto(window, f"Recorde: {partida['recorde']}", 18, CINZA_ESCURO, (378, 137), 'topright')
    total = info['itens']
    feitos = len(partida['resultados'])
    texto(window, f"Lixos: {feitos}/{total}   Acertos: {partida['acertos']}", 22, CINZA_ESCURO, (36, 166), 'topleft')
    # uma bolinha por lixo: verde = acerto, vermelha = erro, cinza = ainda não veio
    passo = min(22, 340 / total)
    for i in range(total):
        cor = (205, 205, 210)
        if i < feitos:
            if partida['resultados'][i]:
                cor = VERDE_OK
            else:
                cor = VERMELHO_ERRO
        centro = (int(46 + i * passo), 212)
        pygame.draw.circle(window, cor, centro, int(passo / 2) - 1)
        pygame.draw.circle(window, PRETO, centro, int(passo / 2) - 1, 2)
    if partida['sequencia'] >= 3:
        texto(window, f"Sequência x{partida['sequencia']}!", 24, LARANJA_UI, (378, 86), 'topright', contorno=2)

    # Painel da direita: ajudas e instruções
    painel(window, (884, 66, 380, 170), CREME, 235)
    texto(window, 'Ajudas:', 30, PRETO, (904, 80), 'topleft')
    # Mateus
    if partida['ajudas_total'] == 0:
        texto(window, 'nenhuma', 26, VERMELHO_ERRO, (1020, 84), 'topleft')
    for i in range(partida['ajudas_total']):
        lampada(window, (1060 + i * 48, 98), i < partida['ajudas'], 0.9)
    # Fim Mateus
    texto(window, 'Arraste o lixo até a lixeira certa.', 19, CINZA_ESCURO, (904, 140), 'topleft')
    # Mateus
    if partida['ajudas_total'] > 0:
        texto(window, 'Clique no lixo para ver uma ajuda.', 19, CINZA_ESCURO, (904, 168), 'topleft')
    else:
        texto(window, 'Modo difícil: sem ajudas!', 19, CINZA_ESCURO, (904, 168), 'topleft')
    # Fim Mateus
    texto(window, 'ESC: pausar o jogo', 19, CINZA_ESCURO, (904, 196), 'topleft')

    segundos = int(partida['tempo_restante'])

    if partida['tempo_restante'] > segundos:
        segundos += 1

    painel(window, (440, 66, 400, 110), CREME, 235)
    
    texto(window, f'Tempo: {segundos}s', 36, PRETO, (WIDTH/2, 121))


def desenha_mensagem(window, partida):
    # Faixa vermelha que aparece depois de um erro
    alpha = min(1.0, partida['tempo_mensagem'] * 2)
    largura = fonte(28).size(partida['mensagem'])[0] + 60
    r = pygame.Rect(0, 0, largura, 56)
    r.center = (WIDTH / 2, 254 - (1 - alpha) * 20)
    painel(window, r, (255, 235, 235), int(240 * alpha), 16, 4, VERMELHO_ERRO)
    texto(window, partida['mensagem'], 28, VERMELHO_ERRO, r.center)


# Mateus
def desenha_contagem(window, fase, info, partida, tempo_estado):
    # Fim Mateus
    escurecer_tela(window, 110)
    texto(window, f'FASE {fase}', 90, AMARELO_OURO, (WIDTH / 2, 200), contorno=5)
    texto(window, info['subtitulo'], 36, BRANCO, (WIDTH / 2, 285), contorno=3)
    # Mateus
    nome_dificuldade = DIFICULDADES[partida['dificuldade']]['nome']
    if partida['ajudas_total'] == 1:
        frase_ajudas = '1 ajuda'
    elif partida['ajudas_total'] == 0:
        frase_ajudas = 'sem ajudas'
    else:
        frase_ajudas = f"{partida['ajudas_total']} ajudas"
    texto(window, f"{info['itens']} lixos   •   {frase_ajudas}   •   {nome_dificuldade}", 28, BRANCO,
          (WIDTH / 2, 335), contorno=3)
    # Fim Mateus
    numero = int(tempo_estado / 0.8)
    rotulos = ['3', '2', '1', 'JÁ!']
    rotulo = rotulos[min(3, numero)]
    fracao = (tempo_estado % 0.8) / 0.8
    if rotulo == 'JÁ!':
        cor = VERDE_OK
    else:
        cor = BRANCO
    texto(window, rotulo, int(140 - fracao * 40), cor, (WIDTH / 2, 470), contorno=6)


def desenha_secao(window, titulo, conteudo, x, y, largura):
    texto(window, titulo, 26, AZUL_UI, (x, y), 'topleft')
    return texto_paragrafo(window, conteudo, 23, PRETO, (x, y + 36), largura) + 18


def desenha_dica(window, assets, lixo, ajudas, tempo_estado, botao_entendi):
    escurecer_tela(window, 160)
    dados_lixo = lixo.dados
    cartao = pygame.Rect(200, 70, 880, 590)
    painel(window, cartao, CREME, 255, 26, 5)
    texto(window, 'AJUDA', 30, LARANJA_UI, (cartao.centerx, cartao.y + 30), contorno=2)

    # coluna da esquerda: desenho grande do lixo balançando
    cx = cartao.x + 190
    cy = cartao.y + 230
    pygame.draw.circle(window, (255, 230, 170), (cx, cy), 125)
    pygame.draw.circle(window, PRETO, (cx, cy), 125, 4)
    balanco = math.sin(tempo_estado * 3) * 6
    imagem = pygame.transform.rotozoom(assets['itens_grandes'][dados_lixo['desenho']], balanco, 1)
    rect = imagem.get_rect()
    rect.center = (cx, cy)
    window.blit(imagem, rect)
    linhas = quebrar_linhas(dados_lixo['nome'], 34, 330)
    for i in range(len(linhas)):
        texto(window, linhas[i], 34, PRETO, (cx, cy + 160 + i * 40))

    # coluna da direita: explicações
    x = cartao.x + 400
    y = cartao.y + 70
    y = desenha_secao(window, 'O que é?', dados_lixo['oque'], x, y, 450)
    y = desenha_secao(window, 'Do que é feito?', dados_lixo['material'], x, y, 450)
    texto(window, 'Vai na lixeira:', 26, AZUL_UI, (x, y), 'topleft')
    info = LIXEIRAS[dados_lixo['lixeira']]
    selo = pygame.Rect(x + 210, y - 6, 190, 42)
    pygame.draw.rect(window, info['cor'], selo, border_radius=14)
    pygame.draw.rect(window, PRETO, selo, 3, border_radius=14)
    texto(window, info['nome'], 26, BRANCO, selo.center, contorno=2)
    desenha_secao(window, 'Por quê?', dados_lixo['porque'], x, y + 56, 450)

    texto(window, f'Ajudas restantes: {ajudas}', 22, CINZA_ESCURO, (cartao.x + 30, cartao.bottom - 30), 'bottomleft')
    texto(window, '(jogo pausado)', 20, CINZA, (cartao.right - 30, cartao.bottom - 30), 'bottomright')
    window.blit(botao_entendi.image, botao_entendi.rect)


def desenha_pausa(window, botoes_pausa):
    escurecer_tela(window, 170)
    painel(window, (WIDTH / 2 - 230, 160, 460, 420), CREME, 250)
    texto(window, 'JOGO PAUSADO', 46, AZUL_UI, (WIDTH / 2, 225), contorno=3)
    botoes_pausa.draw(window)
    texto(window, 'Aperte ESC para continuar', 22, CINZA_ESCURO, (WIDTH / 2, 560))


# ----------------------------------------------------------------------------- tela

def game_screen(window, assets, dados):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    fase = dados['fase']
    info = FASES[fase]
    distancia_fila = (info['itens'] - 1) * info['espacamento']
    percurso = ESTEIRA_X_FIM + 40

    tempo_limite = (distancia_fila + percurso) / info['velocidade']

    total = info['itens']
    # Mateus
    # quantas ajudas a criança tem nesta fase depende da dificuldade escolhida
    ajudas_total = calcula_ajudas(info['ajudas'], dados['dificuldade'])
    # Fim Mateus

    continuar_musica()
    tocar_musica(assets, f'musica_fase{fase}')

    # ----- Cria a esteira e as lixeiras
    esteira = Esteira(info['velocidade'])
    todas_lixeiras = pygame.sprite.Group()
    lixeira_por_chave = {}
    largura_espaco = WIDTH / (len(ORDEM_LIXEIRAS) + 1)
    for i in range(len(ORDEM_LIXEIRAS)):
        chave = ORDEM_LIXEIRAS[i]
        nova_lixeira = Lixeira(chave, largura_espaco * (i + 1), HEIGHT - 14)
        todas_lixeiras.add(nova_lixeira)
        lixeira_por_chave[chave] = nova_lixeira

    # ----- Grupos de sprites
    todos_lixos = pygame.sprite.Group()  # lixos na esteira, voando ou caindo
    todos_efeitos = pygame.sprite.Group()  # confetes e textos que sobem

    # ----- Dados da partida
    partida = {
        'fila': sorteia_lixos(CONJUNTOS[info['conjunto']], total),  # lixos que ainda vão aparecer
        'resultados': [],  # True (acerto) ou False (erro) para cada lixo
        'acertos': 0,
        'pontos': 0,
        'sequencia': 0,  # acertos seguidos
        # Mateus
        'dificuldade': dados['dificuldade'],
        'ajudas_total': ajudas_total,  # ajudas que a fase começa (depende da dificuldade)
        'ajudas': ajudas_total,  # ajudas que ainda restam
        # Fim Mateus
        'distancia_spawn': info['espacamento'],  # já começa pronto para soltar o 1º lixo
        'mensagem': '',  # faixa educativa que aparece depois de um erro
        'tempo_mensagem': 0,
        'tempo_restante': tempo_limite,
        # Eduardo
        # recorde da fase quando a partida começou (para mostrar no painel)
        'recorde': dados['progresso']['recordes'][fase]
    }
    segurando = None  # lixo que está preso no mouse
    pos_clique = (0, 0)
    desloc_mouse = (0, 0)
    lixo_dica = None  # lixo mostrado na janela de ajuda

    # ----- Botões
    botao_entendi = Botao((WIDTH / 2, 610), 260, 66, 'ENTENDI!', VERDE_OK, 32)
    botao_continuar = Botao((WIDTH / 2, 330), 340, 70, 'CONTINUAR', VERDE_OK, 32)
    botao_recomecar = Botao((WIDTH / 2, 420), 340, 70, 'RECOMEÇAR FASE', LARANJA_UI, 30)
    botao_menu = Botao((WIDTH / 2, 510), 340, 70, 'MENU PRINCIPAL', VERMELHO_ERRO, 30)
    botoes_pausa = pygame.sprite.Group()
    botoes_pausa.add(botao_continuar)
    botoes_pausa.add(botao_recomecar)
    botoes_pausa.add(botao_menu)

    state = CONTAGEM
    state_antes_pausa = CONTAGEM
    tempo_estado = 0  # segundos desde que entrou no estado atual
    contagem_som = -1
    proxima_tela = RESULTADO

    # ===== Loop principal =====
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)

        # ----- Trata eventos
        for event in pygame.event.get():
            alternar_pausa = False

            if event.type == pygame.QUIT:
                proxima_tela = QUIT
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                liga_desliga_som(assets)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                alternar_pausa = True

            elif state == PAUSA:
                if botao_continuar.clicado(event):
                    alternar_pausa = True
                elif botao_recomecar.clicado(event):
                    tocar_som(assets, 'clique')
                    continuar_musica()
                    proxima_tela = GAME
                    running = False
                elif botao_menu.clicado(event):
                    tocar_som(assets, 'clique')
                    continuar_musica()
                    proxima_tela = INIT
                    running = False

            elif state == DICA:
                fechar = botao_entendi.clicado(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        fechar = True
                if fechar:
                    tocar_som(assets, 'clique')
                    state = JOGANDO
                    tempo_estado = 0

            elif state == JOGANDO:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # pega o lixo de cima (o último desenhado) que estiver embaixo do mouse
                    lista = todos_lixos.sprites()
                    i = len(lista) - 1
                    while i >= 0 and segurando == None:
                        lixo = lista[i]
                        if lixo.estado == 'esteira' and lixo.area_clique().collidepoint(event.pos):
                            segurando = lixo
                            pos_clique = event.pos
                            desloc_mouse = (lixo.x - event.pos[0], lixo.y - event.pos[1])
                            lixo.estado = 'arrastando'
                            todos_lixos.remove(lixo)  # enquanto está na mão, fica fora do grupo
                        i -= 1

                elif event.type == pygame.MOUSEMOTION and segurando != None:
                    if distancia(event.pos, pos_clique) >= DISTANCIA_CLIQUE:
                        segurando.x = event.pos[0] + desloc_mouse[0]
                        segurando.y = event.pos[1] + desloc_mouse[1]

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and segurando != None:
                    lixo = segurando
                    segurando = None
                    if distancia(event.pos, pos_clique) < DISTANCIA_CLIQUE:
                        # foi só um clique: mostra a ajuda
                        lixo.estado = 'esteira'
                        todos_lixos.add(lixo)
                        if pede_ajuda(partida, lixo, assets, todos_efeitos):
                            lixo_dica = lixo
                            state = DICA
                            tempo_estado = 0
                    else:
                        # soltou o lixo: em qual lixeira?
                        alvo = None
                        for lixeira in todas_lixeiras:
                            if lixeira.area_soltar().collidepoint(event.pos):
                                alvo = lixeira
                        if alvo == None:
                            volta_para_esteira(lixo, todos_lixos)
                        else:
                            todos_lixos.add(lixo)
                            avalia(partida, lixo, alvo, lixeira_por_chave, assets, todos_efeitos)

            # ----- Verifica consequências: pausar ou continuar
            if alternar_pausa and state != FIM:
                if state == PAUSA:
                    state = state_antes_pausa
                    continuar_musica()
                else:
                    if segurando != None:  # se estava arrastando algo, devolve para a esteira
                        volta_para_esteira(segurando, todos_lixos)
                        segurando = None
                    state_antes_pausa = state
                    state = PAUSA
                    pausar_musica()
                tocar_som(assets, 'pausa')

        # ----- Atualiza estado do jogo
        assets['fundo_interno'].update(dt)
        botoes_pausa.update(dt)
        botao_entendi.update(dt)
        tempo_estado += dt

        if state == CONTAGEM:
            numero = int(tempo_estado / 0.8)
            if numero != contagem_som and numero <= 3:
                contagem_som = numero
                if numero == 3:
                    tocar_som(assets, 'vai')
                else:
                    tocar_som(assets, 'contagem')
            if tempo_estado >= 3.4:
                state = JOGANDO
                tempo_estado = 0

        elif state == JOGANDO or state == FIM:
            esteira.update(dt)
            if state == JOGANDO:
                if len(partida['resultados']) < total:
                    partida['tempo_restante'] -= dt

                if partida['tempo_restante'] <= 0:
                    dados['acertos'] = partida['acertos']
                    dados['total'] = total
                    dados['pontos'] = partida['pontos']

                    return RESULTADO 

                solta_proximo_lixo(partida, info, esteira, todos_lixos, assets, dt)

            # lixeiras abrem a tampa quando um lixo arrastado passa por cima
            mouse = pygame.mouse.get_pos()
            for lixeira in todas_lixeiras:
                lixeira.abrir = segurando != None and lixeira.area_soltar().collidepoint(mouse)
            todas_lixeiras.update(dt)

            todos_lixos.update(dt, esteira.velocidade)
            if segurando != None:
                segurando.update(dt, esteira.velocidade)

            # lixo que chegou no fim da esteira cai e conta como erro
            for lixo in todos_lixos:
                if lixo.estado == 'esteira' and lixo.x > ESTEIRA_X_FIM:
                    lixo.cair()
                    tocar_som(assets, 'caiu')
                    nome_certa = LIXEIRAS[lixo.lixeira_certa]['nome']
                    mensagem = f"Ih, caiu! {lixo.dados['nome']} vai no {nome_certa}."
                    registra_erro(partida, lixo, mensagem, lixeira_por_chave, todos_efeitos)

            todos_efeitos.update(dt)
            partida['tempo_mensagem'] = max(0, partida['tempo_mensagem'] - dt)

            terminou = len(partida['resultados']) == total and len(todos_lixos) == 0 and segurando == None
            if state == JOGANDO and terminou:
                state = FIM
                tempo_estado = 0
            elif state == FIM and tempo_estado > 1.2:
                # guarda o resultado para a tela de resultado
                dados['acertos'] = partida['acertos']
                dados['total'] = total
                dados['pontos'] = partida['pontos']
                proxima_tela = RESULTADO
                running = False

        # ----- Gera saídas
        assets['fundo_interno'].draw(window)
        desenha_hud(window, fase, info, partida)
        esteira.draw(window)
        todas_lixeiras.draw(window)
        todos_lixos.draw(window)
        for lixo in todos_lixos:  # lâmpada em cima dos lixos que já tiveram ajuda
            if lixo.ajuda_vista and lixo.estado == 'esteira':
                lampada(window, (int(lixo.x + 32), int(lixo.y - 34)), True, 0.55)
        todos_efeitos.draw(window)

        if segurando != None:  # o lixo na mão é desenhado por cima de tudo, com sombra
            sombra = pygame.Surface((70, 22), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra, (0, 0, 0, 70), sombra.get_rect())
            window.blit(sombra, (segurando.x - 35, segurando.y + 45))
            window.blit(segurando.image, segurando.rect)
            if segurando.ajuda_vista:
                lampada(window, (int(segurando.x + 32), int(segurando.y - 34)), True, 0.55)

        if partida['tempo_mensagem'] > 0:
            desenha_mensagem(window, partida)

        if state == CONTAGEM:
            # Mateus
            desenha_contagem(window, fase, info, partida, tempo_estado)
            # Fim Mateus
        elif state == DICA:
            desenha_dica(window, assets, lixo_dica, partida['ajudas'], tempo_estado, botao_entendi)
        elif state == PAUSA:
            desenha_pausa(window, botoes_pausa)

        pygame.display.update()  # Mostra o novo frame para o jogador

    return proxima_tela
