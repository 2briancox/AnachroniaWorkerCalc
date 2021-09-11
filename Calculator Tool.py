#!/usr/bin/env python3
# coding: utf-8
# Copyright 2009-2021 Brian Cox http://briancox.online
import tkinter as tk
import pygubu, os
from datetime import datetime, timedelta



class Application:
   
   def __init__(self, master):
      self.version = "1.0"
      self.releaseDate = "September 11, 2021"
      self.fullPath = str(os.path.dirname(os.path.realpath(__file__)))
      self.master = master
      self.builder = builder = pygubu.Builder()
      builder.add_from_file('{}\\Resources\\GUI.ui'.format(self.fullPath))
      self.mainwindow = builder.get_object('frame1', master)
      
      self.resource1Var = tk.StringVar(master)
      self.resource2Var = tk.StringVar(master)
      self.resource3Var = tk.StringVar(master)
      self.goalVar = tk.StringVar(master)
      
      self.goodChars = "0123456789"
      
      self.entry_current1 = builder.get_object('entry_current1', master)
      self.entry_current2 = builder.get_object('entry_current2', master)
      self.entry_current3 = builder.get_object('entry_current3', master)
      self.entry_goal = builder.get_object('entry_goal', master)
      
      self.entry_current1.configure(validate="key", textvariable = self.resource1Var)
      self.entry_current2.configure(validate="key", textvariable = self.resource2Var)
      self.entry_current3.configure(validate="key", textvariable = self.resource3Var)
      self.entry_goal.configure(validate="key", textvariable = self.goalVar)
      
      self.resource1Var.trace_add('write', self.resource1StringUpdater)
      self.resource2Var.trace_add('write', self.resource2StringUpdater)
      self.resource3Var.trace_add('write', self.resource3StringUpdater)
      self.goalVar.trace_add('write', self.goalStringUpdater)
      
      self.entry_units1 = builder.get_object('entry_units1', master)
      self.entry_units2 = builder.get_object('entry_units2', master)
      self.entry_units3 = builder.get_object('entry_units3', master)
      self.entry_units1.configure(state = tk.DISABLED)
      self.entry_units2.configure(state = tk.DISABLED)
      self.entry_units3.configure(state = tk.DISABLED)

      self.label_time1 = builder.get_object('label_time1', master)
      self.label_time2 = builder.get_object('label_time2', master)
      self.label_time3 = builder.get_object('label_time3', master)
      self.label_totaltime = builder.get_object('label_totaltime', master)

      self.selectedRadio = tk.IntVar(master)
      self.radiobutton1 = builder.get_object('radiobutton1', master)
      self.radiobutton2 = builder.get_object('radiobutton2', master)
      self.radiobutton3 = builder.get_object('radiobutton3', master)
      self.radiobutton1.configure(variable = self.selectedRadio, command = self.changeRadio, value = 10)
      self.radiobutton2.configure(variable = self.selectedRadio, command = self.changeRadio, value = 30)
      self.radiobutton3.configure(variable = self.selectedRadio, command = self.changeRadio, value = 60)

      self.selectedRadio.set(60)
      builder.connect_callbacks(self)
   
   
   def resource1StringUpdater(self, *args):
      newstring = ""
      if self.resource1Var.get()[:1] == "0":
         self.resource1Var.set("0")
         return
      for char in self.resource1Var.get():
         if char in self.goodChars:
            newstring += char
      self.resource1Var.set(newstring)
      self.calculate()
      return
   
   
   def resource2StringUpdater(self, *args):
      newstring = ""
      if self.resource2Var.get()[:1] == "0":
         self.resource2Var.set("0")
         return
      for char in self.resource2Var.get():
         if char in self.goodChars:
            newstring += char
      self.resource2Var.set(newstring)
      self.calculate()
      return
   
   
   def resource3StringUpdater(self, *args):
      newstring = ""
      if self.resource3Var.get()[:1] == "0":
         self.resource3Var.set("0")
         return
      for char in self.resource3Var.get():
         if char in self.goodChars:
            newstring += char
      self.resource3Var.set(newstring)
      self.calculate()
      return
   
   
   def goalStringUpdater(self, *args):
      newstring = ""
      if self.goalVar.get()[:1] == "0":
         self.goalVar.set("0")
         return
      for char in self.goalVar.get():
         if char in self.goodChars:
            newstring += char
      self.goalVar.set(newstring)
      self.calculate()
      return
   
      
   
   def calculate(self):
      
      if self.resource1Var.get() == "":
         self.label_totaltime['text'] = "Waiting for input ..."
         return
      if self.resource2Var.get() == "":
         self.label_totaltime['text'] = "Waiting for input ..."
         return
      if self.resource3Var.get() == "":
         self.label_totaltime['text'] = "Waiting for input ..."
         return
      if self.goalVar.get() == "":
         self.label_totaltime['text'] = "Waiting for input ..."
         return
      workers = self.selectedRadio.get()
      self.entry_units1.configure(state = tk.NORMAL)
      self.entry_units2.configure(state = tk.NORMAL)
      self.entry_units3.configure(state = tk.NORMAL)
      
      current1 = float(self.entry_current1.get())
      current2 = float(self.entry_current2.get())
      current3 = int(self.entry_current3.get())
      
      goal = float(self.entry_goal.get())
      if not goal>0:
         return
      
      longest = 0.0
      shortest = 99999999999999999999999999999
      unit1 = 1
      unit2 = 1
      unit3 = 1
      time1 = 0
      time2 = 0
      time3 = 0
      
      for x in range(0,workers + 1):
         for y in range(0, workers + 1):
            z = workers - x - y
            if z < 0:
               continue
            
            if current1 < goal:
               if x!=0:
                  t1 = int(3600*(goal - current1) / (60*x))
               else:
                  t1 = 99999999999999999999
            else:
               t1=0
            
            if current2 < goal:
               if y!=0:
                  t2 = int(3600*(goal - current2) / (60*y))
               else:
                  t2 = 99999999999999999999
            else:
               t2 = 0
               
            if current3 < goal:
               if z!=0:
                  t3 = int(3600*(goal - current3) / (60*z))
               else:
                  t3 = 99999999999999999999
            else:
               t3 = 0
            
            if t1 > t2 and t1 > t3:
               longest = t1
            elif t2 > t3:
               longest = t2
            else:
               longest = t3
               
            if longest < shortest:
               shortest = longest
               unit1 = x
               unit2 = y
               unit3 = z
               time1 = t1
               time2 = t2
               time3 = t3
               
      if time1 > time2 and time1>time3:
         longest = time1
      elif time2 > time3:
         longest = time2
      else:
         longest = time3
      
      finishtime = datetime.now() + timedelta(seconds = shortest)
      self.label_totaltime['text'] = finishtime.strftime("If begun now, will finish on: \n\n%A, %B %d at around %I:%M %p")
      self.entry_units1.delete(0, tk.END)
      self.entry_units1.insert(0, str(unit1))
      self.entry_units2.delete(0, tk.END)
      self.entry_units2.insert(0, str(unit2))
      self.entry_units3.delete(0, tk.END)
      self.entry_units3.insert(0, str(unit3))
      hrs, mins = convert(time1)
      self.label_time1['text'] = "{} hours, {} minutes".format(hrs, mins)
      hrs, mins = convert(time2)
      self.label_time2['text'] = "{} hours, {} minutes".format(hrs, mins)
      hrs, mins = convert(time3)
      self.label_time3['text'] = "{} hours, {} minutes".format(hrs, mins)
      
      self.entry_units1.configure(state = tk.DISABLED)
      self.entry_units2.configure(state = tk.DISABLED)
      self.entry_units3.configure(state = tk.DISABLED)
      
      self.master.update()
      return
      
   def changeRadio(self):
      self.calculate()
      return
   


def convert(seconds):
   hrs = seconds // 3600
   secs = seconds % 3600
   mins = secs // 60
   return (hrs, mins)

    
      
if __name__ == '__main__':
   root = tk.Tk()
   app = Application(root)
   fullPath = str(os.path.dirname(os.path.realpath(__file__)))
   root.title('Unit Calculator')
   root.resizable(False, False)
   root.mainloop()
