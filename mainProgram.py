import os,tkinter.messagebox,numpy as np, imagePrep,cnnModel
from tkinter import filedialog, ttk
from tkinter import *
from PIL import Image, ImageTk
class GUI(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.__root=master
        self.__root.title("OCR AI")
        self.grid()
        #Setup the main window with the title OCR AI and
        #grid file management
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        #Change to the current path
        blankImg=Image.open("transparent.png")
        self.mainWindow(595,842,blankImg,True)
        #Sets up the main window  with a placeholder image
        self.__root.mainloop()
    def imageDialog(self):
        self.__filename=filedialog.askopenfilename(initialdir=os.path.expanduser('~/Pictures'),title="Select file",filetypes=(("Images","*.png *.jpg *.jpeg"),("PNG Images","*.png"),("JPG Images","*.jpg"),("JPEG Images","*.jpeg"),("All files","*.*")))
        #Gives the user a filedialog to select from different
        #image files (JPG,PNG and JPEG)
        try:
            self.__userimg=Image.open(self.__filename)
            self.addImage(self.__userimg)
            #Adds the image to the main canvas
        except:
            tkinter.messagebox.showerror("Error","Opening image failed, not a recognized format.")
            #If the format is unrecognised, show an error message
    def addImage(self,img):
        imgSize=img.size
        while imgSize[0]>1600 or imgSize[1]>900:
            imgSize=[int(i//1.05) for i in imgSize]
            img=img.resize(imgSize,Image.LANCZOS)
            #decreases the image size in incrememnts of 1.05 until it is
            #below 1600 in width and below 900 in height
        imgSize=[round(i/32)*32 for i in imgSize]
        img=img.resize(imgSize,Image.LANCZOS)
        #Resizes the image to the earlier calculated size
        self.mainWindow(*img.size,img,False)
        #Reforms the main window
    def imageRotate(self, clockwise, img):
        if clockwise:
            self.addImage(img.rotate(270,expand=1))
        else:
            self.addImage(img.rotate(90,expand=1))
            #Rotates the image then passes it to the addImage subroutine
    def cancelCrop(self):
        self.__cropConfirm.destroy()
        self.__canvas.delete(self.__drawn)
        self.__cropButton.config(state="normal")
        #Removes the rectangle and returns the crop button to its normal state
    def doCrop(self, event,img):
        self.__canvas.delete(self.__drawn)
        self.__cropConfirm.destroy()
        if event.x<self.__start.x and event.y>self.__start.y:
            self.__cropImg=img.crop((event.x, self.__start.y, self.__start.x, event.y))
        elif event.x>self.__start.x and event.y<self.__start.y:
            self.__cropImg=img.crop((self.__start.x, event.y, event.x, self.__start.y))
        elif event.x<self.__start.x and event.y<self.__start.y:
            self.__cropImg=img.crop((event.x, event.y,self.__start.x, self.__start.y))
        else:
            self.__cropImg=img.crop((self.__start.x, self.__start.y, event.x, event.y))
        #Accounts for cropping in any direction (e.g. bottom right to top left)
        #Without this, certain directions for cropping would give errors
        self.__cropButton.config(state="normal")
        #Returns the image back to normal
        self.addImage(self.__cropImg)
        #Crops the image based on the user's crop and then passes the cropped image to addImage
    def cropEnd(self, event,img):
        self.__cropConfirm=Toplevel(self.__root)
        self.__cropConfirm.title("Crop")
        self.__canvas.config(cursor="")
        self.__canvas.unbind("<ButtonPress-1>")
        self.__canvas.unbind("<B1-Motion>")
        self.__canvas.unbind("<ButtonRelease-1>")
        self.__cropButtonA=Button(self.__cropConfirm,text="Confirm",command=lambda: self.doCrop(event,img))
        self.__cancelButton=Button(self.__cropConfirm,text="Cancel",command=self.cancelCrop)
        #Gives the user the option of cancelling their crop or continuing with it
        self.__cropLabel=Label(self.__cropConfirm, text="Crop selection?").grid(row=0, column=0, columnspan=2, padx=3, pady=3)
        self.__cropButtonA.grid(row=1, column=0, padx=3, pady=3)
        self.__cancelButton.grid(row=1, column=1, padx=3, pady=3)
        self.__cropConfirm.grid()
        #Creates the window with the crop selection label
    def growRectangle(self,event):
        self.__canvas = event.widget
        if self.__drawn: self.__canvas.delete(self.__drawn)
        objectId = self.__shape(self.__start.x, self.__start.y, event.x, event.y,fill="gray50", stipple="gray50")
        #Creates a square with a grey faux-transparency
        self.__drawn = objectId
        #Draws the semi-transparent cropping box for every time it grows
    def startRectangle(self,event):
        self.__start=event
        self.__drawn=None
        #Event handler for starting a crop
    def stopCrop(self,event):
        self.__canvas.unbind("<ButtonPress-1>")
        self.__canvas.unbind("<B1-Motion>")
        self.__canvas.unbind("<ButtonRelease-1>")
        self.__cropButton.config(state="normal")
        #Event handling for cancelling the crop
    def crop(self,x,y,img):
        self.__cropButton.config(state=DISABLED)
        self.__canvas.config(cursor="cross")
        #Changes the cursor to a cross
        self.__canvas.bind("<ButtonPress-1>",self.startRectangle)
        self.__canvas.bind("<B1-Motion>", self.growRectangle)
        self.__canvas.bind("<ButtonRelease-1>",lambda event: self.cropEnd(event,img))
        self.__root.bind("<Escape>",self.stopCrop)
        #Creates the binds for stopping the crop and growing the rectangle
        self.__shape=self.__canvas.create_rectangle
        #Starts the cropping process
    def textScan(self):
        spell=SpellChecker(distance=1)
        testList,testStr=[],[]
        self.__img.save("tmp/temp.png")
        coordslist=imagePrep.textDetection("tmp/temp.png")
        #Runs the image through the textDetection
        if len(coordslist)==0:
            tkinter.messagebox.showerror("Error","No text found")
            #If the text detection doesn't return anything, show an error
        else:
            imagesList,threshedList,characterList,resizedList,centerlist,heightlist,predictlist=[],[],[],[],[],[],[]
            for i in coordslist:
                centerlist.append([i[0]+(i[2]-i[0])//2,i[1]+(i[3]-i[1])//2])
                #Get a list of the centers of all the words
                heightlist.append(i[3]-i[1])
                #Get a lsit of the heights of all the words
                imagesList.append(self.__img.crop(i))
                #Makes a list of each image of words as returned by textDetection
            for x in imagesList:
                x.save("tmp/temp.png")
                characterList.append([imagePrep.fitImage(x) for x in imagePrep.charSegment("tmp/temp.png")])
                #Segment the characters and fit them to 30x30, add the result  to the characterlist
            for x in characterList:
                 predictlist.append(cnnModel.getPredict("default_model",np.asarray(x,dtype=np.float32)/255.0))
                 #Gets the predictions for every character in each word then adds it to a list of words
            centerlist, heightlist,predictlist = zip(*sorted(zip(centerlist, heightlist,predictlist), key=lambda x: x[0]))
            #Sort the 3 lists based on the distance from left to right
            highest,height=zip(*sorted(zip(centerlist, heightlist), key=lambda x: x[1]))
            #Sort these two lists by the y-coordinate of the centerlist
            highest=highest[-1] #Set the heighest to the last value in the list
            height=height[-1]
            lines=[[highest]]
            #Create a new line with the highest y-coord
            lineHeight=[[height]]
            #Set the lineHeight initially to the first height
            found=False
            for i in range(len(centerlist)):
                found=False
                for j in range(len(lines)):
                    avgHeight=sum(lineHeight[j])/len(lineHeight[j])
                    #Get the average height of a line
                    if any(centerlist[i][1]<(x[1]-avgHeight/2) for x in lines[j]) or any(centerlist[i][1]<(x[1]+avgHeight/2) for x in lines[j]):
                        lines[j].append(centerlist[i])
                        lineHeight[j].append(heightlist[i])
                        found=True
                        break
                        #If the word being checked is within half of the line's average height of any
                        #word center in the line, then it is added to that line and the loop breaks

                if not found:
                    lines.append([centerlist[i]])
                    lineHeight.append([heightlist[i]])
                #if the word doesn't fit within half of the average height
                #of any center in any line it is added to a new line.
            lines[0].pop(0)
            #Remove the first item of the first line as this would be a duplicate
            predictPrint="".join([("".join([predictlist[centerlist.index(j)]+" " for j in i])+"\n") for i in lines])
            #Join the predictions into a string with a newline for every line
            tkinter.messagebox.showinfo("Image Text",predictPrint)
            #Display the predictions in a message box
    def mainWindow(self,x,y,img,init):
        if init==False:
            self.__canvas.grid_forget()
            self.__canvas.delete("all")
            #Reset the canvas if this isn't the first time being called
        self.__img=img
        self.__imgdisplay=ImageTk.PhotoImage(img)
        self.__canvas=Canvas(self.__root,width=x,height=y,highlightthickness=1, highlightbackground="black")
        self.__canvas.grid(row=0,padx=20,pady=10,columnspan=21)
        self.__canvas.create_image(0,0,image=self.__imgdisplay,anchor="nw")
        #Adds the image to the canvas as a preview
        self.__imageButton=Button(self.__root, text="Import Image", command=self.imageDialog,anchor="e")
        self.__imageButton.grid(column=0,row=1,pady=10,padx=2)
        self.__antiIco=ImageTk.PhotoImage(file="Icons/anticlockwise.ico")
        self.__antiRotate=Button(self.__root,image=self.__antiIco,command=lambda: self.imageRotate(False,img),anchor="w")
        self.__antiRotate.grid(column=17,row=1,padx=2,pady=10)
        self.__clockwiseIco=ImageTk.PhotoImage(file="Icons/clockwise.ico")
        self.__clockRotate=Button(self.__root, image=self.__clockwiseIco,command=lambda: self.imageRotate(True,img),anchor="w")
        self.__clockRotate.grid(column=18,row=1,padx=2,pady=10)
        self.__cropIco=ImageTk.PhotoImage(file="Icons/crop.ico")
        self.__cropButton=Button(self.__root, image=self.__cropIco,command=lambda: self.crop(x,y,img),anchor="w")
        self.__cropButton.grid(column=19,row=1,padx=2,pady=10)
        self.__scanIco=ImageTk.PhotoImage(Image.open("Icons/scan.ico").resize((32,32),Image.ANTIALIAS).convert("RGBA"))
        #Resizes the scan icon to fit in the canvas
        self.__scanButton=Button(self.__root, image=self.__scanIco, command=self.textScan, anchor="w")
        self.__scanButton.grid(column=20, row=1, padx=2, pady=10)
        #Creates all the icons and their respective buttons on the UI
        if init:
            self.__antiRotate.config(state=DISABLED)
            self.__clockRotate.config(state=DISABLED)
            self.__cropButton.config(state=DISABLED)
            self.__scanButton.config(state=DISABLED)
        #Disables the buttons if the user hasn't loaded an iamge yet

instance=GUI(Tk())
