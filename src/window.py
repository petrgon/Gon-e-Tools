# Import the required libraries
from tkinter import *
import tkinter as tk # use QT for FE
from pystray import Menu, MenuItem
import pystray
from PIL import Image, ImageTk
import threading
from os import system

import constants

# UI for the app, defines Tray Icon and Window
class Window:
   _win = None
   _registeredOptions = None
   _text = None
   _icon = None
   _iconThread = None
   _exitThread = Event()
   _isWindowVisible = True

   def __init__(self):
      # Create an instance of tkinter frame or window
      self._win=Tk()
      self._win.title(constants.APP_NAME)
      self._win.iconbitmap(constants.ICON_PATH)

      system("title " + constants.APP_NAME)

      # Set the size of the window
      self._win.geometry("700x350")

      # Override default close button
      self._win.protocol('WM_DELETE_WINDOW', self.HideWindow)

      
      self._registeredOptions = (
         MenuItem('Hidden Default', self.ToggleWindow, default = True, visible = False), 
         MenuItem('Quit', self.QuitWindow), 
         MenuItem('Show Log', self.ShowWindow), 
         pystray.Menu.SEPARATOR
         )

      # Create textbox
      self._text = Text(self._win, height = 5, width = 52)
      label = Label(self._win, text = "Log")
      label.pack(side=TOP, anchor=NW)
      self._text.pack(side='top',fill='both',expand=True)

   # Define a function for quit the window
   def QuitWindow(self, icon, item):
      self._icon.stop()
      self._win.destroy()

   # Hides the log window if visible or shows it if not
   def ToggleWindow(self, icon, item):
      if self._isWindowVisible:
         self.HideWindow(icon, item)
      else:
         self.ShowWindow(icon, item)

   # Define a function to show the window again
   def ShowWindow(self, icon, item):
      self._win.after(0, self._win.deiconify())
      self._isWindowVisible = True

   # Hide the window and show on the system taskbar
   def HideWindow(self, icon = None, item = None):
      self._win.withdraw()
      self._isWindowVisible = False

   # Register new option for the icon.
   # Call without arguments to register DELIMITER.
   # Instead of callable argument, call with a tuple of pairs(name, callable) to register submenu
   def Register(self, name = None, callable = None, submenu = None):
      
      submenuItems = self._UnpackSubmenu(submenu)

      item = None
      if callable == None and name == None:
         item= pystray.Menu.SEPARATOR
      elif not submenuItems == None:
         item = MenuItem(name, Menu(*submenuItems))
      else:
         item = MenuItem(name, callable)
      
      # keep the , to make the item tuple
      self._registeredOptions += (item,)
      return item

   # Starts Icon and Window loops
   def Run(self):
      self._InitIcon()
      self._iconThread = threading.Thread(target=self._icon.run, daemon=True)
      self._iconThread.start()
      
      if(self._win != None):
         self._win.mainloop()

   # Prints text to Log window
   def Log(self, text):
      self._text.config(state=NORMAL)

      self._text.insert(tk.END, text)
      # Scroll to the end
      self._text.see(tk.END)
      self._text.edit_modified(0)

      self._text.config(state=DISABLED)

   # Shows Windows notification
   def Notify(self, text, title=None):
      self._icon.remove_notification()
      self._icon.notify(text, title)

   # Inits icon if not yet initialized
   def _InitIcon(self):
      if self._icon == None:
         image = Image.open(constants.ICON_PATH)
         menu = self._registeredOptions
         self._icon = pystray.Icon(constants.APP_NAME, image, constants.APP_NAME, menu)

   def _UnpackSubmenu(self, input = None):
      items = None
      if not input == None:
         items = ()
         for item in input:
            items += (MenuItem(item[0], item[1]),)
      return items
