import tkinter as tk
from tkinter import ttk
import json

with open("result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

current_index = 0
sed_state = 1#show_eng_def button的state，1代表沒有顯示，2代表有顯示
scd_state = 1#show_eng_def button的state，1代表沒有顯示，2代表有顯示
sb_state = 1#show_button的state，1代表沒有顯示中文解釋2代表有顯示
labels = {}
buttons = {}
show_btn_states = [1, 1, 1, 1, 1, 1, 1, 1, 1]
length = len(data)
    
def move_to_next():#顯示下一個句子
    global current_index #宣告以下的current_index是global變數
    global sb_state
    # print(current_index)#測試用
    # print(length)
    current_index = current_index + 1
    if current_index == length:#length為data長度
        current_index = 0
    t = data[current_index]["word"]#取出data中的word
    t_pos = data[current_index]["POS"]#取出data中的word
    title.config(text = t)#顯示在title
    pos_title.config(text = 'POS : ' + t_pos)#顯示在title
    renew()


def renew():
    #指定以下變數是指global變數
    global sed_state
    global scd_state
    global middle_frame
    global show_btn_states
    sed_state = 1
    scd_state = 1
    eng_def.config(text = "English explanation")
    chi_def.config(text = "Chinese explanation")
    eng_def_button.config(text = "show")#
    chi_def_button.config(text = "show")
    if middle_frame:  # 如果之前有建 frame，就先刪掉
        middle_frame.destroy()
    show_btn_states = [1 for _ in show_btn_states]#把middle_frame中所有button的state設為1
    middle_frame = ttk.Frame(window)#以下為建立新的middle_frame
    for i in range(len(data[current_index]["chi_sen"])):
        middle_frame.pack(anchor='nw', padx=5, pady= 5)
        eng_label = tk.Label(middle_frame, text = data[current_index]["eng_sen"][i], width= 70, bg = "gray")
        eng_label.pack(anchor='nw')
        test_frame = ttk.Frame(middle_frame)
        test_frame.pack()
        labelname = tk.Label(test_frame, text = "translation", bg = 'gray', width=70)
        buttonname = tk.Button(test_frame, text = 'show', width = 20)
        buttonname.config(command=lambda i=i: show_chi_sen(i))
        labelname.pack(side = 'left')
        buttonname.pack(side = 'right')
        labels[i] = labelname
        buttons[i] = buttonname
    
def discard():
    global current_index
    global middle_frame
    global length
    del data[current_index]
    if current_index == length - 1:#length為data長度
        current_index = 0
    t = data[current_index]["word"]
    title.config(text = t)
    length = length - 1
    renew()

def move_to_prev():#顯示前一個句子
    global current_index #宣告以下的b是global的b
    global sb_state
    if current_index == -1:
        current_index = length - 1
        
    if middle_frame:  # 如果之前有建 frame，就先刪掉
        middle_frame.destroy()
    current_index = current_index - 1
    t = data[current_index]["word"]#取出data中的word
    t_pos = data[current_index]["POS"]#取出data中的word
    title.config(text = t)#顯示在title
    pos_title.config(text = 'POS : ' + t_pos)#顯示在title
    renew()

def show_eng_def():
    global current_index
    global sed_state
    if(sed_state == 1):
        t = data[current_index]["eng_def"]
        eng_def.config(text = t)
        sed_state = 2
        eng_def_button.config(text = 'hide')
    else:
        eng_def.config(text = "English explanation")
        sed_state = 1
        eng_def_button.config(text = 'show')
def show_chi_def():
    global current_index
    global scd_state
    if(scd_state == 1):
        t = data[current_index]["chi_def"]
        chi_def.config(text = t)
        scd_state = 2
        chi_def_button.config(text = 'hide')
    else:
        chi_def.config(text = "Chinese explanation")
        scd_state = 1
        chi_def_button.config(text = 'show')

def show_chi_sen(num):
    global current_index
    global show_btn_states
    if(show_btn_states[num] == 1):
        labels[num].config(text = data[current_index]["chi_sen"][num])
        buttons[num].config(text = 'hide')
        show_btn_states[num] = 2
    else:
        labels[num].config(text = "translation")
        buttons[num].config(text = 'show')
        show_btn_states[num] = 1

def save_and_leave():
    with open("result.json", "w", encoding="utf-8") as f2:
        json.dump(data, f2, ensure_ascii=False, indent=2)
    window.destroy()
    


#window
window = tk.Tk()
window.title('Layout intro')
window.geometry('600x400')

#top frame
top_frame = ttk.Frame(window)
titile_frame = ttk.Frame(top_frame)
title = tk.Label(titile_frame, text = data[current_index]["word"], background = 'gray', width= 20)#放單字
pos_title = tk.Label(titile_frame, text = 'POS : ' + data[current_index]["POS"], background = 'gray', width= 20)

top_eng_frame = ttk.Frame(top_frame)
eng_def = tk.Label(top_eng_frame, text = "English explanation", background = 'gray', wraplength=350, height = 3)#放英文解釋
eng_def_button = ttk.Button(top_eng_frame, text = "show")
eng_def_button.config(command=show_eng_def)

top_chi_frame = ttk.Frame(top_frame)
chi_def = tk.Label(top_chi_frame, text = "Chienese explanation", background = 'white', wraplength=350)#放中文解釋
chi_def_button = ttk.Button(top_chi_frame, text = "show")
chi_def_button.config(command=show_chi_def)
#middle widgets

# label3 = ttk.Label(window, text = 'label 3', background = 'green')

#bottome frame
bottom_frame = ttk.Frame(window)
label4 = ttk.Label(bottom_frame, text = 'label 4', background = 'orange')
button = ttk.Button(bottom_frame, text = 'previous', width=20)

# button2 = ttk.Button(bottom_frame, text = 'show explanation', width=20)
# button2.config(command = show_exp)
button3 = ttk.Button(bottom_frame, text = 'next', width=20)
del_button = ttk.Button(bottom_frame, text = 'got it')
save_button = ttk.Button(bottom_frame, text = 'save and leave')
#packs
# label1.pack(side = 'left')
# label2.pack()

#top_frame
top_frame.pack(fill = 'both')
titile_frame.pack(side = 'left', anchor="nw")
title.pack(side = 'top', anchor="nw", pady=10, padx=10)
pos_title.pack(side = 'top', anchor="w", fill = 'both', padx=10)
top_eng_frame.pack(side = 'top', fill = 'x')
eng_def_button.pack(side = 'right', anchor = "ne")
eng_def.pack(side = 'right',  expand = True, fill = 'x')
top_chi_frame.pack(side = 'top', fill = 'x')
chi_def_button.pack(side = 'right', anchor = "ne")
chi_def.pack(side = 'right',  fill = 'x', expand = True)

#middle frame
# middle_frame = ttk.Frame(window)
# middle_frame.pack()
# for i in range(2):
#     out_frame = ttk.Frame(middle_frame)

#     # label = tk.Label(middle_frame, text = "hello", bg = "gray")
#     # label.pack(fill = 'x', pady= 1)
#     eng_sen_label = tk.Label(out_frame)

# def destroy_and_create():

#     move_to_next()
global middle_frame
middle_frame = ttk.Frame(window)
for i in range(len(data[current_index]["chi_sen"])):
    middle_frame.pack(anchor='nw', padx=5, pady= 5)
    eng_label = tk.Label(middle_frame, text = data[current_index]["eng_sen"][i], width= 70, bg = "gray")
    eng_label.pack(anchor='nw')
    test_frame = ttk.Frame(middle_frame)
    test_frame.pack()
    labelname = tk.Label(test_frame, text = "traslation", bg = 'gray', width=70)
    buttonname = tk.Button(test_frame, text = 'show', width = 20)
    buttonname.config(command=lambda i=i: show_chi_sen(i))
    labelname.pack(side = 'left')
    buttonname.pack(side = 'right')
    labels[i] = labelname
    buttons[i] = buttonname

#bottom layout
bottom_frame.pack(side = 'bottom', pady=20)
button.pack(side = 'left', padx = 10)
button.config(command = move_to_prev)
# button2.pack(side = 'left', padx = 10)
button3.config(command = move_to_next)
button3.pack(side = 'left', padx = 10)
del_button.config(command= discard)
del_button.pack(side = 'left')
save_button.config(command= save_and_leave)
save_button.pack(side = 'left')
#run
window.mainloop()
