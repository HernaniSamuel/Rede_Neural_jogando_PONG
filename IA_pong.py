from time import sleep
from random import randint
import pygame
from pygame.locals import *
from sys import exit
import neat
import os

pygame.init()

def treinar(genome1, config):
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    genome1.fitness = 0
    run = True

    IMAGEM_QUADRA = pygame.transform.scale2x(pygame.image.load(os.path.join('ibagens', 'quadra.png')))
    IMAGEM_BOLA = pygame.transform.scale(pygame.image.load(os.path.join('ibagens', 'bola.png')), (60, 60))
    xtela = 1024
    ytela = 672
    tela = pygame.display.set_mode((xtela, ytela))
    vel = 10
    xbola = xtela / 2
    ybola = ytela / 2
    velxb = 0
    velyb = 0
    xbimg = xbola - 31
    ybimg = ybola - 31.5
    corpo = 75
    yj1 = yj2 = ytela / 2 - corpo / 2
    pj1 = pj2 = 0
    pygame.display.set_caption('Tênis')
    fonte = pygame.font.SysFont('arial', 80, True, False)

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.event.pump()
                exit()

        tela.blit(IMAGEM_QUADRA, (0, 0))

        # Bola
        bola = pygame.draw.circle(tela, (250, 250, 0), (xbola, ybola), 20)
        tela.blit(IMAGEM_BOLA, (xbimg, ybimg))
        xbola += velxb
        ybola += velyb
        xbimg += velxb
        ybimg += velyb
        if xbola + 15 >= xtela - 10:
            pj1 += 1
            velxb = velyb = 0
            xbola = xtela / 2
            ybola = ytela / 2
            xbimg = xbola - 31
            ybimg = ybola - 31.5

            yj1 = yj2 = ytela / 2 - corpo / 2
        if xbola - 15 <= 15:
            genome1.fitness -= 0.5
            pj2 += 1
            velxb = velyb = 0
            xbola = xtela / 2
            ybola = ytela / 2
            xbimg = xbola - 31
            ybimg = ybola - 31.5
            yj1 = yj2 = ytela / 2 - corpo / 2
            break
        if ybola + 15 >= ytela - 38:
            velyb *= -1
        if ybola - 15 <= 39:
            velyb *= -1

        # Jogadores
        j1 = pygame.draw.rect(tela, (255, 0, 0), (35, yj1, corpo / 3, corpo))
        output1 = net1.activate((ybola, yj1, xbola - 35))
        decision1 = output1.index(max(output1))

        if decision1 == 0:
            if velxb == 0 and velyb == 0:
                velxb = vel
                r = randint(1, 2)
                if r == 1:
                    velyb = -vel
                else:
                    velyb = vel

        elif decision1 == 1:
            if velyb == 0 and velxb == 0:
                velxb = vel
                r = randint(1, 2)
                if r == 1:
                    velyb = -vel
                else:
                    velyb = vel
            if yj1 <= 39:
                yj1 += 0
            else:
                yj1 -= vel
        else:
            if velxb == 0 and velyb == 0:
                velxb = vel
                r = randint(1, 2)
                if r == 1:
                    velyb = -vel
                else:
                    velyb = vel
            if yj1 + corpo >= ytela - 38:
                if velxb == 0 and velyb == 0:
                    velxb = vel
                    r = randint(1, 2)
                    if r == 1:
                        velyb = -vel
                    else:
                        velyb = vel
                yj1 += 0
            else:
                yj1 += vel

        j2 = pygame.draw.rect(tela, (0, 0, 255), (xtela - 65, yj2, corpo / 3, corpo))
        if pygame.key.get_pressed()[K_UP]:
            if velxb == 0 and velyb == 0:
                velxb = -vel
                r = randint(1, 2)
                if r == 1:
                    velyb = -vel
                else:
                    velyb = vel
            if yj2 <= 39:
                yj2 += 0
            else:
                yj2 -= vel
        if pygame.key.get_pressed()[K_DOWN]:
            if velxb == 0 and velyb == 0:
                velxb = -vel
                r = randint(1, 2)
                if r == 1:
                    velyb = -vel
                else:
                    velyb = vel
            if yj2 + corpo >= ytela - 38:
                yj2 += 0
            else:
                yj2 += vel
        #yj2 = ybola - corpo / 2

        if bola.colliderect(j1):
            genome1.fitness += 0.5
            if genome1.fitness >= 50:
                break
            velxb = +vel
            r = randint(1, 2)
            if r == 1:
                velyb = -vel
            else:
                velyb = vel

        if bola.colliderect(j2):
            velxb = -vel
            r = randint(1, 2)
            if r == 1:
                velyb = -vel
            else:
                velyb = vel

        msg1 = f'{pj1}'
        msg2 = f'{pj2}'
        j1w = 'O Vermelho ganhou!'
        j2w = 'O Azul ganhou!'
        txt1 = fonte.render(msg1, False, (255, 255, 255))
        txt2 = fonte.render(msg2, False, (255, 255, 255))
        txt3 = fonte.render(j1w, False, (255, 0, 0))
        txt4 = fonte.render(j2w, False, (0, 0, 255))
        tela.blit(txt1, (xtela / 2 - (xtela / 2) / 2 - 20, 14))
        tela.blit(txt2, (xtela / 2 + (xtela / 2) / 2 - 20, 14))

        if pj1 >= 10:
            tela.blit(txt3, (xtela / 2 - 360, ytela / 2 - 40))
            pygame.display.update()
            sleep(3)
            break
        if pj2 >= 10:
            tela.blit(txt4, (xtela / 2 - 280, ytela / 2 - 40))
            pygame.display.update()
            sleep(3)
            break
        pygame.display.update()

########################################################################################################################
def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        treinar(genome1, config)


def run_neat(config):
    populacao = neat.Checkpointer.restore_checkpoint('neat-checkpoint-15')
    #populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    status = neat.StatisticsReporter()
    populacao.add_reporter(status)
    populacao.add_reporter(neat.Checkpointer(1))

    melhor = populacao.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "editconfig.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
