#fontChecker
import os
from tkinter import *
from PIL import Image,ImageDraw,ImageFont,ImageTk
os.chdir(os.path.dirname(os.path.realpath(__file__)))
class GUI(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.__root=master
        self.__root.title("Font Checker")
        self.grid()
        #Setup a new tkinter window with title Font Checker
        self.__counter=0
        #Create a counter variable iwth value 0
        self.__fontlist=(os.listdir("charImages/Fonts/"))
        #List all downloaded fonts
        self.updateLabel()
        self.__root.bind("<space>",self.pass1)
        self.__root.bind("<Return>",self.del1)
        #Bind space to pass1 and Return to del1
        self.__root.mainloop()
    def updateLabel(self):
        self.__x=Image.new(mode="L",size=(1200,500),color=255)
        draw=ImageDraw.Draw(self.__x)
        #Create a new 1200,500 white image in B&W mide
        fontchoice=self.__fontlist[self.__counter]
        #Select the font based on what the counter is at
        try:
            font=ImageFont.truetype("charImages/Fonts/"+fontchoice,size=70)
            draw.text((0,0),"A B C D E F G H I J K L \n M N O P Q R S T U V W X Y Z \n 0 1 2 3 4 5 6 7 8 9 \n"+fontchoice,fill=0,font=font)
            #Create an image with this sample text and the fontname at size 70 of the chosen font
            self.__imgdisplay=ImageTk.PhotoImage(self.__x)
            self.__label=Label(self.__root,image=self.__imgdisplay)
            self.__label.grid(row=0,column=0)
            #Display the previously created image
        except:
            os.remove("charImages/Fonts/"+fontchoice)
            #If the font couldn't be read, remove it from the font directory
    def pass1(self,event):
        self.__counter+=1
        self.__label.grid_forget()
        self.updateLabel()
        #Add one to the counter then show the new image
    def del1(self,event):
        fontchoice=self.__fontlist[self.__counter]
        os.remove("charImages/Fonts/"+fontchoice)
        #Remove the font if del is chosen
        self.__counter+=1
        self.__label.grid_forget()
        self.updateLabel()
        #Add one to the counter then show the new image
instance=GUI(Tk())
