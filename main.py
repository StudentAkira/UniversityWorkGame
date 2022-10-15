import pygame
import json
import sys
import math
import time
import random
import threading

class Player:
    def __init__(self, name='Player', rating = 0, level = 0, money = 0, inventory = []):
        self.name = name
        self.level = level
        self.money = money
        self.inventory = inventory
        self.rating = rating
        self.position_x = 0
        self.position_y = 0

    def save_data(self):
        data = {
            "name":self.name,
            "rating":self.rating,
            "level":self.level,
            "money":self.money,
            "inventory":self.inventory
        }
        data_ = json.dumps(data)
        with open(f'{self.name}','w') as file:
            file.write(data_)

    def open_data(self, palyer_name=""):
        try:
            with open(f'{palyer_name}','r') as file:
                data = json.load(file)
                self.name = data['name']
                self.rating = data['rating']
                self.level = data['level']
                self.money = data['money']
                self.inventory = data['inventory']

        except:
            print("NO SUCH PLAYER")

    def show_player_data(self):
        print(" Name :: ", self.name)
        print(" Rating :: ", self.rating)
        print(" Level :: ", self.level)
        print(" Money :: ", self.money)
        print(" Inventory :: ", self.inventory)

    def draw_on_map(self, world):
        step = world.sqared_side_length
        x = self.position_x
        y = self.position_y

        hero = pygame.image.load('images/Venty.png')
        #rundom numbers
        hero = pygame.transform.scale(hero, (30, 50))
        hero_rect = hero.get_rect(
            center=(x*step,y*step)
        )
        screen.blit(hero, hero_rect)

    def beat(self, charecer):
        mouse_postition = pygame.mouse.get_pos()
        beat_pos_x = int(mouse_postition[0]/world.sqared_side_length)
        beat_pos_y = int(mouse_postition[1]/world.sqared_side_length)
        print(beat_pos_x, beat_pos_y)

        i = self.position_x
        j = self.position_y
        while i < beat_pos_x or j < beat_pos_y:
            while i < charecer.damage_engle:
                if world.focused[i] == -1:
                    pass


