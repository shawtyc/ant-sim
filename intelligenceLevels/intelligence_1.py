# Version 2.3 Self Food Coordinate

import tkinter as tk
import random
import math
import numpy as np

def find_closest_value(lst, target):
    closest_value = lst[0]
    for value in lst:
        if abs(value - target) < abs(closest_value - target):
            closest_value = value
    return closest_value

class Ant:
    def __init__(self, canvas, x, y, size=5, speed=1):
        self.canvas = canvas
        self.x, self.y = x, y
        self.size = size
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.food = False
        self.color = 'black'
        self.knowFood = False
        self.food_coordinate = np.nan, np.nan
        
        self.ant = self.canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill=self.color
        )
        self.ant_brain()
        
    def ant_brain(self):
        # Returning to base 
        if self.food == True:
            base_x, base_y = base1.get_location()
            x_rate = random.uniform(math.pi, 2*math.pi)
            y_rate = random.uniform(math.pi/2, 3*math.pi/2)
            dx = self.speed * math.sin(x_rate)
            dy = self.speed * math.cos(y_rate)
            if abs((self.x + dx) - base_x) < abs((self.x - dx) - base_x):
                self.x += dx
            else:
                self.x -= dx

            if abs((self.y + dy) - base_y) < abs((self.y - dy) - base_y):
                self.y += dy
            else:
                self.y -= dy

        else:
            # Chemosense
            radius = 50
            food_x, food_y = food1.check_location()

            # Chemosense Area
            if abs(food_x-self.x) <= radius and abs(food_y-self.y) <= radius:
                # Activate Chemosense
                dx = self.speed * math.sin(self.direction)
                dy = self.speed * math.cos(self.direction)

                if abs((self.x + dx) - food_x) < abs((self.x - dx) - food_x):
                    self.x += dx
                else:
                    self.x -= dx

                if abs((self.y + dy) - food_y) < abs((self.y - dy) - food_y):
                    self.y += dy
                else:
                    self.y -= dy
                
                self.direction += random.uniform(-0.1, 0.1)
            
            else:
                # Food Knowledge starts here
                if self.knowFood == True:
                    self.color = 'blue'
                    dx = self.speed * math.sin(self.direction)
                    dy = self.speed * math.cos(self.direction)

                    if abs((self.x + dx) - self.food_coordinate[0]) < abs((self.x - dx) - self.food_coordinate[0]):
                        self.x += dx
                    else:
                        self.x -= dx

                    if abs((self.y + dy) - self.food_coordinate[1]) < abs((self.y - dy) - self.food_coordinate[1]):
                        self.y += dy
                    else:
                        self.y -= dy
                    
                    self.direction += random.uniform(-0.1, 0.1)

                else:
                    dx = self.speed * math.cos(self.direction)
                    dy = self.speed * math.sin(self.direction)
                    self.x += dx
                    self.y += dy
                    self.direction += random.uniform(-0.1, 0.1)

            # Food Source
            if self.x > 380 and self.y > 380 and self.x < 420 and self.y < 420:
                if self.food == False:
                    # Food is still available
                    if food1.check_value() > 0:
                        self.food = True
                        self.color = 'red'
                        self.knowFood = True
                        self.food_coordinate = food_x, food_y
                        food1.update_value()

        # Boundaries checking
        if self.x < self.size:
            self.direction = random.uniform(-math.pi/2, math.pi/2)
            self.x = self.size
        elif self.x > c_width:
            self.direction = random.uniform(math.pi, 2*math.pi)
            self.x = c_width
        if self.y < self.size:
            self.direction = random.uniform(0, math.pi)
            self.y = self.size
        elif self.y > c_height:
            self.direction = random.uniform(math.pi, 2*math.pi)
            self.y = c_height 
            
        # Base
        elif self.x > 50 and self.x < 150 and self.y > 50 and self.y < 150:
            if self.food == True:
                base1.update_value()
                self.food = False
                self.color = 'black'
            
        self.update_position()

    def update_position(self):
        self.canvas.itemconfig(self.ant, fill=self.color)
        self.canvas.coords(
            self.ant,
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        )
        
        self.canvas.after(10, self.ant_brain)
        
class AntBase:
    def __init__(self, canvas, x, y, size, value):
        self.canvas = canvas
        self.x, self.y = x, y
        self.size = size
        self.value = value
        
        self.antBase = self.canvas.create_rectangle(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill='white'
        )
        
        self.text = self.canvas.create_text(x, y, text=str(value))

    def update_value(self):
        self.value += 1 
        self.canvas.itemconfig(self.text, text=str(self.value))

    def get_location(self):
        return self.x, self.y

class FoodSource:
    def __init__(self, canvas, x, y, size, value):
        self.canvas = canvas
        self.x, self.y = x, y
        self.size = size
        self.value = value
        self.food = self.canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        )
        
        self.text = self.canvas.create_text(x, y, text = str(value))
    
    def update_value(self):
        self.value -= 1
        self.canvas.itemconfig(self.text, text=str(self.value))

    def check_value(self):
        return self.value
    
    def check_location(self):
        return self.x, self.y
        
# Canvas 
c_width = 500
c_height = 500

# Define Canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=c_width, height=c_height)
canvas.pack()

base1 = AntBase(canvas, 100, 100, 50, 0)
food1 = FoodSource(canvas, 400, 400, 20, 100)

ants = []
for i in range(50):
    ant = Ant(canvas, 100, 100)
    ants.append(ant)

root.mainloop()
