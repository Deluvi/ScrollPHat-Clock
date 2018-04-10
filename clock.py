#!/usr/bin/env python3

import requests
import time
import signal
import math
import random
import os

import scrollphathd
from scrollphathd.fonts import font5x7

def get_meteo():
    body = requests.get("http://api.openweathermap.org/data/2.5/weather?id={}&appid={}".format(os.getenv("ScrollPHatClockCITYID"),os.getenv("ScrollPHatClockAPIKEY"))).json()
    main = body['main']
    wind = body['wind']
    return (main,wind)

def draw_circle(x,y,radius):
    if radius == 1:
        scrollphathd.set_pixel(x,y,0.5)
        return
    cur_x = x
    cur_y = y - radius + 1
    while y != cur_y:
        if cur_y >= 0 and cur_x >= 0:
            scrollphathd.set_pixel(cur_x,cur_y,0.5)
        cur_x = cur_x - 1
        cur_y = cur_y + 1
    while x != cur_x:
        if cur_y >= 0 and cur_x >= 0:
            scrollphathd.set_pixel(cur_x,cur_y,0.5)
        cur_x = cur_x + 1
        cur_y = cur_y + 1
    while y != cur_y:
        if cur_y >= 0 and cur_x >= 0:
            scrollphathd.set_pixel(cur_x,cur_y,0.5)
        cur_x = cur_x + 1
        cur_y = cur_y - 1
    while x != cur_x:
        if cur_y >= 0 and cur_x >= 0:
            scrollphathd.set_pixel(cur_x,cur_y,0.5)
        cur_x = cur_x - 1
        cur_y = cur_y - 1

def display_animated_circle():
    scrollphathd.clear()
    frame = -1
    (width,height) = scrollphathd.get_shape()
    center_x = math.floor(width/2)
    center_y = math.floor(height/2)
    started_time = time.time()
    while time.time() - started_time < 15:
        scrollphathd.clear()
        frame = (frame + 1) % 3
        for i in range(5):
            draw_circle(center_x,center_y,(frame+1)+i*3)
        scrollphathd.show()
        yield

def draw_square(x,y,length):
    if length == 1:
        scrollphathd.set_pixel(x,y,0.5)
        return
    for i in range(length+1):
        if x + i >= 0 and y >=0:
            scrollphathd.set_pixel(x+i,y,0.5)
        if x >= 0 and y + i >= 0:
            scrollphathd.set_pixel(x,y+i,0.5)
        if x + length - i >= 0 and y + length >= 0:
           scrollphathd.set_pixel(x+length-i,y+length,0.5)
        if x + length >= 0 and y + length - i >= 0:
           scrollphathd.set_pixel(x+length,y+length-i,0.5)

def display_animated_square():
    scrollphathd.clear()
    frame = -1
    (width,height) = scrollphathd.get_shape()
    center_x = math.floor(width/2)
    center_y = math.floor(height/2)
    started_time = time.time()
    while time.time() - started_time < 15:
        scrollphathd.clear()
        frame = (frame + 1)%3
        for i in range(5):
            draw_square(center_x-((frame+1)+i*3)//2,center_y-((frame+1)+i*3)//2,(frame+1)+i*3)
        scrollphathd.show()
        yield

def display_animated_cosinus():
    (width,height) = scrollphathd.get_shape()
    frame = -1
    started_time = time.time()
    while time.time() - started_time < 15:
       scrollphathd.clear()
       frame = frame + 1
       for x in range(width):
           x_real = ((x+frame)/width) * 4 * math.pi
           scrollphathd.set_pixel(x,math.floor(math.cos(x_real)*(height//2)+height//2),brightness=0.5)
       scrollphathd.show()
       yield

def display_animated_diagonals():
    (width,height) = scrollphathd.get_shape()
    frame = -1
    started_time = time.time()
    while time.time() - started_time < 15:
       scrollphathd.clear()
       frame = frame + 1 % width
       y_frame = frame
       for x in range(width):
           scrollphathd.set_pixel(x,y_frame,brightness=0.5)
           y_frame = (y_frame + 1) % height
       scrollphathd.show()
       yield

def display_animated_bars():
    (width,height) = scrollphathd.get_shape()
    frame = -1
    started_time = time.time()
    while time.time() - started_time < 15:
       scrollphathd.clear()
       frame = frame + 1 % width
       for x in range(width//4):
           for strip in range(2):
               for y in range(height):
                   scrollphathd.set_pixel(((strip+frame)+x*width//4)%width,y,brightness=0.5)
       scrollphathd.show()
       yield

def pick_animated_random():
    anim_array = [display_animated_circle,display_animated_cosinus,display_animated_diagonals,display_animated_bars,display_animated_square]
    return random.choice(anim_array)()

def display_time():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%H:%M****%a %b %d****"), font=font5x7,brightness=0.5)
    scrollphathd.show()
    started_time = time.time()
    yield
    while time.time() - started_time < 30:
         scrollphathd.scroll()
         scrollphathd.show()
         yield

def display_temperature(temperature):
    scrollphathd.clear()
    scrollphathd.write_string("{}C".format(temperature),font=font5x7,brightness=0.5)
    scrollphathd.show()
    started_time = time.time()
    while time.time() - started_time < 15:
        yield


def pick_next_anim():
    subroutine_array = [display_time,display_temperature]
    #Première synchro ici
    (main,wind) = get_meteo()
    temperature = math.floor(main['temp'] - 273.15)
    last_synch = time.time()
    print("Synchronisation done at {}!".format(time.strftime("%H:%M")))
    while True:
        for subroutine in subroutine_array:
            if subroutine == display_temperature:
                yield display_temperature(temperature)
                #Faire la synchronisation ici
                if time.time() - last_synch > 1800:
                    (main,wind) = get_meteo()
                    temperature = math.floor(main['temp'] - 273.15)
                    last_synch = time.time()
                    print("Synchronisation done at {}!".format(time.strftime("%H:%M")))
            else:
                yield subroutine()
            yield pick_animated_random()
def main():
    scrollphathd.rotate(180)

    print("""
Overbeautiful clock

Press Ctrl+C to exit!
    """)

    scrollphathd.set_brightness(0.5)

    while True:
        subroutine_anim_picker = pick_next_anim()
        current_subroutine = next(subroutine_anim_picker)
        #current_subroutine = display_animated_square()
        time_displaying = True
        last_time_changed = math.floor(time.time())
        while True:
            time.sleep(0.05)
            try:
                next(current_subroutine)
            except StopIteration:
                current_subroutine = next(subroutine_anim_picker)
                next(current_subroutine)
if __name__ == "__main__":
    main()
