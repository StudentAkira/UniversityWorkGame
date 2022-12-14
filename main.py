import pygame
import json
import sys
import math
import time
import random
import threading


pi = math.pi


class Player:
    def __init__(self, name='Player', inventory = []):
        self.name = name
        self.inventory = inventory
        self.kill_count = 0
        self.damage = 0
        self.speed = 0
        self.hp = 0
        self.chosen_charecter_name = 0

        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.can_spin = False
        self.scaled = False

        self.img = pygame.image.load('images/Mob.png')
        self.size = (60, 100)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.rect = self.img.get_rect(
            center=(self.x, self.y)
        )

    def set_charecter(self, charecter):
        self.chosen_charecter = charecter
        self.damage = charecter.damage
        self.speed = charecter.speed
        self.hp = charecter.hp
        self.chosen_charecter_name = charecter.name
        self.img = pygame.image.load(charecter.img)
        self.size = (100, 75)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))

    def save_data(self):
        data = {
            "name":self.name,
            "inventory":self.inventory,
            "killcount":self.kill_count,
        }
        data_ = json.dumps(data)
        with open(f'{self.name}','w') as file:
            file.write(data_)

    def open_data(self, palyer_name=""):
        try:
            with open(f'{palyer_name}','r') as file:
                data = json.load(file)
                self.name = data['name']
                self.inventory = data['inventory']
                self.kill_count = data['killcount']

        except:
            print("NO SUCH PLAYER")

    def show_player_data(self):
        print(" Name :: ", self.name)
        print(" Inventory :: ", self.inventory)

    def hide(self, prev_x, prev_y):
        pygame.draw.rect(screen, (90, 90, 90), (
            prev_x-self.size[0]/2,
            prev_y-self.size[1]/2-30,
            self.size[0]*1.1,
            self.size[1]*1.1 + 30))

    def draw_hp(self, charecters):
        max_hp = list(filter(lambda charecter: charecter.name == self.chosen_charecter.name, charecters))[0].hp
        currecnt_hp = self.hp

        pygame.draw.rect(screen, (0, 0, 0), (
            self.x - self.size[0]/2,
            self.y - self.size[1]/2 - 30,
            self.size[0],
            5))

        pygame.draw.rect(screen, (200, 200, 200), (
            self.x - self.size[0]/2,
            self.y - self.size[1]/2 - 30,
            self.size[0]*(currecnt_hp/max_hp),
            5))

    def draw(self, win, charecters):
        if world.focused:
            world.draw()
            screen.blit(self.img, self.rect)
            self.draw_hp(charecters)


    def update(self):
        self.velX = 0
        self.velY = 0
        if world.focused:

            if self.left_pressed and not self.right_pressed:
                self.velX = -self.speed
            if self.right_pressed and not self.left_pressed:
                self.velX = self.speed
            if self.up_pressed and not self.down_pressed:
                self.velY = -self.speed
            if self.down_pressed and not self.up_pressed:
                self.velY = self.speed

            prev_x = self.x
            prev_y = self.y

            self.hide(prev_x, prev_y)

            self.x += self.velX
            self.y += self.velY

            if self.x > world.w : self.x = 0
            if self.x < 0 : self.x = world.w - 1
            if self.y > world.h : self.y = 0
            if self.y < 0 : self.y = world.h - 1

            self.rect = self.img.get_rect(
                center=(self.x, self.y)
            )


            moving_right = self.x-prev_x > 0 and not self.scaled
            moving_left = self.x - prev_x < 0 and self.scaled

            if moving_right:
                self.img = pygame.transform.flip(self.img, True, False)
                self.scaled = True

            if moving_left:
                self.img = pygame.transform.flip(self.img, True, False)
                self.scaled = False
                
            return

    def attack(self, mobs):
        for mob in mobs:
            if self.rect.colliderect(mob.rect):
                mob.hp -= player.damage


