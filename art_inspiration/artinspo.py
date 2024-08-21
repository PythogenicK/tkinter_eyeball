import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
from numpy import random


#variables
#create backgroundcolor variabel/reusing background color/easy use
bg_color = "#3d6466"

db_path = "data/productions.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

button_width = 10
button_height = 1


class TableTK:
    id_gen = random.randint(1,99999)

    def validate_entry(self, title, arts, mvmt, mdm, yr):
        if not all([title, arts, mvmt, mdm, yr]):
            empty_fields = [field for field, value in 
                            zip(["Title", "Artist", "Movement", "Medium", "Year"], 
                                [title, arts, mvmt, mdm, yr]) if not value]
            messagebox.showerror("Error", f"The following fields cannot be empty: {', '.join(empty_fields)}")
            return False
        return True

    def create_table(self, title, arts, mvmt, mdm, yr):
        if self.validate_entry(title, arts, mvmt, mdm, yr):
            # Existing code for creating the table
            cursor.execute(f"CREATE TABLE IF NOT EXISTS\"{title}\"(artist_name TEXT, movement_period TEXT, medium_type TEXT, debut_year TEXT, ID INTEGER)")
            cursor.execute(f"INSERT INTO \"{title}\" (artist_name, movement_period, medium_type, debut_year, ID) VALUES (?, ?, ?, ?, ?)", (arts, mvmt, mdm, yr, self.id_gen))
            connection.commit()
            messagebox.showinfo("Success", f"Table '{title}' has been added.")
            return True
        return False
    def submit_entry(self, title_entry, arts_entry, mvmt_entry, mdm_entry, yr_entry):
        if self.create_table(title_entry.get(), arts_entry.get(), mvmt_entry.get(), mdm_entry.get(), yr_entry.get()):
            # Clear the entry fields after successful submission
            for entry in [title_entry, arts_entry, mvmt_entry, mdm_entry, yr_entry]:
                entry.delete(0, tk.END)

    def edit_table(self, table, column, column_value, marker, marker_value):
        cursor.execute(f"UPDATE \"{table}\" SET \"{column}\" = \"{column_value}\" WHERE \"{marker}\"  = \"{marker_value}\"  ")
        connection.commit()
        messagebox.showinfo("Success", f"Table '{table}' has been edited.")
    
    def delete_table(self, table):
        cursor.execute(f"DROP TABLE IF EXISTS \"{table}\"")
        connection.commit()
        messagebox.showinfo("Success", f"Table '{table}' has been deleted.")

    def delete_confirmation(self,table):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{table}'?"):
            table_tk.delete_table(table)
            load_frame4()
    
    def edit_entry_prompt(self, table_name, record):
        edit_window = tk.Toplevel(root)
        edit_window.title(f"Edit {table_name}")
        edit_window.config(bg=bg_color)

        columns = ["artist_name", "movement_period", "medium_type", "debut_year"]
        entries = []

        for i, (column, value) in enumerate(zip(columns, record[:4])):
            tk.Label(edit_window, text=column.replace("_", " ").title(), bg=bg_color, fg="white").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        submit_btn = WidgetTK.create_button(edit_window, "Submit", lambda: self.submit_edit(table_name, entries, columns, record, edit_window))
        submit_btn.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def submit_edit(self, table_name, entries, columns, record, edit_window):
        for column, entry in zip(columns, entries):
            new_value = entry.get()
            if new_value != record[columns.index(column)]:
                self.edit_table(table_name, column, new_value, "ID", record[4])
        edit_window.destroy()
        load_frame5(table_name)  # Reload the frame to show updated info

    def delete_confirmation(self, table_name):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{table_name}'?"):
            self.delete_table(table_name)
            load_frame4()

table_tk = TableTK()

class WidgetTK():
    @staticmethod
    def create_label(home_frame, text_insert):
        label = tk.Label(home_frame, text = text_insert, bg = bg_color, font= ("TkHeadingFont",20))
        return label
    @staticmethod
    def create_entry(home_frame):
        entry = tk.Entry(home_frame, font = ("TkHeadingFont",15),
            bg = "#28393a",
            fg = "white",
            cursor = "hand2")
        return entry
    @staticmethod
    def create_button(home_frame, text_insert,cmnd):
        button = tk.Button(home_frame, text = text_insert, font = ("TkHeadingFont",20),
            bg = "#28393a",
            fg = "white",
            cursor = "hand2",
            activebackground = "#badee2",
            activeforeground = "black",
            command = cmnd,
            width = button_width,
            height = button_height
            )
        return button
    @staticmethod
    def close_widgets(frame):
        for widget in frame.winfo_children():
            widget.destroy()

