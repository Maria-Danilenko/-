from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring
import os

withWind = 425
heightWind = 550
fileName = ""
fileName0 = ""
file = ""
path = ""
txt = None
tab2 = None
tabNames = ""
tab_names_list = []


def folder():
    global path
    path = os.getcwd()
    path += "/Notes"
    if not os.path.exists(path):
        try:
            os.mkdir(path, 0o755)
        except:
            messagebox.showerror(title="Помилка!", message="Не вдалось створити папку")

def mainMenu():
    global path, tab1, var_list, chBox_list, fileName_list, canvas, btnOpen, btnRename, btnDel
    tab_control.add(main_tab, text='Головна')
    tab_control.pack(expand=1, fill=BOTH)

    canvas = Canvas(main_tab)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = Scrollbar(main_tab, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda i: canvas.configure(scrollregion=canvas.bbox("all")))
    tab1 = Frame(canvas, pady=7)
    canvas.create_window((0, 0), window=tab1, anchor=NW)

    lbl = Label(tab1, height=1)
    lbl.pack(side=BOTTOM)
    place_for_btn = Frame(canvas, background='#F0F0F0')
    place_for_btn.pack(side=BOTTOM, fill=X)

    var_list = []
    chBox_list = []
    fileName_list = []

    for file in os.listdir(path):
        if file.endswith('.txt'):
            i = file
            fileName_list.append(i)

            file = IntVar()
            var_list.append(file)

            chBox = Checkbutton(tab1, text=i, variable=var_list[var_list.index(file)])
            chBox_list.append(chBox)
            chBox.pack(ipadx=3, ipady=2, side=TOP, anchor=W)

    btnNew = Button(place_for_btn, padx=3, pady=3, text="Створити", command=newFile)
    btnNew.pack(padx=(4, 4), pady=3, side=LEFT)
    btnOpen = Button(place_for_btn, padx=3, pady=3, text="Відкрити", command=openFile)
    btnOpen.pack(side=LEFT)
    btnOpenAs = Button(place_for_btn, padx=3, pady=3, text="Відкрити як", command=openFileAs)
    btnOpenAs.pack(padx=4, pady=3, side=LEFT)

    btnRename = Button(place_for_btn, padx=3, pady=3, text="Перейменувати", command=lambda: renameFile())
    btnRename.pack(side=LEFT)
    btnDel = Button(place_for_btn, padx=3, pady=3, text="Видалити", command=lambda: deleteFile())
    btnDel.pack(padx=4, pady=3, side=LEFT)

    checkFiles()

def checkFiles():
    global btnOpen, btnRename, btnDel
    l = []
    for f in os.listdir(path):
        if f.endswith('.txt'): l.append(f)
    if len(l) < 1:
        btnOpen.config(state='disabled')
        btnRename.config(state='disabled')
        btnDel.config(state='disabled')
    else:
        btnOpen.config(state='normal')
        btnRename.config(state='normal')
        btnDel.config(state='normal')

def checkBoxes():
    global var_list, chBox_list, fileName_list, canvas
    for i in chBox_list:
        if var_list[chBox_list.index(i)] == 1:
            i.deselect()
        i.destroy()

    var_list = []
    chBox_list = []
    fileName_list = []

    for file in os.listdir(path):
        if file.endswith('.txt'):
            i = file
            fileName_list.append(i)

            file = IntVar()
            var_list.append(file)

            chBox = Checkbutton(tab1, text=i, variable=var_list[var_list.index(file)])
            chBox_list.append(chBox)
            chBox.pack(ipadx=3, ipady=2, side=TOP, anchor=W)

    window.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))


def deleteFile():
    global path, chBox_list, var_list, fileName_list
    for var in var_list:
        if (var.get() == 1):
            var0 = var_list.index(var)
            if fileName_list[var0][:-4] in tab_names_list:
                messagebox.showerror(title="Помилка!",
                                     message=f"Файл з ім'ям {fileName_list[var0]} відкритий.\nЗакрийте його для видалення")
                chBox_list[var0].deselect()
                deleteFile()
                return 0
            usAnsw = messagebox.askquestion(title="Видалення нотатку",
                                            message=f"Ви впевнені, що хочете видалити {fileName_list[var0]}?")
            if usAnsw == 'no':
                chBox_list[var0].deselect()
                deleteFile()
                return 0
            if usAnsw == 'yes':
                chBox_list[var0].deselect()
                chBox_list[var0].destroy()
                os.remove(path + '/' + fileName_list[var0])
    checkFiles()


