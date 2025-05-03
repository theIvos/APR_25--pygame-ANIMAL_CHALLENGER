from db_handler import *
import pygame
import time
from random import randint
import json

pygame.init()

class ContinueButton(pygame.sprite.Sprite):
    def __init__(self, x, y, user, points, opponent = "", opponent_scoring = "", opponent_total_points = "", user_scoring = "", user_total_points = "", opponent_animals = "", user_animals = "", final_country = ""):
        super().__init__()

        self.x = x
        self.y = y
        self.user = user
        self.points = points
        self.opponent = opponent
        self.opponent_status = opponent[6]
        
        self.user_ff = json.dumps(user)
        self.opponent_ff = json.dumps(opponent)
        self.opponent_scoring = json.dumps(opponent_scoring)
        self.opponent_total_points = opponent_total_points
        self.user_scoring = json.dumps(user_scoring)
        self.user_total_points = user_total_points
        self.opponent_animals = json.dumps(opponent_animals)
        self.user_animals = json.dumps(user_animals)
        self.final_country = json.dumps(final_country)

        self.og_color = CHALLENGE_BUTTON_COLOR_1
        self.hover_color = MARKED

        self.current_color = self.og_color

        self.continue_label = BASE_FONT.render("CONTINUE", 1, "white")
        self.continue_label_rect = self.continue_label.get_rect(topleft = (self.x - 68, self.y + 20))
        self.rect = pygame.Rect(self.x - 125, self.y, 250, 70)

        continue_button_group.add(self)

    def update(self):

        pygame.draw.rect(SCREEN, self.current_color, self.rect, 0, 10)
        SCREEN.blit(self.continue_label, self.continue_label_rect)

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.current_color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                if self.opponent_status == "challenging":
                    handle_db("answered_2",self.opponent[0]) 
                    handle_db("copy_opponent_for_final",self.opponent[0],self.opponent_ff,self.opponent_scoring,self.opponent_total_points,self.user_ff,self.user_scoring,self.user_total_points,self.final_country,self.opponent_animals,self.user_animals)      
                    handle_db("continue",self.user[0],self.points)
                    handle_db("last_3_update",self.user[0],self.opponent[0])             
                else:
                    handle_db("clean_user",self.user[0])
                    handle_db("continue",self.user[0],self.points)
                    handle_db("last_3_update",self.user[0],self.opponent[0])

                return lobby_screen(self.user[1])
        else:
            self.current_color = self.og_color

class FinalAnimalMiniCard(pygame.sprite.Sprite):
    def __init__(self, x, y, pic):
        super().__init__()

        self.x = x
        self.y = y
        self.pic = pic

        size_coeff = 0.095

        self.image = pygame.transform.scale(pygame.image.load(f"img/animals/{self.pic}.png").convert_alpha(),(672 * size_coeff, 900 * size_coeff))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        final_animal_mini_card_group.add(self)

class FinalCountryCard(pygame.sprite.Sprite):
    def __init__(self, x, y, country):
        super().__init__()

        self.x = x
        self.y = y
        self.country = country

        size_coeff = 1.6

        self.image = pygame.transform.scale(pygame.image.load(f"img/countries/{self.country[0]}.png").convert_alpha(),(225 * size_coeff, 225 * size_coeff))
        self.rect = self.image.get_rect(center = (self.x, self.y))

        final_country_card_group.add(self)

class RejectOrAcceptButton(pygame.sprite.Sprite):
    def __init__(self, x, y, type, user, opponent, country):
        super().__init__()

        self.x = x
        self.y = y
        self.type = type

        self.user = user
        self.opponent = opponent
        self.country = country

        if self.type == "reject" or "cancel":
            self.og_color = "#a50032"
            self.hover_color = "#dc4472"
            if self.type == "cancel":
                self.what = "CANCEL"
            else:
                self.what = "REJECT"

        if self.type == "accept":
            self.og_color = CHALLENGE_BUTTON_COLOR_1
            self.hover_color = CHALLENGE_BUTTON_COLOR_2
            self.what = "ACCEPT"

        if self.type == "ok":
            self.og_color = CHALLENGE_BUTTON_COLOR_1
            self.hover_color = CHALLENGE_BUTTON_COLOR_2
            self.what = "OK"            

        self.current_color = self.og_color

        self.button = pygame.Rect(self.x, self.y, 200, 80)
        
        self.reject_label = BIGGER_FONT.render(self.what, 1, "white")
        if self.type == "cancel":
            self.rect = self.reject_label.get_rect(topleft = (self.x + 30, self.y + 20))
        elif self.type == "reject":
            self.rect = self.reject_label.get_rect(topleft = (self.x + 37, self.y + 20))
        elif self.type == "accept":
            self.rect = self.reject_label.get_rect(topleft = (self.x + 30, self.y + 20))
        elif self.type == "ok":
            self.button = pygame.Rect(self.x, self.y, 100, 60)
            self.rect = self.reject_label.get_rect(topleft = (self.x + 20, self.y + 10))       
        
        reject_or_accept_buttons_group.add(self)

    def update(self):        

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.current_color = self.hover_color

            if pygame.mouse.get_pressed()[0]:

                if self.type == "cancel":                                                     
                    handle_db("cancelled_challenge", self.user, self.opponent)                    
                    return lobby_screen(self.user)
                
                if self.type == "reject":
                    handle_db("rejected_challenge", self.user, self.opponent)                    
                    return lobby_screen(self.user)
                
                if self.type == "accept":                                      
                    return you_challenge_screen(self.user, self.opponent, self.country)
                
                if self.type == "ok":
                    handle_db("rejected_ok", self.user)                    
                    return lobby_screen(self.user)
                
        else:
            self.current_color = self.og_color
        
        pygame.draw.rect(SCREEN, self.current_color, self.button, 0, 10)
        SCREEN.blit(self.reject_label, self.rect)

class GoButton(pygame.sprite.Sprite):
    def __init__(self, x, y, user, opponent):
        super().__init__()

        self.x = x
        self.y = y
        self.user = user
        self.opponent = opponent

        self.og_color = CHALLENGING_COLOR
        self.hover_color = CHALLENGE_BUTTON_COLOR_2
        self.color = self.og_color

        self.button = pygame.Rect(self.x, self.y, 170, 50)

        self.go_label = BIGGER_FONT.render("GO! >>", 1, "white")
        self.rect = self.go_label.get_rect(topleft = (self.x + 42, self.y + 7))

        go_button_group.add(self)

    def update(self):       

        pygame.draw.rect(SCREEN, self.color, self.button, 0, 10)
        SCREEN.blit(self.go_label, self.rect)

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                count_screen(user = self.user, opponent = self.opponent, country=list(country_cards_group)[0], animals = [anima.chosen_animals for anima in list(you_challenged_group)][0])  
                return lobby_screen(user_logged)
        else:
            self.color = self.og_color

class TotalMini(pygame.sprite.Sprite):
    def __init__(self, x, y, object, index):
        super().__init__()

        self.x = x
        self.y = y
        self.object = object
        self.index = index

        self.image_coeff = 0.6

        self.image = pygame.transform.scale(object.og_image,(object.og_image.get_width()*self.image_coeff, object.og_image.get_height()*self.image_coeff))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.user_animal_list = next((animals.chosen_animals for animals in you_challenged_group),None)

        total_minis_group.add(self)
    
    def update(self):

        SCREEN.blit(self.image, self.rect)

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                self.user_animal_list.remove(self.object)
                self.object.image = self.object.og_image
                self.object.clickable = True
                self.kill()
                total_minis_group.remove(self)                

class AddAnimalButton(pygame.sprite.Sprite):
    def __init__(self, x, y, animal, object, chosen_card_object):
        super().__init__()

        self.x = x
        self.y = y
        self.animal = animal
        self.object = object
        self.chosen_card_object = chosen_card_object

        self.og_color = CHALLENGE_BUTTON_COLOR_1
        self.hover_color = CHALLENGE_BUTTON_COLOR_2

        self.color = self.og_color

        add_animal_buttons_group.add(self)

        self.add_label = SMALLER_FONT.render("<< add animal", 1, (255, 255, 255))
        self.add_label_rect = self.add_label.get_rect(topleft = (self.x + 15, self.y +6))
        
        self.rect = pygame.Rect(self.x, self.y, 200, 35)

    def update(self):

        pygame.draw.rect(SCREEN, self.color, self.rect, 0, 3)
        SCREEN.blit(self.add_label, self.add_label_rect)

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.color = self.hover_color
            if pygame.mouse.get_pressed()[0]:                

                self.object.clickable = False
                self.object.image = self.object.used_card
                self.kill()
                add_animal_buttons_group.remove(self)
                self.chosen_card_object.kill()
                chosen_animal_group.remove(self.chosen_card_object)
                height = 80
                width_start = 107
                width_coeff = 60

                index = 0
                index_list = []
                for one_total in total_minis_group: 
                    index_list.append(one_total.rect.left)

                if width_start not in index_list:
                    index = 0
                elif width_start + (width_coeff*1) not in index_list:
                    index = 1
                elif width_start + (width_coeff*2) not in index_list:
                    index = 2
                elif width_start + (width_coeff*3) not in index_list:
                    index = 3
                elif width_start + (width_coeff*4) not in index_list:
                    index = 4

                TotalMini(width_start + (width_coeff*index), height, self.object, index)
                next((user.chosen_animals.append(self.object) for user in you_challenged_group),None)
                
        else:
            self.color = self.og_color

class CountryCard(pygame.sprite.Sprite):
    def __init__(self, x, y, country):
        super().__init__()

        country_atts = country[0]

        self.x = x
        self.y = y
        
        self.pic = country_atts[0]
        self.continent = country_atts[3]        

        size_coeff = 1.7

        self.image = pygame.transform.scale(pygame.image.load(f"img/countries/{self.pic}.png").convert_alpha(),(225 * size_coeff, 225 * size_coeff))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        country_cards_group.add(self)

        list(you_challenged_group)[0].country = country_atts

class ChosenAnimalCard(pygame.sprite.Sprite):
    def __init__(self, x, y, pic, object):
        super().__init__()

        self.x = x
        self.y = y
        self.pic = pic
        self.object = object

        animal_coeff = 1.7
        
        self.image = pygame.transform.scale(pygame.image.load(f"img/animals/{self.pic}.png").convert_alpha(),(168 * animal_coeff, 225 * animal_coeff))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        self.animal_full = handle_db("bring_me_the_animal",self.pic)
        self.animal_full_detail = self.animal_full[0]
        self.country_continent = next((country.continent for country in country_cards_group),"6")
        self.animal_continent = self.animal_full_detail[3]

        if self.country_continent == self.animal_continent and len(list(total_minis_group)) < 5:
            AddAnimalButton(550, 124, self.animal_full_detail, self.object, self)        

        chosen_animal_group.add(self)

    def update(self):

        SCREEN.blit(self.image, self.rect)

class YouChallenged(pygame.sprite.Sprite):
    def __init__(self, user, opponent):
        super().__init__()

        self.user = user
        self.used_indexes = []
        self.chosen_animals = []
        self.opponent = opponent
        self.country = "not here!" 

        you_challenged_group.add(self)

        GoButton(710, 8, user = self.user, opponent = self.opponent)

class AnimalMiniCard(pygame.sprite.Sprite):
    def __init__(self, x, y, pic, index):
        super().__init__()

        self.x = x
        self.y = y
        self.pic = pic
        self.index = index
        self.clickable = True

        pic_coeff = 0.15

        self.og_image = pygame.transform.scale(pygame.image.load(f"img/animals/{self.pic}.png").convert_alpha(),(672*pic_coeff, 900*pic_coeff))
        self.used_card = pygame.transform.scale(pygame.image.load(f"img/animals/card_used.png").convert_alpha(),(672*pic_coeff, 900*pic_coeff))

        self.image = self.og_image
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        animal_mini_card_group.add(self)

    def update(self):
                                
        SCREEN.blit(self.image, self.rect)

        mouse  = pygame.mouse.get_pos()

        for one_you in you_challenged_group:
            
            if self.rect.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0] and self not in one_you.used_indexes and self.clickable:
                    one_you.used_indexes = []  
                    one_you.used_indexes.append(self.index)              
                    
                    for card in chosen_animal_group:
                        card.kill()
                        chosen_animal_group.remove(card)
                    for button in add_animal_buttons_group:
                        button.kill()
                        add_animal_buttons_group.remove(button)
                    ChosenAnimalCard(530, 110, self.pic, self)

class GetCard(pygame.sprite.Sprite):
    def __init__(self, x, y, pic):
        super().__init__()

        self.x = x
        self.y = y

        animal_coeff = 0.5
        
        self.image = pygame.transform.scale(pygame.image.load(f"img/animals/{pic}.png").convert_alpha(),(672*animal_coeff, 900*animal_coeff))
        self.rect = self.image.get_rect(center = (self.x, self.y))

        get_cards_group.add(self)

