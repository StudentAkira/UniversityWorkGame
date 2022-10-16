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

        self.x = 0
        self.y = 0

        self.img = pygame.image.load('images/Mob.png')
        self.size = (30, 50)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.rect = self.img.get_rect(
            center=(self.x, self.y)
        )

        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 1
        self.scaled = False


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

    def hide(self, prev_x, prev_y):
        pygame.draw.rect(screen, (90, 90, 90), (prev_x-self.size[0]/2,
                                                prev_y-self.size[1]/2,
                                                self.size[0],
                                                self.size[1]))

    def draw(self, win):
        if world.focused:
            world.draw()
            screen.blit(self.img, self.rect)

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
            if self.x < 0 : self.x = world.w-1
            if self.y > world.h : self.y = 0
            if self.y < 0 : self.y = world.h-1

            self.rect = self.img.get_rect(
                center=(self.x, self.y)
            )

            if self.x-prev_x > 0 and not self.scaled:
                player.img = pygame.transform.flip(player.img, True, False)
                self.scaled = True

            if self.x - prev_x < 0 and self.scaled:
                player.img = pygame.transform.flip(player.img, True, False)
                self.scaled = False
                
            return

        #spawn place
        self.x = 200
        self.y = 200


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

    def __init__(self, w = 1000, h = 400):
        self.focused = False
        self.w = w
        self.h = h

    def draw_border(self):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.w, self.h), 1)

    def draw(self):
        self.focused = True
        self.draw_border()

    def hide(self):
        self.focused = False
        screen.fill((90, 90, 90))



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
                screen.fill((90, 90, 90))
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
                back_menu_button.draw()
                player.position_x = 300
                player.position_y = 300
                exit_button.draw()

    player.update()
    player.draw(screen)
    pygame.display.flip()









