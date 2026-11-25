"""
Desenhos dos lixos, feitos só com formas geométricas do pygame.

Cada função recebe uma superfície 100x100 transparente e desenha o objeto nela.
As imagens prontas são criadas uma vez só, em assets.py (load_assets).
"""

import math

import pygame

CONTORNO = (45, 45, 60)
TRANSPARENTE = (0, 0, 0, 0)


# --- Atalhos: preenchem a forma e desenham o contorno escuro por cima ---------

def retangulo(s, cor, rect, raio=0, borda=3):
                # s = Surface, genérica, sempre utilizada a mesma
                # rect = Dimensões do retângulo (x, y, largura, altura)
    pygame.draw.rect(s, cor, rect, border_radius=raio)     
    pygame.draw.rect(s, CONTORNO, rect, borda, border_radius=raio)


def elipse(s, cor, rect, borda=3):
    pygame.draw.ellipse(s, cor, rect)
    if borda > 0:
        pygame.draw.ellipse(s, CONTORNO, rect, borda)


def poligono(s, cor, pontos, borda=3):
    pygame.draw.polygon(s, cor, pontos)
    if borda > 0:
        pygame.draw.polygon(s, CONTORNO, pontos, borda)


def circulo(s, cor, centro, raio, borda=3):
    pygame.draw.circle(s, cor, centro, raio)
    if borda > 0:
        pygame.draw.circle(s, CONTORNO, centro, raio, borda)


def brilho(s, x1, y1, x2, y2):
    """Risquinho branco que dá impressão de objeto brilhante."""
    pygame.draw.line(s, (255, 255, 255, 200), (x1, y1), (x2, y2), 4)        # (Base, cor, ponto inicial, ponto final, espessura)


# =============================== PLÁSTICO ===================================

def garrafa_pet(s):
    poligono(s, (170, 220, 245, 210), [(40, 30), (60, 30), (56, 16), (44, 16)])
    retangulo(s, (170, 220, 245, 210), (32, 28, 36, 64), 10)
    retangulo(s, (30, 90, 200), (42, 6, 16, 11), 3)
    retangulo(s, (225, 60, 60), (32, 50, 36, 16), 0)
    brilho(s, 38, 34, 38, 46)
    brilho(s, 38, 70, 38, 84)


def sacola(s):
    pygame.draw.arc(s, CONTORNO, (24, 8, 22, 44), 0, math.pi, 5)
    pygame.draw.arc(s, CONTORNO, (54, 8, 22, 44), 0, math.pi, 5)
    poligono(s, (240, 240, 248), [(20, 32), (80, 32), (86, 92), (14, 92)])
    pygame.draw.line(s, (190, 190, 200), (34, 44), (30, 84), 2)
    pygame.draw.line(s, (190, 190, 200), (66, 46), (72, 84), 2)
    circulo(s, (60, 180, 90), (50, 62), 9, 2)


def copo_plastico(s):
    poligono(s, (248, 248, 252), [(26, 18), (74, 18), (66, 92), (34, 92)])
    pygame.draw.line(s, (90, 160, 230), (29, 36), (71, 36), 5)
    pygame.draw.line(s, (90, 160, 230), (31, 52), (69, 52), 5)
    retangulo(s, (230, 230, 238), (22, 12, 56, 9), 3)


def pote_iogurte(s):
    poligono(s, (250, 195, 215), [(24, 32), (76, 32), (70, 90), (30, 90)])
    circulo(s, (225, 50, 70), (50, 60), 10, 2)
    pygame.draw.line(s, (60, 160, 60), (50, 50), (54, 45), 3)
    elipse(s, (205, 205, 215), (19, 22, 62, 17))


# ================================ PAPEL =====================================

def jornal(s):
    retangulo(s, (238, 236, 225), (14, 20, 72, 62), 2)
    pygame.draw.rect(s, (70, 70, 80), (20, 26, 60, 8))
    pygame.draw.rect(s, (160, 160, 170), (20, 40, 26, 22))
    for y in range(40, 76, 6):
        pygame.draw.line(s, (130, 130, 140), (52, y), (80, y), 2)
    for y in range(66, 78, 6):
        pygame.draw.line(s, (130, 130, 140), (20, y), (46, y), 2)