class Charecter:

    def __init__(self, id = -1, name = '', history = '', rarity = 0, hp = 0, damage = 0, speed = 1):
        self.id = id
        self.name = name
        self.history = history
        self.rarity = rarity
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.img = ''

    def save_data(self):
        data = {
            "id":self.id,
            "name":self.name,
            "history":self.history,
            "rarity":self.rarity,
            "hp":self.hp,
            "damage":self.damage,
            "speed": self.speed,
            "img": self.img,
        }
        data_ = json.dumps(data)
        with open('charecters','r+') as file:

            file.seek(0, 2)
            file.write(data_)
            file.write('\n')

    def open_data(self, charecter_id):
        with open('charecters','r') as file:
            data = file.readlines()[charecter_id]
            data = json.loads(data)
            self.id = data['id']
            self.name = data['name']
            self.history = data['history']
            self.rarity = data['rarity']
            self.hp = data['hp']
            self.damage = data['damage']
            self.speed = data['speed']
            self.img = data['img']
        return self

    def print_data(self):
        print({
            "id":self.id,
            "name":self.name,
            "history":self.history,
            "rarity":self.rarity,
            "hp":self.hp,
            "damage":self.damage
        })


class  Mob(Player):

    def __init__(self, world):
        super(Mob, self).__init__(self)
        self.world = world
        self.chosen_charecter = Charecter(-1,#id
                                          'NoName',#name
                                          '',#history
                                          0,#rarity
                                          random.randint(1000, 18000),#hp
                                          random.randint(1, 2),#damage
                                          random.randint(1, 3))#speed
        self.hp = self.chosen_charecter.hp
        self.damage = self.chosen_charecter.damage
        self.x = random.randint(0, world.w-1)
        self.y = random.randint(0, world.h-1)

        self.img = pygame.image.load('images/Mob.png')
        self.size = (30, 50)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.rect = self.img.get_rect(
            center=(self.x, self.y)
        )

        self.speed = self.chosen_charecter.speed


    def follow_player(self):
        if world.focused and not self.rect.colliderect(player.rect):
            self.hide(self.x, self.y)

            self.velX = 0
            self.velY = 0

            sign_x = 1 if player.x - self.x > 0 else -1
            sign_y = 1 if player.y - self.y > 0 else -1

            prev_x = self.x
            prev_y = self.y

            self.velX += self.speed*sign_x
            self.velY -= self.speed*sign_y

            self.x += self.velX
            self.y -= self.velY

            moving_right = self.x - prev_x > 0 and not self.scaled
            moving_left = self.x - prev_x < 0 and self.scaled

            if moving_right:
                self.img = pygame.transform.flip(self.img, True, False)
                self.scaled = True

            if moving_left:
                self.img = pygame.transform.flip(self.img, True, False)
                self.scaled = False

            self.rect = self.img.get_rect(
                center=(self.x, self.y)
            )
            self.draw(screen, [self.chosen_charecter])
        self.attack()

    def attack(self):
        if self.rect.colliderect(player.rect):
            player.hp -= mob.damage
            world.update_tmp_charecters()


class WheelOfLuck:

    color = [0, 20, 0]
    display = False
    spin = False

    def __init__(self, screen, charecters, y_pos, radius = 100):

        self.screen = screen
        self.charecters = charecters

        self.shuf_charecters()

        self.amount_of_charecters = len(charecters)
        self.pos = [radius, y_pos]
        self.radius = radius

    def shuf_charecters(self):
        random.shuffle(self.charecters)

    def hide(self):
        pygame.draw.rect(screen, (90, 90, 90), (
            self.pos[0] - self.radius,
            self.pos[1] - self.radius,
            self.pos[0] + self.radius,
            self.pos[1] + self.radius)
            )

    def draw_wheel_segment(self, name, rarity, start):
        chance = 1 / rarity

        x = self.pos[0]
        y = self.pos[1]

        font = pygame.font.SysFont('Corbel', 15)
        text = font.render(name, True, [200, 200, 200])
        text = pygame.transform.rotate(text, (360 * (start - chance * pi)) / (2 * pi))
        screen.blit(text, [
            int(x + 0.5 * self.radius * math.cos(start - chance * pi) - 0.5 * text.get_size()[0]),
            int(y - 0.5 * self.radius * math.sin(start - chance * pi) - 0.5 * text.get_size()[1])
        ])

        next_x = int(x + self.radius * math.cos(start - chance * 2 * pi))
        next_y = int(y - self.radius * math.sin(start - chance * 2 * pi))
        pygame.draw.line(screen, self.color, [x, y], [next_x, next_y])


    def show_wheel(self, start=0):

        pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 2)

        start = start
        x = self.pos[0]
        y = self.pos[1]
        next_x = x + self.radius * math.cos(start)
        next_y = y - self.radius * math.sin(start)

        pygame.draw.line(screen, self.color, [x, y], [next_x, next_y])

        for name, rarity in [(ch.name, ch.rarity) for ch in self.charecters]:
            chance = 1/rarity
            self.draw_wheel_segment(name, rarity, start)
            start -= chance*2*pi


    def generate_result(self):
        generated_charecter_location = random.uniform(0, 2 * pi)
        passed_circle_area = 0

        generated_charecter = self.charecters[0]
        for charecter in self.charecters[::-1]:
            passed_circle_area += 2 * pi * (1 / charecter.rarity)
            if (passed_circle_area > generated_charecter_location):
                generated_charecter = charecter
                break;
        return  (generated_charecter_location, generated_charecter)


    def spin_wheel(self, player):

        generated_charecter_location, generated_charecter = self.generate_result()

        generated_charecter.print_data()

        in_radiance_generated_charecter_location = (360*generated_charecter_location)/(2*pi)
        spin = 360+in_radiance_generated_charecter_location
        speed = 3
        j = speed
        clock = pygame.time.Clock()
        while j < spin:
            self.hide()
            pygame.draw.line(screen, self.color, [self.pos[0] + 0.9 * self.pos[0], self.pos[1]],
                             [self.pos[0] + self.pos[0], self.pos[1]])#result_pointer


            start = 0 - (2* pi / 360) * j
            self.show_wheel(start)
            clock.tick(40)
            j += speed
            if(j > 0.8 * spin): speed = 1
            if (j > 0.95 * spin): speed = 0.2

        if generated_charecter.id not in player.inventory:
            player.inventory.append(generated_charecter.id)
            player.show_player_data()
            player.save_data()


