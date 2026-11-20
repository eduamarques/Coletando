import math
import pygame
from config import PRETO, BRANCO, AMARELO_OURO, LIXEIRAS

# Dicionário com as fontes já carregadas (chave = tamanho da fonte).
# Assim cada tamanho de fonte é carregado uma vez só.
FONTES = {}
NOMES_FONTES = 'arialroundedmtbold,comicsansms,trebuchetms,verdana,arial'


def fonte(tamanho):
    # Devolve uma fonte arredondada e amigável no tamanho pedido
    if tamanho < 1:
        tamanho = 1
    if tamanho not in FONTES:
        FONTES[tamanho] = pygame.font.SysFont(NOMES_FONTES, tamanho, bold=True)
    return FONTES[tamanho]


def ajusta_cor(cor, quantidade):
    # Deixa a cor mais clara (quantidade positiva) ou mais escura (quantidade negativa)
    nova_cor = []
    for valor in cor:
        valor = valor + quantidade
        if valor > 255:
            valor = 255
        if valor < 0:
            valor = 0
        nova_cor.append(valor)
    return nova_cor


def imagem_texto(conteudo, tamanho, cor, contorno=0, cor_contorno=PRETO):
    # Cria a imagem de um texto. Se contorno > 0, desenha uma borda escura
    # em volta das letras (estilo desenho animado).
    f = fonte(tamanho)
    letras = f.render(str(conteudo), True, cor)
    if contorno == 0:
        return letras

    borda = f.render(str(conteudo), True, cor_contorno)
    largura = letras.get_width() + 2 * contorno
    altura = letras.get_height() + 2 * contorno
    imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
    # Desenha a borda deslocada para todos os lados e as letras por cima, no meio
    for dx in [0, contorno, 2 * contorno]:
        for dy in [0, contorno, 2 * contorno]:
            if dx != contorno or dy != contorno:
                imagem.blit(borda, (dx, dy))
    imagem.blit(letras, (contorno, contorno))
    return imagem


def texto(window, conteudo, tamanho, cor, pos, ancora='center', contorno=0):
    # Escreve um texto na tela. A ancora diz qual ponto do texto fica em pos.
    # Devolve o retângulo (rect) usado.
    imagem = imagem_texto(conteudo, tamanho, cor, contorno)
    rect = imagem.get_rect()
    if ancora == 'center':
        rect.center = pos
    elif ancora == 'topleft':
        rect.topleft = pos
    elif ancora == 'topright':
        rect.topright = pos
    elif ancora == 'bottomleft':
        rect.bottomleft = pos
    elif ancora == 'bottomright':
        rect.bottomright = pos
    window.blit(imagem, rect)
    return rect


def quebrar_linhas(conteudo, tamanho, largura_max):
    # Divide um texto em linhas que caibam em largura_max pixels
    f = fonte(tamanho)
    linhas = []
    atual = ''
    for palavra in conteudo.split():
        teste = (atual + ' ' + palavra).strip()
        if f.size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual != '':
        linhas.append(atual)
    return linhas


def texto_paragrafo(window, conteudo, tamanho, cor, topo_esquerdo, largura_max):
    # Escreve um parágrafo com quebra de linha automática. Devolve o y final.
    x = topo_esquerdo[0]
    y = topo_esquerdo[1]
    for linha in quebrar_linhas(conteudo, tamanho, largura_max):
        rect = texto(window, linha, tamanho, cor, (x, y), 'topleft')
        y = rect.bottom + 4
    return y


def painel(window, rect, cor=(255, 255, 255), alpha=235, raio=18, borda=4, cor_borda=PRETO):
    # Caixa arredondada com sombra, usada como fundo de menus e cartões
    rect = pygame.Rect(rect)
    sombra = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(sombra, (0, 0, 0, 90), sombra.get_rect(), border_radius=raio)
    window.blit(sombra, rect.move(6, 8))

    caixa = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (cor[0], cor[1], cor[2], alpha), caixa.get_rect(), border_radius=raio)
    window.blit(caixa, rect)
    if borda > 0:
        pygame.draw.rect(window, cor_borda, rect, borda, border_radius=raio)


def escurecer_tela(window, alpha=150):
    # Cobre a tela com uma camada escura (usado em pausas e janelas de ajuda)
    camada = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    camada.fill((0, 0, 0, alpha))
    window.blit(camada, (0, 0))


def pontos_estrela(centro, raio_externo, raio_interno, rotacao=0):
    # Calcula os 10 vértices de uma estrela de 5 pontas
    pontos = []
    for i in range(10):
        if i % 2 == 0:
            r = raio_externo
        else:
            r = raio_interno
        angulo = -math.pi / 2 + i * math.pi / 5 + rotacao
        pontos.append((centro[0] + r * math.cos(angulo), centro[1] + r * math.sin(angulo)))
    return pontos


def estrela(window, centro, raio, cheia=True, rotacao=0):
    # Desenha uma estrela dourada (cheia) ou cinza (vazia)
    pontos = pontos_estrela(centro, raio, raio * 0.45, rotacao)
    if cheia:
        pygame.draw.polygon(window, AMARELO_OURO, pontos)
        centro_brilho = (centro[0] - raio * 0.08, centro[1] - raio * 0.1)
        brilho = pontos_estrela(centro_brilho, raio * 0.45, raio * 0.2, rotacao)
        pygame.draw.polygon(window, (255, 240, 150), brilho)
    else:
        pygame.draw.polygon(window, (150, 150, 160), pontos)
    espessura = int(raio / 9)
    if espessura < 2:
        espessura = 2
    pygame.draw.polygon(window, PRETO, pontos, espessura)


