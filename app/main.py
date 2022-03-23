from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.graphics import *

import time
import math
import os

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

class StartScreen(Screen):
    pass

#Camera screen for capturing wall
class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("WALL.png")

#Wall gallery 
class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)

    #Set the default path for the gallery
    def get_default_path(self):
        self.path = os.getcwd()
        return self.path

    #Selecting images
    def selected(self, filename):
        try:    
            self.ids.my_image.source = filename[0]
        except:
            pass

class HoldsScreen(Screen):
    #Threshold for distance calculation between touch input and hold coordinates
    threshold = 50
    points = [(160,293),(68,73),(22,10),(300, 400), (20, 500), (400, 150)]

    def __init__(self, **kwargs):
        super(HoldsScreen, self).__init__(**kwargs)
        #Dictionary pairing points with canvas object
        self.holds = {}
        #Coordinates for Start and Stop holds
        self.start = None
        self.stop = None
        self.startHold = None
        self.stopHold = None

         #Delete Flag
        self.delete = False
        self.add = False

        #Flags for buttons are toggled
        self.startFlag = False
        self.stopFlag = False

        with self.canvas.before:
            self.rect = Rectangle(source="wall9.jpeg")
        self.draw_points()

    def on_pos(self, *args):
        # update Rectangle position when BetaScreen position changes
        self.rect.pos = self.pos

    def on_size(self, *args):
        # update Rectangle size when BetaScreen size changes
        self.rect.size = self.size

    #Draw points on screen
    def draw_points(self):
        with self.canvas:
            for point in self.points:
                Color(1.0, 0.0, 0.0)
                self.holds[point] = Line(circle=(point[0],point[1],5))
            
            if self.start != None:
                self.canvas.add(self.startHold)

            if self.stop != None:
                self.canvas.add(self.stopHold)

    #Clear all holds from canvas
    def clear_canvas(self):
        for hold in self.holds.values():
            self.canvas.remove(hold)
        self.holds = {}

    #Remove point/hold from Canvas, dictionary, and list of points
    def removeHold(self, point):
        self.canvas.remove(self.holds.get(point))
        del self.holds[point]
        self.points.remove(point)

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

    #Toggling the start flag on button toggle
    def toggle_start(self):
        self.startFlag = not self.startFlag
        print("Toggled Start", self.startFlag)
    
    #Toggle the stop flag on button toggle
    def toggle_stop(self):
        self.stopFlag = not self.stopFlag
        print("Toggled Stop", self.stopFlag)

    #Toggle Delete
    def toggle_delete(self):
        self.delete = not self.delete
        print("Toggled Delete", self.delete)

    #Toggle Add
    def toggle_add(self):
        self.add = not self.add
        print("Toggled Add", self.add)
    
    #Reset all hold points and start/stop selection
    def reset(self):
        self.clear_canvas()
        self.draw_points()
        self.start = None
        self.stop = None

    #Delete and select route functions
    def on_touch_down(self, touch):
        input = touch.pos
        print(input[0], input[1])

        select = self.closest(input, self.points)

        #Delete button toggled, delete point and redraw
        if self.delete and (select != None):
            self.removeHold(select)
            self.delete = False
            self.manager.get_screen("holds_screen").ids.delete_toggle.state = "normal"

        #Print Start and Stop Flag
        print(self.startFlag, self.stopFlag)

        #Selecting start and stop points
        if (self.startFlag == True and self.stopFlag == False):
            #Select start as point closest to selection within threshold
            self.start = self.closest(input, self.points)
            print("Selected start:", self.start)
            
            #Change colour of start hold
            if self.start != None:
                with self.canvas:
                    Color(0, 1.0, 0)
                    self.startHold = Line(circle=(self.start[0],self.start[1],5))
                
                #Reset Toggle
                self.startFlag = False
                self.manager.get_screen("holds_screen").ids.start_toggle.state = "normal"
            
        elif (self.startFlag == False and self.stopFlag == True):
            self.stop = self.closest(input, self.points)
            print("Selected stop:", self.stop)
            
            #Change colour of stop hold
            if self.stop != None:
                with self.canvas:
                    Color(0, 0.0, 1.0)
                    self.holds[input] = Line(circle=(self.stop[0],self.stop[1],5))
                
                #Reset Toggle
                self.stopFlag = False
                self.manager.get_screen("holds_screen").ids.stop_toggle.state = "normal"
                

        #Adding hold based on user input
        if self.add:
            self.points.append(input)
            print(self.points)
            with self.canvas:
                Color(1.0, 0.0, 0.0)
                self.holds[input] = Line(circle=(input[0],input[1],5))
            
            #Reset toggle
            self.add = False
            self.manager.get_screen("holds_screen").ids.add_toggle.state = "normal"

        #Overwrite method by returning the method of the super class
        return super(HoldsScreen, self).on_touch_down(touch)

class BetaScreen(Screen):
    #Threshold for distance calculation between touch input and hold coordinates
    threshold = 50

    #Points for Holds
    points = [(160,293),(68,73),(22,10),(300, 400), (20, 500), (400, 150)]
    
    def __init__(self, **kwargs):
        super(BetaScreen, self).__init__(**kwargs)
        #Add background image of wall
        with self.canvas.before:
            self.rect = Rectangle(source="WALL.PNG")
        self.draw_points()

    def on_pos(self, *args):
        # update Rectangle position when BetaScreen position changes
        self.rect.pos = self.pos

    def on_size(self, *args):
        # update Rectangle size when BetaScreen size changes
        self.rect.size = self.size

    def draw_points(self):
        with self.canvas:
            #Draw points on screen
            for point in self.points:
                Color(1.0, 0.0, 0.0)
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

    #Touch Input from User
    def on_touch_down(self, touch):
        #Get touch coordinates as tuple
        input = touch.pos
        print(input)
        return super(BetaScreen, self).on_touch_down(touch)

#Screen for instructions
class StepsScreen(Screen):
    def __init__(self, **kwargs):
        self.stepNum = 1
        super(StepsScreen, self).__init__(**kwargs)
    
    #display next/previous step and description
    def update(self, n):
        #Update step number
        if n == 1:
            self.stepNum = self.stepNum + 1
        elif n == -1 and self.stepNum > 1:
            self.stepNum = self.stepNum - 1

        #Update figure and description for step
        self.ids.my_image.source = "WALL" + str(self.stepNum) + ".png"
        self.ids.instructions.text = "Step" + str(self.stepNum)


#Load GUI defined by kv file
GUI = Builder.load_file("main.kv")

class captureWallApp(App):
    def build(self):
        return GUI

captureWallApp().run()