class HandleDb:
    
    def fetch_db():
        table_data = []

        cursor.execute("SELECT * FROM sqlite_schema;")
        all_tables = cursor.fetchall()

        for i in all_tables:
            table_name = i[1]
            cursor.execute(f"SELECT * FROM \"{table_name}\";")
            table_records = cursor.fetchall()

            table_data.append((table_name, table_records))
        return table_data
    @staticmethod
    def fetch_db_table(table_name):
        table_data = []
        cursor.execute(f"SELECT * FROM \"{table_name}\";")
        table_records = cursor.fetchall()
        if table_records:
            table_data = (table_name, table_records)
        return table_data

    def fetch_db_random():
        #connect to database using connection/ create variable 'connection'
        #select all tables by string = "production" 
        cursor.execute("SELECT * FROM sqlite_schema;")
        #after select all, fetch must be called
        all_tables = cursor.fetchall()
        #new variable idx - index
        #idx is random number between 0 and the range of index of all_tables
        idx = random.randint(0, len(all_tables))#accomodate by -1 because using len as index random, but len begins at 1, index should begin at 0

        #fetch production title
        table_name = all_tables[idx][1]
        cursor.execute(f"SELECT * FROM\"{table_name}\";")
        table_records = cursor.fetchall()
        #terminate connection
        # connection.close()  

        return table_name, table_records

    def format_entry(s):
        #formatting for TABLE NAME
        # Split the sentence into words
        words = s.split()
        
        # Capitalize the first letter of each word
        capitalized_words = [word.capitalize() for word in words]
        
        # Join the capitalized words without spaces
        capitalized_sentence = ''.join(capitalized_words)
        
        return capitalized_sentence

    def format_table(table_name, table_records):
        #fix table name
        title = table_name
        "".join([char if char.islower() else " "  + char for char in title])
        information = []
        #production record/informationhh
        for i in table_records:
            artist = i[0]
            movement = i[1]
            medium = i[2]
            year = i[3]
            information.append(artist + movement + medium + str(year))
        return title, information

def load_frame1():
    WidgetTK.close_widgets(frame2)
    WidgetTK.close_widgets(frame3)
    WidgetTK.close_widgets(frame4)

    frame1.tkraise()


    logo_img = ImageTk.PhotoImage(file = "assets/logo_img/goon1.png")
    logo_widget = tk.Label(frame1, image = logo_img, bg = bg_color)
    logo_widget.image = logo_img  # Keep a reference to the image
    logo_widget.pack()


    #Text widget/instructions
    heading = WidgetTK.create_label(frame1, "What are you feeling today?")
    heading.pack()

    #Button widget
    shuffle_button = WidgetTK.create_button(frame1, "Shuffle",lambda:load_frame2())
    shuffle_button.pack(padx = 25,pady = 20)

    entry_button = WidgetTK.create_button(frame1, "Add Entry",lambda:load_frame3())
    entry_button.pack(padx = 25,pady = 20)

    view_entries_button = WidgetTK.create_button(frame1, "View Entries",lambda:load_frame4())
    view_entries_button.pack(padx = 25,pady = 20)

def load_frame2():
    WidgetTK.close_widgets(frame1)
    WidgetTK.close_widgets(frame3)
    WidgetTK.close_widgets(frame4)

    #stacking frame one on top of another to show most relevant frame
    frame2.tkraise()
    #format information coming from _random


    table_name, table_records = HandleDb.fetch_db_random()
    table_data = HandleDb.format_table(table_name, table_records)

    #frame2 widgets
    #logo widget

    #production title
    title_widget = WidgetTK.create_label(frame2, table_name)
    title_widget.pack()
    #Label list
    label_list = ["Artist","Movement","Medium","Year"]
    #information widget/loop
    #creating new label for each information slot(artist/medium/year etc.)
    if table_records:
        for label,info in zip(label_list,table_records[0]):
            tk.Label(
                frame2,
                text = f"{label}:{info}",
                bg = "#28393a",
                fg = "white",
                font = ("TkMenuFont",12)
            ).pack(fill = "both")

    #Button widget
    return_btn = WidgetTK.create_button(frame2, "Return", lambda: load_frame1())
    return_btn.pack()