class ScrollArrow(pygame.sprite.Sprite):
    def __init__(self, x, y, type, where = ""):
        super().__init__()

        self.x  = x
        self.y = y
        self.type = type
        self.speed = 8
        self.where = where

        self.arrow_left_free = pygame.transform.rotate(pygame.image.load("img/arrow_free.png").convert_alpha(), 90)
        self.arrow_left_hover = pygame.transform.rotate(pygame.image.load("img/arrow_hover.png").convert_alpha(), 90)
        self.arrow_left_clicked = pygame.transform.rotate(pygame.image.load("img/arrow_clicked.png").convert_alpha(), 90)

        self.arrow_right_free = pygame.transform.rotate(pygame.image.load("img/arrow_free.png").convert_alpha(), 270)
        self.arrow_right_hover = pygame.transform.rotate(pygame.image.load("img/arrow_hover.png").convert_alpha(), 270)
        self.arrow_right_clicked = pygame.transform.rotate(pygame.image.load("img/arrow_clicked.png").convert_alpha(), 270)

        if self.type == "to_left":
            self.image = pygame.transform.rotate(pygame.image.load("img/arrow_free.png").convert_alpha(), 90)
        if self.type == "to_right":
            self.image = pygame.transform.rotate(pygame.image.load("img/arrow_free.png").convert_alpha(), 270)
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        scroll_arrows_group.add(self)

    def update(self):

        mouse = pygame.mouse.get_pos()
        if self.type == "to_left":
            if self.rect.collidepoint(mouse):
                self.image = self.arrow_left_hover
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.arrow_left_clicked
                    for one_card in animal_card_group:
                        one_card.rect.x -= self.speed
            else:
                self.image = self.arrow_left_free

        if self.type == "to_right":
            if self.rect.collidepoint(mouse):
                self.image = self.arrow_right_hover
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.arrow_right_clicked
                    for one_card in animal_card_group:
                        one_card.rect.x += self.speed
                else:
                    self.image = self.arrow_right_free

        # MINI
        if self.type == "to_left" and self.where == "mini":
            if self.rect.collidepoint(mouse):
                self.image = self.arrow_left_hover
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.arrow_left_clicked
                    for one_card in animal_mini_card_group:
                        one_card.rect.x -= self.speed
            else:
                self.image = self.arrow_left_free

        if self.type == "to_right" and self.where == "mini":
            if self.rect.collidepoint(mouse):
                self.image = self.arrow_right_hover
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.arrow_right_clicked
                    for one_card in animal_mini_card_group:
                        one_card.rect.x += self.speed
                else:
                    self.image = self.arrow_right_free        

class AnimalCard(pygame.sprite.Sprite):
    def __init__(self, x, y, animal):
        super().__init__()

        self.x = x
        self.y = y

        self.animal = animal

        self.image = pygame.transform.scale(pygame.image.load(f"img/animals/{self.animal}.png").convert_alpha(),(168 * 1.5, 225 * 1.5))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        animal_card_group.add(self)   

class ChallengeButton(pygame.sprite.Sprite):
    def __init__(self, x, y, user, search = False):
        super().__init__()
       
        self.x = x
        self.y = y

        self.search = search

        self.moving_up = False
        self.moving_down = False

        self.user = user.split(" ")
        del self.user[-1]
        self.user = " ".join(self.user)

        self.type = "challenge"

        self.fading_down = False
        self.fading_up = False
        
        self.og_color = CHALLENGE_BUTTON_COLOR_1
        self.hover_color = CHALLENGE_BUTTON_COLOR_2

        self.current_color = self.og_color

        button_group.add(self)

        self.distance_coeff = 280

        self.clickable = True

        self.challenge_label = CHALLENGE_FONT.render("CHALLENGE!", 1, "white")
        self.challenge_label_rect = self.challenge_label.get_rect(topleft = (self.x + self.distance_coeff + 10, self.y + 9))
        
        self.rect = pygame.Rect(self.x + self.distance_coeff, self.y, 90, 30) 

    def update(self):
        
        button = pygame.draw.rect(SCREEN, self.current_color, (self.x + self.distance_coeff, self.y, 90, 30), 0, 3)
                
        self.current_color = self.og_color

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse) and self.clickable:   
            self.current_color = self.hover_color
        else:
            self.current_color = self.og_color

        self.challenge_label_rect = self.challenge_label.get_rect(topleft = (self.x + self.distance_coeff + 10, self.y + 9))
        SCREEN.blit(self.challenge_label, self.challenge_label_rect)    

class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, type, label, user, search = False):
        super().__init__()

        self.type = type
        self.label = label
        self.user = user

        if label != "--no opponent here so far--" and label != "--no opponents yet--":
            pre_challenge = label.split(" (")
            pre_challenge = pre_challenge[0]
            
            self.challenge = handle_db("get_full_user",pre_challenge)[6]
        else:
            self.challenge = "free"

        self.search = search

        self.moving_down = False
        self.moving_up = False

        if self.type == "search":
            self.user_who = self.label
        else:
            self.user_who = self.label.split(" ")     
            self.user_who.pop(-1)   
            self.user_who = " ".join(self.user_who)

        self.alpha = 255

        self.card = BASE_FONT.render(f"{label}", 1, FONT_COLOR)
        if self.label == "--no opponents yet--":
            self.card_rect = self.card.get_rect(topleft = (x+35, y))
        else:
            self.card_rect = self.card.get_rect(topleft = (x, y))

        if self.label != "--no opponents yet--" and self.user_who != self.user and self.label != "--no opponent here so far--" and self.label != " " and not search and self.challenge == "free":
            ChallengeButton(x, y, self.label)
        elif self.label != "--no opponents yet--" and " ".join(self.user_who.split(" ")[:-1]) != self.user and self.label != "--no opponent here so far--" and self.label != " " and search and self.challenge == "free":
            ChallengeButton(x, y, self.label, True)


        cards_group.add(self)

    def update(self):

        SCREEN.blit(self.card, self.card_rect)    

