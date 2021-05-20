
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from get_TMs import get_TM_names_list
import pandas as pd
from datetime import datetime
import locale
from NewModule_Test import GetResponse as gr
import sys
import os


# Tkinter Window setup
window = tk.Tk()
window.geometry("800x800")
Title = tk.Label(text="Standard Customer responses", font='Helvetica 18 bold')

# Seperators
sep_TM_date = tk.Label(text="____________________________________\nWhen did the customer sent the email?", width=28)
sep_date_gender = tk.Label(text="____________________________________\nWhat's the customers gender?", width=28)
sep_gender_CustomerName = tk.Label(text="____________________________________\nWhat's the customers name?", width=28)
sep_CustomerName_Subject = tk.Label(text="____________________________________\nIhre Anfrage... vom", width=28)
sep_subj = tk.Label(text="z.B.: 'zur Bewerbung'", font='Helvetica 11 italic', width=28)
sep_subj_case = tk.Label(text="____________________________________\nWhat's the case number?", width=28)
sep_case_agent = tk.Label(text="____________________________________\nWhat's your name?", width=28)

locale.setlocale(locale.LC_ALL, 'de_DE')


def return_from_dropdown(dropdown):
    return dropdown.get()


# 1. TM Drop down Box
# def select_TM():
with open('New_TM.txt') as f:
    # Read the file fully and as string. Name it TM
    TM = f.read()
    # Split TM by "----------" to seperate each module
    modules = TM.split("----------")

TM = StringVar(window)
TM_titles = get_TM_names_list.get_TM_names(modules)
TM.set("Select your TM")  # default value
TM_dropdown = OptionMenu(window, TM, *TM_titles)
# return TM_dropdown


# 2. date
cal = Calendar(window)


def select_date():
    selected_date = ''
    date.config(text="Selected Date is: " + cal.get_date())
    selected_date = cal.get_date()
    sd = selected_date.split('/')
    sd = datetime(day=int(sd[1]), month=int(sd[0]), year=int(f'20{sd[2]}'))

    return sd.strftime('%d. %B %Y')
    # return selected_date


date = Label(window, text="")


# 3. gender
m = IntVar()
f = IntVar()
NA = IntVar()


def retrieve_gender():
    result = "male: %d,\nfemale: %d,\nNA: %d" % (m.get(), f.get(), NA.get())
    if m.get() == 1:
        return 'm'
    elif f.get() == 1:
        return 'f'
    elif NA.get() == 1:
        return 'NA'


# 4. name
name_text = tk.Text(window, height=2, width=30, highlightbackground='black')
name_text.insert(tk.END, "")


def retrieve_input(intext):
    input = intext.get("1.0", "end-1c")
    return input


name_submit = Button(window, height=1, width=10, text="Submit",
                     command=lambda: retrieve_input(name_text))


# 5. Subject_topic
subject_topic = tk.Text(window, height=2, width=30, highlightbackground='black')
subject_topic.insert(tk.END, "")

subject_submit = Button(window, height=1, width=10, text="Submit",
                        command=lambda: retrieve_input(subject_topic))


# 6. Case_number
case_num = tk.Text(window, height=2, width=30, highlightbackground='black')
case_num.insert(tk.END, "")

case_submit = Button(window, height=1, width=10, text="Submit",
                     command=lambda: retrieve_input(case_num))


# 7. Porsche Zentrum
#def select_PZ():
location = []
PZ_list = pd.read_excel(r"Porsche_Zentren.xlsx")
df = pd.DataFrame(PZ_list)

PZ = StringVar(window)
PZ_titles = get_TM_names_list.get_PZ_list(df)

for index, row in df.iterrows():
    location.append(row['PZ-Name1'])

PZ.set("Select the Porsche Zentrum")  # default value
PZ_dropdown = OptionMenu(window, PZ, *PZ_titles)


# 8. Agents_name
agent_name = tk.Text(window, height=2, width=30, highlightbackground='black')
agent_name.insert(tk.END, "")


# Submit all with one Button
def submitAll():
    input_valuesList = []
    input_valuesList.append(return_from_dropdown(TM))
    input_valuesList.append(select_date())
    input_valuesList.append(retrieve_gender())
    input_valuesList.append(retrieve_input(name_text))
    input_valuesList.append(retrieve_input(subject_topic))
    input_valuesList.append(retrieve_input(case_num))
    input_valuesList.append(return_from_dropdown(PZ))
    input_valuesList.append(retrieve_input(agent_name))
    # print(input_valuesList)
    return input_valuesList


# Converts Agents input from submitAll() to output text
def convert_to_output():
    il = []
    il = submitAll()
    gettit = gr(topic=il[0], date=il[1], gender=il[2], name=il[3],
                subject_topic=il[4], case=il[5],
                PZ=il[6], sender=il[7])
    res = gettit.response()
    return res


def new_window():
    T = Text(window, height=30, width=80)
    l = Label(window, text="Please confirm the response", width=30)
    l.config(font='Helvetica 14')
    out = str(convert_to_output())
    # b1 = Button(window, text="Back", command=reset_all())
    l.grid(row=12, column=1)
    T.grid(row=13, column=0, rowspan=6, columnspan=3)
    # b1.pack()

    T.insert(tk.END, out)
    # ttk.Label(scrollable_frame, text=convert_to_output()).pack(fill=BOTH)


def reset_all():
    python = sys.executable
    os.execl(python, python, * sys.argv)


submit_all_button = Button(window, height=1, width=20, text="Create Response",
                           command=lambda: [submitAll(), new_window()])


# Packing GUI-Screen
def packing_all():
    Title.grid(row=0, column=1)

    sep_date_gender.grid(row=4, column=0)
    Checkbutton(window, text="male", variable=m).grid(row=5, column=0)
    Checkbutton(window, text="female", variable=f).grid(row=6, column=0)
    Checkbutton(window, text="N/A", variable=NA).grid(row=7, column=0)
    sep_CustomerName_Subject.grid(row=8, column=0)
    sep_subj.grid(row=9, column=0)
    subject_topic.grid(row=10, column=0)


    TM_dropdown.grid(row=1, column=1)
    PZ_dropdown.grid(row=2, column=1)
    sep_case_agent.grid(row=4, column=1)
    agent_name.grid(row=5, column=1)
    sep_gender_CustomerName.grid(row=6, column=1)
    name_text.grid(row=7, column=1)
    sep_subj_case.grid(row=8, column=1)
    case_num.grid(row=10, column=1)

    sep_TM_date.grid(row=4, column=2)  # .pack(anchor=NE)
    cal.grid(row=5, column=2, rowspan=4)
    submit_all_button.grid(row=10, column=2)
    # date.pack(side=RIGHT, anchor=NE, pady=20)


packing_all()


window.mainloop()
