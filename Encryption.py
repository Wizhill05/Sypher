import tkinter as tk
from tkinter import messagebox
import random
import string 
import pickle
import tkinter.font as font
import pyperclip

def Refresh():
    Dict={}
    alpha_list = list(string.printable)
    for i in alpha_list:
        temp = random.choice(alpha_list[:-6])+random.choice(alpha_list[:-6])
        while temp in Dict.values():
            temp = random.choice(alpha_list[:-6])+random.choice(alpha_list[:-6])
        Dict[i]=temp
    File = open("Keys.dat",'wb')
    pickle.dump(Dict,File)
    File.close()

def Encrypt(str,path = "Keys.dat"):
    File = open(path,'rb')
    dict=pickle.load(File)
    File.close()

    enc = ''
    for i in str:
        enc += dict[i]
    
    return enc

def Decrypt(str,path = "Keys.dat"):
    File = open(path,'rb')
    dict=pickle.load(File)
    File.close()

    dec = ''
    for i in range(0,len(str),2):
        val = list(dict.values())
        key = list(dict.keys())
        find = val.index(str[i]+str[i+1])
        dec += key[find]
    return dec

def Get():
    global Ans
    try:
        Ans=entry1.get()
        return Ans
    except SyntaxError:
        entry1.delete(0, tk.END)
        messagebox.showerror("Error","Invalid Submission")
    except NameError:
        entry1.delete(0, tk.END)
        messagebox.showerror("Error","Invalid Submission")

def enc():
    Output.config(text = Encrypt(Get()))
def dec():
    try:
        Output.config(text = Decrypt(Get()))
    except ValueError:
        entry1.delete(0, tk.END)
        messagebox.showerror("Error","Invalid Submission")

def copy():
    out = Output.cget("text")
    pyperclip.copy(out)
def refkey():
    if messagebox.askyesno("Are You Sure?","This will delete your old key so old messeges can not be decrypted"):
        messagebox.showinfo("Key Changed","Key Changed")
        Refresh()
    

if __name__=="__main__":
    Ans=""
    top = tk.Tk()
    top.title('Encryption')
    top.geometry("400x310")
    top.resizable(False,False)
    myFont = font.Font(size=10)
    tk.Label(top, text= "Encrypter - Decrypter", font=('Consolas', 20)).pack(pady=20)
    Text = tk.Label(text="Text:")
    entry1 = tk.Entry(fg="#111111", bg="#dddddd", width=44, font=('Consolas', 10))
    Out = tk.Label(text="Output:")
    Out.place(x=24, y=160)
    Text.place(x=24, y=80)
    entry1.place(x=64, y=80)
    Enc=tk.Button(
        text="Encrypt",
        width=20,
        height=1,
        bg="#333333",
        fg="#eeeeee",
        font="rod",
        activebackground="#999999",
        command=enc,
        highlightcolor="#000000",
        padx=1,
        pady=0
        )
    Enc['font']=myFont
    Enc.place(x=24,y=115)
    Dec=tk.Button(
        text="Decrypt",
        width=20,
        height=1,
        bg="#333333",
        fg="#eeeeee",
        font="rod",
        activebackground="#999999",
        command=dec,
        highlightcolor="#000000",
        padx=1,
        pady=0
        )
    Dec['font']=myFont
    Dec.place(x=208,y=115)
    copy=tk.Button(
        text="Copy",
        width=20,
        height=1,
        bg="#333333",
        fg="#eeeeee",
        font="rod",
        activebackground="#999999",
        command=copy,
        highlightcolor="#000000",
        padx=1,
        pady=0
        )
    copy['font']=myFont
    copy.place(x=24,y=265)
    ref=tk.Button(
        text="Refresh Key",
        width=20,
        height=1,
        bg="#ff4422",
        fg="#eeeeee",
        font="rod",
        activebackground="#999999",
        command=refkey,
        highlightcolor="#000000",
        padx=1,
        pady=0
        )
    
    ref['font']=myFont
    ref.place(x=208,y=265)
    Output = tk.Label(text="",font=('Consolas', 10), height=4, width=50, justify="left", anchor="nw", bg="#cccccc", wraplength=350)
    Output.place(x=23, y=185)
    top.mainloop()
