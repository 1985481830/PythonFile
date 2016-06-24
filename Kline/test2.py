from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import numpy as np
import tkinter as Tk

date = []
open = []
high = []
low = []
close = []
ohlc = []
for i in range(30):
    date.append(i)
    open.append(2 + i)
    high.append(4 + i)
    low.append(1 + i)
    close.append(3 + i)
for x in range(30):
    append_me = [date[x], open[x], high[x], low[x], close[x]]
    ohlc.append(append_me)

class Window():
    def __init__(self, master):
        self.frame = Tk.Frame(master)
        self.fig = plt.figure()

        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        #self.canvas.get_tk_widget().grid(row=0,columnspan = 3)

    def draw(self):
        self.fig.clf()
        self.ax0 = plt.subplot2grid((1, 1), (0, 0))
        self.ax0.set_xlabel('Time')
        self.ax0.set_ylabel('Price')
        plt.ion()
        for i in range(5):
            ohlc[29][4] = ohlc[29][4] + 1
            candlestick_ohlc(self.ax0, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
            plt.pause(0.1)


if __name__ == '__main__':
    root = Tk.Tk()
    app = Window(root)
    root.title( "MatplotLib with Tkinter" )
    Tk.Button(root, text='画图', command=app.draw).pack()
    root.mainloop()