def load_frame3():
    WidgetTK.close_widgets(frame1)
    WidgetTK.close_widgets(frame2)
    WidgetTK.close_widgets(frame4)
    #note to self: when creating labeled tk.entry widgets, separate pack() from rest of widget. Otherwise, no data will be received to table creation
    #e.g : title(yada yada).pack() => WRONG => NoneType
    #title (yada yada),title.pack() => CORRECT => yada yada
    WidgetTK.close_widgets(frame1)
    #stacking frame one on top of another to show most relevant frame
    frame3.tkraise()
    #logo widget
    logo_img = ImageTk.PhotoImage(file = "assets/logo_img/goon1.png")
    logo_widget = tk.Label(frame3, image = logo_img, bg = bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    #entry data
    #title entry, artist, movement, medium, year
    title_label = WidgetTK.create_label(frame3,"Title")
    title_label.pack()
    title = WidgetTK.create_entry(frame3)
    title.pack()

    arts_label = WidgetTK.create_label(frame3,"Artist")
    arts_label.pack()
    arts = WidgetTK.create_entry(frame3)
    arts.pack()

    mvmt_label =WidgetTK.create_label(frame3,"Movement")
    mvmt_label.pack()
    mvmt = WidgetTK.create_entry(frame3)
    mvmt.pack()

    mdm_label = WidgetTK.create_label(frame3,"Medium")
    mdm_label.pack()
    mdm = WidgetTK.create_entry(frame3)
    mdm.pack()

    yr_label = WidgetTK.create_label(frame3, "Year")
    yr_label.pack()
    yr = WidgetTK.create_entry(frame3)
    yr.pack()

    submit_btn = WidgetTK.create_button(frame3, "Submit", lambda:table_tk.create_table(title.get(),arts.get(),mvmt.get(),mdm.get(),yr.get()))
    submit_btn.pack()

    return_btn = WidgetTK.create_button(frame3, "Return", lambda: load_frame1())
    return_btn.pack()
    
def load_frame4():
    #this frame should load in only the title of the artpiece and its artists
    #each entry should have a corresponding view button
    WidgetTK.close_widgets(frame1)
    WidgetTK.close_widgets(frame2)
    WidgetTK.close_widgets(frame3)
    WidgetTK.close_widgets(frame5)

    frame4.tkraise()

    # Configure frame4 to expand and fill the root window
    frame4.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    entries_title = WidgetTK.create_label(frame2, "Entries")
    entries_title.pack()
    # Create a canvas with a scrollbar
    canvas = tk.Canvas(frame4, bg=bg_color)
    scrollbar = tk.Scrollbar(frame4, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid layout for the canvas and scrollbar
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame4.grid_rowconfigure(0, weight=1)
    frame4.grid_columnconfigure(0, weight=1)

    table_data = HandleDb.fetch_db()
    for i, (table_name, _) in enumerate(table_data):
        entry_frame = tk.Frame(scrollable_frame, bg=bg_color)
        entry_frame.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)

        production_title = WidgetTK.create_label(entry_frame, table_name)
        production_title.grid(row=0, column=0, sticky="w")
        
        view_btn = WidgetTK.create_button(entry_frame, "View", lambda: load_frame5(table_name))
        view_btn.grid(row=0, column=1, sticky="e")

    # Create return button
    return_btn = WidgetTK.create_button(frame4, "Return", lambda: load_frame1())
    return_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Update the canvas scroll region
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
def load_frame5(table_name):
    #opening individual entry tables
    #this window should contain all information, excluding the ID of the entry
    #these windows should have an edit or delete button
    #return button also
    WidgetTK.close_widgets(frame4)
    frame5.tkraise()

    table_data = HandleDb.fetch_db_table(table_name)
    
    if not table_data:
        messagebox.showerror("Error", f"No data found for table '{table_name}'")
        load_frame4()
        return

    table_name, table_records = table_data

    title_widget = WidgetTK.create_label(frame5, table_name)
    title_widget.pack()

    label_list = ["Artist", "Movement", "Medium", "Year"]

    if table_records:
        for label, info in zip(label_list, table_records[0]):
            tk.Label(
                frame5,
                text=f"{label}:{info}",
                bg="#28393a",
                fg="white",
                font=("TkMenuFont", 12)
            ).pack(fill="both")

        edit_btn = WidgetTK.create_button(frame5, "Edit", lambda: table_tk.edit_entry_prompt(table_name, table_records[0]))
        edit_btn.pack(padx=15, pady=5, side=tk.LEFT)

        delete_btn = WidgetTK.create_button(frame5, "Delete", lambda: table_tk.delete_confirmation(table_name))
        delete_btn.pack(padx=15, pady=5, side=tk.LEFT)
    else:
        tk.Label(frame5, text="No records found for this table", bg=bg_color, fg="white").pack()

    return_btn = WidgetTK.create_button(frame5, "Return", lambda: load_frame4())
    return_btn.pack(padx=25, pady=5, side=tk.RIGHT)


root = tk.Tk()
root.title("Eyeball")

#displaying application in center of screen as it pops up
#open quotes " "
#double colon allows to fetch PlaceWindow method
#dot/period calls top-level window
#"center" to call pop up to center
root.eval("tk::PlaceWindow . center")


#setting window size(width and height)
#setting window color
#first argument is the "root", or where the window is located
frame1 = tk.Frame(root, width = 800, height = 800, bg = bg_color )
#remove width and height from frame2, since we want the dimensions to be dynamic and fit any of its child elements
frame2 = tk.Frame(root, bg = bg_color)
frame3 = tk.Frame(root, bg = bg_color)
frame4 = tk.Frame(root, bg = bg_color)
frame5 = tk.Frame(root, bg = bg_color)

#THESE LINES OF CODE BECOME REDUNDANT AFTER "FOR FRAME" LOOP is used
# #call grid method after
# frame1.grid(row=0,column=0)
# frame1.grid(row=0,column=0)

# Resize the window to full screen
# resize_window(root, width_ratio=1.0, height_ratio=1.0)
#for frame in tuple of frame1 and frame2
#call iteration of frame
for frame in (frame1,frame2,frame3,frame4, frame5):
    frame.grid(row=0,column=0, sticky = "nesw") #sticky method with nesw asks function to stick to all four corners of window
#DO NOT FORGET TO CALL LOAD_FRAME1/loads assets
load_frame1()


#run app
root.mainloop()
# connection.close()