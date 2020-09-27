#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import tkinter as tk
from tkinter import *
# from threading import Thread
import time
import math

grav_constant = 6.67 * 1e-11


# In[2]:


class space:

    #   ------------------------------클래스 변수
    
    #   단위 시간
    dt = 5000
    #   비율
    r_scale = 1e-9
    #   반발게수 *
    e = 1
    def __init__(self, width = 2400, height = 1200):
        #   폭, 높이
        self.WIDTH = width
        self.HEIGHT = height
        #   원점위치(좌하단 기준 떨어진 정도)
        self.o_x = self.WIDTH/2
        self.o_y = self.HEIGHT - self.HEIGHT/2
        # 시간
        time = 0
        
        #tkinter 창 생성 및 window 기본 세팅
        self.window = Tk()
        self.window.title("만유인력")
        self.window.geometry("{}x{}+100+100".format(self.WIDTH, self.HEIGHT+30))
        self.window.resizable(True,True)
        
        #canvas생성 및 배치
        self.canvas = Canvas(self.window, width = self.WIDTH, height = self.HEIGHT)
        self.canvas.place(x = 0, y = 0, width = self.WIDTH, height = self.HEIGHT)
        
        #원점 중앙 선
        self.canvas.create_line(0, self.o_y, self.WIDTH, self.o_y)
        self.canvas.create_line(self.o_x, 0, self.o_x, self.HEIGHT)
        
        #좌표표시
        self.sun_L = Label(self.window, text = "sun", font = "TkDefaultFont 10 bold")
        self.sun_E = Entry(self.window)
        self.earth_L = Label(self.window, text = "earth", font = "TkDefaultFont 10 bold")
        self.earth_E = Entry(self.window)
        self.sun_L.place(x = 800, y = self.HEIGHT, width = 50, height = 30)
        self.sun_E.place(x = 870, y = self.HEIGHT, width = 150, height = 30)
        self.earth_L.place(x = 1000, y = self.HEIGHT, width = 50, height = 30)
        self.earth_E.place(x = 1070, y = self.HEIGHT, width = 250, height = 30)
        
        self.main()
        
    def main(self):
        global grav_constant
        sun = planet(self, 0, 0, 2e30,20,"The Sun", color = "red")
        earth = planet(self, 15e10, 0, 6e24, 6, "The Earth",dot = True, color = "blue")
        mercury = planet(self, 0, 5.8e10, 3e23, 4, "Mercury", dot=True, color = "grey")
        venus = planet(self, 0, 10.8e10, 5e24, 4,"Venus",dot = True, color = "yellow")
        mars = planet(self, -22.7e10, 0, 6.5e23, 4, "Mars",dot = True, color = "orange")
        jupiter = planet(self,-70e10, 0, 1.8e27, 10,"Jupiter",dot = True, color = "pink")
#         saturn = planet(self, 14e11, 0, 5.6e26, 8, "Saturn", dot = True, color = "brown")

        distance = math.sqrt((sun.x - earth.x)**2 + (sun.y - earth.y)**2)
        earth.set_spd(0,math.sqrt(grav_constant * sun.mass / distance))
#         earth.set_spd(0,math.sqrt(333333)*1e5)
        distance = math.sqrt((sun.x - mercury.x)**2 + (sun.y - mercury.y)**2)
        mercury.set_spd(-math.sqrt(grav_constant * sun.mass / distance),0)

        distance = math.sqrt((sun.x - venus.x)**2 + (sun.y - venus.y)**2)
        venus.set_spd(-math.sqrt(grav_constant * sun.mass / distance),0)
        
        distance = math.sqrt((sun.x - mars.x)**2 + (sun.y - earth.y)**2)
        mars.set_spd(0,-math.sqrt(grav_constant * sun.mass / distance))
        
        distance = math.sqrt((sun.x - jupiter.x)**2 + (sun.y - jupiter.y)**2)
        jupiter.set_spd(0,-math.sqrt(grav_constant * sun.mass / distance))
        
#         distance = math.sqrt((sun.x - saturn.x)**2 + (sun.y - saturn.y)**2)
#         saturn.set_spd(0, math.sqrt(grav_constant * sun.mass / distance))
        self.loop()
        
    def loop(self):
        while True:
            
            for p in planet.list:
                for target in planet.list:
                    if(p!=target):
                        p.accel(gravity(p, target))
                        
                p.move()
            self.sun_E.delete(0,END)
            self.earth_E.delete(0,END)
            self.sun_E.insert(0, "(%.3f, %.3f)" % (planet.list[0].x, planet.list[0].y))
            self.earth_E.insert(0, "(%.3f, %.3f)" % (planet.list[1].x, planet.list[1].y))
