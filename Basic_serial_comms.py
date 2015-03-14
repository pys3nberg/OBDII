__author__ = 'Pysenberg'
#comms with elm327

import serial
from serial.tools import list_ports as lp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import time


class MainProgram(tk.Tk):

    def __init__(self):
        # the main program class inherents the TK class
        tk.Tk.__init__(self)
        # make a frame
        self.frame = ttk.Frame(self)
        self.frame.grid(padx=5, pady=5)
        #  the combobox label
        ttk.Label(self.frame, text='COM PORT').grid(row=0)
        # set up the comport selection drop box, bind its event to the setComPort method
        self.com_selection = tk.StringVar()
        self.com_combo = ttk.Combobox(self.frame, textvariable=self.com_selection)
        self.com_combo.grid(row=1)
        self.com_combo['values'] = self.getcomports()
        self.com_combo.bind('<<ComboboxSelected>>', self.set_com_port)
        # make a connect button and bind it to serialComStart method
        self.connect_button = ttk.Button(self.frame, text='Connect', command=self.serial_com_start)
        self.connect_button.grid(row=2, padx=3, pady=3)
        # message entry box
        ttk.Label(self.frame, text='Send').grid(row=3)
        self.message_in = tk.StringVar()
        self.serial_message_entry = ttk.Entry(self.frame, textvariable=self.message_in).grid(row=4)
        # send button
        self.send_button = ttk.Button(self.frame, text='Send', command=self.send_message).grid(row=5)
        # recieve window
        ttk.Label(self.frame, text='Recieve').grid(row=6)
        self.recieve_message = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.recieve_message).grid(row=7)

        self.protocol('WM_DELETE_WINDOW', self.appclosehandler)


    def getcomports(self):
        COM_PORTS = []
        for port in lp.comports():
            COM_PORTS.append(port[0])
        return COM_PORTS

    def set_com_port(self, event):
        print(self.com_selection.get())

    def serial_com_start(self):
        try:
            self.coms_ref = serial.Serial(self.com_selection.get(), baudrate=38400, timeout=1)
            print(self.coms_ref)
        except:
            msg.showerror(title='Comms Error',message='An invalid or no com port was selected!')

    def send_message(self):
        self.coms_ref.write(bytes(self.message_in.get()+'\r', 'UTF-8'))
        x = self.coms_ref.readline()
        print(x)


        #msg.showerror(title='Comms Error',message='An invalid or no com port was selected!')



    def appclosehandler(self):
        try:
            self.coms_ref.close()
            print('serial closed')
        except:
            print('no comms!')
        self.destroy()

if __name__ == '__main__':

    app = MainProgram()
    app.mainloop()



