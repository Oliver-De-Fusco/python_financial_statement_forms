import tkinter as tk
from pdf_sorter import main
from randomise_names import randomise


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()
        

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.sort = tk.Button(self,text="Sort Files", command=main)
        self.random = tk.Button(self,text="Randomise names", command=randomise)

        self.sort.grid()
        self.random.grid()
        self.quitButton.grid()

app = Application()
app.mainloop()