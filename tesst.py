# import csv


# class MalformedScoreDataError(Exception):
#     pass

# with open("score.csv") as f:
#     people = []
#     reader = csv.DictReader(f)
#     try:
#         for row in reader:
#             name = row["name"]
#             score = int(row["score"])
#             print(name, str(score))
#     except csv.Error:
#         raise MalformedScoreDataError(
#             "Score data file has invalid data")
import pygame
pygame.init()
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()

counter, text = 10, '10'.rjust(3)
counter = 10
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

def set_time(time):
    global counter

    for e in pygame.event.get():
        if e.type == pygame.USEREVENT:
            print(counter)
            counter -= 1
            # counter -= 1
            # text = str(counter).rjust(3) if counter > 0 else 'boom!'
            # if counter < 0:
            #     print('boom')
        if e.type == pygame.QUIT:
            run = False
run = True
counter = 10
while run:
    set_time(10)

    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
    pygame.display.flip()
    clock.tick(60)