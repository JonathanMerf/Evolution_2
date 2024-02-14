# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 16:43:51 2022

@author: jonat
"""
import numpy as np 
import random as rand 
from matplotlib import pyplot as plt 


class world(object): 
    def __init__(self, width, height, population):
        self.width = width 
        self.height = height 
        self.cell_list = [] 
        #self.cell_list.append(cell(20,20,2,2,2,25,25,-.9,0,50))
        for i in range(population): 
            x = rand.randint(-7071067811865475,7071067811865475)/10000000000000000
            y = rand.randint(-7071067811865475,7071067811865475)/10000000000000000 
            val = 0.7071067811865475
            x_final = x*val+y*val 
            y_final = -1*x*val+y*val
            self.cell_list.append(cell(20,20,2,2,2,rand.randint(0,self.width-1)+ rand.triangular(-.5,.5),rand.randint(0,self.height-1)+ rand.triangular(-.5,.5),x_final,y_final,20))
        self.chemical = np.ndarray((width,height), dtype=float)
        for i in range(width): 
            for j in range(height): 
                self.chemical[i,j] = (rand.randint(0,1000)/100)
        self.light = np.ndarray((width,height), dtype=float) 
        for i in range(width): 
            for j in range(height): 
                self.light[i,j] = (rand.randint(0,1000)/100)
        self.corpse_list = []
#        for i in range(round(population/5)): 
#            self.corpse_list.append(corpse(rand.randint(0,self.width-1), rand.randint(0,self.height-1), 3))    
        self.new_cells = [] 
        self.new_corpses = [] 
        
        self.day_count = 0 
        self.hp_max_list = [] 
        self.energy_max_list = [] 
        self.strength_list = [] 
        self.speed_list = [] 
        self.sense_list = []
        self.lifespan_list = [] 
        self.day_list = [] 
        self.cell_pop_list = []
        self.corpse_pop_list = []
    def display_world(self): 
        x_cell = [] 
        y_cell = [] 
        x_corpse = [] 
        y_corpse = [] 
        x_trophe = [] 
        y_trophe = [] 
        for i in self.cell_list:
            x_cell.append(i.position[0])
            y_cell.append(i.position[1])
            x_trophe.append(i.energy_pref[0])
            y_trophe.append(i.energy_pref[1])
        for i in self.corpse_list: 
            x_corpse.append(i.position[0])
            y_corpse.append(i.position[1])
        plt.close() 
        fig, (ax1) = plt.subplots(2, 3)
        ax1[0,0].set_title("Light")
        ax1[0,0].imshow(np.rot90(self.light,1))
        ax1[0,1].set_title("Chemical")
        ax1[0,1].imshow(np.rot90(self.chemical,1))
        ax1[1,0].set_title("Positions")
        ax1[1,0].scatter(x_corpse, y_corpse, 1, color = 'red')
        ax1[1,0].scatter(x_cell, y_cell, 1, color = 'green')
        ax1[1,0].set(xlim=[0,self.width],ylim=[0,self.height])
        ax1[1,1].set_title("Metabolic Preference")
        ax1[1,1].scatter(x_trophe, y_trophe, 1, color = 'blue')
        ax1[1,1].set(xlim=[-1,1], ylim=[-1,1])
        ax1[0,2].set_title("Population")
        ax1[0,2].plot(self.day_list, self.corpse_pop_list, color = "red")
        ax1[0,2].plot(self.day_list, self.cell_pop_list, color = "green")
        ax1[1,2].set_title("Stats")
        ax1[1,2].plot(self.day_list, self.hp_max_list, color = "green")
        ax1[1,2].plot(self.day_list, self.energy_max_list, color = "blue")
        ax1[1,2].plot(self.day_list, self.strength_list, color = "red")
        ax1[1,2].plot(self.day_list, self.speed_list, color = "cyan")
        ax1[1,2].plot(self.day_list, self.sense_list, color = "magenta")
        fig.tight_layout()
        plt.show()
    def day(self): 
        hp_max_list = [] 
        energy_max_list = [] 
        strength_list = [] 
        speed_list = [] 
        sense_list = [] 
        lifespan_list = [] 
        self.cell_pop_list.append(len(self.cell_list))
        self.corpse_pop_list.append(len(self.corpse_list))
        for i in self.cell_list: 
            hp_max_list.append(i.hp_max)
            energy_max_list.append(i.energy_max)
            strength_list.append(i.strength)
            speed_list.append(i.speed)
            sense_list.append(i.sense)
            lifespan_list.append(i.lifespan)
        if len(hp_max_list) > 0: 
            self.hp_max_list.append(np.mean(hp_max_list))
        if len(energy_max_list) > 0: 
            self.energy_max_list.append(np.mean(energy_max_list))
        if len(strength_list) > 0: 
            self.strength_list.append(np.mean(strength_list))
        if len(speed_list) > 0: 
            self.speed_list.append(np.mean(speed_list))
        if len(sense_list) > 0: 
            self.sense_list.append(np.mean(speed_list))
        if len(lifespan_list) > 0: 
            self.lifespan_list.append(np.mean(lifespan_list))
        self.day_list.append(self.day_count)
        self.day_count = self.day_count + 1 

class cell(object): 
    def __init__(self, hp_max, energy_max, strength, speed, sense, x, y, trophe_x, trophe_y, lifespan): 
        self.age = 0 
        self.hp = hp_max
        self.hp_max = hp_max 
        self.lifespan = lifespan 
        self.speed = speed 
        self.strength = strength                                        #mass
        self.energy = energy_max 
        self.energy_max = energy_max 
        self.sense = sense
        self.position = [x,y]  
        self.energy_pref = (trophe_x, trophe_y)                   #(x,y)
        self.meta_eff = (5**(abs(trophe_x)-1), 5**(abs(trophe_y)-1))    #z=f(x,y) 
    def turn(self,world):
        if (self.energy_pref[0] > abs(self.energy_pref[1])) and (self.energy_pref[0] > 0): 
            close = self.find_cell(world)
            if (np.sqrt(close.position[0] - self.position[0])**2 + (close.position[1] - self.position[1])**2) <= self.speed: 
                self.position = close.position
            else: 
                if close.position[0]-self.position[0] != 0: 
                    direction = np.arctan((close.position[1] - self.position[1])/(close.position[0] - self.position[0]))
                else: 
                    if close.position[1] > self.position[1]: 
                        direction = np.pi/2
                    else: 
                        direction = -1*np.pi/2
                if close.position[0] < self.position[0]: 
                    direction = direction + np.pi 
                dist = self.speed 
                self.position[0] = self.position[0] + dist*np.cos(direction) + rand.triangular(-.5,.5)          
                self.position[1] = self.position[1] + dist*np.sin(direction) + rand.triangular(-.5,.5)
            self.attack(world)
        if (abs(self.energy_pref[1]) > abs(self.energy_pref[0])) and (self.energy_pref[1] < 0): 
            if len(world.corpse_list) > 0:
                close = self.find_corpse(world)
                if (np.sqrt(close.position[0] - self.position[0])**2 + (close.position[1] - self.position[1])**2) <= self.speed: 
                    self.position = close.position
                else: 
                    if close.position[0]-self.position[0] != 0: 
                        direction = np.arctan((close.position[1] - self.position[1])/(close.position[0] - self.position[0]))
                    else: 
                        if close[1] > self.position[1]: 
                            direction = np.pi/2
                        else: 
                            direction = -1*np.pi/2
                    if close.position[0] < self.position[0]: 
                        direction = direction + np.pi 
                    dist = self.speed 
                    self.position[0] = self.position[0] + dist*np.cos(direction) + rand.triangular(-.5,.5)           
                    self.position[1] = self.position[1] + dist*np.sin(direction) + rand.triangular(-.5,.5)
                self.scavange(world)
            else: 
                direction = rand.random()*360
                dist = rand.random()*self.speed 
                self.position[0] = self.position[0] + dist*np.cos(direction/(2*np.pi))
                self.position[1] = self.position[1] + dist*np.sin(direction/(2*np.pi)) 
        if (self.energy_pref[1] > abs(self.energy_pref[0])) and (self.energy_pref[1] > 0): 
            close = self.find_light(world)
            if (np.sqrt(close[0] - self.position[0])**2 + (close[1] - self.position[1])**2) <= self.speed: 
                self.position = close
            else: 
                if close[0]-self.position[0] != 0: 
                    direction = np.arctan((close[1] - self.position[1])/(close[0] - self.position[0]))
                else: 
                    if close[1] > self.position[1]: 
                        direction = np.pi/2
                    else: 
                        direction = -1*np.pi/2
                if close[0] < self.position[0]: 
                    direction = direction + np.pi 
                dist = self.speed 
                self.position[0] = self.position[0] + dist*np.cos(direction)  + rand.triangular(-.5,.5)          
                self.position[1] = self.position[1] + dist*np.sin(direction) + rand.triangular(-.5,.5)
            self.photosynthesize(world)
        if (abs(self.energy_pref[0]) > abs(self.energy_pref[1])) and (self.energy_pref[0] < 0) : 
            close = self.find_chemical(world)
            if (np.sqrt(close[0] - self.position[0])**2 + (close[1] - self.position[1])**2) <= self.speed: 
                self.position = close
            else: 
                if close[0]-self.position[0] != 0: 
                    direction = np.arctan((close[1] - self.position[1])/(close[0] - self.position[0]))
                else: 
                    if close[1] > self.position[1]: 
                        direction = np.pi/2
                    else: 
                        direction = -1*np.pi/2
                if close[0] < self.position[0]: 
                    direction = direction + np.pi 
                dist = self.speed 
                self.position[0] = self.position[0] + dist*np.cos(direction) + rand.triangular(-.5,.5)           
                self.position[1] = self.position[1] + dist*np.sin(direction) + rand.triangular(-.5,.5)
            self.chemosynthesize(world)
    def aging(self): 
        self.age = self.age + 1  
    def death(self,world): 
        world.new_corpses.append(corpse(self.position[0],self.position[1],self.strength*.5))
        if not(self.hp > self.hp_max*2 and self.energy >= self.energy_max/2):
            world.cell_list.remove(self)
    def use_energy(self, energy):
        self.energy = self.energy - energy 
    def find_cell(self,world) :                     #closest cell 
        closest = world.cell_list[0]   
        base_dist = self.sense
        for i in world.cell_list: 
            dist = np.sqrt(i.position[0] - self.position[0])**2 + (i.position[1] - self.position[1])**2
            if (dist <= base_dist and i != self): 
                closest = i
                base_dist = dist 
        return closest 
    def find_light(self,world):
        brightest = 0
        bright_pos = [self.position[0],self.position[1]]
        x_max = self.position[0]+self.speed
        x_min = self.position[0]-self.speed
        y_max = self.position[1]+self.speed
        y_min = self.position[1]-self.speed
        if x_max > world.width: 
            x_max = world.width-1 
        if x_min < 0: 
            x_min = 0 
        if y_max > world.height: 
            y_max = world.height-1 
        if y_min < 0: 
            y_min = 0 
        for i in range(round(x_min),round(x_max)): 
            for j in range(round(y_min),round(y_max)):
                dist = np.sqrt(((i-self.position[0])**2)+((j-self.position[1])**2))
                if dist <= self.speed : 
                    if world.light[i][j] > brightest : 
                        bright_pos[0] = i 
                        bright_pos[1] = j 
                        brightest = world.light[i][j]
        return bright_pos 
    def find_chemical(self,world): 
        chemicalest = 0
        chemical_pos = [self.position[0],self.position[1]]
        x_max = self.position[0]+self.sense
        x_min = self.position[0]-self.sense
        y_max = self.position[1]+self.sense
        y_min = self.position[1]-self.sense
        if x_max > world.width: 
            x_max = world.width-1 
        if x_min < 0: 
            x_min = 0 
        if y_max > world.height: 
            y_max = world.height-1 
        if y_min < 0: 
            y_min = 0 
        for i in range(round(x_min),round(x_max)): 
            for j in range(round(y_min),round(y_max)):
                dist = np.sqrt(((i-self.position[0])**2)+((j-self.position[1])**2))
                if dist <= self.speed : 
                    if world.chemical[i][j] > chemicalest : 
                        chemical_pos[0] = i 
                        chemical_pos[1] = j 
                        chemicalest = world.chemical[i][j]
        return chemical_pos  
    def find_corpse(self,world):                    #closest corpse
        closest = world.corpse_list[0]   
        base_dist = self.sense
        for i in world.corpse_list: 
            dist = np.sqrt(i.position[0] - self.position[0])**2 + (i.position[1] - self.position[1])**2
            if (dist <= base_dist): 
                closest = i
                base_dist = dist 
        return closest  
    def exaustion(self): 
        if self.energy <= 0:                                #exaustion
            self.hp = self.hp - 1 
        if self.hp_max < 2:                               #weakness
            self.hp = self.hp - 1  
    def photosynthesize(self, world):
        if (self.position[0] <= world.width and self.position[1] <=world.height):
            self.energy = self.energy + (world.light[round(self.position[0])-1,round(self.position[1])-1]*self.meta_eff[1])
            if self.energy > self.energy_max : 
                extra = self.energy - self.energy_max
                self.energy = self.energy_max
                self.hp = self.hp + extra
        
    def chemosynthesize(self, world): 
        if (self.position[0] <= world.width and self.position[1] <=world.height):
            self.energy = self.energy + (world.chemical[round(self.position[0])-1,round(self.position[1])-1]*self.meta_eff[0])
            if self.energy > self.energy_max : 
                extra = self.energy - self.energy_max
                self.energy = self.energy_max
                self.hp = self.hp + extra
    def attack(self,world): 
        close = self.find_cell(world)
        close.hp = close.hp - self.strength 
        self.energy = self.energy + self.strength*self.meta_eff[0]
        if self.energy > self.energy_max : 
            extra = self.energy - self.energy_max
            self.energy = self.energy_max
            self.hp = self.hp + extra
        if close.hp <= 0: 
            close.death(world)
    def scavange(self,world): 
        close = self.find_corpse(world)
        close.mass = close.mass - self.strength 
        self.energy = self.energy + self.strength*self.meta_eff[0]
        if self.energy > self.energy_max : 
            extra = self.energy - self.energy_max
            self.energy = self.energy_max
            self.hp = self.hp + extra
        if close.mass <= 0: 
            close.remove_corpse(world)
    def reproduce(self, world): 
        if self.hp > self.hp_max*2 and self.energy >= self.energy_max/2: 
            for i in range(2):
                mod_list = [0,0,0,0,0,0,0,0,0,0]
                mod_list[0] = rand.triangular(-1,1)
                mod_list[1] = rand.triangular(-1,1)
                mod_list[2] = rand.triangular(-1,1)
                mod_list[3] = rand.triangular(-1,1)
                mod_list[4] = rand.triangular(-1,1)
                mod_list[5] = rand.triangular(-1,1)
                mod_list[6] = rand.triangular(-1,1)
                mod_list[7] = rand.triangular(-.1,.1)#
                mod_list[8] = rand.triangular(-.1,.1)#
                mod_list[9] = rand.triangular(-1,1)
                x_final = self.energy_pref[0]
                y_final = self.energy_pref[1]
                val = 0.7071067811865475 
                x = (x_final/(2*val)) - (y_final/(2*val))
                y = (y_final/(2*val)) + (x_final/(2*val))
                final_x = x + mod_list[7]
                final_y = y + mod_list[8]
                while (final_x >= val and final_x <= -1*val) or (final_y >= val and final_y <= -1*val): 
                    mod_list[7] = rand.triangular(-.1,.1)
                    mod_list[8] = rand.triangular(-.1,.1)
                    final_x = x + mod_list[7]
                    final_y = y + mod_list[8]
                mod_x = x_final*val+y_final*val 
                mod_y = -1*x_final*val+y_final*val
                world.new_cells.append(cell(self.hp_max+mod_list[0], self.energy_max+mod_list[1], self.strength+mod_list[2], self.speed+mod_list[3], self.sense+mod_list[4], self.position[0]+mod_list[5], self.position[1]+mod_list[6], mod_x, mod_y, self.lifespan+mod_list[9] ))
                
    def day(self,world): 
        self.turn(world)
        self.use_energy(.5*self.strength*self.speed*self.speed)
        self.exaustion() 
        self.reproduce(world)
        self.aging()
        if (self.age > self.lifespan or self.hp <= 0 or (self.hp > self.hp_max*2 and self.energy >= self.energy_max/2)): 
            self.death(world)
    
class corpse(object): 
    def __init__(self, x, y, mass): 
        self.position = [x,y]
        self.mass = mass 
    def remove_corpse(self,world): 
        world.corpse_list.remove(self)
    def decay(self,world): 
        self.mass = self.mass - 1 
        world.chemical[round(self.position[0])-1,round(self.position[1])-1] = world.chemical[round(self.position[0])-1,round(self.position[1])-1] + 1
        if self.mass <= 0: 
            self.remove_corpse(world)
            
erebor = world(50,50,50)

def time(world,days): 
    rand.shuffle(world.cell_list)
    for i in world.cell_list: 
        i.day(world)
    for i in world.corpse_list: 
        i.decay(world)
    for i in world.new_cells: 
        world.cell_list.append(i)
    world.new_cells = [] 
    for i in world.new_corpses: 
        world.corpse_list.append(i)
    world.new_corpses = [] 
    world.day()
    world.display_world()
        