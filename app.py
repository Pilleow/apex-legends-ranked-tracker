import matplotlib.pyplot as plt
import json

from datetime import datetime
from tkinter import *

""" Variables and functions ----------------- """

DATE_FORMAT = "%d %b %Y %H:%M:%S"
RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master"]

root = Tk()
root.iconbitmap("icon.ico")
root.title("Apex Legends Ranked Tracker")
root.configure(padx=10, pady=10)

with open('data/stats.json', 'r') as f:
    stats = json.load(f)


def add_new_entry():
    global rank, rank_icon, rank_icon_l, points_l, rank_name_l
    try:
        new_rp = int(new_entry_e.get())
    except ValueError:
        return
    if new_rp < 0:
        return

    time_now_str = datetime.strftime(datetime.now().today(), DATE_FORMAT)
    new_entry_e.delete(0, END)
    stats['rp'].append([new_rp, time_now_str])
    with open('data/stats.json', 'w') as f:
        json.dump(stats, f)

    rank, rank_icon = get_new_rank_data()
    rank_icon_l = Label(root, image=(rank_icon))
    rank_name_l = Label(root, text=RANKS[rank], font=('Helvetica', 32), justify=CENTER, width=12)
    points_l = Label(root, text=f"{stats['rp'][-1][0]} RP", justify=CENTER, font=('Helvetica', 26), width=12)
    rank_icon_l.grid_remove()
    rank_name_l.grid_remove()
    points_l.grid_remove()
    grid_all()


def get_new_rank_data():
    for i, rp_point in enumerate(stats['ranges']):
        if stats['rp'][-1][0] < rp_point:
            rank = i
            break
        elif i == len(stats['ranges']) - 1:
            rank = i + 1
            break
        
    rank_icon = PhotoImage(file=f"imgs/ranks/rank{rank+1}.gif")
    return rank, rank_icon


def show_plot():
    plt.plot()


def grid_all():
    rank_icon_l.grid(row=0, column=0, rowspan=2)
    new_entry_e.grid(row=0, column=1)
    new_entry_btn.grid(row=0, column=2)

    show_plot_btn.grid(row=1, column=1, columnspan=2)

    rank_name_l.grid(row=2, column=0)
    points_l.grid(row=2, column=1, columnspan=2)


rank, rank_icon = get_new_rank_data()

""" Creating & placing stuff -------------------------- """

rank_icon_l = Label(root, image=(rank_icon))
rank_name_l = Label(root, text=RANKS[rank], font=('Helvetica', 32), justify=CENTER, width=12)
points_l = Label(root, text=f"{stats['rp'][-1][0]} RP", justify=CENTER, font=('Helvetica', 26), width=12)

new_entry_e = Entry(root, font=('Helvetica', 26), width=10)
new_entry_btn = Button(root, text="+", padx=6, pady=0, font=('Helvetica', 18), command=add_new_entry)

show_plot_btn = Button(root, text="Graph it!", padx=40, pady=0,  font=('Helvetica', 26), command=show_plot)

grid_all()
root.mainloop()