class Logo(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()

        self.x = x
        self.y = y
        self.screen = screen
        if self.screen in ("register_new_user_screen", "log_screen"): 
            self.logo = LOGO_FONT.render("ANIMAL CHALLENGER", 1, "black")
        else:
            self.logo = LOGO_FONT_SMALLER.render("ANIMAL CHALLENGER", 1, "black")
        self.logo_rect = self.logo.get_rect(center  = (x, y))

        logos_group.add(self)

    def update(self):

        SCREEN.blit(self.logo, self.logo_rect)        

class Frames(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, type = ""):
        super().__init__()

        self.screen = screen
        self.x = x
        self.y = y

        self.type = type

        self.moving_down = False
        self.moving_up = False
        self.cards_coeff = 9

        self.alpha = 255

        if self.screen == "log_screen":
            self.menu_rectangle = pygame.Surface(pygame.Rect(100, 200, 600, 200).size, pygame.SRCALPHA)

        if self.screen == "register_new_user_screen":
            self.menu_rectangle = pygame.Surface(pygame.Rect(100, 200, 600, 275).size, pygame.SRCALPHA)

        if self.screen == "lobby_screen":
            self.menu_rectangle = pygame.Surface(pygame.Rect(-200 + 6, 40, 879, 40).size, pygame.SRCALPHA)

        if self.screen == "rivals":
            self.menu_rectangle = pygame.Surface(pygame.Rect(0, 0, 430, 520).size, pygame.SRCALPHA)

        if self.screen == "top_10":
            self.menu_rectangle = pygame.Surface(pygame.Rect(300, 0, 430, 520).size, pygame.SRCALPHA)

        if self.screen == "player_card":
            self.menu_rectangle = pygame.Surface(pygame.Rect(0, 0, 400, 50).size, pygame.SRCALPHA)

        if self.screen == "final_animal":
            self.menu_rectangle = pygame.Surface(pygame.Rect(0, 0, 250, 120).size, pygame.SRCALPHA)

        pygame.draw.rect(self.menu_rectangle, (255, 255, 255), self.menu_rectangle.get_rect(), 0, 10)
        self.menu_rectangle.set_alpha(140)

        self.rect = (self.x, self.y)

        frames_group.add(self)

    def update(self):

        SCREEN.blit(self.menu_rectangle, self.rect)        

class Screens(pygame.sprite.Sprite):
    def __init__(self, type, username = "nobody", user_points = "0", animal = "", user = "", user_scoring ="", user_total_points = "", opponent = "", opponent_scoring = "", opponent_total_points = "", country = "", user_point_dif = ""):
        super().__init__()

        self.type = type
        self.username = username
        self.points = user_points
        self.animal = animal

        self.user = user
        self.user_scoring = user_scoring
        self.user_total_points = user_total_points

        self.opponent = opponent
        self.opponent_scoring = opponent_scoring
        self.opponent_total_points = opponent_total_points

        self.user_point_dif = user_point_dif

        if self.type == "log_screen":
            log_screen_group.add(self)
        elif self.type == "lobby_screen":
            lobby_screen_group.add(self)
        elif self.type == "explore_screen":
            explore_screen_group.add(self)
        elif self.type == "register_new_user_screen":
            register_new_user_screen_group.add(self)
        elif self.type == "waiting_screen":
            waiting_screen_group.add(self)
        elif self.type == "get_card_screen":
            animal_type = str(handle_db("get_animal_name",self.animal)).upper()
            if animal_type.startswith(("A","E","I","O","U","Y")):
                self.predlozka = "an"
            else:
                self.predlozka = "a"

            self.get_animal_label = BIGGER_FONT.render(f"You got {self.predlozka} {animal_type}!", 1, GOT_COLOR)
            self.get_animal_rect = self.get_animal_label.get_rect(center = (WIDTH//2, HEIGHT//2+250))
            get_card_screen_group.add(self)
        elif self.type == "challenging_waiting_screen":
            challenging_waiting_screen_group.add(self)
        elif self.type == "challenged_waiting_screen":
            challenged_waiting_screen_group.add(self)
        elif self.type == "rejected_waiting_screen":
            rejected_waiting_screen_group.add(self)
        elif self.type == "final_screen":
            final_screen_group.add(self)
        
        elif self.type == "you_challenge_screen":
            you_challenge_screen_group.add(self)

        

    def update(self):
        
        if self.type == "log_screen":
            
            login_label = BASE_FONT.render("Start with your login, please:", 1, FONT_COLOR)
            login_label_rect = login_label.get_rect(center = (WIDTH//2, 175))
            SCREEN.blit(login_label, login_label_rect)

            username_label = BASE_FONT.render("username:", 1, FONT_COLOR)
            username_label_rect = username_label.get_rect(topright = (240, 207))
            SCREEN.blit(username_label, username_label_rect)

            password_label = BASE_FONT.render("password:", 1, FONT_COLOR)
            password_label_rect = password_label.get_rect(topright = (240, 252))
            SCREEN.blit(password_label, password_label_rect)

            or_label = BASE_FONT.render("or", 1, FONT_COLOR)
            or_rect = or_label.get_rect(center = (WIDTH//2, 460))
            SCREEN.blit(or_label, or_rect)

            login_text = BASE_FONT.render(login_typing, 1, (255, 255, 255))
            login_text_rect = login_text.get_rect(topleft = (258, 207))
            SCREEN.blit(login_text, login_text_rect)

            password_text = BASE_FONT.render(password_typing, 1, (255, 255, 255))
            password_text_rect = password_text.get_rect(topleft = (258, 252))
            SCREEN.blit(password_text, password_text_rect)

            warning_text = BASE_FONT.render(warning_message, 1, WARNING_COLOR)
            warning_text_rect = warning_text.get_rect(center = (WIDTH//2, 310))
            SCREEN.blit(warning_text, warning_text_rect)            

        elif self.type == "lobby_screen":
            welcome_label = BASE_FONT.render(f"Welcome, {self.username}!", 1, FONT_COLOR)
            welcome_rect = welcome_label.get_rect(topleft = (30, 86))
            SCREEN.blit(welcome_label, welcome_rect)

            points = BASE_FONT.render(f"You have currently {self.points} points!", 1, FONT_COLOR)
            points_rect = points.get_rect(topright = (870, 86))
            SCREEN.blit(points, points_rect)

            rivals_label = BASE_FONT.render(f"YOUR LAST 3 OPPONENTS:", 1, FONT_COLOR)
            rivals_label_rect = rivals_label.get_rect(center = (200, 170))
            SCREEN.blit(rivals_label, rivals_label_rect)

            search_label = BASE_FONT.render(f"SEARCH USER:", 1, FONT_COLOR)
            search_label_rect = search_label.get_rect(center = (125, 410))
            SCREEN.blit(search_label, search_label_rect)

            search_text = BASE_FONT.render(search_typing, 1, (255, 255, 255))
            search_text_rect = search_text.get_rect(topleft = (58, 437))
            SCREEN.blit(search_text, search_text_rect)

            top_10 = BASE_FONT.render(f"TOP 8:", 1, FONT_COLOR)
            top_10_rect = top_10.get_rect(center = (530, 170))
            SCREEN.blit(top_10, top_10_rect)

            warning_text = BASE_FONT.render(warning_message, 1, WARNING_COLOR)
            warning_text_rect = warning_text.get_rect(topleft = (108, 560))
            SCREEN.blit(warning_text, warning_text_rect)

        elif self.type == "explore_screen":
            welcome_label = BASE_FONT.render(f"Welcome, {self.username}!", 1, FONT_COLOR)
            welcome_rect = welcome_label.get_rect(topleft = (30, 86))
            SCREEN.blit(welcome_label, welcome_rect)

            points = BASE_FONT.render(f"You have currently {self.points} points!", 1, FONT_COLOR)
            points_rect = points.get_rect(topright = (870, 86))
            SCREEN.blit(points, points_rect)

        elif self.type == "challenging_waiting_screen":

            welcome_user_label = MORE_BIGGER_FONT.render(f"{user_logged}!", 1, CHALLENGING_COLOR)
            welcome_user_label_rect = welcome_user_label.get_rect(center = (WIDTH//2, HEIGHT//2 - 160))
            SCREEN.blit(welcome_user_label, welcome_user_label_rect)

            challenged_label = BIGGER_FONT.render(f"You are currently challenging {self.username}!", 1, CHALLENGING_COLOR)
            challenged_label_rect = challenged_label.get_rect(center = (WIDTH//2, HEIGHT//2 - 20))
            SCREEN.blit(challenged_label, challenged_label_rect)

            waiting_for_response_label = BIGGER_FONT.render(f"Waiting now for {self.username}'s response.", 1, CHALLENGING_COLOR)
            waiting_for_response_label_rect = waiting_for_response_label.get_rect(center = (WIDTH//2, HEIGHT//2 + 20))
            SCREEN.blit(waiting_for_response_label, waiting_for_response_label_rect)

            penalty_label = BASE_FONT.render(f"with penalty 2 points.", 1, NEGATIVE_COLOR)
            penalty_label_rect = penalty_label.get_rect(center = (WIDTH//2, HEIGHT//2 + 170))
            SCREEN.blit(penalty_label, penalty_label_rect)

            current_points_label = BASE_FONT.render(f"You have currently {self.points} points.", 1, CHALLENGING_COLOR)
            current_points_label_rect = current_points_label.get_rect(center = (WIDTH//2, HEIGHT//2 + 220))
            SCREEN.blit(current_points_label, current_points_label_rect)

        elif self.type == "challenged_waiting_screen":

            welcome_challenged_user_label = MORE_BIGGER_FONT.render(f"{user_logged}!", 1, CHALLENGING_COLOR)
            welcome_challenged_user_label_rect = welcome_challenged_user_label.get_rect(center = (WIDTH//2, HEIGHT//2 - 160))
            SCREEN.blit(welcome_challenged_user_label, welcome_challenged_user_label_rect)

            challenged_label = BIGGER_FONT.render(f"You are currently challenged by {self.username}!", 1, CHALLENGING_COLOR)
            challenged_label_rect = challenged_label.get_rect(center = (WIDTH//2, HEIGHT//2 - 20))
            SCREEN.blit(challenged_label, challenged_label_rect)

            waiting_for_response_label = BIGGER_FONT.render(f"You can ACCEPT or REJECT the challenge:", 1, CHALLENGING_COLOR)
            waiting_for_response_label_rect = waiting_for_response_label.get_rect(center = (WIDTH//2, HEIGHT//2 + 20))
            SCREEN.blit(waiting_for_response_label, waiting_for_response_label_rect)

        elif self.type == "rejected_waiting_screen":

            rejected_label = BIGGER_FONT.render(f"{self.username} rejected your challenge!", 1, CHALLENGING_COLOR)
            rejected_label_rect = rejected_label.get_rect(center = (WIDTH//2, HEIGHT//2))
            SCREEN.blit(rejected_label, rejected_label_rect)

  
        elif self.type == "you_challenge_screen":
            choose_label = BASE_FONT.render(f"choose your animals:", 1, CHOOSE_COLOR)
            choose_rect = choose_label.get_rect(center = (WIDTH//2, 520))
            SCREEN.blit(choose_label, choose_rect)

            if self.points == "free":
                inchallenge_text = "You are challenging"
            else:
                inchallenge_text = "You are challenged by"        

            challenging = SMALLER_FONT.render(f"{inchallenge_text} {[chall.opponent[1] for chall in list(you_challenged_group)][0]}!", 1, CHALLENGING_COLOR)
            challenging_rect = challenging.get_rect(topleft = (440, 74))
            SCREEN.blit(challenging, challenging_rect)

        elif self.type == "waiting_screen":
            loading_label = BASE_FONT.render(f"LOADING...", 1, FONT_COLOR)
            loading_rect = loading_label.get_rect(center = (WIDTH//2, HEIGHT//2 - 50))
            SCREEN.blit(loading_label, loading_rect)

            wait_label = BASE_FONT.render(f"please wait", 1, FONT_COLOR)
            wait_rect = wait_label.get_rect(center = (WIDTH//2, HEIGHT//2))
            SCREEN.blit(wait_label, wait_rect)            

            self.kill()
            waiting_screen_group.remove(self)

        elif self.type == "get_card_screen":

            SCREEN.blit(self.get_animal_label, self.get_animal_rect)            

        elif self.type == "register_new_user_screen":
            reg_warning_text = BASE_FONT.render(warning_message, 1, WARNING_COLOR)
            reg_warning_text_rect = reg_warning_text.get_rect(center = (WIDTH//2, 410))
            SCREEN.blit(reg_warning_text, reg_warning_text_rect)

            new_user_label = BASE_FONT.render("Choose your username:", 1, FONT_COLOR)
            new_user_label_rect = new_user_label.get_rect(topleft = (180, 197))
            SCREEN.blit(new_user_label, new_user_label_rect)

            new_password_label = BASE_FONT.render("Choose your password:", 1, FONT_COLOR)
            new_password_label_rect = new_password_label.get_rect(topleft = (180, 297))
            SCREEN.blit(new_password_label, new_password_label_rect)

            new_user_text = BASE_FONT.render(new_user_typing, 1, (255, 255, 255))
            new_user_text_rect = new_user_text.get_rect(topleft = (258, 237))
            SCREEN.blit(new_user_text, new_user_text_rect)

            new_password_text = BASE_FONT.render(new_password_typing, 1, (255, 255, 255))
            new_password_text_rect = new_password_text.get_rect(topleft = (258, 337))
            SCREEN.blit(new_password_text, new_password_text_rect)

        elif self.type == "final_screen":

            BASE_HEIGHT_COEFF = 95
            
            result_label = BASE_FONT.render(f"final result", 1, CHOOSE_COLOR)
            result_label_rect = result_label.get_rect(center = (WIDTH//2, 100))
            SCREEN.blit(result_label, result_label_rect)

            user_points = MORE_BIGGER_FONT.render(f"{self.user_total_points}", 1, CHALLENGING_COLOR)
            user_points_rect = user_points.get_rect(topleft = (290, 70))
            SCREEN.blit(user_points, user_points_rect)

            opponent_points = MORE_BIGGER_FONT.render(f"{self.opponent_total_points}", 1, CHALLENGING_COLOR)
            opponent_points_rect = opponent_points.get_rect(topright = (WIDTH - 290, 70))
            SCREEN.blit(opponent_points, opponent_points_rect)

            vs_label_user = BASE_FONT.render(f"{self.user[1]}", 1, CHALLENGING_COLOR)
            vs_label_user_rect = vs_label_user.get_rect(center = (130, 45))
            SCREEN.blit(vs_label_user, vs_label_user_rect)

            vs_label_opponent = BASE_FONT.render(f"{self.opponent[1]}", 1, CHALLENGING_COLOR)
            vs_label_opponent_rect = vs_label_opponent.get_rect(center = (WIDTH - 130, 45))
            SCREEN.blit(vs_label_opponent, vs_label_opponent_rect)

            if self.user_point_dif >= 0:
                got_or_lose = "You got"
                got_or_lose_color = CHALLENGE_BUTTON_COLOR_1
                pointsy = "+" + str(self.user_point_dif)
            else:
                got_or_lose = "You lost"
                got_or_lose_color = WARNING_COLOR
                pointsy = str(self.user_point_dif)


            points_dif = SLIGHTLY_BIGGER_FONT.render(f"{got_or_lose}", 1, FONT_COLOR)
            points_dif_rect = points_dif.get_rect(center = (WIDTH//2, 505))
            SCREEN.blit(points_dif, points_dif_rect)

            points_dif_nr = SLIGHTLY_BIGGER_FONT.render(f"{pointsy}", 1, got_or_lose_color)
            points_dif_nr_rect = points_dif_nr.get_rect(center = (WIDTH//2, 555))
            SCREEN.blit(points_dif_nr, points_dif_nr_rect)

            points_dif_nr_pt = BASE_FONT.render(f"points", 1, FONT_COLOR)
            points_dif_nr_pt_rect = points_dif_nr_pt.get_rect(center = (WIDTH//2, 590))
            SCREEN.blit(points_dif_nr_pt, points_dif_nr_pt_rect)

            user_animal_1_name = SMALLER_FONT.render(f"{self.user_scoring[0][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            user_animal_1_name_rect = user_animal_1_name.get_rect(topleft = (25, 75 + (125 * 0)))
            SCREEN.blit(user_animal_1_name, user_animal_1_name_rect)

            doubledot = ":"
            if type(self.user_scoring[0][1][1]) == int:
                if self.user_scoring[0][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_country = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][1][0]}{doubledot} {self.user_scoring[0][1][1]}", 1, item_color)
            user_animal_1_country_rect = user_animal_1_country.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 0)))
            SCREEN.blit(user_animal_1_country, user_animal_1_country_rect)

            doubledot = ":"
            if type(self.user_scoring[0][2][1]) == int:
                if self.user_scoring[0][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ":"

            user_animal_1_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][2][0]}{doubledot} {self.user_scoring[0][2][1]}", 1, item_color)
            user_animal_1_daytime_rect = user_animal_1_daytime.get_rect(topleft = (90 + 88, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 0)))
            SCREEN.blit(user_animal_1_daytime, user_animal_1_daytime_rect)

            doubledot = ":"
            if type(self.user_scoring[0][3][1]) == int:
                if self.user_scoring[0][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][3][0]}{doubledot} {self.user_scoring[0][3][1]}", 1, item_color)
            user_animal_1_item1_rect = user_animal_1_item1.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 1)))
            SCREEN.blit(user_animal_1_item1, user_animal_1_item1_rect)

            doubledot = ":"
            if type(self.user_scoring[0][4][1]) == int:
                if self.user_scoring[0][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][4][0]}{doubledot} {self.user_scoring[0][4][1]}", 1, item_color)
            user_animal_1_item2_rect = user_animal_1_item2.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 2)))
            SCREEN.blit(user_animal_1_item2, user_animal_1_item2_rect)

            doubledot = ":"
            if type(self.user_scoring[0][5][1]) == int:
                if self.user_scoring[0][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][5][0]}{doubledot} {self.user_scoring[0][5][1]}", 1, item_color)
            user_animal_1_item3_rect = user_animal_1_item3.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 3)))
            SCREEN.blit(user_animal_1_item3, user_animal_1_item3_rect)

            doubledot = ":"
            if type(self.user_scoring[0][6][1]) == int:
                if self.user_scoring[0][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][6][0]}{doubledot} {self.user_scoring[0][6][1]}", 1, item_color)
            user_animal_1_item4_rect = user_animal_1_item4.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 4)))
            SCREEN.blit(user_animal_1_item4, user_animal_1_item4_rect)

            doubledot = ":"
            if type(self.user_scoring[0][7][1]) == int:
                if self.user_scoring[0][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_1_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[0][7][0]}{doubledot} {self.user_scoring[0][7][1]}", 1, item_color)
            user_animal_1_item5_rect = user_animal_1_item5.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 5)))
            SCREEN.blit(user_animal_1_item5, user_animal_1_item5_rect)

            user_animal_2_name = SMALLER_FONT.render(f"{self.user_scoring[1][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            user_animal_2_name_rect = user_animal_2_name.get_rect(topleft = (25, 75 + (125 * 1)))
            SCREEN.blit(user_animal_2_name, user_animal_2_name_rect)

            doubledot = ":"
            if type(self.user_scoring[1][1][1]) == int:
                if self.user_scoring[1][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_country = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][1][0]}{doubledot} {self.user_scoring[1][1][1]}", 1, item_color)
            user_animal_2_country_rect = user_animal_2_country.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 0)))
            SCREEN.blit(user_animal_2_country, user_animal_2_country_rect)

            doubledot = ":"
            if type(self.user_scoring[1][2][1]) == int:
                if self.user_scoring[1][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][2][0]}{doubledot} {self.user_scoring[1][2][1]}", 1, item_color)
            user_animal_2_daytime_rect = user_animal_2_daytime.get_rect(topleft = (90 + 88, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 0)))
            SCREEN.blit(user_animal_2_daytime, user_animal_2_daytime_rect)

            doubledot = ":"
            if type(self.user_scoring[1][3][1]) == int:
                if self.user_scoring[1][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][3][0]}{doubledot} {self.user_scoring[1][3][1]}", 1, item_color)
            user_animal_2_item1_rect = user_animal_2_item1.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 1)))
            SCREEN.blit(user_animal_2_item1, user_animal_2_item1_rect)

            doubledot = ":"
            if type(self.user_scoring[1][4][1]) == int:
                if self.user_scoring[1][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][4][0]}{doubledot} {self.user_scoring[1][4][1]}", 1, item_color)
            user_animal_2_item2_rect = user_animal_2_item2.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 2)))
            SCREEN.blit(user_animal_2_item2, user_animal_2_item2_rect)

            doubledot = ":"
            if type(self.user_scoring[1][5][1]) == int:
                if self.user_scoring[1][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][5][0]}{doubledot} {self.user_scoring[1][5][1]}", 1, item_color)
            user_animal_2_item3_rect = user_animal_2_item3.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 3)))
            SCREEN.blit(user_animal_2_item3, user_animal_2_item3_rect)

            doubledot = ":"
            if type(self.user_scoring[1][6][1]) == int:
                if self.user_scoring[1][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][6][0]}{doubledot} {self.user_scoring[1][6][1]}", 1, item_color)
            user_animal_2_item4_rect = user_animal_2_item4.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 4)))
            SCREEN.blit(user_animal_2_item4, user_animal_2_item4_rect)

            doubledot = ":"
            if type(self.user_scoring[1][7][1]) == int:
                if self.user_scoring[1][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_2_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[1][7][0]}{doubledot} {self.user_scoring[1][7][1]}", 1, item_color)
            user_animal_2_item5_rect = user_animal_2_item5.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 5)))
            SCREEN.blit(user_animal_2_item5, user_animal_2_item5_rect)

            user_animal_3_name = SMALLER_FONT.render(f"{self.user_scoring[2][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            user_animal_3_name_rect = user_animal_3_name.get_rect(topleft = (25, 75 + (125 * 2)))
            SCREEN.blit(user_animal_3_name, user_animal_3_name_rect)

            doubledot = ":"
            if type(self.user_scoring[2][1][1]) == int:
                if self.user_scoring[2][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_country = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][1][0]}{doubledot} {self.user_scoring[2][1][1]}", 1, item_color)
            user_animal_3_country_rect = user_animal_3_country.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 0)))
            SCREEN.blit(user_animal_3_country, user_animal_3_country_rect)

            doubledot = ":"
            if type(self.user_scoring[2][2][1]) == int:
                if self.user_scoring[2][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][2][0]}{doubledot} {self.user_scoring[2][2][1]}", 1, item_color)
            user_animal_3_daytime_rect = user_animal_3_daytime.get_rect(topleft = (90 + 88, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 0)))
            SCREEN.blit(user_animal_3_daytime, user_animal_3_daytime_rect)

            doubledot = ":"
            if type(self.user_scoring[2][3][1]) == int:
                if self.user_scoring[2][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][3][0]}{doubledot} {self.user_scoring[2][3][1]}", 1, item_color)
            user_animal_3_item1_rect = user_animal_3_item1.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 1)))
            SCREEN.blit(user_animal_3_item1, user_animal_3_item1_rect)

            doubledot = ":"
            if type(self.user_scoring[2][4][1]) == int:
                if self.user_scoring[2][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][4][0]}{doubledot} {self.user_scoring[2][4][1]}", 1, item_color)
            user_animal_3_item2_rect = user_animal_3_item2.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 2)))
            SCREEN.blit(user_animal_3_item2, user_animal_3_item2_rect)

            doubledot = ":"
            if type(self.user_scoring[2][5][1]) == int:
                if self.user_scoring[2][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][5][0]}{doubledot} {self.user_scoring[2][5][1]}", 1, item_color)
            user_animal_3_item3_rect = user_animal_3_item3.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 3)))
            SCREEN.blit(user_animal_3_item3, user_animal_3_item3_rect)

            doubledot = ":"
            if type(self.user_scoring[2][6][1]) == int:
                if self.user_scoring[2][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][6][0]}{doubledot} {self.user_scoring[2][6][1]}", 1, item_color)
            user_animal_3_item4_rect = user_animal_3_item4.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 4)))
            SCREEN.blit(user_animal_3_item4, user_animal_3_item4_rect)

            doubledot = ":"
            if type(self.user_scoring[2][7][1]) == int:
                if self.user_scoring[2][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_3_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[2][7][0]}{doubledot} {self.user_scoring[2][7][1]}", 1, item_color)
            user_animal_3_item5_rect = user_animal_3_item5.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 5)))
            SCREEN.blit(user_animal_3_item5, user_animal_3_item5_rect)

            user_animal_4_name = SMALLER_FONT.render(f"{self.user_scoring[3][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            user_animal_4_name_rect = user_animal_4_name.get_rect(topleft = (25, 75 + (125 * 3)))
            SCREEN.blit(user_animal_4_name, user_animal_4_name_rect)

            doubledot = ":"
            if type(self.user_scoring[3][1][1]) == int:
                if self.user_scoring[3][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_country = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][1][0]}{doubledot} {self.user_scoring[3][1][1]}", 1, item_color)
            user_animal_4_country_rect = user_animal_4_country.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 0)))
            SCREEN.blit(user_animal_4_country, user_animal_4_country_rect)

            doubledot = ":"
            if type(self.user_scoring[3][2][1]) == int:
                if self.user_scoring[3][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][2][0]}{doubledot} {self.user_scoring[3][2][1]}", 1, item_color)
            user_animal_4_daytime_rect = user_animal_4_daytime.get_rect(topleft = (90 + 88, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 0)))
            SCREEN.blit(user_animal_4_daytime, user_animal_4_daytime_rect)

            doubledot = ":"
            if type(self.user_scoring[3][3][1]) == int:
                if self.user_scoring[3][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][3][0]}{doubledot} {self.user_scoring[3][3][1]}", 1, item_color)
            user_animal_4_item1_rect = user_animal_4_item1.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 1)))
            SCREEN.blit(user_animal_4_item1, user_animal_4_item1_rect)

            doubledot = ":"
            if type(self.user_scoring[3][4][1]) == int:
                if self.user_scoring[3][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][4][0]}{doubledot} {self.user_scoring[3][4][1]}", 1, item_color)
            user_animal_4_item2_rect = user_animal_4_item2.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 2)))
            SCREEN.blit(user_animal_4_item2, user_animal_4_item2_rect)

            doubledot = ":"
            if type(self.user_scoring[3][5][1]) == int:
                if self.user_scoring[3][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][5][0]}{doubledot} {self.user_scoring[3][5][1]}", 1, item_color)
            user_animal_4_item3_rect = user_animal_4_item3.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 3)))
            SCREEN.blit(user_animal_4_item3, user_animal_4_item3_rect)

            doubledot = ":"
            if type(self.user_scoring[3][6][1]) == int:
                if self.user_scoring[3][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][6][0]}{doubledot} {self.user_scoring[3][6][1]}", 1, item_color)
            user_animal_4_item4_rect = user_animal_4_item4.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 4)))
            SCREEN.blit(user_animal_4_item4, user_animal_4_item4_rect)

            doubledot = ":"
            if type(self.user_scoring[3][7][1]) == int:
                if self.user_scoring[3][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_4_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[3][7][0]}{doubledot} {self.user_scoring[3][7][1]}", 1, item_color)
            user_animal_4_item5_rect = user_animal_4_item5.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 5)))
            SCREEN.blit(user_animal_4_item5, user_animal_4_item5_rect)

            user_animal_5_name = SMALLER_FONT.render(f"{self.user_scoring[4][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            user_animal_5_name_rect = user_animal_5_name.get_rect(topleft = (25, 75 + (125 * 4)))
            SCREEN.blit(user_animal_5_name, user_animal_5_name_rect)

            doubledot = ":"
            if type(self.user_scoring[4][1][1]) == int:
                if self.user_scoring[4][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_country = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][1][0]}{doubledot} {self.user_scoring[4][1][1]}", 1, item_color)
            user_animal_5_country_rect = user_animal_5_country.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 0)))
            SCREEN.blit(user_animal_5_country, user_animal_5_country_rect)

            doubledot = ":"
            if type(self.user_scoring[4][2][1]) == int:
                if self.user_scoring[4][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][2][0]}{doubledot} {self.user_scoring[4][2][1]}", 1, item_color)
            user_animal_5_daytime_rect = user_animal_5_daytime.get_rect(topleft = (90 + 88, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 0)))
            SCREEN.blit(user_animal_5_daytime, user_animal_5_daytime_rect)

            doubledot = ":"
            if type(self.user_scoring[4][3][1]) == int:
                if self.user_scoring[4][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][3][0]}{doubledot} {self.user_scoring[4][3][1]}", 1, item_color)
            user_animal_5_item1_rect = user_animal_5_item1.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 1)))
            SCREEN.blit(user_animal_5_item1, user_animal_5_item1_rect)

            doubledot = ":"
            if type(self.user_scoring[4][4][1]) == int:
                if self.user_scoring[4][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][4][0]}{doubledot} {self.user_scoring[4][4][1]}", 1, item_color)
            user_animal_5_item2_rect = user_animal_5_item2.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 2)))
            SCREEN.blit(user_animal_5_item2, user_animal_5_item2_rect)

            doubledot = ":"
            if type(self.user_scoring[4][5][1]) == int:
                if self.user_scoring[4][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][5][0]}{doubledot} {self.user_scoring[4][5][1]}", 1, item_color)
            user_animal_5_item3_rect = user_animal_5_item3.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 3)))
            SCREEN.blit(user_animal_5_item3, user_animal_5_item3_rect)

            doubledot = ":"
            if type(self.user_scoring[4][6][1]) == int:
                if self.user_scoring[4][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][6][0]}{doubledot} {self.user_scoring[4][6][1]}", 1, item_color)
            user_animal_5_item4_rect = user_animal_5_item4.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 4)))
            SCREEN.blit(user_animal_5_item4, user_animal_5_item4_rect)

            doubledot = ":"
            if type(self.user_scoring[4][7][1]) == int:
                if self.user_scoring[4][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            user_animal_5_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.user_scoring[4][7][0]}{doubledot} {self.user_scoring[4][7][1]}", 1, item_color)
            user_animal_5_item5_rect = user_animal_5_item5.get_rect(topleft = (90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 5)))
            SCREEN.blit(user_animal_5_item5, user_animal_5_item5_rect)

            opponent_animal_1_name = SMALLER_FONT.render(f"{self.opponent_scoring[0][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            opponent_animal_1_name_rect = opponent_animal_1_name.get_rect(topright = (WIDTH - 25, 75 + (125 * 0)))
            SCREEN.blit(opponent_animal_1_name, opponent_animal_1_name_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][1][1]) == int:
                if self.opponent_scoring[0][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_country = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][1][0]}{doubledot} {self.opponent_scoring[0][1][1]}", 1, item_color)
            opponent_animal_1_country_rect = opponent_animal_1_country.get_rect(topright = (WIDTH - 90 - 88, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 0)))
            SCREEN.blit(opponent_animal_1_country, opponent_animal_1_country_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][2][1]) == int:
                if self.opponent_scoring[0][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ":"

            opponent_animal_1_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][2][0]}{doubledot} {self.opponent_scoring[0][2][1]}", 1, item_color)
            opponent_animal_1_daytime_rect = opponent_animal_1_daytime.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 0)))
            SCREEN.blit(opponent_animal_1_daytime, opponent_animal_1_daytime_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][3][1]) == int:
                if self.opponent_scoring[0][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][3][0]}{doubledot} {self.opponent_scoring[0][3][1]}", 1, item_color)
            opponent_animal_1_item1_rect = opponent_animal_1_item1.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 1)))
            SCREEN.blit(opponent_animal_1_item1, opponent_animal_1_item1_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][4][1]) == int:
                if self.opponent_scoring[0][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][4][0]}{doubledot} {self.opponent_scoring[0][4][1]}", 1, item_color)
            opponent_animal_1_item2_rect = opponent_animal_1_item2.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 2)))
            SCREEN.blit(opponent_animal_1_item2, opponent_animal_1_item2_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][5][1]) == int:
                if self.opponent_scoring[0][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][5][0]}{doubledot} {self.opponent_scoring[0][5][1]}", 1, item_color)
            opponent_animal_1_item3_rect = opponent_animal_1_item3.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 3)))
            SCREEN.blit(opponent_animal_1_item3, opponent_animal_1_item3_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][6][1]) == int:
                if self.opponent_scoring[0][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][6][0]}{doubledot} {self.opponent_scoring[0][6][1]}", 1, item_color)
            opponent_animal_1_item4_rect = opponent_animal_1_item4.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 4)))
            SCREEN.blit(opponent_animal_1_item4, opponent_animal_1_item4_rect)

            doubledot = ":"
            if type(self.opponent_scoring[0][7][1]) == int:
                if self.opponent_scoring[0][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_1_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[0][7][0]}{doubledot} {self.opponent_scoring[0][7][1]}", 1, item_color)
            opponent_animal_1_item5_rect = opponent_animal_1_item5.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 0) + (16 * 5)))
            SCREEN.blit(opponent_animal_1_item5, opponent_animal_1_item5_rect)

            opponent_animal_2_name = SMALLER_FONT.render(f"{self.opponent_scoring[1][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            opponent_animal_2_name_rect = opponent_animal_2_name.get_rect(topright = (WIDTH - 25, 75 + (125 * 1)))
            SCREEN.blit(opponent_animal_2_name, opponent_animal_2_name_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][1][1]) == int:
                if self.opponent_scoring[1][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_country = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][1][0]}{doubledot} {self.opponent_scoring[1][1][1]}", 1, item_color)
            opponent_animal_2_country_rect = opponent_animal_2_country.get_rect(topright = (WIDTH - 90 - 88, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 0)))
            SCREEN.blit(opponent_animal_2_country, opponent_animal_2_country_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][2][1]) == int:
                if self.opponent_scoring[1][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ":"

            opponent_animal_2_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][2][0]}{doubledot} {self.opponent_scoring[1][2][1]}", 1, item_color)
            opponent_animal_2_daytime_rect = opponent_animal_2_daytime.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 0)))
            SCREEN.blit(opponent_animal_2_daytime, opponent_animal_2_daytime_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][3][1]) == int:
                if self.opponent_scoring[1][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][3][0]}{doubledot} {self.opponent_scoring[1][3][1]}", 1, item_color)
            opponent_animal_2_item1_rect = opponent_animal_2_item1.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 1)))
            SCREEN.blit(opponent_animal_2_item1, opponent_animal_2_item1_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][4][1]) == int:
                if self.opponent_scoring[1][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][4][0]}{doubledot} {self.opponent_scoring[1][4][1]}", 1, item_color)
            opponent_animal_2_item2_rect = opponent_animal_2_item2.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 2)))
            SCREEN.blit(opponent_animal_2_item2, opponent_animal_2_item2_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][5][1]) == int:
                if self.opponent_scoring[1][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][5][0]}{doubledot} {self.opponent_scoring[1][5][1]}", 1, item_color)
            opponent_animal_2_item3_rect = opponent_animal_2_item3.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 3)))
            SCREEN.blit(opponent_animal_2_item3, opponent_animal_2_item3_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][6][1]) == int:
                if self.opponent_scoring[1][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][6][0]}{doubledot} {self.opponent_scoring[1][6][1]}", 1, item_color)
            opponent_animal_2_item4_rect = opponent_animal_2_item4.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 4)))
            SCREEN.blit(opponent_animal_2_item4, opponent_animal_2_item4_rect)

            doubledot = ":"
            if type(self.opponent_scoring[1][7][1]) == int:
                if self.opponent_scoring[1][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_2_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[1][7][0]}{doubledot} {self.opponent_scoring[1][7][1]}", 1, item_color)
            opponent_animal_2_item5_rect = opponent_animal_2_item5.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 1) + (16 * 5)))
            SCREEN.blit(opponent_animal_2_item5, opponent_animal_2_item5_rect)

            opponent_animal_3_name = SMALLER_FONT.render(f"{self.opponent_scoring[2][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            opponent_animal_3_name_rect = opponent_animal_3_name.get_rect(topright = (WIDTH - 25, 75 + (125 * 2)))
            SCREEN.blit(opponent_animal_3_name, opponent_animal_3_name_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][1][1]) == int:
                if self.opponent_scoring[2][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_country = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][1][0]}{doubledot} {self.opponent_scoring[2][1][1]}", 1, item_color)
            opponent_animal_3_country_rect = opponent_animal_3_country.get_rect(topright = (WIDTH - 90 - 88, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 0)))
            SCREEN.blit(opponent_animal_3_country, opponent_animal_3_country_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][2][1]) == int:
                if self.opponent_scoring[2][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ":"

            opponent_animal_3_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][2][0]}{doubledot} {self.opponent_scoring[2][2][1]}", 1, item_color)
            opponent_animal_3_daytime_rect = opponent_animal_3_daytime.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 0)))
            SCREEN.blit(opponent_animal_3_daytime, opponent_animal_3_daytime_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][3][1]) == int:
                if self.opponent_scoring[2][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][3][0]}{doubledot} {self.opponent_scoring[2][3][1]}", 1, item_color)
            opponent_animal_3_item1_rect = opponent_animal_3_item1.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 1)))
            SCREEN.blit(opponent_animal_3_item1, opponent_animal_3_item1_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][4][1]) == int:
                if self.opponent_scoring[2][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][4][0]}{doubledot} {self.opponent_scoring[2][4][1]}", 1, item_color)
            opponent_animal_3_item2_rect = opponent_animal_3_item2.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 2)))
            SCREEN.blit(opponent_animal_3_item2, opponent_animal_3_item2_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][5][1]) == int:
                if self.opponent_scoring[2][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][5][0]}{doubledot} {self.opponent_scoring[2][5][1]}", 1, item_color)
            opponent_animal_3_item3_rect = opponent_animal_3_item3.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 3)))
            SCREEN.blit(opponent_animal_3_item3, opponent_animal_3_item3_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][6][1]) == int:
                if self.opponent_scoring[2][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][6][0]}{doubledot} {self.opponent_scoring[2][6][1]}", 1, item_color)
            opponent_animal_3_item4_rect = opponent_animal_3_item4.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 4)))
            SCREEN.blit(opponent_animal_3_item4, opponent_animal_3_item4_rect)

            doubledot = ":"
            if type(self.opponent_scoring[2][7][1]) == int:
                if self.opponent_scoring[2][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_3_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[2][7][0]}{doubledot} {self.opponent_scoring[2][7][1]}", 1, item_color)
            opponent_animal_3_item5_rect = opponent_animal_3_item5.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 2) + (16 * 5)))
            SCREEN.blit(opponent_animal_3_item5, opponent_animal_3_item5_rect)

            opponent_animal_4_name = SMALLER_FONT.render(f"{self.opponent_scoring[3][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            opponent_animal_4_name_rect = opponent_animal_4_name.get_rect(topright = (WIDTH - 25, 75 + (125 * 3)))
            SCREEN.blit(opponent_animal_4_name, opponent_animal_4_name_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][1][1]) == int:
                if self.opponent_scoring[3][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_country = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][1][0]}{doubledot} {self.opponent_scoring[3][1][1]}", 1, item_color)
            opponent_animal_4_country_rect = opponent_animal_4_country.get_rect(topright = (WIDTH - 90 - 88, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 0)))
            SCREEN.blit(opponent_animal_4_country, opponent_animal_4_country_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][2][1]) == int:
                if self.opponent_scoring[3][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][2][0]}{doubledot} {self.opponent_scoring[3][2][1]}", 1, item_color)
            opponent_animal_4_daytime_rect = opponent_animal_4_daytime.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 0)))
            SCREEN.blit(opponent_animal_4_daytime, opponent_animal_4_daytime_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][3][1]) == int:
                if self.opponent_scoring[3][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][3][0]}{doubledot} {self.opponent_scoring[3][3][1]}", 1, item_color)
            opponent_animal_4_item1_rect = opponent_animal_4_item1.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 1)))
            SCREEN.blit(opponent_animal_4_item1, opponent_animal_4_item1_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][4][1]) == int:
                if self.opponent_scoring[3][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][4][0]}{doubledot} {self.opponent_scoring[3][4][1]}", 1, item_color)
            opponent_animal_4_item2_rect = opponent_animal_4_item2.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 2)))
            SCREEN.blit(opponent_animal_4_item2, opponent_animal_4_item2_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][5][1]) == int:
                if self.opponent_scoring[3][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][5][0]}{doubledot} {self.opponent_scoring[3][5][1]}", 1, item_color)
            opponent_animal_4_item3_rect = opponent_animal_4_item3.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 3)))
            SCREEN.blit(opponent_animal_4_item3, opponent_animal_4_item3_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][6][1]) == int:
                if self.opponent_scoring[3][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][6][0]}{doubledot} {self.opponent_scoring[3][6][1]}", 1, item_color)
            opponent_animal_4_item4_rect = opponent_animal_4_item4.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 4)))
            SCREEN.blit(opponent_animal_4_item4, opponent_animal_4_item4_rect)

            doubledot = ":"
            if type(self.opponent_scoring[3][7][1]) == int:
                if self.opponent_scoring[3][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_4_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[3][7][0]}{doubledot} {self.opponent_scoring[3][7][1]}", 1, item_color)
            opponent_animal_4_item5_rect = opponent_animal_4_item5.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 3) + (16 * 5)))
            SCREEN.blit(opponent_animal_4_item5, opponent_animal_4_item5_rect)

            opponent_animal_5_name = SMALLER_FONT.render(f"{self.opponent_scoring[4][0]}", 1, CHALLENGE_BUTTON_COLOR_1)
            opponent_animal_5_name_rect = opponent_animal_5_name.get_rect(topright = (WIDTH - 25, 75 + (125 * 4)))
            SCREEN.blit(opponent_animal_5_name, opponent_animal_5_name_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][1][1]) == int:
                if self.opponent_scoring[4][1][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_country = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][1][0]}{doubledot} {self.opponent_scoring[4][1][1]}", 1, item_color)
            opponent_animal_5_country_rect = opponent_animal_5_country.get_rect(topright = (WIDTH - 90 - 88, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 0)))
            SCREEN.blit(opponent_animal_5_country, opponent_animal_5_country_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][2][1]) == int:
                if self.opponent_scoring[4][2][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = "#8a8a8a"
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_daytime = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][2][0]}{doubledot} {self.opponent_scoring[4][2][1]}", 1, item_color)
            opponent_animal_5_daytime_rect = opponent_animal_5_daytime.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 0)))
            SCREEN.blit(opponent_animal_5_daytime, opponent_animal_5_daytime_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][3][1]) == int:
                if self.opponent_scoring[4][3][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_item1 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][3][0]}{doubledot} {self.opponent_scoring[4][3][1]}", 1, item_color)
            opponent_animal_5_item1_rect = opponent_animal_5_item1.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 1)))
            SCREEN.blit(opponent_animal_5_item1, opponent_animal_5_item1_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][4][1]) == int:
                if self.opponent_scoring[4][4][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_item2 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][4][0]}{doubledot} {self.opponent_scoring[4][4][1]}", 1, item_color)
            opponent_animal_5_item2_rect = opponent_animal_5_item2.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 2)))
            SCREEN.blit(opponent_animal_5_item2, opponent_animal_5_item2_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][5][1]) == int:
                if self.opponent_scoring[4][5][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_item3 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][5][0]}{doubledot} {self.opponent_scoring[4][5][1]}", 1, item_color)
            opponent_animal_5_item3_rect = opponent_animal_5_item3.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 3)))
            SCREEN.blit(opponent_animal_5_item3, opponent_animal_5_item3_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][6][1]) == int:
                if self.opponent_scoring[4][6][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_item4 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][6][0]}{doubledot} {self.opponent_scoring[4][6][1]}", 1, item_color)
            opponent_animal_5_item4_rect = opponent_animal_5_item4.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 4)))
            SCREEN.blit(opponent_animal_5_item4, opponent_animal_5_item4_rect)

            doubledot = ":"
            if type(self.opponent_scoring[4][7][1]) == int:
                if self.opponent_scoring[4][7][1] > 0:
                    item_color = CHALLENGE_BUTTON_COLOR_1
                else:
                    item_color = WARNING_COLOR
            else:
                item_color = "#8a8a8a"
                doubledot = ""

            opponent_animal_5_item5 = SLIGHTLY_SMALLER_FONT.render(f"{self.opponent_scoring[4][7][0]}{doubledot} {self.opponent_scoring[4][7][1]}", 1, item_color)
            opponent_animal_5_item5_rect = opponent_animal_5_item5.get_rect(topright = (WIDTH - 90, BASE_HEIGHT_COEFF + (125 * 4) + (16 * 5)))
            SCREEN.blit(opponent_animal_5_item5, opponent_animal_5_item5_rect)

