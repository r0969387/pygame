"""THE START CODE OF MY MAIN GAME"""
# imports
import pygame
import sys
from menu import *
from settings import *
import random
from pygame import mixer
from draw_text import *
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils



boss_group = pygame.sprite.Group()
boss_bullets_group = pygame.sprite.Group()


def draw_dg():
    screen.blit(bg, (0, 0))

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image_defualt = pygame.image.load('images/zelenskiy v litaky.png')
        self.image_defualt = pygame.transform.scale(self.image_defualt, (150, 100))

        self.image_shooting = pygame.image.load('images/zelenskiy v litaky(1).png')
        self.image_shooting = pygame.transform.scale(self.image_shooting, (100, 175))

        self.image_mirrored = pygame.image.load('images/zelenskiy-v-litaky-mirrored.png')
        self.image_mirrored = pygame.transform.scale(self.image_mirrored, (150, 100))

        self.image_normal = pygame.image.load('images/zelenskiy-v-litaky-normal.png')
        self.image_normal = pygame.transform.scale(self.image_normal, (150, 100))

        self.image = self.image_defualt
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

        # pygame.mixer.music.play()
        pygame.mixer.music.stop()

        self.bullet_type = 1

        ''' adding phisics '''
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.5
        self.max_speed = 10
        self.friction = 0.1

        # cooldown variable
        self.shooting_cooldown = 1000
        self.minimum_cooldown = 100  # Minimum cooldown limit
        self.cooldown_reduction = 900  # Amount to reduce the cooldown by
        self.boost_duration = 3000
        self.cooldown_boost_active = False
        self.boost_start_time = 0
        '''how often i shot the bullets'''
        self.shooting = False
        self.shooting_time = 0

        self.use_hand_tracking = False
        self.cap = None

        self.bullet_type = 'regular'



    def update(self):
        game_over = 0

        if self.shooting:
            offset_y = 50
            offset_x = -30
        else:
            offset_y = 0
            offset_x = 0

        if self.cooldown_boost_active:
            if pygame.time.get_ticks() - self.boost_start_time > self.boost_duration:
                self.shooting_cooldown += self.cooldown_reduction
                self.bullet_type = 'regular'  # Change back to regular bullets
                self.cooldown_boost_active = False

        # make a pixel mask for spaceship
        self.mask = pygame.mask.from_surface(self.image)

        if self.use_hand_tracking and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        wrist = hand_landmarks.landmark[0]
                        wrist_x = wrist.x * screen_width
                        wrist_y = wrist.y * screen_height

                        self.vel_x = (wrist_x - self.rect.centerx) * 0.05
                        self.vel_y = (wrist_y - self.rect.centery) * 0.05

                        time_now = pygame.time.get_ticks()

                        if abs(self.vel_x) > self.max_speed:
                            self.vel_x = self.max_speed * (self.vel_x / abs(self.vel_x))
                        if abs(self.vel_y) > self.max_speed:
                            self.vel_y = self.max_speed * (self.vel_y / abs(self.vel_y))

                        if self.vel_x > 0:
                            self.image_default = self.image_mirrored
                        elif self.vel_x < 0:
                            self.image_default = self.image_normal

                        thumb_tip = hand_landmarks.landmark[4]
                        index_mcp = hand_landmarks.landmark[5]
                        middle_mcp = hand_landmarks.landmark[9]
                        ring_mcp = hand_landmarks.landmark[13]
                        pinky_mcp = hand_landmarks.landmark[17]
                        index_tip = hand_landmarks.landmark[8]
                        middle_tip = hand_landmarks.landmark[12]
                        ring_tip = hand_landmarks.landmark[16]
                        pinky_tip = hand_landmarks.landmark[20]

                        is_fist = (
                                index_tip.y > index_mcp.y and
                                middle_tip.y > middle_mcp.y and
                                ring_tip.y > ring_mcp.y and
                                pinky_tip.y > pinky_mcp.y and
                                abs(thumb_tip.x - index_mcp.x) < 0.05
                        )

                        if is_fist and time_now - self.last_shot > self.shooting_cooldown:
                            self.shooting = True
                            if self.bullet_type == 'boosted':
                                missile_sound.play()
                                bullet = Bullets_2(self.rect.centerx, self.rect.top)
                            else:
                                bullet = Bullets(self.rect.centerx, self.rect.top)
                                machine_gun.play()
                            bullet_group.add(bullet)
                            self.last_shot = time_now
                            self.shooting_time = time_now

                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    cv2.imshow("Hand Tracking", frame)

        # Get key presses
        key = pygame.key.get_pressed()
        # Horizontal movement (left and right)
        if key[pygame.K_d]:  # Move right
            self.vel_x += self.acceleration
            self.image_defualt = self.image_mirrored

        elif key[pygame.K_a]:  # Move left
            self.vel_x -= self.acceleration
            self.image_defualt = self.image_normal

        else:
            # Apply friction when no key is pressed
            if self.vel_x > 0:
                self.vel_x -= self.friction
            elif self.vel_x < 0:
                self.vel_x += self.friction

        # Vertical movement (up and down, if needed)
        if key[pygame.K_w]:  # Move up (if desired)
            self.vel_y -= self.acceleration
        elif key[pygame.K_s]:  # Move down (if desired)
            self.vel_y += self.acceleration
        else:
            # Apply friction for vertical movement
            if self.vel_y > 0:
                self.vel_y -= self.friction
            elif self.vel_y < 0:
                self.vel_y += self.friction

        # Limit the velocity (max speed)
        if abs(self.vel_x) > self.max_speed:
            self.vel_x = self.max_speed * (self.vel_x / abs(self.vel_x))
        if abs(self.vel_y) > self.max_speed:
            self.vel_y = self.max_speed * (self.vel_y / abs(self.vel_y))

        # Update the spaceship's position based on velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Keep the spaceship within screen boundaries
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.vel_x = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.vel_y = 0
        if self.rect.top < 100:
            self.vel_y = -self.vel_y

        # record time
        time_now = pygame.time.get_ticks()
        # shooting
        if pygame.mouse.get_pressed()[0] and time_now - self.last_shot > self.shooting_cooldown:
            self.shooting = True

            if (pygame.mouse.get_pressed()[0]
                    and pygame.time.get_ticks() - self.last_shot > self.shooting_cooldown):
                self.shooting = True
                if self.bullet_type == 'boosted':
                    missile_sound.play()
                    bullet = Bullets_2(self.rect.centerx, self.rect.top)
                else:
                    bullet = Bullets(self.rect.centerx, self.rect.top)
                    machine_gun.play()
                bullet_group.add(bullet)
                self.last_shot = pygame.time.get_ticks()
                self.shooting_time = pygame.time.get_ticks()

        if self.shooting:
            if time_now - self.shooting_time > self.shooting_cooldown:
                self.shooting = False

        if self.shooting:
            self.image = self.image_shooting

        else:
            self.image = self.image_defualt

            # Check if cooldown boost is active and reset after 5 seconds
            if self.cooldown_boost_active:
                if time_now - self.boost_start_time > self.boost_duration:
                    self.shooting_cooldown += self.cooldown_reduction  # Reset the cooldown back
                    self.cooldown_boost_active = False

        # health bar logic and then losing logic with explotions
        pygame.draw.rect(screen, red,(self.rect.x + 30 + offset_x, (self.rect.bottom + 5 + offset_y), 100, 6))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green,(self.rect.x + 30 + offset_x, (self.rect.bottom + 5 + offset_y),
                              100 * (self.health_remaining / self.health_start), 6))
        elif self.health_remaining <= 0:
            explosion = Explosions(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1

        return game_over

    def set_bullet_type(self, new_type):
        self.bullet_type = new_type

    def activate_cooldown_boost(self):
        """ Activates the cooldown boost, reducing the cooldown for 5 seconds """
        if not self.cooldown_boost_active:
            self.shooting_cooldown = max(self.minimum_cooldown,
                                         self.shooting_cooldown - self.cooldown_reduction)
            self.bullet_type = 'boosted'
            self.cooldown_boost_active = True
            self.boost_start_time = pygame.time.get_ticks()

    def enable_hand_tracking(self):
        print("Enabling hand tracking...")
        self.use_hand_tracking = True
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open camera.")
                self.use_hand_tracking = False

    def disable_hand_tracking(self):
        print("Disabling hand tracking...")
        self.use_hand_tracking = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()


#Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/boss.png')
        self.image = pygame.transform.scale(self.image, (600, 400))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.health_start = health
        self.health_remaining = health
        self.move_direction = 1
        self.move_speed = 2
        self.shooting_cooldown = 2000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        global game_over
        game_over = 0
        self.rect.x += self.move_direction * self.move_speed

        if self.rect.right > screen_width or self.rect.left < 0:
            self.move_direction *= -1

        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.shooting_cooldown:
            self.shoot()
            self.last_shot = time_now


        pygame.draw.rect(screen, red,(self.rect.x + 200 , (self.rect.bottom - 100 ), 200, 6))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green,(self.rect.x + 200, (self.rect.bottom - 100),
                              200 * (self.health_remaining / self.health_start), 6))

        elif self.health_remaining <= 0:
            explosion = Explosions(self.rect.centerx, self.rect.centery, 4)
            explosion_group.add(explosion)
            self.kill()
            print("Boss defeated! Game should end.")
            game_over = 1


    def shoot(self):
        bullet_positions = [self.rect.centerx - 150, self.rect.centerx, self.rect.centerx + 150]
        for pos in bullet_positions:
            bullet = Boss_Bullets(pos, self.rect.bottom)
            boss_bullets_group.add(bullet)


