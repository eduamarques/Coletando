import math
import random
import pygame
from config import (WIDTH, HEIGHT, PRETO, BRANCO, LIXEIRAS, ORDEM_LIXEIRAS,
                    ESTEIRA_X_INICIO, ESTEIRA_X_FIM, ESTEIRA_Y, ESTEIRA_ALTURA)
from desenho import simbolo_reciclagem, texto, ajusta_cor

# Cenários animados em estilo desenho animado.
# As partes que não se mexem são desenhadas uma vez só numa superfície (self.estatico).
# A cada frame só desenhamos de novo o que é animado.


def gradiente_vertical(superficie, rect, cor_topo, cor_base):
    # Pinta o retângulo com um degradê de cima para baixo, uma linha de cada vez
    rect = pygame.Rect(rect)
    for i in range(rect.h):
        t = i / (rect.h - 1)
        cor = []
        for k in range(3):
            cor.append(int(cor_topo[k] + (cor_base[k] - cor_topo[k]) * t))
        pygame.draw.line(superficie, cor, (rect.x, rect.y + i), (rect.right, rect.y + i))


def nuvem(window, x, y, escala=1.0):
    # Nuvem fofinha feita de 4 círculos: [dx, dy, raio]
    circulos = [[0, 0, 30], [32, -14, 36], [66, 0, 30], [34, 10, 30]]
    for c in circulos:
        pygame.draw.circle(window, BRANCO, (int(x + c[0] * escala), int(y + c[1] * escala)), int(c[2] * escala))


def arvore(window, x, chao, escala=1.0):
    # Árvore simples: tronco marrom e copa redonda
    tronco = (x - 10 * escala, chao - 70 * escala, 20 * escala, 70 * escala)
    pygame.draw.rect(window, (120, 80, 45), tronco)
    pygame.draw.rect(window, PRETO, tronco, 3)
    # copa: [dx, dy, raio, cor]
    copa = [[-28, -85, 38, (60, 160, 70)], [28, -85, 38, (60, 160, 70)],
            [0, -115, 44, (80, 185, 85)], [0, -75, 36, (70, 170, 75)]]
    for c in copa:  # primeiro o contorno preto de todas as bolas...
        pygame.draw.circle(window, PRETO, (int(x + c[0] * escala), int(chao + c[1] * escala)), int(c[2] * escala) + 3)
    for c in copa:  # ...depois o verde por cima
        pygame.draw.circle(window, c[3], (int(x + c[0] * escala), int(chao + c[1] * escala)), int(c[2] * escala))