class Button:

    def __init__(self, x, y, text="empty button", focused=False, fs=35):
        self.font_size = fs
        self.smallfont = pygame.font.SysFont('Corbel', self.font_size)
        self.text_rect = self.smallfont.render(text, True, (200, 200, 200))

        self.button_position_x = x * width - 0.5 * self.text_rect.get_size()[0]
        self.button_position_y = y * height - 0.5 * self.text_rect.get_size()[1]
        self.text = text
        self.focused = focused

    def draw(self, additional_info = ''):
        screen.blit(self.text_rect, (
            self.button_position_x,
            self.button_position_y
        ))

        additional_info_text = self.smallfont.render(additional_info, True, (200, 200, 200))

        screen.blit(additional_info_text, (
            self.button_position_x,
            self.button_position_y - 20
        ))
        self.focused = True

        
    def hide(self):
        pygame.draw.rect(screen, (90,90,90),[
            self.button_position_x,
            self.button_position_y - 50,
            self.text_rect.get_size()[0] + 50,
            self.text_rect.get_size()[1] + 50
        ])
        self.focused = False


    def clicked(self, forced = False):
        if forced: forced
        pygame.display.update()
        mouse = pygame.mouse.get_pos()

        mouse_on_button_by_x = self.button_position_x <= mouse[0] <= self.button_position_x + len(self.text)*self.font_size
        mouse_on_button_by_y = self.button_position_y <= mouse[1] <= self.button_position_y + self.font_size and self.focused
        mouse_on_button = mouse_on_button_by_x and mouse_on_button_by_y

        if mouse_on_button and self.focused:
            return True
        return  False


