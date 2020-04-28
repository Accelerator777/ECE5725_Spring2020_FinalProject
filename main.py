import pygame
from pygame.locals import*
import os
import RPi.GPIO as GPIO
import time
import free_mode
import guide_mode
import record_mode
import voice_recognition

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

def GPIO27_callback(channel):
    global code_running
    print ("falling edge detected on 27")
    code_running = False
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback)

pygame.init()
pygame.mouse.set_visible(False)

BLACK=0,0,0
WHITE=255,255,255

size=width,height=320,240
screen=pygame.display.set_mode((width,height))

flag_main = True
flag_free = False
flag_guide = False
flag_record = False


# main menu
def main_menu():
    screen.fill(BLACK)
    screen.blit(background,backrect)

    title_text={'music box':(160,25)}
    button_text={'free mode':(50,220),'guide mode':(160,220),'record mode':(270,220)}
    for my_text,text_pos in title_text.items():
        text_surface=title_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
    for my_text,text_pos in button_text.items():
        text_surface=button_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)

    pygame.display.flip()

# free play mode menu
def free_menu():
    screen.fill(BLACK)
    screen.blit(background,backrect)

    title_text={'free mode':(160,25)}
    button_text={'back':(270,220)}
    for my_text,text_pos in title_text.items():
        text_surface=title_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
    for my_text,text_pos in button_text.items():
        text_surface=button_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)

    pygame.display.flip()

# guide play mode menu
def guide_menu(string):
    screen.fill(BLACK)
    screen.blit(background,backrect)
	
    title_text={'guide mode':(160,25)}
    button_text={'start':(50,220),'stop':(160,220),'back':(270,220)}
    for my_text,text_pos in title_text.items():
        text_surface=title_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
    for my_text,text_pos in button_text.items():
        text_surface=button_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)

    text=button_font.render(string,True,WHITE)
    textRect=text.get_rect()
    textRect.center=(160,120)
    screen.blit(text,textRect)
	
    pygame.display.flip()

# record mode menu
def record_menu(string):
    screen.fill(BLACK)
    screen.blit(background,backrect)

    title_text={'record mode':(160,25)}
    button_text={'start':(50,220),'play':(120,220),'load':(200,220),'back':(270,220)}
    for my_text,text_pos in title_text.items():
        text_surface=title_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
    for my_text,text_pos in button_text.items():
        text_surface=button_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
	
    text=button_font.render(string,True,WHITE)
    textRect=text.get_rect()
    textRect.center=(160,180)
    screen.blit(text,textRect)

    pygame.display.flip()

######
code_running = True	
main_menu()
while code_running:
    if flag_main:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                x,y=pos
                if y>200:
                    if x<80: #free mode
                        flag_main = False
                        flag_free = True
                        free_menu()
                        status = play_sound.run("sounds")
                        if status==0:
                            flag_main = True
                            flag_free = False
                            main_menu()

                    elif x>140 and x<180: #guide mode
                        flag_main = False
                        flag_guide = True
                        guide_menu("")

                    elif x>240: #record mode
                        flag_main = False
                        flag_record = True
                        record_menu("")

    if flag_free:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                x,y=pos
                if y>200:
                    if x>240:	# back to main menu
                        flag_main = True
                        flag_free = False
                        main_menu()
    if flag_guide:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                x,y=pos
                if y>200:
                    if x>240:	# back to main menu
                        flag_main = True
                        flag_guide = False
                        main_menu()
    if flag_record:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                x,y=pos
                if y>200:
                    if x<80:
                        record_menu("Recording")
                        record_mode.record()
                    
                    elif x>100 and x<140:
                        record_menu("Playing")
                    
                    elif x>180 and x<220:
                        record_menu("Loading")

                    elif x>240:	# back to main menu
                        flag_main = True
                        flag_record = False
                        main_menu()
GPIO.cleanup()