import tkinter as tk
import tkinter 
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *
import numpy as np
import operator
import math
import copy 






answersGlobal=[]

################################
# FUNCTION DEFINITIONS FOLLOW
################################





# =============================================================================
#  Following function finds the intersection of two lines
#  Input: Coordinates of four points; the first array for the first line points,
#  the second array for the second line points
# =============================================================================

def findInterSectionPoint(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# =============================================================================
# Find boundary circle with minimum radius
# =============================================================================
def get_radii(l):
    r=9999
    for i in range(0,len(l)):
        
        if(l[i].size < r):
            r = int(math.ceil( l[i].size) )
            
    return int(math.ceil( r/2 ) )




# =============================================================================
# parameters for opencv SimpleBlobDetector to detect boundary circles
# =============================================================================
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 50
params.filterByCircularity = True
params.minCircularity = 0.7


# =============================================================================
# Checking version of opencv library 
# use opencv version >=  4.x.x 
# Many functions have been changed in newer version of opencv
# This program is configured according to newer version of opencv
# =============================================================================
is_cv4 = cv2.__version__.startswith("4.")
if is_cv4:
    detector = cv2.SimpleBlobDetector_create(params)

else:
    detector = cv2.SimpleBlobDetector(params)

class SelectCorrectOptions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        startpage = self.controller.get_page("startPage")
        value = startpage.some_entry.get()
        print("Printing no of mcq:")
        print(value)
        
        
        
        try:
            noOfMCQ=int(value,10)
        except ValueError:
            print("Not a float")
            noOfMCQ=11
        
        
        
        
        self.style = ttk.Style()
        
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))      

       
        ttk.Label(self, text = 'Select the correct options', style = 'Header.TLabel').grid(row = 0, column = 1, columnspan = 5)
        ttk.Label(self, wraplength = 300,
                  text = ("Please select the correct option for each MCQ\n")).grid(row = 1, column = 1, columnspan = 5)
        
        

       
        self.answers = []
        self.noOfMCQ = noOfMCQ
        self.checkBoxValuesA = []
        self.checkBoxValuesB = []
        self.checkBoxValuesC = []
        self.checkBoxValuesD = []
        self.checkBoxesA = []
        self.checkBoxesB = []
        self.checkBoxesC = []
        self.checkBoxesD = []
        self.leftSide = []
        self.rightSide = []
        self.topSide = []
        self.bottomSide = []
        self.radii = 999999
        
        correctAnswers = answersGlobal
        listPreInitialzed= False
        if(len(correctAnswers) > 0):
            listPreInitialzed= True
            
        print('Length of saved answers:'+str(len(answersGlobal)))
        print('Number of MCQs:'+str(self.noOfMCQ))
        for i in range(0, self.noOfMCQ):
           ttk.Label(self, text = str(i+1)+'.').grid(row = 4+i, column = 0)
           self.checkBoxValuesA.append(BooleanVar())
           checkBoxA = ttk.Checkbutton(self, text = 'A')
           self.checkBoxesA.append(checkBoxA)
           self.checkBoxesA[i].config(variable = self.checkBoxValuesA[i], onvalue = True,
    		   offvalue = False)
           self.checkBoxesA[i].grid(row = 4+i, column = 1, padx = 5)
           if(listPreInitialzed == True) and (correctAnswers[i][0] == True):
               self.checkBoxValuesA[i].set(True)
           
           self.checkBoxValuesB.append(BooleanVar())
           checkBoxB = ttk.Checkbutton(self, text = 'B')
           self.checkBoxesB.append(checkBoxB)
           self.checkBoxesB[i].config(variable = self.checkBoxValuesB[i], onvalue = True,
    		   offvalue = False)
           self.checkBoxesB[i].grid(row = 4+i, column = 2, padx = 5)
           if(listPreInitialzed == True) and (correctAnswers[i][1] == True):
               self.checkBoxValuesB[i].set(True)
           
           self.checkBoxValuesC.append(BooleanVar())
           checkBoxC = ttk.Checkbutton(self, text = 'C')
           self.checkBoxesC.append(checkBoxC)
           self.checkBoxesC[i].config(variable = self.checkBoxValuesC[i], onvalue = True,
    		   offvalue = False)
           self.checkBoxesC[i].grid(row = 4+i, column = 3, padx = 5)
           if(listPreInitialzed == True) and (correctAnswers[i][2] == True):
               self.checkBoxValuesC[i].set(True)
           
           self.checkBoxValuesD.append(BooleanVar())
           checkBoxD = ttk.Checkbutton(self, text = 'D')
           self.checkBoxesD.append(checkBoxD)
           self.checkBoxesD[i].config(variable = self.checkBoxValuesD[i],  onvalue = True,
    		   offvalue = False)
           self.checkBoxesD[i].grid(row = 4+i, column = 4, padx = 5)
           if(listPreInitialzed == True) and (correctAnswers[i][3] == True):
               self.checkBoxValuesD[i].set(True)
           
        
        
        ttk.Button(self, text = 'Submit',
                   command = self.submit).grid(row = 5+self.noOfMCQ, column = 1,columnspan = 2, padx = 5, pady = 5, sticky = 'n' )
        ttk.Button(self, text = 'Clear',
                   command = self.clear).grid(row = 5+self.noOfMCQ, column = 3,columnspan = 2, padx = 5, pady = 5, sticky = 'n')
        ttk.Button(self, text = 'Go Back',
                   command =  self.clearGlobalVariable).grid(row = 6+self.noOfMCQ, column = 0,columnspan = 5, padx = 5, pady = 5, sticky = 'n')


    def submit(self):
       
        print('inside submit function 1')
        while self.answers:
            print('popping')
            self.answers.pop(0)
            #f
        while answersGlobal:
            print('Popping from global variable')
            answersGlobal.pop(0)
                
        for i in range(0, self.noOfMCQ):
            tempList = []
            tempList.append(self.checkBoxValuesA[i].get())
            tempList.append(self.checkBoxValuesB[i].get())
            tempList.append(self.checkBoxValuesC[i].get())
            tempList.append(self.checkBoxValuesD[i].get())
            self.answers.append(tempList)
            answersGlobal.append(tempList)
        
        
        print('Printing answers')
        print(self.answers)
        
        print('Printing global variable answers')
        print(answersGlobal)
        self.controller.show_frame(SubmittedAnswers)
        
        
    
    def clear(self):
       
        print('inside clear function 1')
        for i in range(0, self.noOfMCQ):
            self.checkBoxValuesA[i].set(0)
            self.checkBoxValuesB[i].set(0)
            self.checkBoxValuesC[i].set(0)
            self.checkBoxValuesD[i].set(0)
        
    def getAnswers(self):
        print('Inside get Answers!!')
        print(self.answers)
        return self.answers
    
    def clearGlobalVariable(self):
        while answersGlobal:
            print('Popping from global variable')
            answersGlobal.pop(0)
        self.controller.show_frame(startPage)
        