#             time.sleep(0.1)
            self.window.update()


# In[3]:


class force:#힘 클래스
    def __init__(self):
        self.x = 0#x성분
        self.y = 0#y성분
        self.total = 0#합력
        self.dir = 0#방향
        
    def sum_force(self, total, dir):#합력과 방향으로 주어지는 힘
        self.total = total
        self.dir = dir
        self.x = total * math.cos(dir)
        self.y = total * math.sin(dir)
        
    def sep_force(self, x, y):#x와 y성분으로 분해되어 주어지는 힘
        self.x = x
        self.y = y
        self.total = math.sqrt(x**2 + y**2)
        try:
            self.dir = math.atan(y/x)
        except ZeroDivisionError:
            if(y>0):
                self.dir = math.atan(math.inf)
            else:
                self.dir = math.atan(-math.inf)
        

class gravity(force):#중력(만유인력)의 값을 반환하는 힘의 자식클래스
    def __init__(self, planet, target):
        global grav_constant
        super().__init__()
        distance = math.sqrt((planet.x - target.x)**2 + (planet.y - target.y)**2)
        try:
            direction = math.atan((planet.y-target.y)/(planet.x-target.x))#planet과 target의 각도 radian값
            if(planet.x-target.x>0):
                direction += math.pi
        except ZeroDivisionError:
            direction = math.atan(math.inf)
        
        self.sum_force(grav_constant * planet.mass * target.mass / distance **2, direction)


# In[4]:


class planet:
    NAME = "planet"
    list = []
    color_list = ["yellow","green","blue","red","orange","pink","grey","violet"]
    
    def __init__(self, space, x = 0, y = 0, mass = 1, size = 10, name = NAME, visible = True, dot = False, color = "red"):
        self.space = space
        self.canvas = space.canvas
        self.name = name
        #좌표
        self.x = x
        self.y = y
        self.org_x = x#원위치 좌표
        self.org_y = y
        #tkinter 상에 그려질 좌표
        self.x_pos = self.space.o_x+x*self.space.r_scale
        self.y_pos = self.space.o_y-y*self.space.r_scale
        #질량
        self.mass = mass
        
        self.size = size
        self.half_size = size/2
        #속도
        self.spdx = 0
        self.spdy = 0
        #가속도
        self.accx = 0
        self.accy = 0
        
        self.color = color
        self.dot_list=[]
        
        self.visible = visible
        if(self.visible):
            self.id = self.canvas.create_oval(self.x_pos-self.half_size, self.y_pos - self.half_size,
                                          self.x_pos + self.half_size, self.y_pos+self.half_size, fill = self.color)
        self.dot = dot
        self.freq = 0
        
        self.list.append(self)
        
    def set_spd(self,x,y):
        self.spdx = x
        self.spdy = y
        
    def accel(self,force):
        dt = self.space.dt
        self.accx = force.x / self.mass
        self.accy = force.y / self.mass
        self.spdx += self.accx * dt
        self.spdy += self.accy * dt
        
    def move(self):
        dt = self.space.dt
        r_scale = self.space.r_scale
        
        if(self.dot and self.freq % 200==0):
            color = len(self.dot_list) % (len(self.color_list))
            self.dot_list.append(self.canvas.create_oval(self.x_pos-1, self.y_pos - 1,
                                          self.x_pos + 1, self.y_pos + 1, fill = self.color_list[color]))
        self.freq+=1
        movement_x = (self.spdx * dt + self.accx / 2 * dt ** 2)
        movement_y = (self.spdy * dt + self.accy / 2 * dt ** 2)
        
        self.canvas.after(25,self.canvas.delete, self.canvas.create_text(self.x_pos, 
                                                                          self.y_pos, text = self.name, anchor = 'sw'))#이름표시
        self.canvas.move(self.id, movement_x * r_scale, -movement_y * r_scale)#이동
        self.x_pos += movement_x * r_scale
        self.y_pos -= movement_y * r_scale
        self.x += movement_x
        self.y += movement_y
        


# In[5]:


main = space()


# In[ ]:




