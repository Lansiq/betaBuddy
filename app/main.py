from ctypes.wintypes import LPDWORD, LPSC_HANDLE
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.graphics import *
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label

import time
import math
import os, sys

'''
betaFile = os.path.realpath(os.path.join(os.path.dirname(__file__),'..','Beta Code'))
sys.path.insert(0, betaFile)
import BetaBuddy_TwoPaths_cos as beta
'''

cvFile = os.path.realpath(os.path.join(os.path.dirname(__file__),'..','Wall Factors'))
sys.path.insert(0, cvFile)
import util as cv

cvFile2 = os.path.realpath(os.path.join(os.path.dirname(__file__),'..','Dominik CV'))
sys.path.insert(0, cvFile2)
import CV_Functions as domCV

store = JsonStore('settings.json')

appWidth = 480
appHeight = 640

Config.set('graphics', 'width', str(appWidth))
Config.set('graphics', 'height', str(appHeight))

class WindowManager(ScreenManager):
    image_source = StringProperty()

    def selected(self, filename):
        try:
            self.image_source = filename[0]
        except:
            pass
    
#Start Up Screen
class StartScreen(Screen):
    pass

#User Settings Screen (height, weight, etc.)
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    #If settings exist before, use previous entered values
    def on_enter(self):
        if store.exists('settings'):
            self.height = store.get('settings')['ht']
            self.weight = store.get('settings')['wt']

            self.manager.get_screen("settings_screen").ids.height.text = str(self.height)
            self.manager.get_screen("settings_screen").ids.weight.text = str(self.weight)

    #Save settings locally
    def save(self):
        height = self.ids.height.text
        weight = self.ids.weight.text
        
        store.put('settings', ht = height, wt = weight)

#Camera screen for capturing wall
class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("WALL.png")

#Use device's files to select photo of wall
class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)

    #Set the default path for the gallery
    def get_default_path(self):
        self.path = os.getcwd()
        return self.path

