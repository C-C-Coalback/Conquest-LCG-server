import sys
import pygame
import FindCard
import ClickDetection
from Drawing import draw_all
from PassCommand import check_for_pass


def pygame_deploy_phase(round_number, p_one, p_two, game_screen):
    p_one_passed = False
    p_two_passed = False
    p_one.set_phase("Deploy")
    p_two.set_phase("Deploy")
    if p_one.get_has_initiative():
        p_one.set_has_turn(True)
        p_two.set_has_turn(False)
    else:
        p_one.set_has_turn(False)
        p_two.set_has_turn(True)
    print("deploy:", round_number)
    print("Hand of", p_one.get_name_player())
    print("Hand of", p_two.get_name_player())
    draw_all(game_screen, p_one, p_two)
    run = True
    while (not p_one_passed or not p_two_passed) and run:
        _ = pygame.time.wait(17)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y, p_one.get_has_turn(), p_two.get_has_turn())
                if 24 < y < 116 and p_two.get_has_turn():
                    if check_for_pass(x, y, p_two.get_number()) == 1:
                        p_two_passed = True
                        p_two.toggle_turn()
                        if not p_one_passed:
                            p_one.toggle_turn()
                        draw_all(game_screen, p_one, p_two)
                    else:
                        position = ClickDetection.determine_pos_hand(x, y, p_two)
                        if position == -1:
                            pass
                        else:
                            x_for_drawing = (position * 80) + 200
                            y_for_drawing = 24
                            pygame.draw.rect(game_screen, [55, 155, 55],
                                             [x_for_drawing, y_for_drawing, 62, 88], 2)
                            pygame.display.flip()
                            object_holder = FindCard.find_card(p_two.get_cards()[position])
                            if p_two.pygame_play_card(object_holder, p_one, game_screen) == 0:
                                if not p_one_passed:
                                    p_one.toggle_turn()
                                    p_two.toggle_turn()
                    draw_all(game_screen, p_one, p_two)
                elif 594 < y < 686 and p_one.get_has_turn():
                    if check_for_pass(x, y, p_one.get_number()) == 1:
                        p_one_passed = True
                        p_one.toggle_turn()
                        if not p_two_passed:
                            p_two.toggle_turn()
                        draw_all(game_screen, p_one, p_two)
                    else:
                        position = ClickDetection.determine_pos_hand(x, y, p_one)
                        if position == -1:
                            pass
                        else:
                            x_for_drawing = (position * 80) + 300
                            y_for_drawing = 594
                            pygame.draw.rect(game_screen, [55, 155, 55],
                                             [x_for_drawing, y_for_drawing, 62, 88], 2)
                            pygame.display.flip()
                            object_holder = FindCard.find_card(p_one.get_cards()[position])
                            if p_one.pygame_play_card(object_holder, p_two, game_screen) == 0:
                                if not p_two_passed:
                                    p_one.toggle_turn()
                                    p_two.toggle_turn()
                            draw_all(game_screen, p_one, p_two)
                elif 319 < y < 376:
                    print("Planets selected")
    print("Success in passing.")

