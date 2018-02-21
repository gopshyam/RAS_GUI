from pyqtgraph import QtCore, QtGui
import csv
import pyqtgraph as pg
from datetime import datetime
import sys
import numpy as np
import sched, time
import threading

class Radiodemo(QtGui.QWidget):

   def __init__(self, parent = None):
      super(Radiodemo, self).__init__(parent)
        
      layout = QtGui.QHBoxLayout()
      self.b1 = QtGui.QRadioButton("Button1")
      self.b1.setChecked(True)
      self.b1.toggled.connect(lambda:self.btnstate(self.b1))
      layout.addWidget(self.b1)
        
      self.b2 = QtGui.QRadioButton("Button2")
      self.b2.toggled.connect(lambda:self.btnstate(self.b2))

      layout.addWidget(self.b2)
      self.setLayout(layout)
      self.setWindowTitle("RadioButton demo")
        
   def btnstate(self,b):
    
      if b.text() == "Button1":
         if b.isChecked() == True:
            print b.text()+" is selected"
         else:
            print b.text()+" is deselected"
                
      if b.text() == "Button2":
         if b.isChecked() == True:
            print b.text()+" is selected"
         else:
            print b.text()+" is deselected"
                
def main():

   app = QtGui.QApplication(sys.argv)
   ex = Radiodemo()
   ex.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()