class FundoExterno:
    # Fachada da Central de Triagem com céu, sol, nuvens e caminhão de coleta (usado nos menus)
    def __init__(self):
        self.tempo = 0
        # cada nuvem é uma lista [x, y, escala, velocidade]
        self.nuvens = []
        for i in range(6):
            self.nuvens.append([random.randint(0, WIDTH), random.randint(40, 200),
                                random.uniform(0.6, 1.2), random.uniform(12, 30)])
        self.caminhao_x = -250
        self.estatico = self.desenha_estatico()

    def desenha_estatico(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        gradiente_vertical(s, (0, 0, WIDTH, HEIGHT), (100, 185, 250), (205, 238, 255))
        # morros ao fundo
        pygame.draw.ellipse(s, (140, 205, 120), (-200, 420, 800, 300))
        pygame.draw.ellipse(s, (125, 195, 110), (500, 440, 1000, 300))
        # galpão
        g = pygame.Rect(560, 250, 620, 330)
        telhado = [(g.x - 30, g.y), (g.centerx, g.y - 110), (g.right + 30, g.y)]
        pygame.draw.polygon(s, (205, 90, 60), telhado)
        pygame.draw.polygon(s, PRETO, telhado, 5)
        for i in range(1, 8):  # telhas
            x = g.x - 30 + i * (g.w + 60) / 8
            topo_y = g.y - 110 * (1 - abs(x - g.centerx) / (g.w / 2 + 30))
            pygame.draw.line(s, (170, 70, 45), (x, g.y), (x, topo_y + 4), 3)
        pygame.draw.rect(s, (235, 230, 210), g)
        pygame.draw.rect(s, (215, 205, 180), (g.x, g.bottom - 40, g.w, 40))
        pygame.draw.rect(s, PRETO, g, 5)
        # portão de garagem
        portao = pygame.Rect(g.x + 40, g.y + 130, 220, 200)
        pygame.draw.rect(s, (150, 160, 175), portao)
        for y in range(portao.y + 16, portao.bottom, 18):
            pygame.draw.line(s, (120, 130, 145), (portao.x, y), (portao.right, y), 3)
        pygame.draw.rect(s, PRETO, portao, 5)
        for i in range(8):  # faixa zebrada
            if i % 2 == 0:
                cor = (250, 200, 40)
            else:
                cor = (40, 40, 40)
            pygame.draw.rect(s, cor, (portao.x + i * portao.w / 8, portao.y - 16, portao.w / 8 + 1, 16))
        # janelas
        for jx in [g.x + 310, g.x + 460]:
            jan = pygame.Rect(jx, g.y + 140, 110, 80)
            pygame.draw.rect(s, (170, 220, 250), jan)
            pygame.draw.line(s, BRANCO, (jan.x + 15, jan.bottom - 15), (jan.x + 45, jan.y + 15), 5)
            pygame.draw.line(s, PRETO, (jan.centerx, jan.y), (jan.centerx, jan.bottom), 4)
            pygame.draw.line(s, PRETO, (jan.x, jan.centery), (jan.right, jan.centery), 4)
            pygame.draw.rect(s, PRETO, jan, 5)
        # placa
        placa = pygame.Rect(0, 0, 520, 76)
        placa.center = (g.centerx, g.y + 58)
        pygame.draw.rect(s, (60, 160, 80), placa, border_radius=14)
        pygame.draw.rect(s, PRETO, placa, 5, border_radius=14)
        texto(s, 'CENTRAL DE TRIAGEM', 34, BRANCO, (placa.centerx + 34, placa.centery), contorno=2)
        pygame.draw.circle(s, (40, 130, 60), (placa.x + 42, placa.centery), 28)
        simbolo_reciclagem(s, (placa.x + 42, placa.centery), 18, BRANCO, 5)
        # lixeiras na frente do galpão
        for i in range(len(ORDEM_LIXEIRAS)):
            cor = LIXEIRAS[ORDEM_LIXEIRAS[i]]['cor']
            r = pygame.Rect(g.x + 300 + i * 62, g.bottom - 70, 48, 62)
            pygame.draw.rect(s, cor, r, border_radius=6)
            pygame.draw.rect(s, PRETO, r, 3, border_radius=6)
            tampa = (r.x - 3, r.y - 10, r.w + 6, 12)
            pygame.draw.rect(s, ajusta_cor(cor, 50), tampa, border_radius=4)
            pygame.draw.rect(s, PRETO, tampa, 3, border_radius=4)
        # grama e estrada
        pygame.draw.rect(s, (95, 180, 80), (0, 580, WIDTH, 40))
        pygame.draw.rect(s, (85, 88, 98), (0, 620, WIDTH, 100))
        pygame.draw.line(s, PRETO, (0, 620), (WIDTH, 620), 4)
        for x in range(0, WIDTH, 90):
            pygame.draw.rect(s, (245, 245, 245), (x, 666, 50, 8))
        arvore(s, 70, 590, 1.0)
        arvore(s, 190, 590, 0.8)
        arvore(s, 470, 590, 0.9)
        return s

    def update(self, dt):
        # Move as nuvens e o caminhão
        self.tempo += dt
        for n in self.nuvens:
            n[0] += n[3] * dt
            if n[0] > WIDTH + 100:
                n[0] = -200
                n[1] = random.randint(40, 200)
        self.caminhao_x += 140 * dt
        if self.caminhao_x > WIDTH + 300:
            self.caminhao_x = -400

    def desenha_sol(self, window):
        cx = 110
        cy = 95
        for i in range(12):  # raios girando
            angulo = self.tempo * 0.5 + i * math.pi / 6
            p1 = (cx + 58 * math.cos(angulo), cy + 58 * math.sin(angulo))
            p2 = (cx + 80 * math.cos(angulo), cy + 80 * math.sin(angulo))
            pygame.draw.line(window, (255, 210, 60), p1, p2, 7)
        pygame.draw.circle(window, (255, 220, 70), (cx, cy), 48)
        pygame.draw.circle(window, PRETO, (cx, cy), 48, 4)
        # carinha sorridente
        pygame.draw.circle(window, PRETO, (cx - 15, cy - 8), 5)
        pygame.draw.circle(window, PRETO, (cx + 15, cy - 8), 5)
        pygame.draw.arc(window, PRETO, (cx - 20, cy - 10, 40, 30), math.pi + 0.3, 2 * math.pi - 0.3, 4)

    def desenha_caminhao(self, window):
        quica = int(abs(math.sin(self.tempo * 12)) * 3)
        x = int(self.caminhao_x)
        y = 600 - quica
        pygame.draw.rect(window, (60, 160, 80), (x, y, 170, 70), border_radius=8)
        pygame.draw.rect(window, PRETO, (x, y, 170, 70), 4, border_radius=8)
        simbolo_reciclagem(window, (x + 85, y + 35), 22, BRANCO, 5)
        cabine = pygame.Rect(x + 172, y + 18, 62, 52)
        pygame.draw.rect(window, (250, 250, 250), cabine, border_radius=10)
        pygame.draw.rect(window, (150, 210, 245), (cabine.x + 24, cabine.y + 8, 30, 20), border_radius=4)
        pygame.draw.rect(window, PRETO, cabine, 4, border_radius=10)
        for rx in [x + 35, x + 135, x + 205]:
            pygame.draw.circle(window, (40, 40, 45), (rx, y + 74 + quica), 17)
            pygame.draw.circle(window, (180, 180, 190), (rx, y + 74 + quica), 7)

    def draw(self, window):
        window.blit(self.estatico, (0, 0))
        self.desenha_sol(window)
        for n in self.nuvens:
            nuvem(window, n[0], n[1], n[2])
        self.desenha_caminhao(window)


class FundoInterno:
    # Interior do galpão: janelas, canos, engrenagens girando e luzes balançando (usado na partida)
    def __init__(self):
        self.tempo = 0
        self.estatico = self.desenha_estatico()

    def desenha_estatico(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        gradiente_vertical(s, (0, 0, WIDTH, 470), (250, 236, 205), (232, 214, 180))
        # tijolinhos suaves
        for y in range(70, 300, 28):
            if (y // 28) % 2 == 1:
                deslocamento = 0
            else:
                deslocamento = 40
            for x in range(-40 + deslocamento, WIDTH, 80):
                pygame.draw.rect(s, (238, 220, 186), (x, y, 76, 24), 2, border_radius=3)
        # janelões com céu
        for jx in [150, 520, 890]:
            jan = pygame.Rect(jx, 60, 240, 120)
            gradiente_vertical(s, jan, (120, 195, 250), (200, 235, 255))
            pygame.draw.circle(s, BRANCO, (jan.x + 70, jan.y + 50), 18)
            pygame.draw.circle(s, BRANCO, (jan.x + 92, jan.y + 44), 22)
            pygame.draw.circle(s, BRANCO, (jan.x + 114, jan.y + 52), 16)
            for i in range(1, 4):
                pygame.draw.line(s, (90, 95, 110), (jan.x + i * 60, jan.y), (jan.x + i * 60, jan.bottom), 5)
            pygame.draw.line(s, (90, 95, 110), (jan.x, jan.centery), (jan.right, jan.centery), 5)
            pygame.draw.rect(s, PRETO, jan, 5)
        # teto com viga e cano
        pygame.draw.rect(s, (120, 125, 140), (0, 0, WIDTH, 34))
        pygame.draw.line(s, PRETO, (0, 34), (WIDTH, 34), 4)
        pygame.draw.rect(s, (70, 150, 200), (0, 40, WIDTH, 14))
        pygame.draw.rect(s, PRETO, (0, 40, WIDTH, 14), 3)
        for x in range(60, WIDTH, 220):
            pygame.draw.rect(s, (50, 120, 170), (x, 37, 16, 20), border_radius=3)
        # fardos de material reciclado no fundo
        cores_fardos = [(225, 70, 70), (60, 120, 220), (60, 175, 80), (240, 195, 40), (225, 70, 70), (60, 120, 220)]
        for i in range(len(cores_fardos)):
            cor = cores_fardos[i]
            r = pygame.Rect(30 + i * 210, 220, 110, 72)
            if i % 2 == 1:
                r.y -= 16
            pygame.draw.rect(s, cor, r, border_radius=6)
            for k in range(1, 4):
                pygame.draw.line(s, ajusta_cor(cor, -50), (r.x + 4, r.y + k * 18), (r.right - 4, r.y + k * 18), 3)
            pygame.draw.line(s, (60, 60, 60), (r.x + 36, r.y), (r.x + 36, r.bottom), 3)
            pygame.draw.line(s, (60, 60, 60), (r.x + 74, r.y), (r.x + 74, r.bottom), 3)
            pygame.draw.rect(s, PRETO, r, 4, border_radius=6)
        # chão
        gradiente_vertical(s, (0, 430, WIDTH, HEIGHT - 430), (170, 175, 185), (130, 135, 148))
        for x in range(-40, WIDTH + 40, 160):
            pygame.draw.line(s, (150, 155, 165), (x, 430), (x - 80, HEIGHT), 2)
        # faixa de segurança zebrada
        for i in range(0, WIDTH, 40):
            pygame.draw.polygon(s, (250, 200, 40), [(i, 440), (i + 20, 440), (i + 10, 452), (i - 10, 452)])
        pygame.draw.line(s, PRETO, (0, 430), (WIDTH, 430), 4)
        return s

    def update(self, dt):
        self.tempo += dt

    def desenha_engrenagem(self, window, centro, raio, angulo, cor):
        dentes = 10
        pontos = []
        for i in range(dentes * 2):
            if i % 2 == 0:
                r = raio
            else:
                r = raio * 0.78
            for k in [-0.18, 0.18]:
                a = angulo + (i + k + 0.5) * math.pi / dentes
                pontos.append((centro[0] + r * math.cos(a), centro[1] + r * math.sin(a)))
        pygame.draw.polygon(window, cor, pontos)
        pygame.draw.polygon(window, PRETO, pontos, 3)
        pygame.draw.circle(window, (90, 90, 100), centro, int(raio * 0.32))
        pygame.draw.circle(window, PRETO, centro, int(raio * 0.32), 3)

    def desenha_luminaria(self, window, x):
        angulo = math.sin(self.tempo * 1.6 + x) * 0.08
        px = x + 46 * math.sin(angulo)
        py = 54 + 46 * math.cos(angulo)
        pygame.draw.line(window, PRETO, (x, 54), (px, py), 3)
        luz = pygame.Surface((180, 140), pygame.SRCALPHA)
        pygame.draw.polygon(luz, (255, 245, 180, 45), [(70, 0), (110, 0), (180, 140), (0, 140)])
        window.blit(luz, (px - 90, py + 6))
        cupula = [(px - 26, py + 14), (px + 26, py + 14), (px + 12, py - 2), (px - 12, py - 2)]
        pygame.draw.polygon(window, (60, 140, 90), cupula)
        pygame.draw.polygon(window, PRETO, cupula, 3)
        pygame.draw.circle(window, (255, 240, 150), (int(px), int(py + 16)), 7)

    def draw(self, window):
        window.blit(self.estatico, (0, 0))
        self.desenha_engrenagem(window, (1180, 250), 42, self.tempo * 1.2, (160, 165, 180))
        self.desenha_engrenagem(window, (1238, 200), 28, -self.tempo * 1.8 + 0.2, (200, 140, 60))
        self.desenha_luminaria(window, 420)
        self.desenha_luminaria(window, 790)


class Esteira:
    # Esteira rolante que leva os lixos da esquerda para a direita
    def __init__(self, velocidade):
        self.velocidade = velocidade  # pixels por segundo
        self.deslocamento = 0
        largura = ESTEIRA_X_FIM - ESTEIRA_X_INICIO + 30
        self.rect = pygame.Rect(ESTEIRA_X_INICIO, ESTEIRA_Y, largura, ESTEIRA_ALTURA)

    def update(self, dt):
        # Faz as listras e os rolos girarem
        self.deslocamento = (self.deslocamento + self.velocidade * dt) % 60

    def draw(self, window):
        r = self.rect
        # pés
        for x in range(r.x + 60, r.right, 240):
            pygame.draw.rect(window, (80, 85, 95), (x, r.bottom, 16, 34))
            pygame.draw.rect(window, PRETO, (x, r.bottom, 16, 34), 3)
        # estrutura
        pygame.draw.rect(window, (95, 100, 112), r.inflate(0, 20), border_radius=16)
        # lona com listras que andam
        lona = r.inflate(-10, -6)
        pygame.draw.rect(window, (55, 58, 66), lona, border_radius=12)
        for x in range(int(lona.x - 60 + self.deslocamento), lona.right, 60):
            pygame.draw.line(window, (80, 84, 94), (x, lona.y + 6), (x + 22, lona.bottom - 6), 6)
        # rolos nas pontas
        for cx in [r.x + 14, r.right - 14]:
            pygame.draw.circle(window, (170, 175, 185), (cx, r.centery), r.h // 2 - 2)
            angulo = self.deslocamento / 60 * 2 * math.pi
            for k in range(3):
                a = angulo + k * 2 * math.pi / 3
                pygame.draw.line(window, (110, 115, 125), (cx, r.centery),
                                 (cx + 40 * math.cos(a), r.centery + 40 * math.sin(a)), 4)
            pygame.draw.circle(window, PRETO, (cx, r.centery), r.h // 2 - 2, 4)
        pygame.draw.rect(window, PRETO, r.inflate(0, 20), 4, border_radius=16)
        # faixa amarela com setas indicando a direção
        faixa = pygame.Rect(r.x + 40, r.y - 30, r.w - 80, 18)
        pygame.draw.rect(window, (250, 200, 40), faixa, border_radius=8)
        pygame.draw.rect(window, PRETO, faixa, 3, border_radius=8)
        for x in range(faixa.x + 30 + int(self.deslocamento), faixa.right - 20, 60):
            pygame.draw.polygon(window, PRETO, [(x, faixa.y + 3), (x + 12, faixa.centery), (x, faixa.bottom - 3)])