class World:

    def __init__(self, player, charecters, w = 1000, h = 400):
        self.focused = False
        self.player = player
        self.charecters = charecters
        self.w = w
        self.h = h
        self.spawnd_delay = 0.3
        self.charecters_switch_buttons = []
        self.names_of_existing = []
        self.tmp_charecters = [charecters[charecter_id] for charecter_id in self.player.inventory]

        for player_charecter_id in player.inventory:
            for charecter_id, charecter_name in [(charecter.id, charecter.name) for charecter in charecters]:
                if charecter_id == player_charecter_id:
                    self.names_of_existing.append(charecter_name)
        for button_number, button_text in list(zip(range(len(self.names_of_existing)), self.names_of_existing)):
            self.charecters_switch_buttons.append(Button(0.1 + 0.1 * button_number, 0.9, button_text, True, 15))

    def draw_border(self):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.w, self.h), 1)

    def draw_charecters_switch_buttons(self):
        for charecter_switch_button in self.charecters_switch_buttons:
            charecter_switch_button.hide()
            charecter_hp = list(filter(lambda charecter:charecter.name == charecter_switch_button.text, self.tmp_charecters))[0].hp

            charecter_switch_button.draw(str(charecter_hp))

    def draw(self):
        self.focused = True
        self.draw_border()
        self.draw_charecters_switch_buttons()

    def hide(self):
        self.focused = False
        screen.fill((90, 90, 90))
        for charecter_switch_button in self.charecters_switch_buttons:
            charecter_switch_button.hide()

    def spawn_mobs(self, mobs, max_mobs):
        while world.focused:
            time.sleep(self.spawnd_delay)
            mobs.append(Mob(self))

    def update_tmp_charecters(self):
        damaged_charecter = list(filter(lambda charecter: charecter.name == self.player.chosen_charecter.name, self.tmp_charecters))[0]
        self.tmp_charecters[self.tmp_charecters.index(damaged_charecter)].hp = self.player.hp

    def check_swith_buttons(self):
        for button in self.charecters_switch_buttons:
            if button.clicked():
                prev_charecter = self.player.chosen_charecter
                #self.tmp_charecters[self.tmp_charecters.index(prev_charecter)].hp = self.player.hp
                current_charecter = list(filter(lambda charecter:charecter.name == button.text, self.tmp_charecters))[0]
                self.player.set_charecter(current_charecter)
                print([(charecter.name, charecter.hp) for charecter in self.tmp_charecters])



width = 1200
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height))

screen.fill((90,90,90))

charecters = [Charecter().open_data(i) for i in range(7)]

player = Player()
player.open_data('Akira')
player.set_charecter(charecters[player.inventory[0]])
player.show_player_data()

world = World(player, charecters)
mobs = []

wheel = WheelOfLuck(screen, charecters, height/2, 175)


spin_button = Button(0.33, 0.5, 'SPIN', True)
spin_button.hide()
back_menu_button = Button(0.9, 0.8, 'Back to menu', True)
back_menu_button.hide()
exit_button = Button(0.9, 0.9, 'EXIT', True)
exit_button.draw()
show_wheel_button = Button(0.5, 0.5, 'WHEEL', False)
show_wheel_button.draw()
play_button = Button(0.5, 0.43, 'PLAY', True)
play_button.draw()


spin_coast = 10


while True:

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.attack(mobs)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True

        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if spin_button.clicked():
                threading.Thread(target=wheel.spin_wheel, args=(player,)).start()
                spin_button.hide()
                player.can_spin = False
                player.save_data()

            if exit_button.clicked():
                pygame.quit()
                sys.exit()

            if show_wheel_button.clicked():
                wheel.shuf_charecters()
                show_wheel_button.hide()
                play_button.hide()
                if player.can_spin:
                    spin_button.draw()
                back_menu_button.draw()
                threading.Thread(target=wheel.show_wheel).start()

            if back_menu_button.clicked():
                world = World(player, charecters)
                player.x = 50
                player.y = 50
                screen.fill((90, 90, 90))
                world.hide()
                wheel.hide()
                back_menu_button.hide()
                show_wheel_button.draw()
                play_button.draw()
                exit_button.draw()

            if play_button.clicked():
                prev_kill_count = player.kill_count
                print(player.inventory)
                charecters = [Charecter().open_data(i) for i in range(7)]
                player.set_charecter(charecters[player.inventory[0]])
                tmp_charecters = [charecters[i] for i in player.inventory]
                mobs_spawning = threading.Thread(target=world.spawn_mobs, args=(mobs, 10))
                player.x = 50
                player.y = 50
                play_button.hide()
                show_wheel_button.hide()
                back_menu_button.draw()
                exit_button.draw()
                world.draw()
                mobs_spawning.start()

            world.check_swith_buttons()

    if world.focused:
        for mob in mobs:
            if player.hp < 0:
                world = World(player, charecters)
                player.set_charecter(charecters[player.inventory[0]])
                player.save_data()
                player.x = 50
                player.y = 50
                screen.fill((90, 90, 90))
                world.hide()
                back_menu_button.hide()
                show_wheel_button.draw()
                play_button.draw()
                exit_button.draw()
                mobs = []
                break
            if mob.hp > 0:
                mob.follow_player()
                continue
            mob.hide(mob.x, mob.y)
            mobs.remove(mob)
            player.kill_count += 1
            if player.kill_count - prev_kill_count > spin_coast: player.can_spin = True

    player.update()
    player.draw(screen, charecters)
    pygame.display.flip()
