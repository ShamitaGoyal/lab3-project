# Name: Shamita Goyal
# Lab 3: Web Access, Data Storage

import sqlite3
import tkinter as tk
import webbrowser
import customtkinter as ctk
from Image import Img
from Query import Query
from AnimatedGIFLabel import GIFLabel


conn = sqlite3.connect('destinations.db')
cursor = conn.cursor()

class MainWin(ctk.CTk):
    """
    THIS WINDOW DISPLAYS 3 BUTTONS ALLOWING THE USER TO PICK
    USER SEARCH FOR TRAVEL DESTINATIONS
    """
    def __init__(self):
        super().__init__()

        query = Query()

        self.choice_methods = {
            "Name": lambda: query.byName(),
            "Month": lambda: query.byMonth(),
            "Rank": lambda: query.byRank()
        }
        self.destination_methods = {
            "Name": query.destination_by_name,
            "Month": query.destination_by_month,
            "Rank": query.destination_by_rank
        }


        self.title("Travel")
        self.geometry("550x560+3+6")
        self.configure(fg_color="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label1 = ctk.CTkLabel(self, text="Best Places to\n Travel in 2024.", text_color="black", font=("Lexend", 45, "bold"))
        label1.grid(sticky="n",pady=10)

        # img1
        img = Img(self, png="./png/boy.png", sizeW=0.55, sizeH=0.55)
        img.grid(sticky="n", pady=10)


        frame = tk.Frame(bg="white")
        frame.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky=tk.EW)

        # Make the 3 Buttons --> Name, Month, Rank
        label2 = ctk.CTkLabel(frame, text="Search by:", text_color="black", font=("RUBIK MONO ONE", 20, "bold"))
        label2.grid(row=0, column=0, padx=(10, 5), sticky=tk.E)



        button1 = ctk.CTkButton(frame, text="Name",command=lambda: self.getInitialChoice('Name'),font=("RUBIK MONO ONE", 15),
                                border_color="black", border_width=3, fg_color="white", text_color="black", hover_color="gray65", width=100, height=36)
        button2 = ctk.CTkButton(frame, text="Month",command=lambda: self.getInitialChoice('Month'),font=("RUBIK MONO ONE", 15),
                                border_color="black", border_width=3, fg_color="white", text_color="black", hover_color="gray65", width=100, height=36)
        button3 = ctk.CTkButton(frame, text="Rank", command=lambda: self.getInitialChoice('Rank'),font=("RUBIK MONO ONE", 15),
                                border_color="black", border_width=3, fg_color="white", text_color="black", hover_color="gray65", width=100, height=36)

        button1.grid(row=0, column=1, padx=5)
        button2.grid(row=0, column=2, padx=5)
        button3.grid(row=0, column=3, padx=(5, 10))

    def getInitialChoice(self, choice):
        """
        once the button is clicked it will close the window
        to open the dialog window
        """
        method = self.choice_methods.get(choice)
        if method:
            chars = method()
            DialogWin(self, chars, choice)
            self.withdraw()

    def handle_choice(self, choice, selected_value):
        """
        - handles the choice made from the getInitialChoice method and
        - calls the specific query from that function
        - the resulting data gets passed on to the Result Window class to display the info
        """
        method = self.destination_methods.get(choice)
        if method:
            specific_destinations = method(selected_value)
            ResultWin(self, specific_destinations, selected_value, choice)

class DialogWin(ctk.CTkToplevel):
    """THIS WINDOW DISPLAYS THE RADIOBUTTON OPTIONS FOR USER SEARCH"""
    def __init__(self, master, chars, search):
        super().__init__(master)
        self.master = master
        self.search = search

        self.title("Travel")
        self.geometry("550x560+3+6")
        self.configure(fg_color="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label3 = ctk.CTkLabel(self, text=f"Click on a\n {search.lower()} to select.", text_color="white",
                              font=("Lexend", 40, "bold"))
        label3.grid(row=0, column=0, sticky="n", pady=20)

        img2 = Img(self, png="./png/Group9.png", sizeW=0.55, sizeH=0.55)
        img2.grid(sticky="n", pady=10)

        # Create a dictionary to map string representation back to original values
        self.value_map = {str(value): value for value in chars}

        self.controlVar = ctk.StringVar(value=str(chars[0]))
        self.option_menu = ctk.CTkOptionMenu(self, values=list(self.value_map.keys()), command=self.on_option_select,
                                             variable=self.controlVar)
        self.option_menu.grid(pady=40, sticky="s")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_option_select(self, choice):
        """
        once an option is selected it will destroy the window
        and pass the selected choice to the main window
        """
        original_value = self.value_map[choice]  # Get the original value (int or str)
        self.master.deiconify()
        self.destroy()
        self.master.handle_choice(self.search, original_value)

    def on_close(self):
        """closes the window"""
        self.master.deiconify()
        self.destroy()

