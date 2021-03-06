import datetime
from typing import Container
#import led info, replace with relay info
#from gpiozero import PWMLED
#LED1 = PWMLED(17)

#import DataLogger.py
from DataLogger import DataLogger

#import tkinter for GUI
import tkinter as tk
from tkinter import *
from tkinter import ttk
#font types
TITLE_FONT = ("Verdana", 14,) #"bold")
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
#import stuff for graph
import matplotlib
import matplotlib.ticker as mticker
from matplotlib import pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import csv
#import/enable garbage collector to clear memory
import gc
gc.enable()
#import animation to make graph live
import matplotlib.animation as animation
from matplotlib import style
style.use("seaborn-darkgrid")
#import vertical scroll bar
from vertical_scroll_frame import VerticalScrolledFrame
#create figure for plots and set figure size/layout
f = Figure(figsize=(8.6,17.5), dpi=100)
f.subplots_adjust(top=0.993, bottom=0.015)
#plots
plot1 = f.add_subplot(6,2,1)
plot2 = f.add_subplot(6,2,2)
plot3 = f.add_subplot(6,2,3)
plot4 = f.add_subplot(6,2,4)
plot5 = f.add_subplot(6,2,5)
plot6 = f.add_subplot(6,2,6)
plot7 = f.add_subplot(6,2,7)
plot8 = f.add_subplot(6,2,8)
plot9 = f.add_subplot(6,2,9)
plot10 = f.add_subplot(6,2,10)
plot11 = f.add_subplot(6,2,11)
#set file path
file_path = "/Users/Bill Yen/Desktop/NU Urban Ag/test3.csv"
#animate function
def animate(ii):
    pullData = open(file_path,"r").read()
    dataList = pullData.split('\n')
    open(file_path,"r").close()
    #setting timeframe and making sure GUI runs on short CSVs too
    input_file = open(file_path, "r")
    reader_file = csv.reader(input_file)
    dataLen = len(list(reader_file))
    if dataLen < 240:
        timeframe = -dataLen
    else:
        timeframe = int(-240)
    input_file.close()
    #make all the x and y variable lists
    dataList = dataList[timeframe:]
    tList = []
    vList = []
    v1List = []
    for eachLine in dataList:
        if len(eachLine) >1:
            timedate, voltage, voltage1 = eachLine.split(',')
            tList.append(datetime.datetime.strptime(timedate, "%m/%d/%Y %H:%M:%S"))
            vList.append(float(voltage))
            v1List.append(float(voltage1))
            #keep the lists to a reasonable length to save memory
            tList = tList[timeframe:]
            vList = vList[timeframe:]
            v1List = v1List[timeframe:]
    #plot graphs
    plot1.clear()
    plot2.clear()
    #plot1.plot(tList, vList, 'r')
    #plot2.plot(tList, v1List, 'b')
    #this is to get the reference to fill the graph, can change to more meaningful
    #values later so we can change graph fill color based on water parameter
    listofzeros = [0] * len(tList)
    #add labels and config axis
    plot1.set_ylabel("pH (v)")
    plot1.set_ylim(2,4)
    plot2.set_ylabel("Temperature (v)")
    plot2.set_ylim(0,5)
    #show half the length of our timeframe, set functionality to let user scroll
    #to next half later
    plot1.set_xlim(tList[int(timeframe/2)], tList[-1])
    plot2.set_xlim(tList[int(timeframe/2)], tList[-1])
    #slant the x axis tick labels for extra coolness
    for label in plot1.xaxis.get_ticklabels():
        label.set_rotation(10)
    for label in plot2.xaxis.get_ticklabels():
        label.set_rotation(10)
    #make sure the xticks aren't overlapping
    plot1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
    plot2.xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
    #fill the graphs
    plot1.fill_between(tList, vList,
                       where=(vList > listofzeros),
                       facecolor = 'r', edgecolor = 'r', alpha = 0.5)
    plot2.fill_between(tList, v1List,
                       where=(v1List > listofzeros),
                       facecolor = 'b', edgecolor = 'b', alpha = 0.5)
    #collect garbage
    gc.collect()