class Form(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()

        self.type = type

        if type == "search":
            rectangle = pygame.Rect(x, y, 350, 40)
        else:
            rectangle = pygame.Rect(x, y, 400, 40)

        self.image = pygame.image.load("img/button.png")
        self.rect = rectangle
        
        self.marked = False

        forms_group.add(self)

    def update(self):

        if self.marked:
            pygame.draw.rect(SCREEN, MARKED, self.rect, 0)
        else:
            pygame.draw.rect(SCREEN, NOT_MARKED, self.rect, 0)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, type, parm1, parm2, search = False):
        super().__init__()

        self.x = x
        self.y = y

        self.search = search

        self.type = type
        self.parm1 = parm1
        self.parm2 = parm2
        self.mouse_on = False
        self.og_color = "#eacc54"
        self.hover_color = "#e1b70b"
        self.current_color = self.og_color
        self.getting_color = FONT_COLOR

        self.clickable = True

        if self.type == "get_card":

            self.og_color = CHALLENGE_BUTTON_COLOR_2
            self.hover_color = "#aaf573"            

            enough_points = handle_db("get_points",user_logged)

            if enough_points < 5:
                self.clickable = False
                self.og_color = "#dedede"
                self.getting_color = "gray"
                
            else:
                self.clickable = True
                self.og_color = CHALLENGE_BUTTON_COLOR_2
                self.getting_color = FONT_COLOR

        self.height_coeff = 30

        if self.type == "login":
            self.text = BASE_FONT.render("LOGIN", 1, FONT_COLOR)
        elif self.type == "register_new_user":
            self.text = BASE_FONT.render("Register new user", 1, FONT_COLOR)
        elif self.type == "back_to_login":
            self.text = BASE_FONT.render("Back to login", 1, FONT_COLOR)
        elif self.type == "<< LOGOFF":
            self.text = SMALLER_FONT.render("<< LOGOFF", 1, FONT_COLOR)
        elif self.type == "EXPLORE >>":
            self.text = SMALLER_FONT.render("EXPLORE >>", 1, FONT_COLOR)        
        elif self.type == "register_user":            
            self.text = BASE_FONT.render("REGISTER USER", 1, FONT_COLOR)
        elif self.type == "show_me_the_list":            
            self.text = BASE_FONT.render("Show me the list!", 1, FONT_COLOR)
        elif self.type == "search_user":            
            self.text = SMALLER_FONT.render("GO SEARCH >>", 1, FONT_COLOR)
        elif self.type == "<< BACK  ":            
            self.text = SMALLER_FONT.render("<< BACK  ", 1, FONT_COLOR)
        elif self.type == "back_to_explore":            
            self.text = SMALLER_FONT.render("<< BACK  ", 1, FONT_COLOR)
        elif self.type == "GET CARD >>":            
            self.text = SMALLER_FONT.render("GET CARD >>", 1, FONT_COLOR)
        elif self.type == "get_card":            
            self.text = BASE_FONT.render("GET CARD FOR 5 points >>", 1, self.getting_color)
        

        self.text_rect = self.text.get_rect(center = (x + 100, y + 30))
        self.rect = pygame.Rect(self.text_rect.x -40, self.text_rect.y - (self.height_coeff//2), self.text.get_width() + 80, self.text.get_height() + self.height_coeff)
        
        button_group.add(self)
        
        if self.type == "fetchall" or "insert" or "login" or "register_new_user":
            log_screen_group.add(self)
        if self.type == "back_to_login" or self.type == "show_me_the_list":           
            lobby_screen_group.add(self)
        if self.type == "register_user":
            register_new_user_screen_group.add(self)

    def update(self):
                                
        if self.type == self.type == "login":
            self.parm1 = login_typing
            self.parm2 = password_typing
        
        if self.type == "register_user":            
            self.parm1 = new_user_typing
            self.parm2 = new_password_typing

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse) and self.clickable:       
            self.current_color = self.hover_color
        
            
        else:
            self.current_color = self.og_color

        pygame.draw.rect(SCREEN,self.current_color, (self.text_rect.x -40, self.text_rect.y - (self.height_coeff//2), self.text.get_width() + 80, self.text.get_height() + self.height_coeff), 0, 15)

        SCREEN.blit(self.text, self.text_rect)

    def action(self):
            if self.type == "login":        
                return handle_db(self.type, self.parm1, self.parm2)
            if self.type == "register_user":                
                return handle_db("insert", self.parm1, self.parm2)

def moving_up():
    for one_frame in frames_group:
        if one_frame.screen == "player_card":          
            one_frame.moving_up = True   

    for one_card in cards_group:
        one_card.moving_up = True

    for one_button in button_group:
        if one_button.type == "challenge":
            one_button.moving_up = True

def clear_screen():
    global warning_message
    warning_message = ''
    
    for one_object in continue_button_group:
        one_object.kill()
        continue_button_group.remove(one_object)

    for one_object in final_animal_mini_card_group:
        one_object.kill()
        final_animal_mini_card_group.remove(one_object)

    for one_object in final_screen_group:
        one_object.kill()
        final_screen_group.remove(one_object)

    for one_object in final_country_card_group:
        one_object.kill()
        final_country_card_group.remove(one_object)

    for one_object in rejected_waiting_screen_group:
        one_object.kill()
        rejected_waiting_screen_group.remove(one_object)

    for one_object in reject_or_accept_buttons_group:
        one_object.kill()
        reject_or_accept_buttons_group.remove(one_object)

    for one_object in go_button_group:
        one_object.kill()
        go_button_group.remove(one_object)

    for one_card in total_minis_group:
        one_card.kill()
        total_minis_group.remove(one_card)

    for one_card in country_cards_group:
        one_card.kill()
        country_cards_group.remove(one_card)

    for one_card in chosen_animal_group:
        one_card.kill()
        chosen_animal_group.remove(one_card)

    for one_card in animal_mini_card_group:
        one_card.kill()
        animal_mini_card_group.remove(one_card)

    for one_card in get_cards_group:
        one_card.kill()
        get_cards_group.remove(one_card)

    for one_card in animal_card_group:
        one_card.kill()
        animal_card_group.remove(one_card)

    for one_object in scroll_arrows_group:
        one_object.kill()
        scroll_arrows_group.remove(one_object)

    for one_object in scrollers_group:
        one_object.kill()
        scrollers_group.remove(one_object)

    for one_object in button_group:
        one_object.kill()
        button_group.remove(one_object)

    for one_object in cards_group:
        one_object.kill()
        cards_group.remove(one_object)

    for one_object in frames_group:
        one_object.kill()
        frames_group.remove(one_object)

    for one_object in forms_group:
        one_object.kill()
        forms_group.remove(one_object)

    for one_object in register_new_user_screen_group:
        one_object.kill()
        register_new_user_screen_group.remove(one_object)

    for one_object in lobby_screen_group:
        one_object.kill()
        lobby_screen_group.remove(one_object)

    for one_object in explore_screen_group:
        one_object.kill()
        explore_screen_group.remove(one_object)

    for one_object in log_screen_group:
        one_object.kill()
        log_screen_group.remove(one_object)

    for one_object in waiting_screen_group:
        one_object.kill()
        waiting_screen_group.remove(one_object)

    for one_object in challenging_waiting_screen_group:
        one_object.kill()
        challenging_waiting_screen_group.remove(one_object)   
 
    for one_object in challenged_waiting_screen_group:
        one_object.kill()
        challenged_waiting_screen_group.remove(one_object)   

    for one_object in get_card_screen_group:
        one_object.kill()
        get_card_screen_group.remove(one_object)

    for one_object in you_challenge_screen_group:
        one_object.kill()
        you_challenge_screen_group.remove(one_object)

    for one_object in you_challenged_group:
        one_object.kill()
        you_challenged_group.remove(one_object)
    
    for one_object in add_animal_buttons_group:
        one_object.kill()
        add_animal_buttons_group.remove(one_object)

    for one_object in logos_group:
        one_object.kill()
        logos_group.remove(one_object)
    
def waiting_screen():
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()
        
    Screens("waiting_screen")    

def waiting_waiting():    
    waiting_screen()    
    waiting_screen_group.update()   
    pygame.display.update()  

def get_card():
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()

    Logo(WIDTH//2-8, 47, "lobby_screen")

    back_to_login_button = Button(2, 6, "back_to_explore", "", "")

    new_card = randint(1,handle_db("count_the_animals")) # TADY PAK NAPSAT AT TO POCITA ANIMALSY STEJNE JAK COUNTRIES Z DB

    GetCard(WIDTH//2, HEIGHT//2 - 28, new_card)

    handle_db("get_card",user_logged, new_card)

    Screens("get_card_screen",animal=new_card)

def count_screen(user = "", opponent = "", animals = "", country = ""):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()  

    pre_animals = [anima.pic for anima in list(animals)]
    animals = ""
    for anima in pre_animals:
        animals += anima + ","

    animals = animals.strip(",")

    user_status = user[6]
    user = user[0]
    
    opponent = opponent[0]

    country = country.pic

    if user_status == "free":
        handle_db("challenging", user, opponent, country, animals)
    if user_status == "challenged":
        handle_db("challenged", user, opponent, country, animals)

def answered(user):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()  

    full_user = handle_db("get_full_user", user)
    full_opponent = handle_db("get_full_user_by_id",handle_db("get_full_user",user)[8])    
    full_country = handle_db("get_country",full_user[7])[0]

    user_animals = (full_user[9]).split(",")
    opponent_animals = full_opponent[9].split(",")

    user_animals_full_list = []
    opponent_animals_full_list = []

    for animal in user_animals:
        user_animals_full_list.append(handle_db("get_animal",animal))

    for animal in opponent_animals:
        opponent_animals_full_list.append(handle_db("get_animal",animal))

    user_results = {}
    user_pre_final_count = []
    user_pre_verdict = []

    if user_animals_full_list[0] != None:

        for i in range(len(user_animals_full_list)):
            user_results[f"animal_{i}"] = []
            for k in range(len(full_country)):
                user_results[f"animal_{i}"].append(f"{full_country[k]},{user_animals_full_list[i][k]}")
                
        for i in range(len(user_results)):
            pre_counting = []
            row = -1
            for k in user_results[f"animal_{i}"]:
                row += 1
                k = k.split(",")
                if row == 1:
                    animalko = k[1]
                    pre_counting.append(animalko)
                if (k[0] != '0' or k[1] != '0') and k[1] != '0' and row not in [0,1,3]:
                    loc_type = ""
                    if row == 2:
                        loc_type = "country"
                        if k[0] == k[1]:
                            k = [loc_type, 10]
                        else:
                            k = [loc_type, 0]
                    if row == 4:
                        loc_type = "daytime"
                        if k[0] == k[1]:
                            k = [loc_type, 1]
                        else:
                            k = [loc_type, 0]
                    if row == 5:
                        loc_type = "woods"
                    if row == 6:
                        loc_type = "sea"
                    if row == 7:
                        loc_type = "waters"
                    if row == 8:
                        loc_type = "tree"
                    if row == 9:
                        loc_type = "air"
                    if row == 10:
                        loc_type = "mountains"
                    if row == 11:
                        loc_type = "fields"
                    if row == 12:
                        loc_type = "caves"
                    if row == 13:
                        loc_type = "desert"
                    if row == 14:
                        loc_type = "savanna"
                    if row == 15:
                        loc_type = "snow"

                    if k[0] == '0':
                        k[1] = int(k[1]) * (-1)
                        k = [loc_type, k[1]]

                    if k[0] != '0' and k[0].isdigit():
                        k[1] = int(k[0]) + int(k[1])
                        k = [loc_type, k[1]]

                    pre_counting.append(k)

                if row == 15:
                    user_pre_verdict.append(pre_counting)

        for one_animal in user_pre_verdict:
            for item in one_animal:
                if type(item) == list:
                    user_pre_final_count.append(item[1])

        user_final_count = sum(user_pre_final_count)

    else:
        user_final_count = 0
        user_animals_full_list = []

    opponent_results = {}
    opponent_pre_final_count = []
    opponent_pre_verdict = []

    if opponent_animals_full_list[0] != None:

        for i in range(len(opponent_animals_full_list)):
            opponent_results[f"animal_{i}"] = []
            for k in range(len(full_country)):
                opponent_results[f"animal_{i}"].append(f"{full_country[k]},{opponent_animals_full_list[i][k]}")
                
        for i in range(len(opponent_results)):
            opponent_pre_counting = []
            row = -1
            for k in opponent_results[f"animal_{i}"]:
                row += 1
                k = k.split(",")
                if row == 1:
                    animalko = k[1]
                    opponent_pre_counting.append(animalko)
                if (k[0] != '0' or k[1] != '0') and k[1] != '0' and row not in [0,1,3]:
                    loc_type = ""
                    if row == 2:
                        loc_type = "country"
                        if k[0] == k[1]:
                            k = [loc_type, 10]
                        else:
                            k = [loc_type, 0]
                    if row == 4:
                        loc_type = "daytime"
                        if k[0] == k[1]:
                            k = [loc_type, 1]
                        else:
                            k = [loc_type, 0]
                    if row == 5:
                        loc_type = "woods"
                    if row == 6:
                        loc_type = "sea"
                    if row == 7:
                        loc_type = "waters"
                    if row == 8:
                        loc_type = "tree"
                    if row == 9:
                        loc_type = "air"
                    if row == 10:
                        loc_type = "mountains"
                    if row == 11:
                        loc_type = "fields"
                    if row == 12:
                        loc_type = "caves"
                    if row == 13:
                        loc_type = "desert"
                    if row == 14:
                        loc_type = "savanna"
                    if row == 15:
                        loc_type = "snow"

                    if k[0] == '0':
                        k[1] = int(k[1]) * (-1)
                        k = [loc_type, k[1]]

                    if k[0] != '0' and k[0].isdigit():
                        k[1] = int(k[0]) + int(k[1])
                        k = [loc_type, k[1]]

                    opponent_pre_counting.append(k)

                if row == 15:
                    opponent_pre_verdict.append(opponent_pre_counting)

        for one_animal in opponent_pre_verdict:
            for item in one_animal:
                if type(item) == list:
                    opponent_pre_final_count.append(item[1])

        opponent_final_count = sum(opponent_pre_final_count)
    
    else:
        opponent_final_count = 0
        opponent_animals_full_list = []

    user_verdict = []

    for one_item in user_pre_verdict:
        user_verdict.append(one_item)

    for one_animal in user_verdict:
        animal_item_count = 8 - len(one_animal)
        for new_empty in range(animal_item_count):
            one_animal.append(["",""])

    empty_animal = ["", ["",""], ["",""], ["",""], ["",""], ["",""], ["",""], ["",""]]

    for empty_animalko in range(5 - len(user_pre_verdict)):
        user_verdict.append(empty_animal)

    opponent_verdict = []

    for one_item in opponent_pre_verdict:
        opponent_verdict.append(one_item)

    for one_animal in opponent_verdict:
        animal_item_count = 8 - len(one_animal)
        for new_empty in range(animal_item_count):
            one_animal.append(["",""])

    empty_animal = ["", ["",""], ["",""], ["",""], ["",""], ["",""], ["",""], ["",""]]

    for empty_animalko in range(5 - len(opponent_pre_verdict)):
        opponent_verdict.append(empty_animal)

    return final_screen(user=full_user, user_scoring=user_verdict, user_total_points=user_final_count, opponent=full_opponent, opponent_scoring=opponent_verdict, opponent_total_points=opponent_final_count, country=full_country, user_animals=user_animals_full_list, opponent_animals=opponent_animals_full_list)


def final_screen(user, user_scoring, user_total_points, opponent, opponent_scoring, opponent_total_points, country, user_animals, opponent_animals):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()

    final_user = user
    final_user_scoring = user_scoring
    final_user_points = user_total_points
    final_opponent = opponent
    final_opponent_scoring = opponent_scoring
    final_opponent_points = opponent_total_points
    final_country = country
    final_user_animals = user_animals
    final_opponent_animals = opponent_animals

    frame_height = 70
    frame_height_coeff = 125

    user_animal_card_nr = -1
    for frame in range(len(final_user_animals)):
        user_animal_card_nr += 1
        Frames(15, frame_height + (frame * frame_height_coeff),"final_animal")
        FinalAnimalMiniCard(20, frame_height + (frame * frame_height_coeff) + 25, final_user_animals[user_animal_card_nr][0])

    opponent_animal_card_nr = -1
    for frame in range(len(final_opponent_animals)):
        opponent_animal_card_nr += 1
        Frames(WIDTH - 265, frame_height + (frame * frame_height_coeff),"final_animal")
        FinalAnimalMiniCard(WIDTH - 84, frame_height + (frame * frame_height_coeff) + 25, final_opponent_animals[opponent_animal_card_nr][0])

    user_points_difference = final_user_points - final_opponent_points        

    Logo(WIDTH//2-8, 47, "lobby_screen")
    FinalCountryCard(WIDTH//2, HEIGHT//2 - 50, final_country)

    ContinueButton(WIDTH//2, HEIGHT//2+269, final_user, user_points_difference, opponent=final_opponent, opponent_scoring=final_opponent_scoring,opponent_total_points=final_opponent_points,user_scoring=final_user_scoring,user_total_points=final_user_points,opponent_animals=final_opponent_animals,user_animals=final_user_animals,final_country=final_country)

    Screens("final_screen", user=final_user, user_scoring=final_user_scoring, user_total_points=final_user_points, opponent=final_opponent, opponent_scoring=final_opponent_scoring, opponent_total_points=final_opponent_points, country=final_country, user_point_dif = user_points_difference)

def you_challenge_screen(username, opponent, country_num):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()
    full_user = (handle_db("get_full_user",username))
    full_opponent = (handle_db("get_full_user",opponent)) 

    YouChallenged(full_user, full_opponent)   

    Logo(WIDTH//2-8, 47, "lobby_screen")
    Button(2, 6, "<< BACK  ", "", "")

    list = full_user[4].split(",")
    status = full_user[6]

    width = 0
    width_coeff = 110
    index = -1
    for animal in list:
        index += 1
        width += width_coeff
        AnimalMiniCard(width, 550, animal, index)
    
    country = handle_db("get_country",country_num)

    CountryCard(85, 110, country)  

    Screens("you_challenge_screen", user_points = status)   

def explore_screen(username):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()
    user_points = (handle_db("get_full_user",username))[3]
    bring_animals(username)

    Frames(10, 80, "lobby_screen")

    Logo(WIDTH//2-8, 47, "lobby_screen")

    back_to_login_button = Button(2, 6, "<< BACK  ", "", "")
    
    height = 500

    Button(370, 560, "get_card", "", "")

    Screens("explore_screen", username, user_points)

def answered_2(username):
    user = handle_db("get_full_user",username)

    user_ff = tuple(json.loads(user[10]))

    user_scoring_ff = json.loads(user[11])

    user_total_points_ff = user[12]

    opponent_ff = tuple(json.loads(user[13]))

    opponent_scoring_ff = json.loads(user[14])

    opponent_total_points_ff = user[15]

    country_ff = tuple(json.loads(user[16]))

    pre_user_animals_ff = json.loads(user[17])
    
    user_animals_ff = []

    for i in pre_user_animals_ff:
        user_animals_ff.append(tuple(i))

    pre_opponent_animals_ff = json.loads(user[18])
    
    opponent_animals_ff = []

    for i in pre_opponent_animals_ff:
        opponent_animals_ff.append(tuple(i))

    final_screen(user=user_ff,user_scoring=user_scoring_ff,user_total_points=user_total_points_ff,opponent=opponent_ff,opponent_scoring=opponent_scoring_ff,opponent_total_points=opponent_total_points_ff,country=country_ff,user_animals=user_animals_ff,opponent_animals=opponent_animals_ff)
    

def lobby_screen(username):
    # user_logged = username
    global user_logged
    user_logged = username

    waiting_waiting()
    clear_screen()

    status = (handle_db("get_full_user",username))[6]
    
    if status == "challenging":
        waiting_waiting()
        return challenging_waiting_screen(username)
    if status == "challenged":
        waiting_waiting()
        return challenged_waiting_screen(username)
    if status == "rejected":
        waiting_waiting()
        return rejected_waiting_screen(username)
    if status == "answered":
        waiting_waiting()
        return answered(username)
    if status == "answered_2":
        waiting_waiting()
        return answered_2(username)
    
    global warning_message
    warning_message = ''

    user_points = (handle_db("get_full_user",username))[3]
    get_the_list(handle_db("top_10"),"top_10",username)
    get_the_list(handle_db("fetchall",username,"last_3"),"last_3",username)

    Frames(10, 80, "lobby_screen")
    Frames(10, 140, "rivals")
    Frames(460, 140, "top_10")

    Button(120, 480, "search_user", "", "")

    Logo(WIDTH//2-8, 47, "lobby_screen")

    back_to_login_button = Button(2, 6, "<< LOGOFF", "", "")
    explore_world = Button(690, 6, "EXPLORE >>", "", "")

    Form(50, 430, "search")   

    Screens("lobby_screen", username, user_points)

def challenging_waiting_screen(user):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()

    Button(2, 6, "<< LOGOFF", "", "")
    Logo(WIDTH//2-8, 47, "lobby_screen")
   
    pre_opponent = (handle_db("get_full_user",user))[8]
    points = (handle_db("get_full_user",user))[3]

    opponent = (handle_db("get_full_user_by_id",pre_opponent))[1]  

    RejectOrAcceptButton(WIDTH//2 - 100, HEIGHT//2 + 60, "cancel", user, opponent, "")

    Screens("challenging_waiting_screen", opponent, user_points = points)

def challenged_waiting_screen(user):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()

    Button(2, 6, "<< LOGOFF", "", "")
    Logo(WIDTH//2-8, 47, "lobby_screen")
   
    complete_user = handle_db("get_full_user",user)
    pre_opponent = complete_user[8]
    country = complete_user[7]
    
    opponent = (handle_db("get_full_user_by_id",pre_opponent))[1]  

    RejectOrAcceptButton(WIDTH//2 - 210, HEIGHT//2 + 60, "reject", user, opponent, country)
    RejectOrAcceptButton(WIDTH//2 + 20 , HEIGHT//2 + 60, "accept", user, opponent, country)

    Screens("challenged_waiting_screen", opponent)

def rejected_waiting_screen(user):
    waiting_waiting()
    global warning_message
    global scroll_arrows
    warning_message = ''
    scroll_arrows = []

    clear_screen()

    Button(2, 6, "<< LOGOFF", "", "")
    Logo(WIDTH//2-8, 47, "lobby_screen")
   
    pre_opponent = (handle_db("get_full_user",user))[8]
    points = (handle_db("get_full_user",user))[3]
    opponent = (handle_db("get_full_user_by_id",pre_opponent))[1]  

    RejectOrAcceptButton(WIDTH//2 - 40, HEIGHT//2 + 60, "ok", user, opponent, "")

    Screens("rejected_waiting_screen", opponent, user_points = points) 

def log_screen():
    global warning_message
    warning_message = ''

    clear_screen()

    Logo(WIDTH//2, 100, "log_screen")

    login_button = Button(WIDTH//2 - 100, 350, "login", "", "")
    register_button = Button(WIDTH//2 - 100, 520, "register_new_user", "", "")

    Form(250,200,"login")
    Form(250,245,"password")

    Frames(95, 135, "log_screen")

    Screens("log_screen")

def register_new_user_screen():
    global warning_message
    warning_message = ''

    clear_screen()
    
    Logo(WIDTH//2, 100, "register_new_user_screen")

    Frames(130, 170, "register_new_user_screen")
    
    Form(250,230,"new_user")
    Form(250,330,"new_password")

    Button(WIDTH//2 - 100, 480, "register_user", "", "")
    Button(WIDTH//2 - 100, 580, "back_to_login", "", "")

    Screens("register_new_user_screen")

def get_the_list(received, game_type, username):

    if type(received) == str:
        list = received.split(",")
    else:
        list = received                   

    if list[0] == "":
        list = ["nobody"]

    nr = 155
    nr_card = nr-10
    nr_coeff = 52
    left_distance = 45
    if game_type == "friends":        


        for card in list:
            nr += nr_coeff
            nr_card += nr_coeff
            Card(left_distance, nr, "friends", str(handle_db("fetch",card,"friends")), username)
            Frames(left_distance - 20, nr_card, "player_card")

    if game_type == "all_users":        

        for card in list:
            nr += 30
            Card(WIDTH//2 - 200, nr, "all_users", str(handle_db("fetch",card[0],"all_users")), username)

    if game_type == "top_10":

        for card in list:
            nr += nr_coeff
            nr_card += nr_coeff
            Card(left_distance + 450, nr, "friends", f"{card[0]} ({card[1]})", username)
            Frames(left_distance - 20 +450, nr_card, "player_card")

    if game_type == "last_3":        
        
        for card in list:
            nr += nr_coeff
            nr_card += nr_coeff
            Card(left_distance, nr, "friends", str(handle_db("fetch",card,"last_3")), username)
            if card != "nobody":
                Frames(left_distance - 20, nr_card, "player_card")
        
        if list != ["nobody"]:
            for ghost in range(3 - len(list)):
                nr += nr_coeff
                nr_card += nr_coeff
                Card(left_distance, nr+5, "friends", "--no opponent here so far--" , username)
                Frames(left_distance - 20, nr_card, "player_card")

def search_user(username):
    global warning_message
    nr = 570
    nr_card = nr-10
    nr_coeff = 52
    left_distance = 45
    if handle_db("search_user",username) != " ":
        Card(left_distance, nr, "search", str(handle_db("search_user",username)), user_logged, True)
        warning_message = ''
        Frames(left_distance - 20, nr_card, "player_card", "search_user")
    elif handle_db("search_user",username) == " ":
        warning_message = "User doesn't exist!"

def bring_animals(username):

    list = handle_db("bring_animals", username).split(",")

    width = -170
    width_coeff = 168 * 1.5
    
    for animal in list:
        width += width_coeff
        AnimalCard(width, 140, get_animal_info(animal))

    height = 500 

def get_animal_info(animal_id):
    return handle_db("animal_info",animal_id)

def bring_me_the_animal_count():
    return handle_db("count_the_animals")  

button_group = pygame.sprite.Group()
forms_group = pygame.sprite.Group()
log_screen_group = pygame.sprite.Group()
lobby_screen_group = pygame.sprite.Group()
explore_screen_group = pygame.sprite.Group()
register_new_user_screen_group = pygame.sprite.Group()
frames_group = pygame.sprite.Group()
logos_group = pygame.sprite.Group()
cards_group = pygame.sprite.Group()
scrollers_group = pygame.sprite.Group()
animal_card_group = pygame.sprite.Group()
scroll_arrows_group = pygame.sprite.Group()
waiting_screen_group = pygame.sprite.Group()
get_cards_group = pygame.sprite.Group()
get_card_screen_group = pygame.sprite.Group()
you_challenge_screen_group = pygame.sprite.Group()
animal_mini_card_group = pygame.sprite.Group()
you_challenged_group = pygame.sprite.Group()
chosen_animal_group = pygame.sprite.Group()
country_cards_group = pygame.sprite.Group()
add_animal_buttons_group = pygame.sprite.Group()
total_minis_group = pygame.sprite.Group()
go_button_group = pygame.sprite.Group()
reject_or_accept_buttons_group = pygame.sprite.Group()
challenging_waiting_screen_group = pygame.sprite.Group()
challenged_waiting_screen_group = pygame.sprite.Group()
rejected_waiting_screen_group = pygame.sprite.Group()
final_country_card_group = pygame.sprite.Group()
final_screen_group = pygame.sprite.Group()
final_animal_mini_card_group = pygame.sprite.Group()
continue_button_group = pygame.sprite.Group()

WIDTH = 900
HEIGHT = 700

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE = pygame.image.load("img/background.png").convert_alpha()

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
NOT_MARKED = "#c8c8c8"
MARKED = "#2eb612"
WARNING_COLOR = "red"

MORE_BIGGER_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 60)
SLIGHTLY_BIGGER_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 50)
BIGGER_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 40)
BASE_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 28)
SMALLER_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 22)
SLIGHTLY_SMALLER_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 15)
FONT_COLOR = (0, 0, 0)

LOGO_FONT = pygame.font.Font("fonts/challenger.otf",100)
LOGO_FONT_SMALLER = pygame.font.Font("fonts/challenger.otf",60)

CHALLENGE_FONT = pygame.font.Font("fonts/Radlush_Bold.ttf", 12)
CHALLENGE_BUTTON_COLOR_1 = "#327600"
CHALLENGE_BUTTON_COLOR_2 = "#65c61e"

GOT_COLOR = "#620074"
CHOOSE_COLOR = "#1aff0f"
CHALLENGING_COLOR = "#a5008e"
NEGATIVE_COLOR = "#a50032"

FADE_DOWN_MAX = 550
FADE_UP_MAX = 210

FADE_DOWN_MIDDLE = 590
FADE_DOWN_MIN = 580

MOVING_SPEED = 2

login_typing = ''
password_typing = ''
warning_message = ''
new_user_typing = ''
new_password_typing = ''
search_typing = ''
scroll_arrows = []

user_logged = ''

log_screen()
switch = False
run = True
while run:    
    
    SCREEN.blit(BG_IMAGE, (0,-10))

    pos = pygame.mouse.get_pos()
    marked_buttons = 0

    height = 500
     
    for one_card in animal_card_group:
        if one_card.rect.left < 0 and "right_arrow" not in scroll_arrows:
            ScrollArrow(800, height, "to_right")
            scroll_arrows.append("right_arrow")
        elif one_card.rect.left > len(animal_card_group)*252 and "right_arrow" in scroll_arrows:
            for one_arrow in scroll_arrows_group:
                if one_arrow.type == "to_right":
                    one_arrow.kill()
                    scroll_arrows_group.remove(one_arrow)
                    scroll_arrows.remove("right_arrow")

    for one_card in animal_card_group:
        if one_card.rect.right > WIDTH and "left_arrow" not in scroll_arrows:
            ScrollArrow(50, height, "to_left")
            scroll_arrows.append("left_arrow")
        elif one_card.rect.right < WIDTH and "left_arrow" in scroll_arrows:
            for one_arrow in scroll_arrows_group:
                if one_arrow.type == "to_left":
                    one_arrow.kill()
                    scroll_arrows_group.remove(one_arrow)
                    scroll_arrows.remove("left_arrow")

    for one_card in animal_mini_card_group:
        if one_card.rect.left < 0 and "right_arrow" not in scroll_arrows:
            ScrollArrow(800, height, "to_right", "mini")
            scroll_arrows.append("right_arrow")
        elif one_card.rect.left > len(animal_mini_card_group)*120 and "right_arrow" in scroll_arrows:
            for one_arrow in scroll_arrows_group:
                if one_arrow.type == "to_right":
                    one_arrow.kill()
                    scroll_arrows_group.remove(one_arrow)
                    scroll_arrows.remove("right_arrow")

    for one_card in animal_mini_card_group:
        if one_card.rect.right > WIDTH and "left_arrow" not in scroll_arrows:
            ScrollArrow(50, height, "to_left", "mini")
            scroll_arrows.append("left_arrow")
        elif one_card.rect.right < WIDTH and "left_arrow" in scroll_arrows:
            for one_arrow in scroll_arrows_group:
                if one_arrow.type == "to_left":
                    one_arrow.kill()
                    scroll_arrows_group.remove(one_arrow)
                    scroll_arrows.remove("left_arrow")   

    for one_form in forms_group:
        if one_form.marked:
            marked_buttons += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
                for one_button in button_group:
                    
                    if one_button.current_color == one_button.hover_color and (one_button.type == "EXPLORE >>" or one_button.type == "back_to_explore"):                        
                        explore_screen(user_logged)
                    elif one_button.current_color == one_button.hover_color and one_button.type == "search_user":
                        
                        for one_card in cards_group:
                            if one_card.search:
                                one_card.kill()
                                cards_group.remove()

                        for one_object in button_group:
                            if one_object.search:
                                one_object.kill()
                                one_object.remove()

                        for one_object in frames_group:
                            if one_object.type == "search_user":
                                one_object.kill()
                                one_object.remove()

                        search_user(search_typing)
                        search_typing = ''                        
                        
                    elif one_button.current_color == one_button.hover_color and one_button.type == "challenge":
                        you_challenge_screen(user_logged, one_button.user, randint(1,handle_db("get_countries_count")))
                    elif one_button.current_color == one_button.hover_color and one_button.type == "get_card":
                        get_card()                    
                    elif one_button.current_color == one_button.hover_color and one_button.type == "<< LOGOFF":
                        log_screen()
                    elif one_button.current_color == one_button.hover_color and one_button.type == "<< BACK  ":                        
                        lobby_screen(user_logged)                    
                    elif one_button.current_color == one_button.hover_color and one_button.type == "back_to_login":
                        log_screen()
                    elif one_button.current_color == one_button.hover_color and one_button.type == "register_new_user":
                        register_new_user_screen()
                    elif one_button.current_color == one_button.hover_color and one_button.type == "login" and password_typing != "" and login_typing != "":
                                           
                        action_done = one_button.action()
                        user_logged = login_typing                        
                        login_typing, password_typing = "", ""

                        if action_done == True:                            
                            if one_button.type == "login":
                                lobby_screen(user_logged)
                                warning_message = ''
                        else:
                            warning_message = "Incorrect credentials! Please try again!"


                    elif one_button.current_color == one_button.hover_color and one_button.type == "login" and password_typing != "":
                        action_done = one_button.action()                        
                        warning_message = "Please enter your username!"

                    elif one_button.current_color == one_button.hover_color and one_button.type == "login" and login_typing != "":
                        action_done = one_button.action()                        
                        warning_message = "Please enter your password!"

                    elif one_button.current_color == one_button.hover_color and one_button.type == "login":
                        warning_message = "Please enter your credentials!"

                    elif one_button.current_color == one_button.hover_color and one_button.type == "register_user" and new_password_typing != "" and new_user_typing != "":
                        action_done = one_button.action() 
                        new_user = new_user_typing 
 
                        if action_done == True:
                            user_logged = new_user     
                            lobby_screen(new_user)                                                 
                            new_user_typing, new_password_typing = "", ""
                        elif action_done == "duplicate user":
                            warning_message = "User already exists! Try something else!"
                        else:
                            warning_message = "Something went wrong!"


                    elif one_button.current_color == one_button.hover_color and one_button.type == "register_user" and new_password_typing != "":
                        action_done = one_button.action()                        
                        warning_message = "Please choose your username!"

                    elif one_button.current_color == one_button.hover_color and one_button.type == "register_user" and new_user_typing != "":
                        action_done = one_button.action()                        
                        warning_message = "Please choose your password!"

                    elif one_button.current_color == one_button.hover_color and one_button.type == "register_user":
                        warning_message = "Please choose your credentials!" 

                for one_form in forms_group:              
                    if one_form.rect.collidepoint(pos):
                        one_form.marked = True
                        
                    else:
                        one_form.marked = False           
        if marked_buttons == 0:
            for one_form in forms_group:
                one_form.marked = True
                break

        if event.type == pygame.KEYDOWN:
                            
            for one_form in forms_group:
                if one_form.marked:
                    switch = False
                    if one_form.type == "search":

                        if event.key == pygame.K_BACKSPACE:
                            search_typing = search_typing[:-1]
                        
                        elif event.key == pygame.K_RETURN:

                            for one_card in cards_group:
                                if one_card.search:
                                    one_card.kill()
                                    cards_group.remove()

                            for one_object in button_group:
                                if one_object.search:
                                    one_object.kill()
                                    one_object.remove()

                            for one_object in frames_group:
                                if one_object.type == "search_user":
                                    one_object.kill()
                                    one_object.remove()

                            search_user(search_typing)
                            search_typing = ''
                        
                        else:
                            search_typing += event.unicode

                    elif one_form.type == "login":

                        if event.key == pygame.K_TAB:
                            one_form.marked = False
                            switch = True

                        elif event.key == pygame.K_BACKSPACE:
                            login_typing = login_typing[:-1]

                        elif event.key == pygame.K_RETURN and password_typing != "" and login_typing != "":
                            login_done = handle_db("login", login_typing, password_typing)
                            user_logged = login_typing
                            login_typing, password_typing = "", ""
                            if login_done == True:
                                lobby_screen(user_logged)
                                warning_message = ''
                            else:
                                warning_message = "Incorrect credentials! Please try again!"

                        elif event.key == pygame.K_RETURN and password_typing != "":
                            warning_message = "Please enter your username!"

                        elif event.key == pygame.K_RETURN and login_typing != "":
                            warning_message = "Please enter your password!"
                                
                        elif event.key == pygame.K_RETURN:
                            warning_message = "Please enter your credentials!"

                        else:
                            login_typing += event.unicode

                    elif one_form.type == "password":

                        if event.key == pygame.K_TAB:
                            one_form.marked = False
                            switch = True

                        elif event.key == pygame.K_BACKSPACE:
                            password_typing = password_typing[:-1]

                        elif event.key == pygame.K_RETURN and password_typing != "" and login_typing != "":
                            login_done = handle_db("login", login_typing, password_typing)
                            user_logged = login_typing
                            login_typing, password_typing = "", ""
                            if login_done == True:
                                lobby_screen(user_logged)
                                warning_message = ''
                            else:
                                warning_message = "Incorrect credentials! Please try again!"

                        elif event.key == pygame.K_RETURN and password_typing != "":
                            warning_message = "Please enter your username!"

                        elif event.key == pygame.K_RETURN and login_typing != "":
                            warning_message = "Please enter your password!"

                        elif event.key == pygame.K_RETURN:
                            warning_message = "Please enter your credentials!"
                            
                        else:
                            password_typing += event.unicode

                    elif one_form.type == "new_user":

                        if event.key == pygame.K_TAB:
                            one_form.marked = False
                            switch = True

                        elif event.key == pygame.K_BACKSPACE:
                            new_user_typing = new_user_typing[:-1]

                        elif event.key == pygame.K_RETURN and new_password_typing != "" and new_user_typing != "":                            
                            register_done = handle_db("insert", new_user_typing, new_password_typing)
                            new_user = new_user_typing
                            user_logged = new_user_typing
                            if register_done == True:                                
                                lobby_screen(new_user)
                                warning_message = 'user added'
                                new_user_typing, new_password_typing = "", ""
                            elif register_done == "duplicate user":
                                warning_message = "User already exists! Try something else!"
                            else:
                                warning_message = "Something went wrong!"

                        elif event.key == pygame.K_RETURN and new_password_typing != "":
                            warning_message = "Please enter your username!"

                        elif event.key == pygame.K_RETURN and new_user_typing != "":
                            warning_message = "Please enter your password!"
                                
                        elif event.key == pygame.K_RETURN:
                            warning_message = "Please enter your credentials!"

                        else:
                            new_user_typing += event.unicode

                    elif one_form.type == "new_password":

                        if event.key == pygame.K_TAB:
                            one_form.marked = False
                            switch = True

                        elif event.key == pygame.K_BACKSPACE:
                            new_password_typing = new_password_typing[:-1]

                        elif event.key == pygame.K_RETURN and new_password_typing != "" and new_user_typing != "":
                            register_done = handle_db("insert", new_user_typing, new_password_typing)
                            new_user = new_user_typing
                            new_user_typing, new_password_typing = "", ""
                            if register_done == True:
                                lobby_screen(new_user)
                            elif register_done == "duplicate user":
                                warning_message = "User already exists! Try something else!"
                            else:                               
                                warning_message = "Incorrect credentials! Please try again!"

                        elif event.key == pygame.K_RETURN and new_password_typing != "":
                            warning_message = "Please enter your username!"

                        elif event.key == pygame.K_RETURN and new_user_typing != "":
                            warning_message = "Please enter your password!"

                        elif event.key == pygame.K_RETURN:
                            warning_message = "Please enter your credentials!"
                            
                        else:
                            new_password_typing += event.unicode                   
                
                else:
                    if switch:
                        one_form.marked = True
                        switch = False
 
    frames_group.update()
    logos_group.update()
    button_group.update()
    forms_group.update()
    log_screen_group.update()
    lobby_screen_group.update()
    explore_screen_group.update()
    register_new_user_screen_group.update()
    you_challenge_screen_group.update()
    cards_group.update()
    scrollers_group.update()
    scroll_arrows_group.update()    
    animal_mini_card_group.update()
    chosen_animal_group.update()
    animal_card_group.draw(SCREEN)
    scroll_arrows_group.draw(SCREEN)
    get_cards_group.draw(SCREEN)
    country_cards_group.draw(SCREEN)
    final_country_card_group.draw(SCREEN)
    final_animal_mini_card_group.draw(SCREEN)
    get_card_screen_group.update()
    waiting_screen_group.update()    
    add_animal_buttons_group.update()
    total_minis_group.update()
    go_button_group.update()
    challenging_waiting_screen_group.update()
    challenged_waiting_screen_group.update()
    reject_or_accept_buttons_group.update()
    rejected_waiting_screen_group.update()
    final_screen_group.update()
    continue_button_group.update()    
    
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()