def lampada(window, centro, acesa=True, tamanho=1.0):
    # Ícone de lâmpada que representa uma ajuda disponível
    x = centro[0]
    y = centro[1]
    r = int(16 * tamanho)
    if acesa:
        brilho = pygame.Surface((r * 5, r * 5), pygame.SRCALPHA)
        pygame.draw.circle(brilho, (255, 240, 120, 90), (r * 2.5, r * 2.5), r * 2)
        window.blit(brilho, (x - r * 2.5, y - r * 2.5))
        cor = (255, 225, 60)
    else:
        cor = (170, 170, 175)
    pygame.draw.circle(window, cor, (x, y), r)
    pygame.draw.circle(window, PRETO, (x, y), r, 3)
    base = pygame.Rect(0, 0, int(r * 1.1), int(r * 0.8))
    base.midtop = (x, y + r - 3)
    pygame.draw.rect(window, (150, 150, 160), base, border_radius=3)
    pygame.draw.rect(window, PRETO, base, 2, border_radius=3)
    if acesa:
        pygame.draw.arc(window, BRANCO, (x - r * 0.6, y - r * 0.6, r * 0.8, r * 0.8), 1.6, 3.0, 3)


def simbolo_reciclagem(window, centro, raio, cor=BRANCO, espessura=5):
    # Três setas girando em círculo: o símbolo da reciclagem
    cx = centro[0]
    cy = centro[1]
    caixa = pygame.Rect(cx - raio, cy - raio, raio * 2, raio * 2)
    for i in range(3):
        inicio = math.radians(90 + i * 120 + 15)
        fim = inicio + math.radians(80)
        pygame.draw.arc(window, cor, caixa, inicio, fim, espessura)
        # ponta da seta no fim do arco (o pygame mede ângulos com y para cima)
        px = cx + raio * math.cos(fim)
        py = cy - raio * math.sin(fim)
        dx = math.cos(fim + math.pi / 2)
        dy = -math.sin(fim + math.pi / 2)
        nx = math.cos(fim)
        ny = -math.sin(fim)
        t = espessura * 1.6
        pygame.draw.polygon(window, cor, [(px + dx * t * 1.4, py + dy * t * 1.4),
                                          (px + nx * t, py + ny * t),
                                          (px - nx * t, py - ny * t)])


def lixeira(window, rect, chave, abertura=0, destaque=False):
    # Desenha uma lixeira colorida de coleta seletiva.
    # abertura vai de 0 (tampa fechada) a 1 (tampa aberta).
    # destaque desenha um brilho em volta (ex.: lixeira certa depois de um erro).
    info = LIXEIRAS[chave]
    cor = info['cor']
    escura = ajusta_cor(cor, -55)
    clara = ajusta_cor(cor, 50)
    rect = pygame.Rect(rect)

    if destaque:
        brilho = pygame.Surface((rect.w + 40, rect.h + 40), pygame.SRCALPHA)
        pygame.draw.rect(brilho, (255, 255, 150, 140), brilho.get_rect(), border_radius=30)
        window.blit(brilho, (rect.x - 20, rect.y - 20))

    # corpo (trapézio um pouco mais estreito embaixo)
    topo = rect.y + 22
    corpo = [(rect.x + 6, topo), (rect.right - 6, topo), (rect.right - 16, rect.bottom), (rect.x + 16, rect.bottom)]
    pygame.draw.polygon(window, cor, corpo)
    pygame.draw.polygon(window, escura, [(rect.right - 30, topo), (rect.right - 6, topo),
                                         (rect.right - 16, rect.bottom), (rect.right - 36, rect.bottom)])
    pygame.draw.polygon(window, clara, [(rect.x + 14, topo + 6), (rect.x + 24, topo + 6),
                                        (rect.x + 30, rect.bottom - 8), (rect.x + 22, rect.bottom - 8)])
    pygame.draw.polygon(window, PRETO, corpo, 4)

    # boca escura (aparece quando a tampa abre)
    if abertura > 0.05:
        pygame.draw.rect(window, (30, 30, 35), (rect.x + 8, topo - 4, rect.w - 16, 10), border_radius=4)

    # tampa: sobe conforme a abertura
    sobe = int(abertura * 26)
    tampa = pygame.Rect(rect.x, topo - 18 - sobe, rect.w, 18 - int(abertura * 8))
    pygame.draw.rect(window, clara, tampa, border_radius=8)
    pygame.draw.rect(window, PRETO, tampa, 4, border_radius=8)
    alca = pygame.Rect(0, 0, 40, 10)
    alca.midbottom = (tampa.centerx, tampa.y + 2)
    pygame.draw.rect(window, escura, alca, border_radius=4)
    pygame.draw.rect(window, PRETO, alca, 3, border_radius=4)

    simbolo_reciclagem(window, (rect.centerx, topo + 48), 24, BRANCO, 6)
    if len(info['nome']) <= 7:
        tamanho = 22
    else:
        tamanho = 19
    texto(window, info['nome'], tamanho, BRANCO, (rect.centerx, rect.bottom - 30), contorno=2)