def newFile():
    global fileName, tabNames, tab_names_list
    fileName = ""

    name = askstring('', 'Введіть назву нотатку:\t')
    if name == None:
        return 0
    if name == "":
        messagebox.showwarning(title="Помилка!", message="Назва файлу порожня")
        newFile()
        return 0
    if os.path.exists(path + "/" + name + ".txt") or name in tab_names_list:
        messagebox.showerror(title="Помилка!", message="Файл з таким ім'ям вже існує")
        newFile()
        return 0
    chars = set('/\:*?"<>|')
    if any((c in chars) for c in name):
        messagebox.showwarning(title="Помилка!", message="У назві файлу присутній недопустимий символ!")
        newFile()
        return 0
    if len(name) > 21:
        messagebox.showwarning(title="Помилка!", message="Назва довша за 20 символів")
        newFile()
        return 0

    tab_names_list.append(name)
    newTab(name)

def newTab(name):
    global tab2, txt
    tab2 = ttk.Frame(tab_control, takefocus=True)
    tab_control.add(tab2, text=f'{name}.txt')
    tab_control.select(tab2)

    scrollbar = Scrollbar(tab2)
    scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 37))

    txt = Text(tab2, yscrollcommand=scrollbar.set, undo=True)
    txt.pack(expand=1, fill='both', pady=(0, 37))
    scrollbar.config(command=txt.yview)
    txt.focus_set()

    btnSave = Button(tab2, padx=3, pady=3, text="Зберегти", command=saveFile)
    btnSave.place(x=148, y=491)
    btnClose = Button(tab2, padx=3, pady=3, text="Закрити", command=closeFile)
    btnClose.place(x=217, y=491)

    window.bind("<Control-KeyPress>", keypress)

def keypress(e):
    if e.keycode == 86 and e.keysym != 'v':
        paste()
    elif e.keycode == 67 and e.keysym != 'c':
        copy()
    elif e.keycode == 88 and e.keysym != 'x':
        cut()
    elif e.keycode == 65 and e.keysym != 'a':
        select_all()
    elif e.keycode == 90 and e.keysym != 'z':
        undo()
    elif e.keycode == 89 and e.keysym != 'y':
        redo()

def undo():
    window.event_generate("<<Undo>>")
def redo():
    window.event_generate("<<Redo>>")
def copy():
    window.event_generate("<<Copy>>")
def cut():
    window.event_generate("<<Cut>>")
def paste():
    window.event_generate("<<Paste>>")
def select_all():
    window.event_generate("<<SelectAll>>")

def openFile():
    global path, chBox_list, var_list, fileName_list, txt, tab_names_list
    for var in var_list:
        if (var.get() == 1):
            var0 = var_list.index(var)
            chBox_list[var0].deselect()
            try:
                if fileName_list[var0][:-4] in tab_names_list:
                    messagebox.showerror(title="Помилка!", message=f"Файл з ім'ям {fileName_list[var0]} вже відкритий")
                    continue
                tab_names_list.append(fileName_list[var0][:-4])
                newTab(fileName_list[var0][:-4])
                with open(path + '/' + fileName_list[var0], mode='r', encoding='utf8') as file:
                    txtFile = file.read()
                    txt.insert(END, txtFile)
            except:
                try:
                    with open(path + '/' + fileName_list[var0], mode='r') as file:
                        txtFile = file.read()
                        txt.insert(END, txtFile)
                except:
                    messagebox.showerror(title="Помилка!", message="Не вдалось відкрити файл")


def openFileAs():
    global fileName, txt, tab_names_list
    try:
        fileName = filedialog.askopenfilename(filetypes=(("Text Documents", "*.txt"),))
        if fileName == "": return 0
        if fileName[fileName.rfind('/') + 1:-4] in tab_names_list:
            messagebox.showerror(title="Помилка!",
                                 message=f"Файл з ім'ям {fileName[fileName.rfind('/') + 1:]} вже відкритий")
            return 0
        tab_names_list.append(fileName[fileName.rfind('/') + 1:-4])
        newTab(fileName)
        tab_control.tab(tab2, text=fileName[fileName.rfind('/') + 1:])

        with open(fileName, mode='r', encoding='utf8') as file:
            txtFile = file.read()
            txt.insert(END, txtFile)
    except Exception as e:
        print(e)
        try:
            with open(fileName, mode='r') as file:
                txtFile = file.read()
                txt.insert(END, txtFile)
        except Exception as e:
            print(e)
            tab_control.forget(tab_control.select())
            messagebox.showerror(title="Помилка!", message="Не вдалось відкрити файл")


