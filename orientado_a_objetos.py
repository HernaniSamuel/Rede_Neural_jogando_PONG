import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
pygame.font.init()


class Player:
    def __init__(self, x, y, velocidade, largura, altura, cor):
        self.x = x
        self.y = y
        self.pontos = 0
        self.velocidade = velocidade
        self.largura = largura
        self.altura = altura
        self.cor = cor

    def mover(self, limite_cima, limite_baixo, cima=True):
        if cima and self.y > limite_cima:
            self.y -= self.velocidade
        if not cima and self.y + self.altura < limite_baixo:
            self.y += self.velocidade


class Bola:
    def __init__(self, x, y, velocidade_x, velocidade_y, raio, cor):
        self.x = x
        self.y = y
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.raio = raio
        self.cor = cor

    def ricochete(self, limite_1, limite_2):
        if self.y - self.raio <= limite_1:
            self.velocidade_y *= -1
        if self.y + self.raio >= limite_2:
            self.velocidade_y *= -1

    def ponto_marcado(self, largura):
        if self.x - self.raio <= 0:
            return 'esquerda'
        if self.x + self.raio >= largura:
            return 'direita'


class Tela:
    def __init__(self, largura, altura, titulo):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(self.titulo)

    def desenhar_placar(self, p1, p2):
        msg1 = f'{p1}'
        msg2 = f'{p2}'
        font = pygame.font.SysFont('Arial', 50)
        text1 = font.render(msg1, True, (255, 255, 255))
        text2 = font.render(msg2, True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(self.largura / 2 / 2, 30))
        text_rect2 = text2.get_rect(center=(self.largura / 2 / 2 + self.largura/2, 30))
        self.tela.blit(text1, text_rect1)
        self.tela.blit(text2, text_rect2)


def main():
    tela = Tela(1200, 700, 'Ping Pong')
    player1 = Player(10, tela.altura/2-45, 9, 20, 90, (255, 0, 0))
    player2 = Player(tela.largura - 30, tela.altura/2-45, 9, 20, 90, (0, 0, 255))
    bola = Bola(tela.largura/2, tela.altura/2, 10, 10, 15, (0, 255, 0))
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        tela.tela.fill((0, 0, 100))
        pygame.draw.line(tela.tela, (255, 255, 255), (tela.largura/2, 0), (tela.largura/2, tela.altura), 3)
        player1_rect = pygame.draw.rect(tela.tela, player1.cor, (player1.x, player1.y, player1.largura, player1.altura))
        player2_rect = pygame.draw.rect(tela.tela, player2.cor, (player2.x, player2.y, player2.largura, player2.altura))
        bola_rect = pygame.draw.circle(tela.tela, bola.cor, (bola.x, bola.y), bola.raio)
        tela.desenhar_placar(player1.pontos, player2.pontos)

        if bola.ponto_marcado(tela.largura) == 'direita':
            bola.velocidade_y, bola.velocidade_x = 0, 0
            bola.x, bola.y = tela.largura/2, tela.altura/2
            player1.pontos += 1

        if bola.ponto_marcado(tela.largura) == 'esquerda':
            bola.velocidade_y, bola.velocidade_x = 0, 0
            bola.x, bola.y = tela.largura/2, tela.altura/2
            player2.pontos += 1

        bola.ricochete(0, tela.altura)

        if bola_rect.colliderect(player1_rect) or bola_rect.colliderect(player2_rect):
            r = randint(0, 1)
            if r == 1:
                bola.velocidade_y *= -1
            bola.velocidade_x *= -1

        if pygame.key.get_pressed()[K_w]:
            player1.mover(0, tela.altura)
        if pygame.key.get_pressed()[K_s]:
            player1.mover(0, tela.altura, False)

        if pygame.key.get_pressed()[K_UP]:
            player2.mover(0, tela.altura)
        if pygame.key.get_pressed()[K_DOWN]:
            player2.mover(0, tela.altura, False)

        if pygame.key.get_pressed()[K_SPACE] and bola.velocidade_x == 0:
            bola.velocidade_y, bola.velocidade_x = 10, 10

        bola.x += bola.velocidade_x
        bola.y += bola.velocidade_y

        pygame.display.update()


if __name__ == '__main__':
    main()