#initialization
class AllWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #add title
        tk.Tk.wm_title(self, "NU Aquaponics")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #create navigation menu
        menubar = tk.Menu(container)
        navimenu = tk.Menu(menubar, tearoff=0)
        #add new items in navimenu to navigate to pages
        navimenu.add_command(label="Dashboard", command=lambda: self.show_frame(HomePage))
        navimenu.add_command(label="Control Panel", command=lambda: self.show_frame(ControlPanel))
        navimenu.add_command(label="Video Stream", command=lambda: self.show_frame(VideoStream))
        navimenu.add_command(label="Settings", command=lambda: self.show_frame(Settings))
        #add separator line
        navimenu.add_separator()
        #add quit button in menu that triggers a command
        navimenu.add_command(label="Quit", command=self.die)
        #actually add the bar
        menubar.add_cascade(label="Menu", menu=navimenu)

        tk.Tk.config(self, menu=menubar)

        #show the frames
        self.frames = {}
        #remember to add page to this list when making new ones
        for F in (HomePage, ControlPanel, Settings, VideoStream):
            frame = F(container, self)
            #set background color for the pages
            frame.config(bg='white')
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    #end program fcn triggered by quit button
    def die(self):
        exit()


#add home page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #bring up vertical scroll frame and place it
        scframe = VerticalScrolledFrame(self)
        scframe.place(x=130, y=40)
        #bring up canvas with plot in the frame with vertical scroll bar
        canvas = FigureCanvasTkAgg(f, scframe.interior)
        canvas.draw()
        #create title label
        label = tk.Label(self, text="Dashboard", bg='white', font = TITLE_FONT)
        label.place(x=460, y=10)
        #embed graph into canvas
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        #add navigation bar
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        #color variables
        pHcolor = "white"
        #data table labels
        table_title = tk.Label(self, text="Data Summary", bg="white", font = LARGE_FONT)
        table_title.place(x=28, y=40)
        leak_label = tk.Label(self, text="Leakage", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        leak_label.place(x=5, y=65)
        waterlvl_label = tk.Label(self, text="Water Level", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        waterlvl_label.place(x=5, y=87)
        pH_label = tk.Label(self, text="pH", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        pH_label.place(x=5, y=109)
        wtemp_label = tk.Label(self, text="Water Temp", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        wtemp_label.place(x=5, y=131)
        atemp_label = tk.Label(self, text="Air Temp", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        atemp_label.place(x=5, y=153)
        NO3_label = tk.Label(self, text="Nitrate", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        NO3_label.place(x=5, y=175)
        TDS_label = tk.Label(self, text="TDS", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        TDS_label.place(x=5, y=197)
        DO_label = tk.Label(self, text="DO", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        DO_label.place(x=5, y=219)
        NH3_label = tk.Label(self, text="Ammonia", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        NH3_label.place(x=5, y=241)
        PO4_label = tk.Label(self, text="Phosphate", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        PO4_label.place(x=5, y=263)
        humidity_label = tk.Label(self, text="Humidity", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        humidity_label.place(x=5, y=285)
        flowrate_label = tk.Label(self, text="Flow Rate", fg="black", bg=pHcolor,
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1, anchor=W, justify=LEFT)
        flowrate_label.place(x=5, y=307)
        #updating live texts
        leak_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        leak_data.place(x=91, y=65)
        waterlvl_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        waterlvl_data.place(x=91, y=87)
        pH_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        pH_data.place(x=91, y=109)
        wtemp_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        wtemp_data.place(x=91, y=131)
        atemp_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        atemp_data.place(x=91, y=153)
        NO3_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        NO3_data.place(x=91, y=175)
        TDS_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        TDS_data.place(x=91, y=197)
        DO_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        DO_data.place(x=91, y=219)
        NH3_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        NH3_data.place(x=91, y=241)
        PO4_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        PO4_data.place(x=91, y=263)
        humidity_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        humidity_data.place(x=91, y=285)
        flowrate_data = tk.Label(self, text="Loading", fg="black", bg="white",
                            font = MEDIUM_FONT, borderwidth = 2, relief = "ridge",
                            width=10, height=1)
        flowrate_data.place(x=91, y=307)
#function to update live text
        def GetValues():
            pullData = open(file_path,"r").read()
            dataList = pullData.split('\n')
            for eachLine in dataList:
                if len(eachLine) >1:
                    #add to this list of data read as we add more sensors
                    timedate, voltage, voltage1 = eachLine.split(',')
                    pH_data.config(text = voltage)
                    wtemp_data.config(text = voltage1)
            open(file_path,"r").close()
            gc.collect()
            self.after(5000, GetValues)
        self.after(5000, GetValues)

#add control panel page
class ControlPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    #text labels
        Title = tk.Label(self, text="Control Panel", bg= 'white', font = TITLE_FONT)
        Title.pack(pady=10, padx=10)
        ChannelTitle = tk.Label(self, text="Channel Overrides", bg='white', font = MEDIUM_FONT)
        ChannelTitle.place(x=108, y=90)
    #channel labels
        Channel_1 = tk.Label(self, text="1", bg='white', font = SMALL_FONT)
        Channel_1.place(x=38, y=122)
        Channel_2 = tk.Label(self, text="2", bg='white', font = SMALL_FONT)
        Channel_2.place(x=38, y=157)
        Channel_3 = tk.Label(self, text="3", bg='white', font = SMALL_FONT)
        Channel_3.place(x=38, y=192)
        Channel_4 = tk.Label(self, text="4", bg='white', font = SMALL_FONT)
        Channel_4.place(x=38, y=227)
        Channel_5 = tk.Label(self, text="5", bg='white', font = SMALL_FONT)
        Channel_5.place(x=38, y=262)
        Channel_6 = tk.Label(self, text="6", bg='white', font = SMALL_FONT)
        Channel_6.place(x=38, y=297)
        Channel_7 = tk.Label(self, text="7", bg='white', font = SMALL_FONT)
        Channel_7.place(x=38, y=332)
        Channel_8 = tk.Label(self, text="8", bg='white', font = SMALL_FONT)
        Channel_8.place(x=38, y=367)
        Channel_9 = tk.Label(self, text="9", bg='white', font = SMALL_FONT)
        Channel_9.place(x=283, y=122)
        Channel_10 = tk.Label(self, text="10", bg='white', font = SMALL_FONT)
        Channel_10.place(x=283, y=157)
        Channel_11 = tk.Label(self, text="11", bg='white', font = SMALL_FONT)
        Channel_11.place(x=283, y=192)
        Channel_12 = tk.Label(self, text="12", bg='white', font = SMALL_FONT)
        Channel_12.place(x=283, y=227)
        Channel_13 = tk.Label(self, text="13", bg='white', font = SMALL_FONT)
        Channel_13.place(x=283, y=262)
        Channel_14 = tk.Label(self, text="14", bg='white', font = SMALL_FONT)
        Channel_14.place(x=283, y=297)
        Channel_15 = tk.Label(self, text="15", bg='white', font = SMALL_FONT)
        Channel_15.place(x=283, y=332)
        Channel_16 = tk.Label(self, text="16", bg='white', font = SMALL_FONT)
        Channel_16.place(x=283, y=367)
    #relay control buttons
        #relays 1-8
        self.channelButton1 = tk.Button(self, text="Channel OFF",
                                        bg= "red", fg= "white",
                                        width=10, height=1,
                                        command=self.channel_1)
        self.channelButton1.place(x=50, y=115)
        self.channelButton2 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_2)
        self.channelButton2.place(x=50, y=150)
        self.channelButton3 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_3)
        self.channelButton3.place(x=50, y=185)
        self.channelButton4 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_4)
        self.channelButton4.place(x=50, y=220)
        self.channelButton5 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_5)
        self.channelButton5.place(x=50, y=255)
        self.channelButton6 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_6)
        self.channelButton6.place(x=50, y=290)
        self.channelButton7 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_7)
        self.channelButton7.place(x=50, y=325)
        self.channelButton8 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_8)
        self.channelButton8.place(x=50, y=360)
        #relays 9-16
        self.channelButton9 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_9)
        self.channelButton9.place(x=170, y=115)
        self.channelButton10 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_10)
        self.channelButton10.place(x=170, y=150)
        self.channelButton11 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_11)
        self.channelButton11.place(x=170, y=185)
        self.channelButton12 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_12)
        self.channelButton12.place(x=170, y=220)
        self.channelButton13 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_13)
        self.channelButton13.place(x=170, y=255)
        self.channelButton14 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_14)
        self.channelButton14.place(x=170, y=290)
        self.channelButton15 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_15)
        self.channelButton15.place(x=170, y=325)
        self.channelButton16 = tk.Button(self, text="Channel OFF",
                                         bg= "red", fg= "white",
                                         width=10, height=1,
                                         command=self.channel_16)
        self.channelButton16.place(x=170, y=360)

        #navigation button
        navibutton1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(HomePage))
        navibutton1.pack()
        OptionList = [
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
        ]

        dropon1=tk.OptionMenu(self, "Turn On", *OptionList)
        dropon1.config(width=10, font=SMALL_FONT)
        dropon1.place(x=570,y=122)

        #fcns triggered by control button
        #fcn to turn LED on or off
    def channel_1(self):
        #if LED1.value == 0:
        #    LED1.value = 1
        if self.channelButton1.cget('bg') == "red":
        #change light button color
            self.channelButton1.configure(bg= "green")
            self.channelButton1.configure(text = "Channel ON")
        else:
            #LED1.value = 0
        #change light button color to red if light off
            self.channelButton1.configure(bg= "red")
            self.channelButton1.configure(text = "Channel OFF")
    def channel_2(self):
        if self.channelButton2.cget('bg') == "red":
        #change light button color
            self.channelButton2.configure(bg= "green")
            self.channelButton2.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton2.configure(bg= "red")
            self.channelButton2.configure(text = "Channel OFF")
    def channel_3(self):
        if self.channelButton3.cget('bg') == "red":
        #change light button color
            self.channelButton3.configure(bg= "green")
            self.channelButton3.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton3.configure(bg= "red")
            self.channelButton3.configure(text = "Channel OFF")
    def channel_4(self):
        if self.channelButton4.cget('bg') == "red":
        #change light button color
            self.channelButton4.configure(bg= "green")
            self.channelButton4.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton4.configure(bg= "red")
            self.channelButton4.configure(text = "Channel OFF")
    def channel_5(self):
        if self.channelButton5.cget('bg') == "red":
        #change light button color
            self.channelButton5.configure(bg= "green")
            self.channelButton5.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton5.configure(bg= "red")
            self.channelButton5.configure(text = "Channel OFF")
    def channel_6(self):
        if self.channelButton6.cget('bg') == "red":
        #change light button color
            self.channelButton6.configure(bg= "green")
            self.channelButton6.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton6.configure(bg= "red")
            self.channelButton6.configure(text = "Channel OFF")
    def channel_7(self):
        if self.channelButton7.cget('bg') == "red":
        #change light button color
            self.channelButton7.configure(bg= "green")
            self.channelButton7.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton7.configure(bg= "red")
            self.channelButton7.configure(text = "Channel OFF")
    def channel_8(self):
        if self.channelButton8.cget('bg') == "red":
        #change light button color
            self.channelButton8.configure(bg= "green")
            self.channelButton8.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton8.configure(bg= "red")
            self.channelButton8.configure(text = "Channel OFF")
    def channel_9(self):
        if self.channelButton9.cget('bg') == "red":
        #change light button color
            self.channelButton9.configure(bg= "green")
            self.channelButton9.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton9.configure(bg= "red")
            self.channelButton9.configure(text = "Channel OFF")
    def channel_10(self):
        if self.channelButton10.cget('bg') == "red":
        #change light button color
            self.channelButton10.configure(bg= "green")
            self.channelButton10.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton10.configure(bg= "red")
            self.channelButton10.configure(text = "Channel OFF")
    def channel_11(self):
        if self.channelButton11.cget('bg') == "red":
        #change light button color
            self.channelButton11.configure(bg= "green")
            self.channelButton11.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton11.configure(bg= "red")
            self.channelButton11.configure(text = "Channel OFF")
    def channel_12(self):
        if self.channelButton12.cget('bg') == "red":
        #change light button color
            self.channelButton12.configure(bg= "green")
            self.channelButton12.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton12.configure(bg= "red")
            self.channelButton12.configure(text = "Channel OFF")
    def channel_13(self):
        if self.channelButton13.cget('bg') == "red":
        #change light button color
            self.channelButton13.configure(bg= "green")
            self.channelButton13.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton13.configure(bg= "red")
            self.channelButton13.configure(text = "Channel OFF")
    def channel_14(self):
        if self.channelButton14.cget('bg') == "red":
        #change light button color
            self.channelButton14.configure(bg= "green")
            self.channelButton14.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton14.configure(bg= "red")
            self.channelButton14.configure(text = "Channel OFF")
    def channel_15(self):
        if self.channelButton15.cget('bg') == "red":
        #change light button color
            self.channelButton15.configure(bg= "green")
            self.channelButton15.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton15.configure(bg= "red")
            self.channelButton15.configure(text = "Channel OFF")
    def channel_16(self):
        if self.channelButton16.cget('bg') == "red":
        #change light button color
            self.channelButton16.configure(bg= "green")
            self.channelButton16.configure(text = "Channel ON")
        else:
        #change light button color to red if light off
            self.channelButton16.configure(bg= "red")
            self.channelButton16.configure(text = "Channel OFF")

#add settings page
class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Settings", bg='white', font = TITLE_FONT)
        label.pack(pady=10, padx=10)
        #navigation button
        navibutton1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(HomePage))
        navibutton1.pack()
        navibutton2 = ttk.Button(self, text="Go to Control Panel",
                            command=lambda: controller.show_frame(ControlPanel))
        navibutton2.pack()
#add Video Stream page
class VideoStream(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Video Stream", bg='white', font = TITLE_FONT)
        label.pack(pady=10, padx=10)
        #navigation button
        navibutton1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(HomePage))
        navibutton1.pack()

app = AllWindow()
app.geometry('1025x672')
#this makes app full screen, not sure if it's good for us or not
#app.attributes('-fullscreen', True)
#update animation first
ani = animation.FuncAnimation(f, animate, interval=5000)
#mainloop
app.mainloop()