class ResultWin(ctk.CTkToplevel):
    """
    THIS WINDOW DISPLAYS THE CHOICES MADE BY USER AS A LISTBOX FORMAT
    WHICH CAN BE SELECTED FROM
    """
    def __init__(self, master, rowText: list, selected_value: str, param: str):
        super().__init__(master)

        self.param = param
        self.title("Travel")
        self.geometry("550x680+3+6")
        self.configure(fg_color="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if param == "Name":
            label = ctk.CTkLabel(self, text=f"Destinations Starting\n With {selected_value}",
                             font=("Lexend", 35, "bold"), text_color="black")
        elif param == "Month":
            label = ctk.CTkLabel(self, text=f"Top Destinations for\n {selected_value} in ranking order",
                             font=("Lexend", 35, "bold"), text_color="black")
        else:
            label = ctk.CTkLabel(self, text=f"Destinations with rank {selected_value}\n for the listed months",
                             font=("Lexend", 35, "bold"), text_color="black")
        label.grid(row=0, column=0, pady=10, sticky="n")


        # Create a scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=200)
        scrollable_frame.grid(row=1, column=0, padx=10, pady=10)

        for item in rowText:
            item_label = ctk.CTkLabel(scrollable_frame, text=item, font=("Comfortaa", 15), anchor="w")
            item_label.pack(fill="x", pady=2, padx=5)
            item_label.bind("<Double-Button-1>", lambda event, val=item: self.on_select(val))

        img3 = Img(self, png="./png/Group8.png", sizeW=0.55, sizeH=0.55)
        img3.grid(sticky="s")

    def on_select(self, selected_item):
        """
        - once an item is selected from the scrollable frame
        - the destination_description query is called and passed the value
        - the window gets destroyed and the summary and url values get passed on to Display Window
        """
        query = Query()
        dest_summary, dest_url = query.destination_description(selected_item, self.param)
        self.destroy()
        DisplayWin(self.master, dest_summary, dest_url, selected_item)

class DisplayWin(ctk.CTkToplevel):
    """
    THIS WINDOW DISPLAYS THE SUMMARY AND URL INFORMATION OF THE USER
    SELECTED COUNTRY/ITEM FROM RESULT WINDOW
    """
    def __init__(self, master, summary, url, selected_item):
        super().__init__(master)


        self.title("Travel")
        self.geometry("550x680+3+6")
        self.configure(fg_color="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        animated_label = GIFLabel(self, gif_path="./png/friendship.gif", delay=30, width=150, height=150)
        animated_label.grid(sticky="nsew", padx=10, pady=40)


        # title
        label = ctk.CTkLabel(self, text=selected_item, text_color="black", font=("Lexend", 35, "bold"))
        label.grid(row=0, column=0, pady=20, sticky="n")

        #summary text widget
        summary_text = ctk.CTkTextbox(self, width=500, height=300,
                                      corner_radius=10, font=("Comfortaa", 16), activate_scrollbars=True, wrap="word")
        summary_text.grid(row=1, column=0, pady=20)
        summary_text.insert("0.0", summary)
        summary_text.configure(state="disabled")

        url_button = ctk.CTkButton(self, text=f"See details", command=lambda: self.open_url(url),font=("RUBIK MONO ONE", 15),
                                border_color="black", border_width=3, fg_color="white", text_color="black", hover_color="gray65", width=100, height=36)
        url_button.grid(pady=10, sticky="s")

    def open_url(self, url):
        """open the web url from the button"""
        webbrowser.open_new(url)


app = MainWin()
app.mainloop()
conn.close()