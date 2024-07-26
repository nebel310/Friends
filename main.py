import random as rn
from tkinter import *




def done():
    maintext.configure(text='Задание: ')
    
    activity = rn.choice(Activities)
    tasktext.configure(text=activity)
    
    attention.configure(text='Если задание не влезает, то расширь окно, еблан')
    
    btn.configure(text='Сделано')


Activities = [
    "погладить кошку",
    "помыть посуду",
    "почитать книгу",
    "прогуляться в парке",
    "позаниматься спортом",
    "приготовить ужин",
    "смотреть фильм",
    "поиграть в настольную игру",
    "позвонить другу",
    "сходить в магазин",
    "написать письмо",
    "порисовать",
    "послушать музыку",
    "выпить кофе в кафе",
    "посетить музей",
    "поучаствовать в волонтерской деятельности",
    "посадить растение",
    "убраться в квартире",
    "выучить новое слово",
    "попробовать медитацию"
]


root = Tk()


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 800
window_height = 800
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


root.title("Friends")
root.configure(bg="#2E2E2E")

maintext = Label(root, text='Привет', font=("Arial", 50), bg="#2E2E2E", fg="#FFFFFF")
maintext.pack(pady=20)  # добавим отступ для красоты

tasktext = Label(root, text='', font=("Arial", 50), bg="#2E2E2E", fg="gold")
tasktext.pack(pady=20)

attention = Label(root, text='', font=("Arial", 15), bg="#2E2E2E", fg="#FF6347")
attention.pack(pady=10)  # добавим отступ для красоты

btn = Button(root, text="Начать", width=40, height=4, command=done, bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF")
btn.pack(pady=20)  # добавим отступ для красоты

root.mainloop()