# =============================================================================
# Following class generate parent window GUI elements for the  application 
# =============================================================================
class parentFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.video_source = 0
 
        
        self.vid = MyVideoCapture(self.video_source)
        
        
        panedwindow = ttk.Panedwindow(self, orient = HORIZONTAL)
        
        #close the webcam feed and gui window 
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        panedwindow.pack(fill = BOTH, expand = True)
        
        #Frame for displaying video from webcam (Leftside)
        vidFrame = ttk.Frame(panedwindow, width = self.vid.width, height = self.vid.height, relief = SUNKEN)
        
        #Frame for various other GUI elements (Rightside)
        container = ttk.Frame(panedwindow, width = 100, height = 400, relief = SUNKEN)
        panedwindow.add(vidFrame, weight = 1)
        panedwindow.add(container, weight = 4)
        
        #setting height and width for video frame based on  webcam resolution
        self.canvas = tkinter.Canvas(vidFrame, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
        
        self.btn_snapshot=tkinter.Button(vidFrame, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        
        self.delay = 15
        self.update()   #Function to update frames from webcam
 
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.c = container
        self.frames = {}

        for F in (startPage, SelectCorrectOptions, SubmittedAnswers):
            frame = F(container, self)  #startPage container
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.show_frame(startPage)
        self.mainloop()
        
        
    def show_frame(self, page_name):
        print('inside show_frame function:'+str(page_name)+'::'+str(type(page_name)))
        if page_name == SelectCorrectOptions:
            print('page requested: SelectCorrectOptions')
            frame = page_name(self.c, self)  #startPage container
            
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame
        
        elif page_name == SubmittedAnswers:
            frame = page_name(self.c, self)
            
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame
            
            
            
        frame = self.frames[page_name]
        frame.tkraise()
# =============================================================================
#     Following function close GUI window and release webcam resource
# =============================================================================
    def close(self):
        self.vid.__del__()
        self.destroy()
        
    def get_page(self, page_name):
        for page in self.frames.values():
            if str(page.__class__.__name__) == page_name:
                return page
        return None    
    
# =============================================================================
#     Following function converts raw webcam frame to grey scale
#     then blur it and apply simpleblobdetection function to detect boundaries
#     these boundaries are stored in 4 lists leftSide, rightSide, topSide and bottomSide
#     it then marks the detected boundaries and retrun that frame as im_with_keypoints
# =============================================================================
    
    def func(self,frame):
    
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY );
        
        
        tmp=gray_image
        frame_gray=cv2.blur(tmp,(1,8))
        
        keypointsBKP = detector.detect(frame_gray)
        keypoints=copy.copy(keypointsBKP)
        keypoints.sort(key=operator.attrgetter('pt'))
        
        
        
        
        
        # Gets the marker points
        self.leftSide = []
        self.rightSide = []
        self.topSide = []
        self.bottomSide = []
        
        if len(keypoints) >= 2*10+ 2*4:
                keypoints.sort(key=lambda x: x.pt[1])
        
                for i in range(0,10):
                    self.leftSide.append(keypoints[0])
                    
                    keypoints.pop(0)
                    
        
                for i in range(0,10):
                    self.rightSide.append(keypoints[len(keypoints) - 1])
                    
                    keypoints.pop(len(keypoints) - 1)
        
                self.leftSide.sort(key=lambda x: x.pt[0])
                self.rightSide.sort(key=lambda x: x.pt[0])
        
                keypoints.sort(key=lambda x: x.pt[0])
        
                for i in range(0,4):
                    self.topSide.append(keypoints[0])
                    
                    keypoints.pop(0)
        
                for i in range(0,4):
                    self.bottomSide.append(keypoints[len(keypoints) - 1])
                    
                    keypoints.pop(len(keypoints) - 1)
        
                self.topSide.sort(key=lambda x: x.pt[1])
                self.bottomSide.sort(key=lambda x: x.pt[1])
        bdr_keypts=self.leftSide+self.rightSide+self.topSide+self.bottomSide
        
        
        self.radii = get_radii(bdr_keypts)
       
        topAnsImg = cv2.drawKeypoints(tmp, self.topSide, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        botAnsImg = cv2.drawKeypoints(topAnsImg, self.bottomSide, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        rightAnsImg = cv2.drawKeypoints(botAnsImg, self.rightSide, np.array([]), (255,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints = cv2.drawKeypoints(rightAnsImg, self.leftSide, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        return im_with_keypoints
    
# =============================================================================
#     Follwing function converts the frame returned by func() to a binary frame of black and white pixels
#     using Simple binarization value THERSH_TOZERO read more about it at (https://docs.opencv.org/3.4.0/d7/d4d/tutorial_py_thresholding.html)
#     **selecting a threshold function for frame in a work in progress**
#     findInterSectionPoint() function is used to get center point for each option of a question
#     black pixels are detected around these points in a circle of radii returned by get_radii()
#     
#     rgb values of each pixel are converted to a hex code 
#     this hex code is further converted into an integer of base 16 and compared with a preset value/ threshhold value
#     int('%02x%02x%02x' % (60,60,60),16) = 3947580 (threshold value)
#     **selecting a more suitable threshold value for pixels is a work in progress**
#     based on this value of each pixel it is consider as marked or unmarked (0 or 1 )
#     
#     
#     
#     a list of list for each option containing [filledPixels,TotalPixelschecked,(center point)] is generated
# =============================================================================
   
   
    def snapshot(self):
        
         print("Inside snapshot:")
         tempPage = self.get_page("SelectCorrectOptions")
        
         answers1 =tempPage.getAnswers()
         print("Inside snapshot Printing selected Answers:")
         print(answersGlobal)
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
         self.frame = self.func(frame)
         leftSide = self.leftSide
         rightSide = self.rightSide
         topSide = self.topSide
         bottomSide = self.bottomSide
         frame_gray=cv2.blur(self.frame,(1,8))
         cv2.imshow("MW", np.hstack([frame_gray]))
         if ret:
            print(leftSide)
            ansListFromSheet=[]
            #Binarization of frame
            ret,im_with_keypoints = cv2.threshold(self.frame,127,255,cv2.THRESH_TOZERO)
            allAnswersCenterPoints=[]
     
            for k in reversed(range(0,len(rightSide))):
                     #print(type(topSide[k]))
                     ptAx = round(rightSide[k].pt[0])
                     ptAy = round(rightSide[k].pt[1])
                     #print('pt1x:'+str(ptAx)+' pt1y:'+str(ptAy))
                     
                     ptBx = round(leftSide[k].pt[0])
                     ptBy = round(leftSide[k].pt[1])
                     #print('pt2x:'+str(ptBx)+' pt2y:'+str(ptBy))       
                     #cv2.line(im_with_keypoints, (ptAx, ptAy), (ptBx, ptBy), (255, 0, 0), 1)
                     tempCenterPoints=[]
                     for l in range(0,len(topSide)):
                         ptCx = round(topSide[l].pt[0])
                         ptCy = round(topSide[l].pt[1])
                         #print('pt1x:'+str(ptCx)+' pt1y:'+str(ptCy))
                         
                         ptDx = round(bottomSide[l].pt[0])
                         ptDy = round(bottomSide[l].pt[1])
                         #print('pt2x:'+str(ptDx)+' pt2y:'+str(ptDy))
                         
                         pointA =(ptAx, ptAy)
                         pointB =(ptBx, ptBy)
                         pointC =(ptCx, ptCy)
                         pointD =(ptDx, ptDy)
                         
                         #center point for each option for each question
                         interPtX,interPtY = findInterSectionPoint((pointA,pointB),(pointC,pointD))
                         print('interPtX:'+str(int(interPtX))+' interPtY:'+str(int(interPtY)))
                         text = str(int(interPtX))
                        
                         interPtXIntVal=int(interPtX)
                         interPtYIntVal=int(interPtY)
                         
                         
                         tempCenterPoints.append((interPtXIntVal,interPtYIntVal))
                         
                     allAnswersCenterPoints.append(tempCenterPoints)
            arr = im_with_keypoints[interPtYIntVal: interPtYIntVal+5,interPtXIntVal:interPtXIntVal+5]
         
         # '%02x%02x%02x' % rgb(169,169,169)
            print('Printing stored centers:')
            print(allAnswersCenterPoints)
            answersData=[]
            totalPixels=0
            count=0
            filedCount=0
            colorComparisonVal=3947580  #threshold value
            for questionCenters in allAnswersCenterPoints:
                for centerPt in questionCenters:
                     count=count+1
                     totalPixels=0
                     
                     
                     #pixels around a center point in a circle of radius = radii
                     #selected using circle formula ( (X-Cₓ)² + (Y-Cᵧ)² < r² )
                     filedCount=0
                     for i in range(0,self.radii-1):
                         for j in range(0,self.radii-1):
                             x = int(centerPt[1])+i
                             y =int(centerPt[0])+j
                             if( (x-centerPt[1])**2 + (y-centerPt[0])**2 < 7**2 ):
                                 pixelPosition=im_with_keypoints[centerPt[1]+i,centerPt[0]+j]
                                 var1= '%02x%02x%02x' %  (pixelPosition[0],pixelPosition[1],pixelPosition[2])
                                 #im_with_keypoints[centerPt[1]+i,centerPt[0]+j]=[0,0,0]
                                 totalPixels=totalPixels+1
                                 if(int(var1,16) < colorComparisonVal):
                                     filedCount=filedCount+1 
                             
                             x = int(centerPt[1])-i
                             y =int(centerPt[0])-j
                             if( (x-centerPt[1])**2 + (y-centerPt[0])**2 < 7**2 ):
                                 totalPixels=totalPixels+1
                                 pixelPosition=im_with_keypoints[centerPt[1]+i,centerPt[0]-j]
                                 var1= '%02x%02x%02x' %  (pixelPosition[0],pixelPosition[1],pixelPosition[2])
                                 #im_with_keypoints[centerPt[1]+i,centerPt[0]-j]=[0,0,0]
                                 if(int(var1,16) < colorComparisonVal):
                                     filedCount=filedCount+1
                             x = int(centerPt[1])+i
                             y =int(centerPt[0])-j
                             if( (x-centerPt[1])**2 + (y-centerPt[0])**2 < 7**2 ):
                                 totalPixels=totalPixels+1
                                 pixelPosition=im_with_keypoints[centerPt[1]-i,centerPt[0]+j]
                                 var1= '%02x%02x%02x' %  (pixelPosition[0],pixelPosition[1],pixelPosition[2])
                                 #im_with_keypoints[centerPt[1]-i,centerPt[0]+j]=[0,0,0]
                                 if(int(var1,16) < colorComparisonVal):
                                     filedCount=filedCount+1
                             x = int(centerPt[1])-i
                             y =int(centerPt[0])+j
                             if( (x-centerPt[1])**2 + (y-centerPt[0])**2 < 7**2 ):
                                 totalPixels=totalPixels+1
                                 pixelPosition=im_with_keypoints[centerPt[1]-i,centerPt[0]-j]
                                 var1= '%02x%02x%02x' %  (pixelPosition[0],pixelPosition[1],pixelPosition[2])
                                 #im_with_keypoints[centerPt[1]-i,centerPt[0]-j]=[0,0,0]
                                 if(int(var1,16) < colorComparisonVal):
                                     filedCount=filedCount+1
                     

                     opt=[] #contains information about each option 
                     opt.append(filedCount)
                     opt.append(totalPixels)
                     opt.append(tuple(  (int(centerPt[0]) , int(centerPt[1]))  ) )
                     ansListFromSheet.append(opt)   #contains information about every option 
                     cv2.putText(im_with_keypoints, str(filedCount), (centerPt[0], centerPt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (225, 225, 225), lineType=cv2.LINE_AA) 
                     
                
            print(ansListFromSheet)
            
            totalMark=0
            #sample marking logic 
            ansKey=answersGlobal
            i=0
            for ques in answersGlobal:
                for q_opt in ques:
                    opt = ansListFromSheet[i]
                    i+=1
                    filledPixelPercentage = (opt[0]/opt[1]) * 100
                    if( filledPixelPercentage >= 80 ):
                        k = True
                    else:
                        k = False
                        
                    print(str(i)+" "+ str(k)+" " + str(q_opt))    
                    if(k == q_opt):
                        totalMark += 1
                    
                        
            print(totalMark)
            #shows final graded MCQ sheet
            cv2.imshow("MW", np.hstack([im_with_keypoints])) 
# =============================================================================
#     Following function get frames from webcam video feed and display it on tkinter GUI        
# =============================================================================
    def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
             self.frame = self.func(frame)
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
                        
         self.after(self.delay, self.update)


# =============================================================================
# Following class generate GUI elements for the right side Frame of the application
# =============================================================================
class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
       
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font = ('Arial', 5, 'bold')) 
        
        label = ttk.Label(self, text = "Enter no. of questions and press submit", style = 'Header.TLabel')
        label.grid(row = 0, column = 1, columnspan = 3, padx = 5, pady = 5)
        
        self.make_widget(controller)
        
        

       
# =============================================================================
#     Following function generate an input box, submit button and answer sheet generater button
# =============================================================================
    def make_widget(self, controller):
        some_input = StringVar()
        
        self.some_entry = Spinbox(self,textvariable=some_input, from_ = 1, to = 20)
        self.some_entry.grid(row = 2, column = 1, padx = 5, pady = 5)
        button1 = tk.Button(self, text='Submit', command=lambda: controller.show_frame(SelectCorrectOptions))
        button1.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'n')
        button2 = tk.Button(self, text='Generate Sheet', command=self.generateSheet)
        button2.grid(row = 4, column = 2, padx = 5, pady = 5, sticky = 'n')
# =============================================================================
#     Following function generate MCQ answer sheet
# =============================================================================
    def generateSheet(self):
        noOfMCQs = self.some_entry.get()
        print('Generating sheet for {} MCQs'.format(noOfMCQs))
        noOfQuestions=int(noOfMCQs,10)
        noOfAnswerOptions=4
        circleSize=15
        gapBetweenCircles=circleSize*4
        gapBetweenBoundryAndCircles=gapBetweenCircles+10
        circleThickness=2
        circleColor=(0,0,0)
        imageLength=noOfQuestions*80
        imageLength += 100
        ones = np.ones([imageLength ,540,3],'uint8')
        
        
        color = ones.copy()
        color[:,:] = (255,255,255)
        
        
        print(color[0,0,:])
        
        
        #Creating white blank image
        cv2.imwrite("MCQ_Sheet.jpeg", color)
        image = cv2.imread("MCQ_Sheet.jpeg", 1)
        
        
        horizStartPostion=200
        vertiStartPosition=50
        horizPosition=horizStartPostion
        vertiPosition=vertiStartPosition
        
        #First 4 black boundry circles
        for x in range(0, noOfAnswerOptions):
              print(x)  
              cv2.circle(image,(horizPosition, vertiPosition), circleSize, circleColor, -1)
              
              horizPosition += gapBetweenCircles
        horizPosition=horizStartPostion
        vertiPosition += gapBetweenBoundryAndCircles
        for x in range(0, noOfQuestions):
             #Right side black boundry circle
            cv2.circle(image,(horizPosition-gapBetweenBoundryAndCircles -20 , vertiPosition), circleSize, circleColor, -1)
            cv2.putText(image, str(x+1)+'.', (horizPosition-gapBetweenBoundryAndCircles , vertiPosition+10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
            
            for x in range(0, noOfAnswerOptions):
              cv2.putText(image, chr(65+x), (horizPosition-35, vertiPosition+10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
              cv2.circle(image,(horizPosition, vertiPosition), circleSize, circleColor, circleThickness)
              horizPosition += gapBetweenCircles
              
            #Left side black boundry circle
            cv2.circle(image,((horizPosition-gapBetweenCircles)+gapBetweenBoundryAndCircles, vertiPosition), circleSize, circleColor, -1)
            vertiPosition += gapBetweenCircles
            horizPosition=horizStartPostion
            
        #Last 4 black boundry circles
        for x in range(0, noOfAnswerOptions):
              print(x)  
              cv2.circle(image,(horizPosition, (vertiPosition-gapBetweenCircles)+gapBetweenBoundryAndCircles), circleSize, circleColor, -1)
              
              horizPosition += gapBetweenCircles
        
        
        dimensions = image.shape
        # height, width, number of channels in image
        height = dimensions[0]
        width = dimensions[1]
        ht=height
        wd=width
        if(height > 550):
            ht=550
        if(width > 450):
            wd=450
        imageResized = cv2.resize(image, (wd, ht)) 
        
        #Saving the created sheet image and displaying on screen
        cv2.imwrite("MCQ_Sheet.jpeg", image)
        cv2.imshow("MCQ_Sheet",imageResized)


# =============================================================================
# Following class opens webcam video feed 
# return: single frame from webcam video feed
# =============================================================================
class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                 
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
             
# =============================================================================
# Following class takes submitted answers for each question and display it in a user friendly way
# in form of an answer key 
# =============================================================================
class SubmittedAnswers(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        SelectCorrectOptionsTemp = self.controller.get_page("SelectCorrectOptions")
        print('inside SubmittedAnswers init ')
        answers =SelectCorrectOptionsTemp.getAnswers()
        print("Printing selected Answers:")
        print(answers)
        
        
        for i in range(len(answersGlobal)):
            for j in range(0,4):   
                print('Value:'+str(answersGlobal[i][j]))
      
        
       
        
        
        correctAnswers = answersGlobal
        answersInitialized=True
        noOfMCQ=10
        noOfOptions=4
        try:
            noOfMCQ=int(str(len(correctAnswers)),10)
            if(noOfMCQ > 0):
                noOfOptions=int(str(len(correctAnswers[0])),10)
        except:
            print("answersGlobal not initialized taking default values")
            noOfMCQ=10
            noOfOptions=4
            answersInitialized=False
            
        print('no of questions:'+str(noOfMCQ))
        print('no of options:'+str(noOfOptions))
        noOfQuestions=noOfMCQ
        noOfAnswerOptions=noOfOptions
        circleSize=15
        gapBetweenCircles=circleSize*3
        gapBetweenBoundryAndCircles=gapBetweenCircles+10
        circleThickness=2
        circleColor=(0,0,0)
        imageLength=noOfQuestions*60
        imageLength += 50        
        
        ones = np.ones([imageLength ,noOfAnswerOptions*130,3],'uint8')
        
        
        color = ones.copy()
        color[:,:] = (255,255,255)
        
        cv2.imwrite("correct_Answers.jpeg", color)
        self.image1 = cv2.imread("correct_Answers.jpeg", 1)
        
        horizStartPostion=100
        vertiStartPosition=50
        horizPosition=horizStartPostion
        vertiPosition=vertiStartPosition
        print('Correct Answers:')
        if(answersInitialized == False):
            correctAnswers = [[True,True,True,True]]
        for x in range(0, noOfAnswerOptions):
              cv2.putText(self.image1, chr(65+x), (horizPosition-circleSize, vertiPosition),
              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
              horizPosition += gapBetweenCircles
        
        horizPosition=horizStartPostion
        vertiPosition += circleSize+10
        for x in range(0, noOfQuestions):
           
           horizPosition=horizStartPostion
           cv2.putText(self.image1, str(x+1)+'.', (horizPosition-gapBetweenBoundryAndCircles, vertiPosition+10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)            
           
           for y in range(0, noOfAnswerOptions):
              #print('running for x:'+str(x)+ ' y:'+str(y))
              if(correctAnswers[x][y] == True):
                  #print('value is true')
                  circleColor=(0,255,0)
                  circleThickness=-1
              else:
                  circleColor=(0,0,0)
                  circleThickness=2
              cv2.circle(self.image1,(horizPosition, vertiPosition), circleSize, circleColor, circleThickness)
              horizPosition += gapBetweenCircles
              
           vertiPosition += gapBetweenCircles
            
        
        
        
        cv2.imwrite("correct_Answers.jpeg", self.image1)
        imgTemp = cv2.imread("correct_Answers.jpeg", cv2.IMREAD_UNCHANGED)
 
        # get dimensions of image
        dimensions = imgTemp.shape
        # height, width, number of channels in image
        height = dimensions[0]
        width = dimensions[1]
        ht=550
        wd=450
        if(height < 550):
            ht=height
        if(width < 450):
            wd=width
        self.img = PIL.Image.open("correct_Answers.jpeg").resize((wd, ht))
        self.correctAnsImg = PIL.ImageTk.PhotoImage(self.img)
        imglabel = ttk.Label(self, image=self.correctAnsImg).grid(row=1, column=1) 
        ttk.Button(self, text = 'Go Back',
                   command = lambda: self.controller.show_frame(SelectCorrectOptions)).grid(row = 2, column = 0,columnspan = 5, padx = 5, pady = 5, sticky = 'n')


        



    
app1 = parentFrame()
