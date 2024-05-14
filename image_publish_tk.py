import asyncio
import tkinter as tk
from functools import partial
import json
from xhs import xhs

# 读取 JSON 配置文件
with open('config.json', 'r') as file:
    config = json.load(file)

cover_dir = config['cover_path']
md_file = config['md_file']

# 创建主窗口
root = tk.Tk()
root.geometry("400x300")

# 定义包装函数
async def run_coroutine(coroutine, md, cover):
    try:
        await coroutine(md, cover)
    except Exception as e:
        print(f"An error occurred: {e}")
# 创建按钮并绑定对应的函数
button1 = tk.Button(root, text="xhs", command=partial(asyncio.run, run_coroutine(xhs, md_file, cover_dir)))
button1.pack()

# button2 = tk.Button(root, text="BaiJiaHao", command=partial(asyncio.run, run_coroutine(baijiahao, md_file, cover_dir)))
# button2.pack()

# button3 = tk.Button(root, text="blbl", command=partial(asyncio.run, run_coroutine(bilibili, md_file, cover_dir)))
# button3.pack()

# button4 = tk.Button(root, text="csdn", command=partial(asyncio.run, run_coroutine(csdn, md_file, cover_dir)))
# button4.pack()

# button5 = tk.Button(root, text="jianshu", command=partial(asyncio.run, run_coroutine(jianshu, md_file, cover_dir)))
# button5.pack()

# button6 = tk.Button(root, text="juejin", command=partial(asyncio.run, run_coroutine(juejin, md_file, cover_dir)))
# button6.pack()

# button7 = tk.Button(root, text="tencentcloud", command=partial(asyncio.run, run_coroutine(tencentcloud, md_file, cover_dir)))
# button7.pack()

# button8 = tk.Button(root, text="toutiao", command=partial(asyncio.run, run_coroutine(toutiao, md_file, cover_dir)))
# button8.pack()

# button9 = tk.Button(root, text="zhihu", command=partial(asyncio.run, run_coroutine(zhihu, md_file, cover_dir)))
# button9.pack()

# 运行应用程序
root.mainloop()
