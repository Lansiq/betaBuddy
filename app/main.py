from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.graphics import *

import time
import math

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

class StartScreen(Screen):
    pass

class HoldsScreen(Screen):
    #Threshold for distance calculation between touch input and hold coordinates
    threshold = 50

    #Delete Flag
    delete = False

    points = [(160,293),(68,73),(22,10),(300, 400), (20, 500), (400, 150)]

    def __init__(self, **kwargs):
        super(HoldsScreen, self).__init__(**kwargs)
        self.draw_points()

    def draw_points(self):
        #Draw points on screen
        with self.canvas:
            self.canvas.clear()
            for point in self.points:
                Color(1.0, 0, 0)
                Line(circle=(point[0],point[1],5))

    #Calculate distance between two points
    def distance(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2
        dist = math.sqrt(dist)
        return dist
    
    #Find closest point to given point P1 and list of points
    def closest(self, p1, points):
        min_dist = self.distance(p1, points[0])
        closest_p = None

        for point in points:
            dist = self.distance(p1, point)
            if (dist <= self.threshold) and (dist <= min_dist):
                min_dist = dist
                closest_p = point
        return closest_p

    #Toggle Delete
    def toggle_delete(self):
        self.delete = not self.delete
        print("Toggled Delete")

    #Delete and select route functions
    def on_touch_down(self, touch):
        input = touch.pos
        print(input)

        select = self.closest(input, self.points)

        #Delete toggled, delete point and redraw
        if self.delete and (select != None):
            self.points.remove(select)
            self.draw_points()

        #Overwrite method by returning the method of the super class
        return super(HoldsScreen, self).on_touch_down(touch)

class BetaScreen(Screen):
    #Threshold for distance calculation between touch input and hold coordinates
    threshold = 50

    #Flags for buttons are toggled
    startFlag = False
    stopFlag = False

    #Coordinates for Start and Stop holds
    start = None
    stop = None

    #Points for Holds
    points = [(160,293),(68,73),(22,10),(300, 400), (20, 500), (400, 150)]
    
    def __init__(self, **kwargs):
        super(BetaScreen, self).__init__(**kwargs)
        self.draw_points()

    def draw_points(self):
        #Draw points on screen
        with self.canvas:
            for point in self.points:
                Color(1.0, 0, 0)
                Line(circle=(point[0],point[1],5))
    
    #Toggling the start flag on button toggle
    def toggle_start(self):
        self.startFlag = not self.startFlag
        print("Toggled Start", self.startFlag)
    
    #Toggle the stop flag on button toggle
    def toggle_stop(self):
        self.stopFlag = not self.stopFlag
        print("Toggled Stop", self.stopFlag)

    #Calculate distance between two points
    def distance(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2
        dist = math.sqrt(dist)
        return dist
    
    #Find closest point to given point P1 and list of points
    def closest(self, p1, points):
        min_dist = self.distance(p1, points[0])
        closest_p = None

        for point in points:
            dist = self.distance(p1, point)
            if (dist <= self.threshold) and (dist <= min_dist):
                min_dist = dist
                closest_p = point
        return closest_p

    #Touch Input from User
    def on_touch_down(self, touch):
        #Get touch coordinates as tuple
        input = touch.pos
        print(input)

        #Print Start and Stop Flag
        print(self.startFlag, self.stopFlag)

        #Selecting start and stop points
        if (self.startFlag == True and self.stopFlag == False):
            self.start = self.closest(input, self.points)
            print("Selected start:", self.start)
            
            #Change colour of start hold
            if self.start != None:
                with self.canvas:
                    Color(0, 1.0, 0)
                    Line(circle=(self.start[0],self.start[1],5))
            
        elif (self.startFlag == False and self.stopFlag == True):
            self.stop = self.closest(input, self.points)
            print("Selected stop:", self.stop)
            
            #Change colour of stop hold
            if self.stop != None:
                with self.canvas:
                    Color(0, 1.0, 0)
                    Line(circle=(self.stop[0],self.stop[1],5))
            
        return super(BetaScreen, self).on_touch_down(touch)

    #Reset all hold points and start/stop selection
    def reset(self):
        self.draw_points()
        self.start = None
        self.stop = None

class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("WALL.png")

#Load GUI defined by kv file
GUI = Builder.load_file("main.kv")

class captureWallApp(App):
    def build(self):
        return GUI

captureWallApp().run()