def caixa(s):
    poligono(s, (225, 180, 120), [(16, 40), (72, 40), (86, 26), (30, 26)])
    poligono(s, (165, 115, 65), [(72, 40), (86, 26), (86, 74), (72, 88)])
    retangulo(s, (200, 150, 90), (16, 40, 56, 48), 0)
    pygame.draw.line(s, (240, 220, 170), (44, 40), (58, 26), 6)
    pygame.draw.rect(s, CONTORNO, (30, 56, 28, 10), 2)


def folha(s):
    retangulo(s, (252, 252, 252), (24, 8, 52, 84), 2)
    for y in range(22, 90, 9):
        pygame.draw.line(s, (130, 180, 235), (26, y), (74, y), 2)
    pygame.draw.line(s, (230, 90, 90), (36, 10), (36, 90), 2)
    for y in (22, 50, 78):
        circulo(s, (220, 220, 225), (30, y), 3, 1)


def rolo(s):
    elipse(s, (190, 145, 95), (30, 70, 40, 16))
    pygame.draw.rect(s, (210, 170, 120), (30, 26, 40, 52))
    pygame.draw.line(s, CONTORNO, (30, 26), (30, 78), 3)
    pygame.draw.line(s, CONTORNO, (69, 26), (69, 78), 3)
    pygame.draw.line(s, (180, 135, 90), (32, 40), (68, 56), 3)
    elipse(s, (225, 190, 145), (30, 18, 40, 16))
    elipse(s, (110, 75, 45), (38, 21, 24, 9), 0)


# ================================ VIDRO =====================================

def garrafa_vidro(s):
    vidro = (70, 170, 95, 220)
    retangulo(s, vidro, (42, 12, 16, 34), 3)
    poligono(s, vidro, [(42, 40), (58, 40), (66, 52), (34, 52)])
    retangulo(s, vidro, (34, 48, 32, 46), 8)
    retangulo(s, (230, 190, 70), (41, 5, 18, 9), 2)
    retangulo(s, (250, 240, 210), (34, 60, 32, 18), 0, 2)
    brilho(s, 39, 54, 39, 88)


def pote_vidro(s):
    retangulo(s, (200, 235, 240, 170), (24, 30, 52, 62), 12)
    pygame.draw.rect(s, (170, 40, 90), (29, 48, 42, 38), border_radius=8)
    brilho(s, 32, 38, 32, 56)
    retangulo(s, (225, 185, 60), (21, 18, 58, 15), 4)
    retangulo(s, (250, 245, 225), (34, 56, 32, 14), 0, 2)


def perfume(s):
    retangulo(s, (245, 175, 225, 210), (26, 42, 48, 46), 14)
    pygame.draw.rect(s, (230, 120, 200, 220), (30, 60, 40, 24), border_radius=10)
    retangulo(s, (230, 190, 70), (43, 30, 14, 14), 2)
    circulo(s, (150, 80, 200), (50, 22), 10)
    brilho(s, 33, 50, 33, 64)


# ================================ METAL =====================================

def lata(s):
    retangulo(s, (225, 45, 45), (32, 14, 36, 76), 6)
    pygame.draw.lines(s, (255, 255, 255), False, [(33, 50), (42, 44), (52, 54), (67, 46)], 4)
    elipse(s, (205, 210, 220), (32, 8, 36, 12))
    elipse(s, (205, 210, 220), (32, 84, 36, 10))
    brilho(s, 38, 22, 38, 40)


def lata_conserva(s):
    retangulo(s, (195, 200, 210), (22, 22, 56, 66), 4)
    retangulo(s, (250, 215, 60), (22, 38, 56, 34), 0)
    for x in (38, 50, 62):
        circulo(s, (245, 200, 40), (x, 55), 6, 2)
    circulo(s, (70, 170, 70), (50, 47), 4, 0)
    elipse(s, (215, 220, 228), (22, 16, 56, 12))


def panela(s):
    retangulo(s, (60, 60, 70), (4, 42, 22, 9), 4)
    retangulo(s, (60, 60, 70), (74, 42, 22, 9), 4)
    retangulo(s, (175, 180, 190), (22, 38, 56, 44), 8)
    retangulo(s, (205, 210, 220), (18, 34, 64, 9), 4)
    brilho(s, 30, 50, 30, 72)
    pygame.draw.circle(s, (120, 120, 130), (60, 66), 4)


def chave(s):
    retangulo(s, (230, 190, 60), (42, 45, 48, 11), 3)
    retangulo(s, (230, 190, 60), (68, 54, 7, 14), 0)
    retangulo(s, (230, 190, 60), (80, 54, 7, 20), 0)
    circulo(s, (230, 190, 60), (28, 50), 18)
    circulo(s, (255, 255, 255, 0), (24, 50), 6)
    brilho(s, 20, 40, 28, 36)


# =============================== ORGÂNICO ===================================

def banana(s):
    amarelo = (250, 220, 70)
    poligono(s, amarelo, [(46, 22), (30, 58), (20, 88), (38, 72), (50, 44)])
    poligono(s, amarelo, [(54, 22), (72, 58), (82, 86), (64, 72), (50, 44)])
    poligono(s, (240, 205, 55), [(44, 22), (56, 22), (58, 92), (44, 92)])
    retangulo(s, (120, 85, 40), (45, 8, 10, 16), 3)
    for p in ((50, 60), (30, 74), (70, 70), (52, 80)):
        pygame.draw.circle(s, (130, 90, 40), p, 3)


def maca(s):
    elipse(s, (220, 45, 45), (26, 64, 48, 26))
    retangulo(s, (252, 240, 200), (37, 28, 26, 44), 8)
    elipse(s, (220, 45, 45), (26, 12, 48, 26))
    for y in (44, 54):
        pygame.draw.ellipse(s, (90, 50, 30), (45, y, 6, 9))
    pygame.draw.line(s, (110, 70, 40), (50, 14), (54, 2), 4)
    elipse(s, (80, 180, 70), (54, 2, 20, 10), 2)


def ovo(s):
    casca = (252, 245, 225)
    elipse(s, casca, (10, 36, 48, 56))
    pygame.draw.polygon(s, TRANSPARENTE, [(0, 0), (70, 0), (70, 54), (58, 60), (50, 50), (42, 60), (34, 50), (26, 60), (18, 50), (6, 56), (0, 56)])
    pygame.draw.lines(s, CONTORNO, False, [(11, 58), (18, 50), (26, 60), (34, 50), (42, 60), (50, 50), (57, 58)], 3)
    elipse(s, casca, (52, 10, 40, 46))
    pygame.draw.polygon(s, TRANSPARENTE, [(50, 100), (50, 40), (58, 34), (64, 42), (72, 34), (80, 42), (88, 34), (96, 40), (100, 100)])
    pygame.draw.lines(s, CONTORNO, False, [(53, 40), (58, 34), (64, 42), (72, 34), (80, 42), (88, 34), (91, 38)], 3)


def folha_seca(s):
    pontos = [(50, 6), (74, 28), (82, 54), (64, 80), (50, 88), (36, 80), (18, 54), (26, 28)]
    poligono(s, (215, 130, 50), pontos)
    pygame.draw.line(s, (140, 80, 30), (50, 12), (50, 96), 3)
    for y in (32, 48, 64):
        pygame.draw.line(s, (140, 80, 30), (50, y + 8), (30, y), 2)
        pygame.draw.line(s, (140, 80, 30), (50, y + 8), (70, y), 2)


def pao(s):
    elipse(s, (215, 160, 80), (10, 34, 80, 46))
    pygame.draw.ellipse(s, (235, 190, 110), (18, 38, 64, 24))
    for x in (30, 46, 62):
        pygame.draw.line(s, (170, 110, 50), (x, 42), (x + 10, 58), 4)


# ========================= FASE 3 (mais difíceis) ===========================

def aluminio(s):
    pontos = [(30, 22), (52, 14), (74, 24), (86, 46), (80, 72), (60, 86), (34, 84), (16, 66), (14, 40)]
    poligono(s, (205, 210, 222), pontos)
    pygame.draw.polygon(s, (235, 238, 245), [(30, 22), (52, 14), (50, 44), (28, 46)])
    pygame.draw.polygon(s, (170, 175, 190), [(60, 86), (80, 72), (62, 56), (48, 66)])
    pygame.draw.lines(s, (150, 155, 170), False, [(28, 46), (50, 44), (62, 56), (86, 46)], 2)
    pygame.draw.line(s, (150, 155, 170), (50, 44), (48, 66), 2)


