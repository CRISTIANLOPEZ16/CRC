from cProfile import label
from time import sleep
from tkinter import *
from tkinter import messagebox
from turtle import left
import socket	
import time
import random
key = "1001"
class PyClient(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.parent = master
        self.grid()
        self.createWidgets()

    def encodeData(self):
        global key, binary,response,send,result
                # Create a socket object
        s = socket.socket()	

        # Define the port on which you want to connect
        port = 12345		

        # connect to the server on local computer
        s.connect(('127.0.0.1', port))
        l_key = len(key)
        data=''.join(format(ord(x), 'b') for x in self.display.get())
        binary.set("Binary data : "+data)
        # Appends n-1 zeroes at end of data
        appended_data = data + '0'*(l_key-1)
        remainder = self.mod2div(appended_data, key)
        array = ["1-1=0","0-0=0","0-1=1","1-0=1"]
        for x in range(0,60):
            self.update()
            if x==0:
                result.set("Add 000")
                time.sleep(1.5)
            else:
                result.set(random.choice(array))  
                time.sleep(0.7)
        # Append remainder in the original data
        codeword = data + remainder
        #binary.set("Binary data : "+codeword) 
        send.set("Data sender : "+codeword)
        s.sendto(codeword.encode(),('127.0.0.1', port))
        self.update()
        for x in range(0,60):
            self.update()
            response.set("Enviando"+"-"*x+">")  
            time.sleep(0.05)  
        response.set("Received feedback from server :"+s.recv(1024).decode())
        
    def xor(self,a, b):

	# initialize result
        result = []

        # Traverse all bits, if bits are
        # same, then XOR is 0, else 1
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')

        return ''.join(result)


    # Performs Modulo-2 division
    def mod2div(self,divident, divisor):

        # Number of bits to be XORed at a time.
        pick = len(divisor)

        # Slicing the divident to appropriate
        # length for particular step
        tmp = divident[0 : pick]

        while pick < len(divident):

            if tmp[0] == '1':

                # replace the divident by the result
                # of XOR and pull 1 bit down
                tmp = self.xor(divisor, tmp) + divident[pick]
            else: # If leftmost bit is '0'

                # If the leftmost bit of the dividend (or the
                # part used in each step) is 0, the step cannot
                # use the regular divisor; we need to use an
                # all-0s divisor.
                tmp = self.xor('0'*pick, tmp) + divident[pick]
            # increment pick to move further
            pick += 1

        # For the last n bits, we have to carry it out
        # normally as increased value of pick will cause
        # Index Out of Bounds.
        if tmp[0] == '1':
            tmp = self.xor(divisor, tmp)
        else:
            tmp = self.xor('0'*pick, tmp)

        checkword = tmp
        return checkword

    def createWidgets(self):
        global binary,response,send,result
        self.label= Label(self,text="Input your data: ")
        self.label.grid(row=0, column=0, columnspan=1 ,sticky="nsew", padx=5, pady=5)
        self.display = Entry(self, font=("Arial", 24), relief=RAISED, justify=LEFT, bg='white', fg='black', borderwidth=0.5)
        self.display.insert(0, "")
        self.display.grid(row=0, column=1, columnspan=6, sticky="nsew",padx=5, pady=5)
        self.labelG= Label(self,text="Generados:1001 ")
        self.labelG.grid(row=2, column=0, columnspan=1 ,sticky="nsew", padx=5, pady=5)
        self.negToggleButton = Button(self, font=("Arial", 12), fg='black', bg='white', borderwidth=0.5, text="Calcular", highlightbackground='lightgrey',command=lambda: self.encodeData())
        self.negToggleButton.grid(row=1, column=6, sticky="nsew",padx=5, pady=5)
        binary = StringVar()
        self.label2= Label(self,textvariable = binary)
        self.label2.grid(row=3, column=0, columnspan=6 ,sticky="nsew", padx=5, pady=5)
        response = StringVar()
        self.label4= Label(self,textvariable = response)
        self.label4.grid(row=8, column=0, columnspan=6 ,sticky="nsew", padx=5, pady=5)
        send = StringVar()
        self.label3= Label(self,textvariable = send)
        self.label3.grid(row=4, column=0, columnspan=6 ,sticky="nsew", padx=5, pady=5)
        result = StringVar()
        self.label5= Label(self,textvariable = result)
        self.label5.grid(row=5, column=0, columnspan=6 ,sticky="nsew", padx=5, pady=5)



# create new view for the client   
    
cliente = Tk()
cliente.title("Cliente CRC")
cliente.configure(bg = 'white')

cliente.resizable(False, False)
root=PyClient(cliente).grid()

#execute the view
cliente.mainloop()