class Charecter:

    def __init__(self, id=-1, name='', history='', rarity=0, health=0, damage=0, damage_engle=2):
        self.id = id
        self.name = name
        self.history = history
        self.rarity = rarity
        self.health = health
        self.damage = damage

    def save_data(self):
        data = {
            "id":self.id,
            "name":self.name,
            "history":self.history,
            "rarity":self.rarity,
            "health":self.health,
            "damage":self.damage
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
            self.health = data['health']
            self.damage = data['damage']
        return self

    def print_data(self):
        print({
            "id":self.id,
            "name":self.name,
            "history":self.history,
            "rarity":self.rarity,
            "health":self.health,
            "damage":self.damage
        })

class Mob:

    health = 500
    damage = 30
    def draw_on_map(self):
        step = world.sqared_side_length

        mob = pygame.image.load('images/Mob.png')
        mob = pygame.transform.scale(mob, (30, 50))
        world.field[int(200/step)][int(200/step)] = -1
        mob_rect = mob.get_rect(
            center=(300, 200)
        )
        screen.blit(mob, mob_rect)

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
        pygame.draw.rect(screen, (90, 90, 90), (self.pos[0] - self.radius,
                                                self.pos[1] - self.radius,
                                                self.pos[0] + self.radius,
                                                self.pos[1] + self.radius))


    def show_wheel(self, start=0):

        pygame.draw.circle(self.screen, self.color,
                   self.pos, self.radius, 2)

        pi = math.pi
        start = start

        x = self.pos[0]
        y = self.pos[1]

        next_x = x + self.radius * math.cos(start)
        next_y = y - self.radius * math.sin(start)


        pygame.draw.line(screen, self.color, [x, y], [next_x, next_y])

        for i in range(len(self.charecters)):
            chance = 1/charecters[i].rarity
            #TODO
            font = pygame.font.SysFont('Corbel', 15)
            text = font.render(charecters[i].name, True, [200, 200, 200])
            text = pygame.transform.rotate(text, (360 * (start - chance * pi)) / (2 * pi) )
            screen.blit(text, [
                int(x + 0.5 * self.radius * math.cos(start - chance * pi) - 0.5*text.get_size()[0]),
                int(y - 0.5 * self.radius * math.sin(start - chance * pi) - 0.5*text.get_size()[1])
            ])

            next_x = int(x + self.radius * math.cos(start - chance * 2 * pi))
            next_y = int(y - self.radius * math.sin(start - chance * 2 * pi))
            pygame.draw.line(screen, self.color, [x, y], [next_x, next_y])
            start -= chance*2*pi


    def spin_wheel(self, player):

        pi = math.pi
        chosen_charecter_location = random.uniform(0, 2 * pi)
        passed_circle_area = 0

        chosen_charecter = self.charecters[0]
        for i in range(len(self.charecters)-1, -1, -1):
            passed_circle_area += 2*pi*(1/self.charecters[i].rarity)
            if(passed_circle_area > chosen_charecter_location):
                chosen_charecter = self.charecters[i]
                break;

        print(chosen_charecter_location)
        chosen_charecter.print_data()
        spin = 360+(360*chosen_charecter_location)/(2*pi)
        speed = 3
        j = speed
        clock = pygame.time.Clock()
        while j < spin:
            self.hide()
            pygame.draw.line(screen, self.color, [self.pos[0] + 0.9 * self.pos[0], self.pos[1]],
                             [self.pos[0] + self.pos[0], self.pos[1]])
            start = 0 - (pi * 2 / 360) * j
            self.show_wheel(start)
            clock.tick(40)
            j += speed
            if(j > 0.8 * spin): speed = 1
            if (j > 0.95 * spin): speed = 0.2
        player.inventory.append(chosen_charecter.id)
        player.show_player_data()
        player.save_data()

class Button:
    font_size = 35

    def __init__(self, x, y, text="empty button", focused=False):

        smallfont = pygame.font.SysFont('Corbel', self.font_size)
        self.text_rect = smallfont.render(text, True, (200, 200, 200))

        self.button_position_x = x * width - 0.5 * self.text_rect.get_size()[0]
        self.button_position_y = y * height - 0.5 * self.text_rect.get_size()[1]
        self.text = text
        self.focused = focused

    def draw(self):
        screen.blit(self.text_rect, (
            self.button_position_x,
            self.button_position_y
        ))
        self.focused = True
        
    def hide(self):
        pygame.draw.rect(screen, (90,90,90),[
            self.button_position_x,
            self.button_position_y,
            self.text_rect.get_size()[0],
            self.text_rect.get_size()[1]
        ])
        
        self.focused = False


    def clicked(self):

        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        if self.button_position_x \
                <= mouse[0] <= self.button_position_x + self.font_size\
                *len(self.text) and self.button_position_y <= mouse[1] \
                    <= self.button_position_y + self.font_size and self.focused:
            return True
        
        return  False

class World:

    def __init__(self, w = 200, h = 120):
        self.w = w#row
        self.h = h#column
        self.sqared_side_length = 4

        self.field = [[0 for j in range(self.w)] for i in range(int(self.h))]
        self.focused = False

    def draw_border(self):
        pygame.draw.rect(screen, (255, 90, 90), [
            1,
            1,
            self.w * self.sqared_side_length,
            self.h * self.sqared_side_length
        ], 1)
    def draw(self):
        self.draw_border()
        self.focused = True
        for h in range(int(len(self.field))):
            for w in range(len(self.field[h])):
                pygame.draw.rect(screen, (90, 90, 90), [
                    (w*self.sqared_side_length),
                    (h*self.sqared_side_length),
                    (self.sqared_side_length),
                    (self.sqared_side_length)
                ], 1)

    def hide(self):
        self.focused = False
        screen.fill((90, 90, 90))

    def spawn_mob(self):
        mob = Mob()
        mob.draw_on_map()

    def splawn_player(self, player, prev_x=0, prev_y=0, new_x=0, new_y=0):

        pygame.draw.rect(screen, (90, 90, 90), [
            prev_x*self.sqared_side_length-15,
            prev_y*self.sqared_side_length-25,
            30,
            50
        ],)
        self.draw_border()
        if new_x > world.w: new_x = 0
        if new_x < 0: new_x = world.w - 1
        if new_y > world.h: new_y = 0
        if new_y < 0: new_y = world.h - 1
        
        player.position_x = new_x
        player.position_y = new_y
        player.draw_on_map(self)


width = 1200
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height))
screen.fill((90,90,90))

charecters = [Charecter().open_data(i) for i in range(7)]

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

player = Player()
player.open_data('Akira')
player.show_player_data()

world = World()

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        prev_position_x = player.position_x
        prev_position_y = player.position_y
        keys = pygame.key.get_pressed()
        if world.focused:
            player.position_x += keys[pygame.K_d] - keys[pygame.K_a]
            player.position_y -= keys[pygame.K_w] - keys[pygame.K_s]

            world.splawn_player(player, prev_position_x, prev_position_y, player.position_x, player.position_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.beat()




        if event.type == pygame.MOUSEBUTTONDOWN:
            if spin_button.clicked():
                threading.Thread(target=wheel.spin_wheel, args=(player,)).start()
                spin_button.hide()

            if exit_button.clicked():
                pygame.quit()
                sys.exit()

            if show_wheel_button.clicked():
                wheel.shuf_charecters()
                show_wheel_button.hide()
                play_button.hide()
                spin_button.draw()
                back_menu_button.draw()
                threading.Thread(target=wheel.show_wheel).start()

            if back_menu_button.clicked():
                player.position_x = 0
                player.position_y = 0
                world.hide()
                spin_button.hide()
                wheel.hide()
                back_menu_button.hide()
                show_wheel_button.draw()
                play_button.draw()
                exit_button.draw()

            if play_button.clicked():
                play_button.hide()
                show_wheel_button.hide()
                world.draw()
                world.spawn_mob()
                world.splawn_player(player, 0, 0, 20, 20)
                back_menu_button.draw()
                exit_button.draw()








