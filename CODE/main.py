import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import files
from ctypes import windll

user32 = windll.user32
user32.SetProcessDPIAware()


def get_dpi():
    return user32.GetDpiForSystem()


save_or_as = False
file_path = ''
the_type = [('Kaixin File', '.kx'), ('All files', '.*')]
global root, text


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=the_type, title='打开')  # 打开文件对话框选择文件
    if file_path:  # 如果选择了文件
        if os.path.splitext(file_path)[-1] == '.kx':
            Open(file_path)
        else:
            messagebox.showinfo('提示', '请打开.kx文件')


def Open(path):
    global file_path
    file_path_read_1 = files.read_file(path)
    text.delete('1.0', 'end')  # 删除Text组件中的所有内容
    text.insert('end', file_path_read_1)  # 在Text组件末尾添加文件内容
    file_path = path


def save_file():
    global file_path
    if file_path != '':  # 如果已经打开过文件
        files.save_file(file_path, text.get("1.0", "end-1c"))
        messagebox.showinfo('提示', '已保存')
    else:
        save_as_file()


def save_as_file():
    file_path_1 = filedialog.asksaveasfilename(filetypes=the_type, title='另存为')  # 保存文件对话框
    if file_path_1:  # 如果选择了路径
        if os.path.splitext(file_path_1)[-1] == '.kx':
            files.save_file(file_path_1, text.get("1.0", "end-1c"))
            Open(file_path_1)
        else:
            files.save_file(file_path_1 + '.kx', text.get("1.0", "end-1c"))
            Open(file_path_1 + '.kx')
        messagebox.showinfo('提示', '已保存')


def close():
    Message = messagebox.askyesnocancel('询问', '是否保存？')
    if Message:
        save_file()
        root.destroy()
    elif Message is None:
        pass
    elif not Message:
        root.destroy()


def help_window():
    root_1 = tk.Tk()  # 创建新的Tk对象
    root_1.resizable(False, False)  # 禁止调整窗口大小
    root_1.iconbitmap(f'{os.path.dirname(os.path.abspath(__file__))}\\icon.ico')
    root_1.title("kaixin格式文本编辑器")
    help_big = tk.Label(root_1, text='帮助', font=('华文仿宋', '30'))  # 创建Label组件
    help_big.pack()  # 显示Label组件
    print_help = tk.Label(root_1, text='''打开:文件>打开
保存:文件>保存
另存为:文件>另存为
新建:文件>新建
退出:文件>退出
帮助:帮助>打开帮助
关于:帮助>关于
剪切:编辑>剪切
复制:编辑>复制
粘贴:编辑>粘贴''', font=('华文仿宋', 20))  # 创建Label组件
    print_help.pack()  # 显示Label组件
    root_1.mainloop()  # 进入事件循环


def help_window_1():
    root_2 = tk.Tk()  # 创建新的Tk对象
    root_2.resizable(False, False)  # 禁止调整窗口大小
    root_2.iconbitmap(f'{os.path.dirname(os.path.abspath(__file__))}\\icon.ico')
    root_2.title("kaixin格式文本编辑器")
    help_big = tk.Label(root_2, text='关于', font=('华文仿宋', '30'))  # 创建Label组件
    help_big.pack()  # 显示Label组件
    print_help = tk.Label(root_2, text='''Copyright (c) 2023 SongXinZhe
kaixin格式文本编辑器  版本:2.0''', font=('华文仿宋', 20))  # 创建Label组件
    print_help.pack()  # 显示Label组件
    root_2.mainloop()  # 进入事件循环


def cut():
    try:
        text.selection_get()
    except tk.TclError:
        pass
    else:
        text.clipboard_clear()  # 清空剪切板
        text.clipboard_append(text.selection_get())  # 将选中内容添加到剪切板
        text.delete("sel.first", "sel.last")  # 删除选中内容


def copy():
    try:
        text.selection_get()
    except tk.TclError:
        pass
    else:
        text.clipboard_clear()  # 清空剪切板
        text.clipboard_append(text.selection_get())  # 将选中内容添加到剪切板


def new_file():
    if messagebox.askquestion('询问', '是否新建，当前的内容将会消失') == 'yes':
        text.delete('1.0', 'end')  # 删除Text组件中的所有内容


def paste():
    try:
        text.clipboard_get()
    except tk.TclError:
        pass
    else:
        text.insert("insert", text.clipboard_get())  # 在光标位置插入剪切板中的内容


def run():
    global root, text
    root = tk.Tk()  # 创建Tk对象
    if get_dpi() == 96:
        root.tk.call('tk', 'scaling', 1.5)
    root.title("kaixin格式文本编辑器")  # 设置窗口标题
    root.geometry("900x800")  # 设置窗口大小
    root.iconbitmap(f'{os.path.dirname(os.path.abspath(__file__))}\\icon.ico')
    root.protocol('WM_DELETE_WINDOW', close)

    text = tk.Text(root, wrap="word", font=('KaixinCodeFont', 15))  # 创建Text组件
    text.pack(expand=True, fill="both")  # 显示Text组件

    try:
        Open(sys.argv[1])
    except IndexError:
        pass

    menu_bar = tk.Menu(root)  # 创建菜单栏

    file_menu = tk.Menu(menu_bar, tearoff=0)  # 创建文件菜单
    file_menu.add_command(label="打开", command=open_file)  # 添加打开命令
    file_menu.add_command(label="保存", command=save_file)  # 添加保存命令
    file_menu.add_command(label="另存为", command=save_as_file)  # 添加另存为命令
    file_menu.add_command(label="新建", command=new_file)  # 添加新建命令
    menu_bar.add_cascade(label="文件", menu=file_menu)  # 添加文件菜单到菜单栏

    help_menu = tk.Menu(menu_bar, tearoff=0)  # 创建帮助菜单
    help_menu.add_command(label="打开帮助", command=help_window)  # 添加打开帮助命令
    help_menu.add_separator()  # 添加分隔线
    help_menu.add_command(label="关于", command=help_window_1)  # 添加关于命令
    menu_bar.add_cascade(label="帮助", menu=help_menu)  # 添加帮助菜单到菜单栏

    make_menu = tk.Menu(menu_bar, tearoff=0)  # 创建编辑菜单
    make_menu.add_command(label="剪切", command=cut)  # 添加剪切命令
    make_menu.add_command(label="复制", command=copy)  # 添加复制命令
    make_menu.add_command(label="粘贴", command=paste)  # 添加粘贴命令
    menu_bar.add_cascade(label="编辑", menu=make_menu)  # 添加编辑菜单到菜单栏

    root.config(menu=menu_bar)  # 将菜单栏添加到窗口

    root.mainloop()  # 进入事件循环


if __name__ == '__main__':
    run()
