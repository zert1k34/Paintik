from django.db import models

# Create your models here.



import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    """
    Класс для приложения рисования с возможностью сохранения изображения.
    """

    def __init__(self, root):
        """
        Инициализация приложения.

        :param root: Корневой виджет.
        """

        self.color_preview = None
        self.brush_size_scale = None
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создание нового изображения
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создание холста, видимого для пользователя
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Хранение текущего значения размера кисти
        self.brush_size = tk.IntVar()
        self.brush_size.set(1)

        # Переменные, отслеживающие последние координаты x и y, на которых пользователь отпустил мышь
        self.last_x, self.last_y = None, None

        # Цвет кисти по умолчанию
        self.pen_color = 'black'

        # Привязка события к холсту
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.root.bind('<Control-s>', lambda event: self.save_image())
        self.root.bind('<Control-c>', lambda event: self.choose_color())

        self.text_mode = False

        self.setup_ui()

    def setup_ui(self):
        """
        Создание пользовательского интерфейса.
        """

        # Создается фрейм (контейнер для виджетов)
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Создание кнопок
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=tk.EW)

        brush_button = tk.Button(control_frame, text="Кисть", command=self.brush)
        brush_button.grid(row=0, column=1, pady=(10, 0), sticky=tk.EW)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.eraser)
        eraser_button.grid(row=0, column=2, pady=(10, 0), sticky=tk.EW)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.grid(row=0, column=3, pady=(10, 0), sticky=tk.EW)

        brush_size_frame = tk.Frame(control_frame)
        brush_size_frame.grid(row=0, column=4, pady=(10, 0), sticky=tk.EW)

        sizes = [1, 2, 5, 10]
        self.create_brush_size_menu(brush_size_frame, sizes)

        size_button = tk.Button(control_frame, text="Размер холста", command=self.size_canvas)
        size_button.grid(row=0, column=5, pady=(10, 0), sticky=tk.EW)

        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.grid(row=0, column=6, pady=(10, 0), sticky=tk.EW)

        bg_button = tk.Button(control_frame, text="Изменить фон", command=self.change_bg_color)
        bg_button.grid(row=0, column=7, pady=(10, 0), sticky=tk.EW)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.grid(row=0, column=8, pady=(10, 0), sticky=tk.EW)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.grid(row=0, column=9, pady=(10, 0), sticky=tk.EW)

        self.color_preview = tk.Label(control_frame, bg=self.pen_color, width=2, height=1)
        self.color_preview.grid(row=0, column=10, padx=(10, 10), pady=(10, 0), sticky=tk.EW)

    def eraser(self):
        """
        Меняет цвет кисти на "white" при нажатии на кнопку ластика.
        """

        self.pen_color = "white"
        self.update_preview_color()

    def brush(self):
        """
        Меняет цвет кисти на "black" при нажатии на кнопку кисти.
        """

        self.pen_color = 'black'
        self.update_preview_color()

    def create_brush_size_menu(self, parent, sizes):
        """
        Создает меню для выбора размера кисти и шкалу для его изменения.

        :param parent: Родительский виджет, внутри которого будет создано меню и шкала.
        :param sizes: Список доступных размеров кисти.
        """

        size_menu = tk.OptionMenu(parent, self.brush_size, *sizes, command=self.update_brush_size)
        size_menu.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(parent, from_=1, to=10, orient=tk.HORIZONTAL,
                                         variable=self.brush_size, length=100,
                                         command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

    def update_brush_size(self, new_size):
        """
        Обновляет размер кисти.

        :param new_size: Новое значение размера кисти.
        """

        self.brush_size.set(new_size)

    def pick_color(self, event):
        """
        Определяет цвет пикселя под курсором и устанавливает его как цвет кисти.

        :param event: Событие, содержащее координаты курсора.
        """

        # Получаем координаты курсора на холсте в момент события.
        x = event.x
        y = event.y

        pixel_color = self.image.getpixel((x, y))[:3]
        pipette = "#{:02X}{:02X}{:02X}".format(*pixel_color)
        self.pen_color = pipette
        self.update_preview_color()

    def size_canvas(self):
        """
        Обновляет размер холста.
        """

        width = simpledialog.askinteger("Введите новые размеры холста", "Ширина (min=100, max=1800):")
        height = simpledialog.askinteger("Введите новые размеры холста", "Высота (min=100, max=900):")

        self.canvas.config(width=width, height=height)
        self.image = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def paint(self, event):
        """
        Рисует линии от предыдущих координат до текущих с заданным размером и цветом кисти.

        :param event: Событие, содержащее координаты курсора.
        """

        if self.last_x and self.last_y:
            width = self.brush_size_scale.get()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=width, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=width)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает координаты начала рисования.

        :param event: Событие, содержащее координаты курсора.
        """

        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст и создает новое пустое изображение.
        """

        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Запрашивает у пользователя выбор цвета кисти с помощью диалога выбора цвета.
        """

        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_preview_color()

    def update_preview_color(self):
        """
        Обновляет цвет предварительного просмотра до текущего цвета кисти.
        """

        self.color_preview.config(bg=self.pen_color)

    def add_text(self):
        """
        Добавляет текст на холст.
        """

        # Запрос текста у пользователя
        text = simpledialog.askstring("Ввод текста", "Введите текст:")
        if text:
            self.text_mode = True
            self.current_text = text
            self.canvas.bind('<Button-1>', self.place_text)

    def place_text(self, event):
        """
        Размещает введенный текст на холсте.
        """

        if self.text_mode:
            x, y = event.x, event.y
            self.canvas.create_text(x, y, text=self.current_text, fill=self.pen_color, anchor='nw')
            self.draw.text((x, y), self.current_text, fill=self.pen_color)
            self.text_mode = False
            self.canvas.unbind('<Button-1>')

    def change_bg_color(self):
        """
        Изменяет цвет фона холста.
        """

        color = colorchooser.askcolor(title="Выбрать цвет фона")
        if color[1]:
            self.canvas.config(bg=color[1])
            self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), color[1])
            self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        """
        Сохраняет изображение в формате PNG.
        """

        # Запрашиваем у пользователя путь для сохранения файла
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])

        # Проверяем, был ли выбран путь и сохраняем
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