def tampinha_metal(s):
    pontos = []
    for i in range(42):
        ang = 2 * math.pi * i / 42
        if i % 2 == 0:
            r = 34
        else:
            r = 29
        pontos.append((50 + r * math.cos(ang), 50 + r * math.sin(ang)))
    poligono(s, (195, 200, 210), pontos, 2)
    circulo(s, (220, 50, 50), (50, 50), 22, 2)
    circulo(s, (250, 250, 250), (50, 50), 9, 0)


def marmitex(s):
    poligono(s, (195, 200, 212), [(14, 40), (86, 40), (78, 82), (22, 82)])
    retangulo(s, (220, 224, 232), (8, 33, 84, 10), 3)
    for x in (30, 50, 70):
        pygame.draw.line(s, (165, 170, 185), (x, 46), (x - 2, 78), 2)
    brilho(s, 22, 48, 26, 74)


def clipe(s):
    # primeiro o arame escuro e grosso (contorno), depois o arame claro e fino por cima
    for camada in [[CONTORNO, 9], [(200, 205, 215), 5]]:
        pygame.draw.rect(s, camada[0], (32, 8, 34, 84), camada[1], border_radius=17)
        pygame.draw.rect(s, camada[0], (40, 22, 18, 58), camada[1], border_radius=9)
    pygame.draw.rect(s, TRANSPARENTE, (54, 70, 14, 26))
    pygame.draw.line(s, (200, 205, 215), (61, 70), (61, 80), 5)


def isopor(s):
    retangulo(s, (248, 248, 244), (8, 34, 84, 42), 12)
    pygame.draw.rect(s, (226, 226, 220), (18, 41, 64, 28), border_radius=8)
    for x in range(24, 80, 10):
        for y in (48, 60):
            pygame.draw.circle(s, (205, 205, 200), (x, y), 2)


def xampu(s):
    retangulo(s, (250, 250, 250), (40, 10, 20, 22), 5)
    retangulo(s, (60, 190, 195), (28, 28, 44, 64), 16)
    retangulo(s, (255, 255, 255), (34, 48, 32, 24), 6, 2)
    for bolha in [[(44, 58), 5], [(56, 62), 4], [(52, 54), 3]]:  # [centro, raio]
        pygame.draw.circle(s, (120, 200, 240), bolha[0], bolha[1])
    brilho(s, 34, 36, 34, 44)


def escova(s):
    retangulo(s, (150, 80, 200), (43, 50, 14, 46), 7)
    elipse(s, (150, 80, 200), (24, 6, 52, 56))
    for x in range(36, 68, 8):
        for y in range(18, 52, 8):
            pygame.draw.circle(s, (60, 40, 80), (x, y), 2)


def caixa_ovos(s):
    cor = (185, 180, 168)
    for x in (24, 50, 76):
        circulo(s, cor, (x, 50), 14)
    retangulo(s, cor, (8, 50, 84, 34), 6)
    for x in (37, 63):
        pygame.draw.line(s, (150, 145, 135), (x, 54), (x, 80), 2)


def envelope(s):
    retangulo(s, (248, 242, 225), (10, 24, 80, 54), 3)
    pygame.draw.lines(s, CONTORNO, False, [(11, 25), (50, 56), (89, 25)], 3)
    pygame.draw.line(s, (200, 195, 180), (11, 77), (40, 52), 2)
    pygame.draw.line(s, (200, 195, 180), (89, 77), (60, 52), 2)
    retangulo(s, (225, 70, 70), (70, 30, 14, 14), 0, 2)


def saco_papel(s):
    poligono(s, (205, 160, 110), [(24, 22), (76, 22), (82, 92), (18, 92)])
    pygame.draw.lines(s, CONTORNO, False, [(24, 22), (30, 14), (36, 22), (42, 14), (48, 22), (54, 14), (60, 22), (66, 14), (72, 22), (76, 22)], 3)
    elipse(s, (235, 200, 140), (34, 50, 32, 20), 2)
    for x in (42, 50, 58):
        pygame.draw.line(s, (180, 130, 80), (x, 54), (x + 2, 66), 2)


