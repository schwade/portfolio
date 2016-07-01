#!/usr/bin/env python3.5

### The tkinter module provides the core GUI tools for user interface.
from tkinter import *
### The inventory location file is a csv file.
import csv

# .pack() will place text in the center
# .place(x=0, y=0) will allow us to place the label on an x-y grid
# .grid(row=0,column=0, sticky=[N, S, E, W]) qill allow us to place things in rows and colums, will expand to text size

### The mInventory variable holds the shop's inventory database after each entry has been processed.
mInventory=[]

### Opens the shop's inventory file. It should be a .csv file with 4 headers: brand, yarn, location, and generalLocation.
with open('ssinventory.csv', 'rt') as minventoryfile:
    
    ###  Creates a reader object from the shop's inventory.
    reader = csv.reader(minventoryfile)
    ### The counter variable will determine the unique ID for each entry in the mInventory variable.
    counter=0
    
    ### Takes each entry from the shop's inventory and creates a corresponding entry in the mInvetory variable. These entries
    ### are tuples. Each tuple contains: 
    ###     (i) a unique ID number determined by the counter variable.
    ###     (ii) a tuple containing the entry's brand
    ###     (iii) a tuple containing the entry's yarn name
    ###     (iv) a tuple containing the entry's location
    ###     (v) a tuple containing the entry's generalLocation
    for row in reader:
        mInventory.append( (counter, [('brand',row[0]), ('yarn',row[1]), ('location',row[2]), ('generalLocation',row[3])]) )
        counter+=1

### Creates an instance of a tk widget.
mGui = Tk()
### Creates two string variables to be used 
keyBrand=StringVar()
keyYarn=StringVar()
### Defines the UI window size in pixles.
mGui.geometry('+600+250')
### Only for window's operating systems.
# mGuin.mainloop()
mGui.title('Yarn Location Search')


def findLocation():
    """
    Searches the shop's inventory for the location of a particular yarn, by yarn name or by brand.
    
    
    """
    mResultsWindow = Tk()
    mResultsWindow.title('Search Results')
    mResultsWindow.geometry('800x800+600+250')
    searchTerm1=keyBrand.get()
    searchTerm2=keyYarn.get()
    ### Attribute :: 0=brand, 1=yarn
    database=mInventory
    userResults='{0: <40}{1: <40}{2: <40}\n'.format('BRAND', 'YARN', 'LOCATION')
    for x in range(len(database)):
        if database[x][1][0][1].lower() == searchTerm1.lower():
            userResults+='{0: <30}\t{1: <30}\t{3} - {2} \n'.format(database[x][1][0][1],database[x][1][1][1],database[x][1][2][1],database[x][1][3][1])
        if database[x][1][1][1].lower() == searchTerm2.lower():
            userResults+='{0: <30}\t{1: <30}\t{3} - {2} \n'.format(database[x][1][0][1],database[x][1][1][1],database[x][1][2][1],database[x][1][3][1])
    
    Label(mResultsWindow,text=userResults, justify=LEFT).pack()

    

mbrand = Label(mGui,text='BRAND:', fg='purple').grid(row=0,column=0,sticky=E)
mbrandTextBox = Entry(mGui, textvariable=keyBrand).grid(row=0,column=1,sticky=W)
myarn = Label(mGui,text='YARN:', fg='blue').grid(row=1,column=0,sticky=E)
myarnTextBox = Entry(mGui, textvariable=keyYarn).grid(row=1,column=1,sticky=W)
mbutton = Button(mGui,text='Tell Me Where!', command=findLocation).grid(row=2,column=1)

       



