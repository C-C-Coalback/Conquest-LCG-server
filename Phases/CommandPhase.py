import pygame

def command_phase(p_one, p_two):
    p_one.commit_warlord_step()
    p_two.commit_warlord_step()
    while True:
        pygame.time.wait(10000)