class Boss_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/missile.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 5
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_remaining -= 1
            damage_sound.play()
            explosion = Explosions(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.image = pygame.transform.scale(self.image, (70, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y -= 5
        if self.rect.bottom < 50:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask):
            self.kill()
            global points
            points += 1
            explotion_sound.play()
            explosion = Explosions(self.rect.centerx, self.rect.centery - 50, 2)
            explosion_group.add(explosion)
        elif pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
            self.kill()
            for boss in boss_group:
                boss.health_remaining -= 1
                explotion_sound.play()
                explosion = Explosions(self.rect.centerx, self.rect.centery - 50, 4)
                explosion_group.add(explosion)

class Bullets_2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/missile_3.png')
        self.image = pygame.transform.scale(self.image, (70, 140))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y -= 7
        if self.rect.bottom < 50:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask):
            self.kill()
            global points
            points += 1
            explotion_sound.play()
            explosion = Explosions(self.rect.centerx, self.rect.centery - 50, 4)
            explosion_group.add(explosion)

class Bullets_boost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/America_PNG.png')
        self.image = pygame.transform.scale(self.image, (120, 40))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1

        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.set_bullet_type(2)
            spaceship.activate_cooldown_boost()
            bullets_boost_sound.play()

class Revo_Gray(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/revo_gray.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1

        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce the health of spaceship
            spaceship.health_remaining = min(spaceship.health_remaining + 2, MAX_HEATLH)
            revo_healing.play()
            # explosion = Explosions(self.rect.centerx, self.rect.centery, 3)
            # explosion_group.add(explosion)  AND MAYBE TH ANIMATION OF HEALTING

class Revo_Red(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/revo_red.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1

        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce the health of spaceship
            spaceship.health_remaining = min(spaceship.health_remaining + 10, MAX_HEATLH)
            revo_red_sound.play()

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        alien_type = random.randint(1, 5)
        self.image = pygame.image.load(f'images/alien{alien_type}.png')
        if alien_type == 1:
            self.image = pygame.transform.scale(self.image, (90, 90))
        if alien_type == 2:
            self.image = pygame.transform.scale(self.image, (130, 90))
        if alien_type == 3:
            self.image = pygame.transform.scale(self.image, (125, 125))
        if alien_type == 4:
            self.image = pygame.transform.scale(self.image, (125, 90))
        if alien_type == 5:
            self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # movement
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if self.rect.top > screen_height:
            self.kill()
            global points
            points -= 5

class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bomb.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 3
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce the health of spaceship
            spaceship.health_remaining -= 1
            damage_sound.play()
            explosion = Explosions(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)

# create explosions class
class Explosions(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'images/Explosion/exp{num}.png')
            if size == 1:
                img = pygame.transform.scale(img, (100, 100))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (60, 60))
            if size == 4:
                img = pygame.transform.scale(img, (150, 150))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # speed of animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        # delete the animation if its fifished
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


def create_aliens(num_aliens):
    for _ in range(num_aliens):
        valid_position = False
        while not valid_position:
            x = random.randint(50, screen_width - 50)
            y = random.randint(-1500, -50)
            new_alien = Aliens(x, y)

            if not pygame.sprite.spritecollide(new_alien, alien_group, False):
                alien_group.add(new_alien)
                valid_position = True


create_aliens(num_aliens)

def create_revo(num_revo):
    for _ in range(num_revo):
        valid_position = False
        while not valid_position:
            x = random.randint(50, screen_width - 50)
            y = random.randint(-1500, -50)
            newe_revo = Revo_Gray(x, y)

            if not pygame.sprite.spritecollide(newe_revo, revo_group, False):
                revo_group.add(newe_revo)
                valid_position = True

create_revo(num_revo)

def create_revo_red(num_revo_red):
    for _ in range(num_revo_red):
        valid_position = False
        while not valid_position:
            x = random.randint(50, screen_width - 50)
            y = random.randint(-1500, -50)
            newe_revo_red = Revo_Red(x, y)

            if not pygame.sprite.spritecollide(newe_revo_red, revo_red_group, False):
                revo_red_group.add(newe_revo_red)
                valid_position = True


create_revo_red(num_revo_red)

def create_bullets_boost(num_bullets_boost):
    for _ in range(num_bullets_boost):
        valid_position = False
        while not valid_position:
            x = random.randint(50, screen_width - 50)
            y = random.randint(-1500, -50)
            newe_bullets_boost = Bullets_boost(x, y)

            if not pygame.sprite.spritecollide(newe_bullets_boost, bullets_boost_group, False):
                bullets_boost_group.add(newe_bullets_boost)
                valid_position = True


create_bullets_boost(num_bullets_boost)

spaceship = SpaceShip(int(screen_width / 2), screen_height - 100, MAX_HEATLH)  # 15 is the health of the spaceship
spaceship_group.add(spaceship)

def restart_game():
    global game_started, game_over, last_alien_shot, countdown, last_count,alien_group, bullet_group, alien_bullet_group, explosion_group, revo_group, revo_red_group, bullets_boost_group, points, boss_group, boss_bullets_group

    # Reset game state
    game_started = False
    game_over = 0
    last_alien_shot = pygame.time.get_ticks()
    countdown = 3
    last_count = pygame.time.get_ticks()
    points = 0

    # Clear all sprite groups
    alien_group.empty()
    bullet_group.empty()
    alien_bullet_group.empty()
    explosion_group.empty()
    revo_group.empty()
    revo_red_group.empty()
    bullets_boost_group.empty()
    boss_group.empty()
    boss_bullets_group.empty()

    # Recreate aliens and revos
    create_aliens(num_aliens)
    create_revo(num_revo)
    create_revo_red(num_revo_red)
    create_bullets_boost(num_bullets_boost)

    # Recreate spaceship

    global spaceship
    spaceship = SpaceShip(int(screen_width / 2), screen_height - 100, MAX_HEATLH)
    spaceship_group.add(spaceship)
    spaceship.enable_hand_tracking()
    pygame.mixer.music.play(-1)  # Play music in a loop when the game restarts

    # Restart music
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(1)

run = True
while run:

    clock.tick(fps)

    draw_dg()

    if not game_started:
        draw_text('Press Space to start the game', 30, screen_width / 2, screen_height / 2 - 50)

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_started = True
            countdown = 3
            last_count = pygame.time.get_ticks()
        if keys[pygame.K_h]:
            spaceship.enable_hand_tracking()

    elif game_started:
        # making work thing only after the countdown is 0
        if countdown > 0:
            draw_text('Get ready', 30, screen_width / 2, screen_height / 2 - 50)
            draw_text(str(countdown), 20, screen_width / 2, screen_height / 2)
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer
        else:
            draw_text(f'Score :  {points}', 20, screen_width / 2 + 500, screen_height / 2 - 325)
            if not pygame.mixer.music.get_busy():  # Play only if not already playing
                pygame.mixer.music.play(-1)  # Loop the soundtrack

            # creating alien bullet shoot
            time_now = pygame.time.get_ticks()
            if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 20 and len(
                    alien_group) > 0:  # here can control the ammount of bullets
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now

                '''Winning and loosing conditions HERE'''
                # check if all aiens are dead
            # if len(alien_group) == 0:
            #     game_over = 1
            #     spaceship.kill()
            global game_over
            if game_over == 0:
                game_over = spaceship.update()
                bullet_group.update()
                alien_group.update()
                alien_bullet_group.update()
                revo_group.update()
                revo_red_group.update()
                boss_group.update()
                boss_bullets_group.update()

            else:
                if game_over == -1:
                    pygame.mixer.music.stop()
                    draw_text('GAME OVER', 30, screen_width / 2, screen_height / 2 - 50)
                    draw_text('Press Enter to restart', 20, screen_width / 2, screen_height / 2 + 50)
                    draw_text('Press Backspace to quit', 20, screen_width / 2, screen_height / 2)
                    draw_text(f'Final Score :  {points}', 20, screen_width / 2, screen_height / 2 + 100)

                if game_over == 1:
                    pygame.mixer.music.stop()
                    draw_text('You won', 30, screen_width / 2, screen_height / 2 - 50)
                    draw_text('Press Enter to restart', 20, screen_width / 2, screen_height / 2 + 50)
                    draw_text('Press Backspace to quit', 20, screen_width / 2, screen_height / 2)

            if points <= -15:
                game_over = -1
                spaceship.kill()

            keys = pygame.key.get_pressed()
            if game_over != 0 and keys[pygame.K_RETURN]:
                restart_game()
            if keys[pygame.K_BACKSPACE]:
                # if self.state == "game_screen":
                #     self.state = self.cur_menu
                pass

            now = pygame.time.get_ticks()
            if now - difficulty_timer > difficulty_interval_aliens:
                difficulty_timer = now
                # Add more aliens to increase difficulty
                create_aliens(num_aliens)
                if points >= 5:
                    create_aliens(num_aliens * 2)
                if points >= 10:
                    create_aliens(num_aliens * 3)
                if points >= 15:
                    create_aliens(num_aliens * 4)
            now2 = pygame.time.get_ticks()
            if now2 - difficulty_timer_revo_gray > difficulty_interval_revo_gray:
                difficulty_timer_revo_gray = now2
                # Add more revo to increase difficulty
                create_revo(num_revo)
            now3 = pygame.time.get_ticks()
            if now3 - difficulty_timer_revo_red > difficulty_interval_revo_red:
                difficulty_timer_revo_red = now3
                # Add more revo to increase difficulty
                create_revo_red(num_revo_red)
            now4 = pygame.time.get_ticks()
            if now4 - difficulty_timer_boost > difficulty_interval_boost:
                difficulty_timer_boost = now4
                # Add more revo to increase difficulty
                create_bullets_boost(num_bullets_boost)

        if boss_spawned == True:
            alien_group.empty()

        #spawn the boss here
        if points >= 2 and not boss_spawned:
            # Spawn the boss
            boss = Boss(screen_width // 2, 200, 15)  # Adjust health and position as needed
            boss_group.add(boss)
            # Change the music
            pygame.mixer.music.load('sounds/boss_song.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            # Mark the boss as spawned
            boss_spawned = True
            print(f"Game Over Status: {game_over}")

    explosion_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)
    revo_group.draw(screen)
    revo_red_group.draw(screen)
    bullets_boost_group.draw(screen)
    boss_group.draw(screen)
    boss_bullets_group.draw(screen)


    def cleanup():
        if 'spaceship' in globals() and spaceship.cap:
            spaceship.cap.release()
        cv2.destroyAllWindows()


    import atexit

    atexit.register(cleanup)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()