def renameFile():
    global path, chBox_list, var_list, fileName_list, tab_names_list
    for var in var_list:
        if (var.get() == 1):
            var0 = var_list.index(var)
            if fileName_list[var0][:-4] in tab_names_list:
                messagebox.showerror(title="Помилка!",
                                     message=f"Файл з ім'ям {fileName_list[var0]} відкритий.\nЗакрийте його для перейменування")
                return 0
            name = askstring(title="Перейменування нотатку", prompt=f"Введіть нове ім'я нотатку {fileName_list[var0]}:")
            if name == None:
                chBox_list[var0].deselect()
                renameFile()
                return 0
            name = name.strip()
            if name == "" or name.isspace():
                messagebox.showwarning(title="Помилка!", message="Назва файлу порожня")
                renameFile()
                return 0
            if os.path.exists(path + "/" + name + ".txt") or name in tab_names_list:
                messagebox.showerror(title="Помилка!", message="Файл з таким ім'ям вже існує")
                renameFile()
                return 0
            chars = set('/\:*?"<>|')
            if any((c in chars) for c in name):
                messagebox.showwarning(title="Помилка!", message="У назві файлу присутній недопустимий символ!")
                renameFile()
                return 0
            if len(name) > 21:
                messagebox.showwarning(title="Помилка!", message="Назва довша за 20 символів")
                renameFile()
                return 0
            chBox_list[var0].deselect()
            chBox_list[var0].config(text=name + '.txt')
            os.rename(f'{path}/{fileName_list[var0]}', f'{path}/{name}.txt')
    checkBoxes()


def closeFile():
    global tab2, tab_names_list
    filename = tab_control.tab(tab_control.select(), "text")
    if not os.path.exists(path + "/" + filename):
        usAnsw = messagebox.askyesnocancel(title="Закриття файлу", message="Зберегти файл перед закриттям?")
    else:
        with open(path + '/' + filename, mode='r') as file:
            txtFile = file.read()
            if (str(tab_control.focus_get())[-6:] != ".!text"):
                messagebox.showerror(title="Помилка!", message="Клацніть на поле вводу")
                return 0
            correntTxt = str(tab_control.focus_get().get('1.0', 'end-1c'))
            if (txtFile != correntTxt):
                usAnsw = messagebox.askyesnocancel(title="Закриття файлу", message="Зберегти файл перед закриттям?")
            else:
                tab_names_list.remove(tab_control.tab(tab_control.select(), "text")[:-4])
                tab_control.forget(tab_control.select())
                return 0

    if usAnsw == None:
        return 0
    if usAnsw:
        saveFile()
        tab_names_list.remove(tab_control.tab(tab_control.select(), "text")[:-4])
        tab_control.forget(tab_control.select())
    if not usAnsw:
        tab_names_list.remove(tab_control.tab(tab_control.select(), "text")[:-4])
        tab_control.forget(tab_control.select())


def saveFile():
    filename = tab_control.tab(tab_control.select(), "text")
    try:
        with open(path + "/" + filename, mode='w') as file:
            if (str(tab_control.focus_get())[-6:] != ".!text"):
                messagebox.showerror(title="Помилка!", message="Клацніть на поле вводу")
            else:
                with open(path + '/' + filename, mode='w') as f:
                    file.write(str(tab_control.focus_get().get('1.0', 'end-1c')))
                checkBoxes()
                checkFiles()
    except:
        messagebox.showerror(title="Помилка!", message="Не вдалось зберегти файл")

if __name__ == '__main__':
    folder()

    window = Tk()
    window.resizable(width=False, height=False)
    tab_control = ttk.Notebook(window)
    main_tab = ttk.Frame(tab_control)
    window.title("Нотатник")
    window.geometry(f"{withWind}x{heightWind}")

    mainMenu()
    window.mainloop()
