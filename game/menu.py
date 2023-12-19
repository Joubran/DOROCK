import sys
import random

import pygame

from scripts import button
from scripts import slider
from scripts import sprite_sheet as ss
import game

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('Sounds/menu_music.mp3')

        #screen
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dorock')

        #FPS
        clock = pygame.time.Clock()
        FPS = 60

        #SLIDER
        test_slider = slider.Slider(1150, 665, 100, 5, screen)

        #define fonts
        PIXEL_50 = pygame.font.Font('Fonts/pixel.ttf', 50)

        #define color
        WHITE_COLOR = (255, 255, 255)
        BLACK_COLOR = (0, 0, 0)

        #music
        pygame.mixer.init()

        # sounds
        sound_hover = pygame.mixer.Sound('Sounds/hover_button_sound.ogg')
        sound_hover.set_volume(0.15)

        def draw_text(text, font, text_color, x, y):
            img = font.render(text, True, text_color)
            screen.blit(img, (x, y))

        def draw_fade_text(text, font, text_color, x, y, fade_speed=1, increasing = True, alpha = 0, circles = 0):
            if increasing:
                alpha += fade_speed
                if alpha >= 255:
                    alpha = 255
                    increasing = False
            else:
                alpha -= fade_speed
                if alpha <= 0:
                    alpha = 0
                    increasing = True
                    circles += 1

            fade_text = font.render(text, True, text_color)
            fade_text.set_alpha(alpha)

            text_rect = fade_text.get_rect(center=(x, y))

            screen.blit(fade_text, text_rect)

            pygame.display.update()
            pygame.time.delay(20)

            return increasing, alpha, circles

        def main_menu(self, fresh_start):
            running = True

            # game variables
            game_started = fresh_start
            turn_on_first_time = fresh_start
            increasing = True
            alpha = 0
            circles = 2

            start_hovered = False
            settings_hovered = False
            exit_hovered = False

            # loading images for menu
            bg_img = pygame.image.load('Images/bg_menu.jpg').convert_alpha()
            bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            sound_on_img = pygame.image.load('Images/sound_on.png').convert_alpha()
            sound_off_img = pygame.image.load('Images/sound_off.png').convert_alpha()
            start_img = pygame.image.load('Images/sign_play.png').convert_alpha()
            start_img_bright = pygame.image.load('Images/sign_play_bright.png').convert_alpha()
            settings_img = pygame.image.load('Images/sign_settings.png').convert_alpha()
            settings_img_bright = pygame.image.load('Images/sign_settings_bright.png').convert_alpha()
            exit_img = pygame.image.load('Images/sign_exit.png').convert_alpha()
            exit_img_bright = pygame.image.load('Images/sign_exit_bright.png').convert_alpha()

            # making them buttons
            sound_button = button.Button(1100, 650, sound_on_img, 0.14)
            sound_off_button = button.Button(1100, 650, sound_off_img, 0.14)
            start_button = button.Button(465, 50, start_img, 0.15)
            start_button_bright = button.Button(465, 50, start_img_bright, 0.15)
            settings_button = button.Button(465, 230, settings_img, 0.15)
            settings_button_bright = button.Button(465, 230, settings_img_bright, 0.15)
            exit_button = button.Button(465, 410, exit_img, 0.15)
            exit_button_bright = button.Button(465, 410, exit_img_bright, 0.15)

            #music
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1, fade_ms=5000)
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.pause()
            vol = int(pygame.mixer.music.get_volume() * 1000)
            prevol = vol
            turn_on_first_time = False


            # birds
            bird_sheet_image = pygame.image.load('Images/bird_sprites.png').convert_alpha()
            bird_sprites = ss.SpriteSheet(bird_sheet_image)

            # birds parameters
            bird_width, bird_height = 160, 160
            bird_scale = 0.5

            bird_x = 1280
            bird_y = random.randint(0, 300)
            last_bird = pygame.time.get_ticks()

            # creating birds list
            bird_list = []
            animations = 8
            last_update = pygame.time.get_ticks()
            animation_cd = 100
            frame = 0

            for frame in range(animations):
                bird_list.append(bird_sprites.get_image(frame, bird_width, bird_height, bird_scale, BLACK_COLOR))

            while running:
                screen.fill(BLACK_COLOR)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not(game_started):
                            game_started = True
                            alpha = 0
                            increasing = True
                            circles = 0

                    if event.type == pygame.QUIT:
                        running = False

                #check if game is started
                if game_started == True:
                    if circles == 0:
                        increasing, alpha, circles = draw_fade_text("\"The Procrastinators\" presents", PIXEL_50, WHITE_COLOR, 640, 360, 100, increasing, alpha,circles)
                    elif circles == 1:
                        increasing, alpha, circles = draw_fade_text("Dorock", PIXEL_50, (179, 0, 0), 640, 360, 100, increasing, alpha,circles)
                    else:
                        screen.blit(bg_img, (0, 0))
                        if start_button.draw(screen, 'hover'):
                            if start_button_bright.draw(screen):
                                game.Game(self).run()
                                running = False
                            if not start_hovered:
                                pygame.mixer.Sound.play(sound_hover)
                                start_hovered = True
                        else:
                            start_button.draw(screen)
                            start_hovered = False

                        if settings_button.draw(screen, 'hover'):
                            if settings_button_bright.draw(screen):
                                running = False
                                settings_menu()
                            if not settings_hovered:
                                pygame.mixer.Sound.play(sound_hover)
                                settings_hovered = True
                        else:
                            settings_button.draw(screen)
                            settings_hovered = False

                        if exit_button.draw(screen, 'hover'):
                            if exit_button_bright.draw(screen):
                                running=False
                            if not exit_hovered:
                                sound_hover.play(0, 0, fade_ms=0)
                                exit_hovered = True
                        else:
                            exit_button.draw(screen)
                            exit_hovered = False


                        if turn_on_first_time == False:
                            pygame.mixer.music.unpause()
                            turn_on_first_time = True
                            vol = pygame.mixer.music.get_volume()

                        if vol == 0:
                            if sound_off_button.draw(screen):
                                pygame.mixer.music.set_volume(prevol/100)
                                vol = prevol
                        else:
                            if sound_button.draw(screen):
                                pygame.mixer.music.set_volume(0)
                                prevol = vol
                                vol = 0
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEMOTION:
                                if pygame.mouse.get_pressed()[0] and test_slider.on_slider(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                                    test_slider.handle_event(screen, pygame.mouse.get_pos()[0])
                                    prevol = vol
                                    vol = test_slider.get_volume()
                                    pygame.mixer.music.set_volume(vol/100)

                        test_slider.draw(screen, vol)

                        #update animation
                        current_time = pygame.time.get_ticks()
                        if current_time - last_update >= animation_cd:
                            if frame == animations-1:
                                frame = 0
                            else:
                                frame += 1
                            last_update = current_time

                        if bird_x > 0:
                            bird_x -= random.randint(3, 10)
                            screen.blit(bird_list[frame], (bird_x, bird_y))
                        else:
                            if current_time - last_bird > random.randint(4000,30000):
                                bird_x = 1280
                                bird_y = random.randint(0, 300)
                                screen.blit(bird_list[frame], (bird_x, bird_y))
                                animation_cd = random.randint(50, 150)
                                last_bird = current_time

                else:
                    increasing, alpha, circles = draw_fade_text("Press SPACE to start the game", PIXEL_50, WHITE_COLOR, 640, 360, 10, increasing, alpha, circles)
                pygame.display.update()

                clock.tick(FPS)

        def settings_menu():
            # image stuff for settings menu
            settings_bg = pygame.image.load('Images/settings_bg.png').convert_alpha()
            settings_bg = pygame.transform.scale(settings_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            audio_img = pygame.image.load('Images/audio_sign.png').convert_alpha()
            audio_img_bright = pygame.image.load('Images/audio_bright_sign.png').convert_alpha()
            video_img = pygame.image.load('Images/video_sign.png').convert_alpha()
            video_img_bright = pygame.image.load('Images/video_bright_sign.png').convert_alpha()
            back_img = pygame.image.load('Images/back.png').convert_alpha()
            back_img_bright = pygame.image.load('Images/back_bright.png').convert_alpha()

            #making buttons
            audio_button = button.Button(465, 160, audio_img, 0.15)
            audio_button_bright = button.Button(465, 160, audio_img_bright, 0.15)
            video_button = button.Button(465, 340, video_img, 0.15)
            video_button_bright = button.Button(465, 340, video_img_bright, 0.15)
            back_button = button.Button(350, 75, back_img, 0.4)
            back_button_bright = button.Button(350, 75, back_img_bright, 0.4)

            #sounds
            audio_hovered = False
            video_hovered = False
            back_hovered = False


            running = True
            while running:
                screen.fill(BLACK_COLOR)
                screen.blit(settings_bg, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                if audio_button.draw(screen, 'hover'):
                    if audio_button_bright.draw(screen):
                        running = False
                        audio_menu()
                    if not audio_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        audio_hovered = True
                else:
                    audio_button.draw(screen)
                    audio_hovered = False

                if video_button.draw(screen, 'hover'):
                    video_button_bright.draw(screen)
                    if not video_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        video_hovered = True
                else:
                    video_button.draw(screen)
                    video_hovered = False

                if back_button.draw(screen, 'hover'):
                    if back_button_bright.draw(screen):
                        running = False
                        main_menu(self,True)
                    if not back_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        back_hovered = True
                else:
                    back_button.draw(screen)
                    back_hovered = False



                pygame.display.update()
                clock.tick(FPS)

        # def audio_menu():
        #
        #     settings_bg = pygame.image.load('Images/settings_bg.png').convert_alpha()
        #     settings_bg = pygame.transform.scale(settings_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #
        #     running = True
        #     while running:
        #         screen.fill(BLACK_COLOR)
        #         screen.blit(settings_bg, (0, 0))
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 running = False
        #                 pygame.quit()
        #                 sys.exit()
        #             elif event.type == pygame.KEYDOWN:
        #                 if event.key == pygame.K_ESCAPE:
        #                     running = False


        main_menu(self,False)

        pygame.quit()
        sys.exit()

Menu()