#Display the wall photo with the identified holds (can add, delete, select route)
class HoldsScreen(Screen):
    def __init__(self, **kwargs):
        super(HoldsScreen, self).__init__(**kwargs)
        #Dictionary pairing points (coordinate tuple) with canvas object
        self.holdObj = {}
        
        #Add/Delete Flag
        self.delete = False
        self.add = False
        self.selectFlag = False

    def on_enter(self):
        #Get background image as selected from gallery screen
        image = self.manager.get_screen("gallery_screen").ids.my_image.source

        #CV Wall with image input
        cvWall = cv.inputImageFile(image)

        #Output from Dom's Function
        self.holdList = domCV.CV(image)[1]
        print(self.holdList)

        #Creating dictionary that separates routes by colour {colour: [[[x1,y1], ID1], [[x2,y2],ID2]} 
        routes = {} 
        for holdInfo in self.holdList:
            if holdInfo[1] in routes.keys():
               routes[holdInfo[1]].append([holdInfo[0],holdInfo[2]])
            else:
                routes[holdInfo[1]] = [[holdInfo[0],holdInfo[2]]]      

        self.appRoutes = routes.copy()
        self.extractCoords(routes, cvWall)

        #Self.holds is a holdList but in app coordinates
        self.holds = []
        for colour in self.appRoutes:
            #Add coordinates and hold IDs to list
            for holdInfo in self.appRoutes[colour]:
                print(holdInfo)
                self.holds.append([tuple(holdInfo[0]), colour, holdInfo[1]])

        #Save original set of points for reset button
        self.origHolds = self.holds.copy()
        
        self.draw_points(self.holds)

    #Convert coordinates into app system
    def extractCoords(self, routes, cvWall):
        
        
        #Loop through keys and convert coordinates into app system
        for colour in routes:
            coordList = []
            
            #Loop through the coordinates in a given route color
            for holdInfo in routes[colour]:
                print(holdInfo[0])
                coordList.append(holdInfo[0])
            print(coordList)
            #Convert coordinates to app system
            appCoords = cv.cvCoordsToAppCoords(coordList,cvWall,appHeight,appWidth)
            
            #Replace old coordintes with converted coordinates
            i = 0
            for coords in appCoords:
                self.appRoutes[colour][i][0] = coords
                i = i + 1

    #Draw points on the holds screen
    def draw_points(self, holds):
        with self.canvas:
            for hold in holds:
                Color(1.0, 0.0, 0.0)
                #Change to this after
                self.holdObj[hold[0]] = Line(circle=(hold[0][0],hold[0][1],5))

    #Calculate distance between two points
    def distance(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2
        dist = math.sqrt(dist)
        return dist
    
    #Find closest point (tuple) to given point P1 and list of points
    def closest(self, p1, holds):
        #Threshold for distance calculation between touch input and hold coordinates
        threshold = 40
        min_dist = self.distance(p1, holds[0][0])
        closest_p = None

        #Find if closest point in list of points
        for hold in holds:
            dist = self.distance(p1, hold[0])
            if (dist <= threshold) and (dist <= min_dist):
                min_dist = dist
                closest_p = hold
        return closest_p

    #Toggle Delete
    def toggle_delete(self):
        self.delete = not self.delete
        print("Toggled Delete", self.delete)

    #Toggle Add
    def toggle_add(self):
        self.add = not self.add
        print("Toggled Add", self.add)

    #Toggle the select flag on button toggle
    def toggle_select(self):
        self.selectFlag = not self.selectFlag
        print("Toggled Select", self.selectFlag)
    
    #Reset all hold points and start/stop selection
    def reset(self):
        self.clear_canvas()
        self.draw_points(self.origHolds)
        self.holds = self.origHolds.copy()

    #Clear all holds from canvas
    def clear_canvas(self):
        for holdObj in self.holdObj.values():
            self.canvas.remove(holdObj)
        self.holdObj = {}

    #Remove holds of all other colours
    def isolateColour(self, colour):
        #Go through list of holds
        #holdList is the data Dom outputs [[(x,y), "colour", holdID], ... ]
        for holdInfo in self.holds:
            #If hold colour is not the selected, remove it
            if colour != holdInfo[1]:
                self.removeHold(holdInfo[0])
        
        self.selectFlag = False
        self.manager.get_screen("holds_screen").ids.select_toggle.state = "normal"

    #Remove point/hold from canvas, holds dictionary, and list of points
    def removeHold(self, coords):
        self.canvas.remove(self.holdObj.get(coords))
        del self.holdObj[coords]

        #Remove hold from list of holds
        for holdInfo in self.holds:
            if coords == holdInfo[0]:
                self.holds.remove(holdInfo)

        #Find hold in [(x,y), holdID] list and remove  it
        i = 0
        for hold in self.holds:
            if coords == hold[0]:
                del self.holds[i]
                break
            i = i + 1

    #Delete and select route functions
    def on_touch_down(self, touch):
        input = touch.pos
        print(input[0], input[1])

        select = self.closest(input, self.holds)

        #Delete button toggled, delete point and redraw
        if self.delete and (select != None):
            self.removeHold(select)
            self.delete = False
            self.manager.get_screen("holds_screen").ids.delete_toggle.state = "normal"

        #Adding hold based on user input
        if self.add:
            self.holds.append(input)
            print(self.holds)
            with self.canvas:
                Color(1.0, 0.0, 0.0)
                self.holdObj[input] = Line(circle=(input[0],input[1],5))
            
            #Reset toggle
            self.add = False
            self.manager.get_screen("holds_screen").ids.add_toggle.state = "normal"

        #Select Route
        if self.selectFlag:
            #Find which hold was selected and colour of that hold
            #holdList is the data Dom output [[(x,y), "colour", holdID], ... ]
            print("Selected: ", select)
            for holdInfo in self.holds:
                if select[0] == holdInfo[0]:
                    #Store colour of selected hold
                    colour = holdInfo[1]
                    print(colour)
                    #Remove holds of other colours
                    self.isolateColour(colour)
                    break
            
        #Overwrite method by returning the method of the super class
        return super(HoldsScreen, self).on_touch_down(touch)
'''
#Screen for selecting start, end, and calculation of beta
class BetaScreen(Screen):
    def __init__(self, **kwargs):
        super(BetaScreen, self).__init__(**kwargs)
        #Dictionary pairing points with canvas object
        self.holdObj = {}

    def on_pre_enter(self):
        #List of hold coords and hold IDs [[(x,y), holdID], ...]
        self.holds = self.manager.get_screen('holds_screen').holds
        #Make a copy
        self.origHolds = self.holds.copy()
        self.draw_points(self.holds)

        #Start and End IDs from Start/End Select
        self.startID = self.manager.get_screen("startendselect_screen").startID
        self.endID = self.manager.get_screen("startendselect_screen").endID

        self.startCoords = self.manager.get_screen("startendselect_screen").startCoords
        self.endCoords = self.manager.get_screen("startendselect_screen").endCoords

        self.draw_startEnd()

    #Draw points on the screen
    def draw_points(self, holds):
        with self.canvas:
            for hold in holds:
                Color(1.0, 0.0, 0.0)
                self.holdObj[hold[0]] = Line(circle=(hold[0][0],hold[0][1],5))

    def draw_startEnd(self):
        print(self.startID["RHand"])
        if self.startID["RHand"] != -1:
            with self.canvas:
                for point in self.startCoords:
                    Color(0.0, 1.0, 0.0)
                    Line(circle=(point[0],point[1],5))
                Color(0.0, 0.0, 1.0)
                Line(circle=(self.endCoords[0],self.endCoords[1],5))
                
    
    #Clear all holds from canvas
    def clear_canvas(self):
        for hold in self.holdObj.values():
            self.canvas.remove(hold)
        self.holdObj = {}

    #Calculate distance between two points
    def distance(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2
        dist = math.sqrt(dist)
        return dist
    
    #Find closest point (tuple) to given point P1 and list of points
    def closest(self, p1, holds):
        #Threshold for distance calculation between touch input and hold coordinates
        threshold = 40
        min_dist = self.distance(p1, holds[0][0])
        closest_p = None

        #Find if closest point in list of points
        for hold in holds:
            dist = self.distance(p1, hold[0])
            if (dist <= threshold) and (dist <= min_dist):
                min_dist = dist
                closest_p = hold
        return closest_p

    #Reset all hold points and start/stop selection
    def reset(self):
        self.clear_canvas()
        self.draw_points(self.origHolds)
        self.start = None
        self.stop = None
    
    #Select the starting holds for hands and feet
    def selectStart(self):
        #Select start as point closest to selection within threshold
        self.start = self.closest(self.input, self.holds)
        print("Selected start:", self.start)
        
        #Change the display to appropriate prompt
        display = self.manager.get_screen("beta_screen").ids.display
        display.text = "Select Left Arm Start"

        #Change colour of start hold
        if self.start != None:
            with self.canvas:
                Color(0, 1.0, 0)
                self.startHold = Line(circle=(self.start[0],self.start[1],5))
            
            #Reset Toggle
            self.startFlag = False
            self.manager.get_screen("beta_screen").ids.start_toggle.state = "normal"
    
    #Select stop hold
    def selectStop(self):
        self.stop = self.closest(self.input, self.holds)
        print("Selected stop:", self.stop)
        
        #Change colour of stop hold
        if self.stop != None:
            with self.canvas:
                Color(0, 0.0, 1.0)
                self.holdObj[self.input] = Line(circle=(self.stop[0],self.stop[1],5))
            
            #Reset Toggle
            self.stopFlag = False
            self.manager.get_screen("beta_screen").ids.stop_toggle.state = "normal"

    #Touch Input from User
    def on_touch_down(self, touch):
        #Get touch coordinates as tuple
        self.input = touch.pos
        print(self.input)
                
        return super(BetaScreen, self).on_touch_down(touch)
'''
class StartEndSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(StartEndSelectScreen, self).__init__(**kwargs)

        self.startID = {"RHand": -1, "LHand": -1, "RFoot": -1, "LFoot": -1 }
        self.endID = -1
        self.startCoords = []
        self.endCoords = []

    def on_enter(self):
        self.flags = {"RHand": False, "LHand": False, "RFoot": False, "LFoot": False }
        self.stopFlag = False

        self.holds = self.manager.get_screen("holds_screen").holds
        self.draw_points(self.holds)

    #Draw points on the screen
    def draw_points(self, holds):
        with self.canvas:
            for hold in holds:
                Color(1.0, 0.0, 0.0)
                Line(circle=(hold[0][0],hold[0][1],5))

    #Find closest point (tuple) to given point P1 and list of points
    def closest(self, p1, holds):
        #Threshold for distance calculation between touch input and hold coordinates
        threshold = 40
        min_dist = self.distance(p1, holds[0][0])
        closest_p = None

        #Find if closest point in list of points
        for hold in holds:
            dist = self.distance(p1, hold[0])
            if (dist <= threshold) and (dist <= min_dist):
                min_dist = dist
                closest_p = hold
        return closest_p
    
    #Returns the ID given hold coordinates
    def holdID(self, coords):
        for holdInfo in self.holds:
            if coords == holdInfo[0]:
                return holdInfo[2]
    
    def toggle(self, limb):
        self.flags[limb] = not self.flags[limb]

    def toggle_stop(self):
        self.stopFlag = not self.stopFlag

    #Select Hold for Limb
    def selectHold(self, coords, limb): 
        if limb != "End":
            #self.startID[limb] = self.holdID(coords)
            print(limb + " is selected")
            self.toggle(limb)
        else:
            #self.endID = self.holdID(coords)
            print(limb + " is selected")
            self.toggle_stop()

        #Highlight the start and end hold selected
        with self.canvas:
            if limb != "End":
                Color(0,1.0,0)
            else:
                Color(0,0,1.0)
            Line(circle=(coords[0],coords[1],5))

    #Calculate distance between two points
    def distance(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2
        dist = math.sqrt(dist)
        return dist
    
    #Reset selections and buttons
    def reset(self):
        self.draw_points(self.holds)
        self.startID = {"RHand": -1, "LHand": -1, "RFoot": -1, "LFoot": -1 }
        self.endID = -1
        self.manager.get_screen("startendselect_screen").ids.toggleRHand.disabled = False
        self.manager.get_screen("startendselect_screen").ids.toggleLHand.disabled = False
        self.manager.get_screen("startendselect_screen").ids.toggleRFoot.disabled = False
        self.manager.get_screen("startendselect_screen").ids.toggleLFoot.disabled = False
        self.manager.get_screen("startendselect_screen").ids.toggleEnd.disabled = False

    #Enable the beta button
    def enableBeta(self):
        RHD = self.manager.get_screen("startendselect_screen").ids.toggleRHand.disabled 
        LHD = self.manager.get_screen("startendselect_screen").ids.toggleLHand.disabled 
        RFD = self.manager.get_screen("startendselect_screen").ids.toggleRFoot.disabled 
        LFD = self.manager.get_screen("startendselect_screen").ids.toggleLFoot.disabled
        ED = self.manager.get_screen("startendselect_screen").ids.toggleEnd.disabled 

        if (RHD and LHD and RFD and LFD and ED):
            self.manager.get_screen("startendselect_screen").ids.returnToBeta.disabled = False

    #Get touch coordinates as tuple
    def on_touch_down(self, touch):
        input = touch.pos
        selectedHold = self.closest(input, self.holds)

        if selectedHold != None:
            #Selecting start and stop points
            if (self.flags["RHand"] and not self.flags["LHand"] and not self.flags["RFoot"] and not self.flags["LFoot"]):
                self.selectHold(selectedHold[0],"RHand")
                self.startCoords.append(selectedHold[0])
                self.manager.get_screen("startendselect_screen").ids.toggleRHand.state = "normal"
                self.manager.get_screen("startendselect_screen").ids.toggleRHand.disabled = True
            elif (self.flags["LHand"] and not self.flags["RHand"] and not self.flags["RFoot"] and not self.flags["LFoot"]):
                self.selectHold(selectedHold[0],"LHand")
                self.startCoords.append(selectedHold[0])
                self.manager.get_screen("startendselect_screen").ids.toggleLHand.state = "normal"
                self.manager.get_screen("startendselect_screen").ids.toggleLHand.disabled = True
            elif (self.flags["RFoot"] and not self.flags["RHand"] and not self.flags["LHand"] and not self.flags["LFoot"]):
                self.selectHold(selectedHold[0],"RFoot")
                self.startCoords.append(selectedHold[0])
                self.manager.get_screen("startendselect_screen").ids.toggleRFoot.state = "normal"
                self.manager.get_screen("startendselect_screen").ids.toggleRFoot.disabled = True
            elif (self.flags["LFoot"] and not self.flags["RHand"] and not self.flags["RFoot"] and not self.flags["LHand"]):
                self.selectHold(selectedHold[0],"LFoot")
                self.startCoords.append(selectedHold[0])
                self.manager.get_screen("startendselect_screen").ids.toggleLFoot.state = "normal"
                self.manager.get_screen("startendselect_screen").ids.toggleLFoot.disabled = True
            if self.stopFlag:
                self.selectHold(selectedHold[0],"End")
                self.endCoords.append(selectedHold[0])
                self.manager.get_screen("startendselect_screen").ids.toggleEnd.state = "normal"
                self.manager.get_screen("startendselect_screen").ids.toggleEnd.disabled = True
            
            self.enableBeta()

        return super(StartEndSelectScreen, self).on_touch_down(touch)
    
#Screen for instructions
class StepsScreen(Screen):
    def __init__(self, **kwargs):
        self.stepNum = 0
        super(StepsScreen, self).__init__(**kwargs)

    def on_enter(self):
        #Hold Coords and Hold IDS
        self.holds = self.manager.get_screen("holds_screen").holds

        #Start and End IDs from Start/End Select
        self.startID = self.manager.get_screen("startendselect_screen").startID
        self.endID = self.manager.get_screen("startendselect_screen").endID

        #Calculate Beta with Outputs for each Limb
        self.RHand = {
            '1' : '25',
            '2' : '21',
            '5' : '13',
            '9' : '11',
            '14' : '4',
            '17' : '3'
        }
        self.LHand = {
            '1' : '25',
            '3' :'19',
            '6' : '13',
            '10' : '11',
            '11': '9',
            '12' : '6',
            '16' : '3'
        }
        self.RFoot = {
            '1' : '33',
            '4' : '31',
            '8' : '23',
            '15' : '13'
        }

        self.LFoot = {
            '1' : '31',
            '7' : '25',
            '13' : '19'
        }
    
    #display next/previous step and description
    def update(self, n):
        #Update step number
        if n == 1:
            self.stepNum = self.stepNum + 1
        elif n == -1 and self.stepNum > 1:
            self.stepNum = self.stepNum - 1

        #Update figure and description for step
        self.ids.my_image.source = "step" + str(self.stepNum) + ".png"

        self.moves(self.RHand, self.LHand, self.RFoot, self.LFoot)

    def moves(self, RHand, LHand, RFoot, LFoot):
        key = str(self.stepNum)

        if key == '1':
            self.ids.instructions.text = "Step 1: Get into starting position"
        elif key in RHand.keys():
            self.ids.instructions.text = "Step " + key + ": Move Right Hand to Hold " + RHand[key]
        elif key in LHand.keys():
            self.ids.instructions.text = "Step " + key + ": Move Left Hand to Hold " + LHand[key]
        elif key in RFoot.keys():
            self.ids.instructions.text = "Step " + key + ": Move Right Foot to Hold " + RFoot[key]
        elif key in LFoot.keys():
            self.ids.instructions.text = "Step " + key + ": Move Left Foot to Hold " + LFoot[key]
        else:
            print("Step not found")
    
class InstructionScreen(Screen):
        def __init__(self, **kwargs):
            super(InstructionScreen, self).__init__(**kwargs)

        def on_enter(self):
            RHand = self.manager.get_screen("steps_screen").RHand
            LHand = self.manager.get_screen("steps_screen").LHand
            RFoot = self.manager.get_screen("steps_screen").RFoot
            LFoot = self.manager.get_screen("steps_screen").LFoot

            instructText = ""
            
            #Range is from 1 to (Number of steps - 4)
            #Need to add 2 to get to end because range stops 1 short and for ends 1 early
            for i in range(1, len(RHand) + len(LHand)+ len(RFoot) + len(LFoot) - 4 + 2):
                key = str(i)
                if key == '1':
                    instructText += "Step 1: Get into starting position\n"
                elif key in RHand.keys():
                    instructText +=  "Step " + key + ": Move Right Hand to Hold " + RHand[key] + " \n"
                elif key in LHand.keys():
                    instructText +=  "Step " + key + ": Move Left Hand to Hold " + LHand[key] + " \n"
                elif key in RFoot.keys():
                    instructText +=  "Step " + key + ": Move Right Foot to Hold " + RFoot[key] + " \n"
                elif key in LFoot.keys():
                    instructText += "Step " + key + ": Move Left Foot to Hold " + LFoot[key] + " \n"
                else:
                    print("Step not found")

            self.manager.get_screen("instruction_screen").ids.allSteps.text = instructText

#Load GUI defined by kv file
GUI = Builder.load_file("main.kv")

class captureWallApp(App):
    def build(self):
        '''
        if platform == 'android':
            from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        '''
        return GUI

captureWallApp().run()