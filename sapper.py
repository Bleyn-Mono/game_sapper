import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


colors = {1: 'blue',
          2: 'green',
          3: 'maroon',
          4: 'red',
          5: 'teal',
          6: 'Lime',
          7: 'Maroon',
          8: 'dark green',
          9: 'spring green',
}

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *arg, **kwarg):   #переопределение метода __init__ из родительского класса
        super(MyButton, self).__init__(master, width=3, font='calibri 15 bold', *arg, **kwarg)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False


    def __repr__(self):
        return f'MyButton, {self.x}, {self.y}, {self.is_mine}, {self.number}'


class MainSweeper:

    window = tk.Tk()
    ROW = 5
    COLUMNS = 7
    MINES = 8
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True
    number_of_checkboxes = 0

    def __init__(self):   #создание кнопки
        self.button = []
        for i in range(MainSweeper.ROW + 2):
            temp = []
            for j in range(MainSweeper.COLUMNS + 2):
                btn = MyButton(MainSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button)) #при нажатии на кнопку
                temp.append(btn)                                          #будет срабатывать функция
                btn.bind("<Button-3>", self.right_click)
            self.button.append(temp)

    def right_click(self, event):
        if MainSweeper.IS_GAME_OVER:
            return

        cur_btn = event.widget

        if cur_btn['state'] == 'normal':
            cur_btn['text'] = '🚩'
            cur_btn['state'] = 'disabled'
            cur_btn['disabledforeground'] = 'red'
            MainSweeper.number_of_checkboxes += 1
            self.Ladel_count_mine()
        else:
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ''
            MainSweeper.number_of_checkboxes -= 1
            self.Ladel_count_mine()


    def Ladel_count_mine(self):
        a, b = MainSweeper.MINES, MainSweeper.number_of_checkboxes
        bottom_panel_mine = tk.Label(self.window, text=f'Мины = {a - b}', justify=tk.RIGHT)
        bottom_panel_mine.grid(row=MainSweeper.ROW + 2, column=MainSweeper.COLUMNS - 1, columnspan=2)

    def click(self, clicked_button:MyButton):  #действие при нажатии
        not_open = 0

        if MainSweeper.IS_GAME_OVER:
            return None

        if MainSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.counting_mines()
            self.print_btn()
            MainSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine == True:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            MainSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли')
            for i in range(1, MainSweeper.ROW + 1):
                for j in range(1, MainSweeper.COLUMNS + 1):
                    btn = self.button[i][j]
                    if btn.is_mine == True:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)

        for i in range(1, MainSweeper.ROW + 1):
            for j in range(1, MainSweeper.COLUMNS + 1):
                btn = self.button[i][j]
                if not btn.is_open:
                    not_open += 1

        if not_open == MainSweeper.MINES:
            showinfo('Поздравляем', 'Вы выиграли')

        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn:MyButton):   #  поиск в ширину
        tyrn = [btn]
        while tyrn:
            cur_btn = tyrn.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='')
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            cur_btn.is_open = True

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.button[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MainSweeper.ROW and \
                                1 <= next_btn.y <= MainSweeper.COLUMNS and next_btn not in tyrn:
                            tyrn.append(next_btn)

    def reload(self):   # перезагрузка кнопок
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.creat_widgets()
        MainSweeper.IS_FIRST_CLICK = True
        MainSweeper.IS_GAME_OVER = False
        self.number_of_checkboxes = 0



    def create_sattings_win(self):  # подменю настройки и нижняя панель

        win_settings = tk.Toplevel(self.window)
        row_entry = tk.Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, MainSweeper.ROW)
        tk.Label(win_settings, text='Количество колонок').grid(row=0, column=0)

        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MainSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количесто столбцов').grid(row=1, column=0)

        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MainSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количесто мин').grid(row=2, column=0)

        save_btn = tk.Button(win_settings, text='Применить',    #lambda нужна для того что б
                  command=lambda :self.chenge_settings(row_entry,  #chenge_settings мог принять аргументы
                                                       column_entry,
                                                       mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def chenge_settings(self, row: tk.Entry, column: tk.Entry, mine: tk.Entry): #проверка на корректность ввода данных
        try:
            int(row.get()), int(column.get()), int(mine.get())
        except ValueError:                                          #отлов ошибки
            showerror('Ошибка', 'Вы ввели неправильное значение')

        MainSweeper.ROW = int(row.get())
        MainSweeper.COLUMNS = int(column.get())
        MainSweeper.MINES = int(mine.get())
        self.reload()


    def creat_widgets(self):    #вывод кнопок меню файл
        a, b = MainSweeper.MINES, MainSweeper.number_of_checkboxes
        bottom_panel_mine = tk.Label(self.window, text=f'Мины = {a - b}', justify=tk.RIGHT)
        bottom_panel_mine.grid(row=MainSweeper.ROW + 2, column=MainSweeper.COLUMNS - 1, columnspan=2)

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть',  command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_sattings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label="Файл", menu=settings_menu)


        count = 1
        for i in range(1, MainSweeper.ROW + 1):
            for j in range(1, MainSweeper.COLUMNS + 1):
                btn = self.button[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='WENs')
                count += 1

        for i in range(1, MainSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for j in range(1, MainSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, j, weight=1)

    def open_all_battun(self):
        for i in range(MainSweeper.ROW + 2):
            for j in range(MainSweeper.COLUMNS + 2):
                btn = self.button[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, disabledforeground=color)
                btn.config(state='disabled')

    def print_btn(self):
        for i in range(1, MainSweeper.ROW + 1):
            for j in range(1, MainSweeper.COLUMNS + 1):
                btn = self.button[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()

    def insert_mines(self, number: int):
        print(self.get_mines_places(number))
        index_mines = self.get_mines_places(number)
        for i in range(1, MainSweeper.ROW + 1):
            for j in range(1, MainSweeper.COLUMNS + 1):
                btn = self.button[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def counting_mines(self):  # обход в ширину
        for i in range(1, MainSweeper.ROW + 1):
            for j in range(1, MainSweeper.COLUMNS + 1):
                btn = self.button[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0 , 1]:
                        for col_dx in [-1, 0 , 1]:
                            neighbour = self.button[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                    btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):   #перемешивание номеров
        indexes = list(range(1, MainSweeper.ROW * MainSweeper.COLUMNS + 1))
        indexes.remove(exclude_number)
        print(f'исключить кнопу {exclude_number}')
        shuffle(indexes)
        return indexes[:MainSweeper.MINES]

    def start(self):
        self.window.title('sapper')
        self.creat_widgets()

        #self.open_all_battun()
        MainSweeper.window.mainloop()


game = MainSweeper()
game.start()