def remedio(s):
    ambar = (170, 95, 30, 225)
    retangulo(s, ambar, (40, 24, 20, 16), 2)
    retangulo(s, ambar, (28, 36, 44, 56), 10)
    retangulo(s, (250, 250, 250), (36, 10, 28, 16), 4)
    retangulo(s, (250, 250, 250), (32, 52, 36, 24), 0, 2)
    pygame.draw.rect(s, (225, 50, 50), (47, 56, 6, 16))
    pygame.draw.rect(s, (225, 50, 50), (42, 61, 16, 6))


def pote_palmito(s):
    retangulo(s, (205, 238, 232, 170), (28, 20, 44, 74), 8)
    for x in (34, 45, 56):
        retangulo(s, (240, 235, 195), (x, 32, 10, 56), 4, 2)
    retangulo(s, (225, 185, 60), (25, 10, 50, 13), 3)
    brilho(s, 32, 26, 32, 40)


def borra_cafe(s):
    poligono(s, (250, 250, 245), [(14, 30), (86, 30), (62, 88), (38, 88)])
    for x in (36, 50, 64):
        pygame.draw.line(s, (215, 215, 205), (x, 34), (50 + (x - 50) // 3, 84), 2)
    elipse(s, (95, 58, 32), (16, 18, 68, 26))
    for p in ((36, 26), (52, 22), (64, 30), (44, 33)):
        pygame.draw.circle(s, (70, 40, 20), p, 3)


def laranja(s):
    pygame.draw.arc(s, CONTORNO, (16, 6, 60, 50), 0.2, 2.8, 12)
    pygame.draw.arc(s, (250, 150, 30), (16, 6, 60, 50), 0.2, 2.8, 8)
    elipse(s, (250, 150, 30), (14, 44, 72, 44))
    elipse(s, (255, 225, 180), (22, 48, 56, 22), 2)
    for p in ((30, 76), (50, 80), (68, 74)):
        pygame.draw.circle(s, (220, 120, 20), p, 2)


def milho(s):
    elipse(s, (238, 222, 165), (34, 6, 32, 88))
    for y in range(18, 86, 10):
        for x in (42, 50, 58):
            if (x + y) % 3:
                pygame.draw.ellipse(s, (250, 205, 50), (x - 4, y - 4, 8, 8))
            else:
                pygame.draw.ellipse(s, (215, 195, 140), (x - 3, y - 3, 6, 6))


def abacate(s):
    elipse(s, (150, 95, 50), (24, 18, 52, 64))
    pygame.draw.ellipse(s, (185, 125, 70), (32, 26, 22, 30))
    pygame.draw.ellipse(s, (230, 220, 160), (30, 70, 40, 16))
    pygame.draw.ellipse(s, CONTORNO, (30, 70, 40, 16), 2)


# ---------------------------------------------------------------------------
# Dicionário que liga o nome do desenho (campo "desenho" em dados.py) à função que o desenha.
# Ele é usado em assets.py para criar a imagem de cada lixo uma única vez.

DESENHOS = {
    'garrafa_pet': garrafa_pet,
    'sacola': sacola,
    'copo_plastico': copo_plastico,
    'pote_iogurte': pote_iogurte,
    'jornal': jornal,
    'caixa': caixa,
    'folha': folha,
    'rolo': rolo,
    'garrafa_vidro': garrafa_vidro,
    'pote_vidro': pote_vidro,
    'perfume': perfume,
    'lata': lata,
    'lata_conserva': lata_conserva,
    'panela': panela,
    'chave': chave,
    'banana': banana,
    'maca': maca,
    'ovo': ovo,
    'folha_seca': folha_seca,
    'pao': pao,
    'aluminio': aluminio,
    'tampinha_metal': tampinha_metal,
    'marmitex': marmitex,
    'clipe': clipe,
    'isopor': isopor,
    'xampu': xampu,
    'escova': escova,
    'caixa_ovos': caixa_ovos,
    'envelope': envelope,
    'saco_papel': saco_papel,
    'remedio': remedio,
    'pote_palmito': pote_palmito,
    'borra_cafe': borra_cafe,
    'laranja': laranja,
    'milho': milho,
    'abacate': abacate,
}
