from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from controller_create_rosters import *
from controller_create_stacks import *
from controller_db_read import *
from controller_db_write import *
from controller_timer import *
import time


def run_program():
    root = Tk()
    root.title('Stack Builder')
    root.geometry("480x1000")
    last_updated_var = StringVar()
    number_of_rosters_var = StringVar()
    number_of_players_var = StringVar()
    max_ratio_var = StringVar()
    max_projection_var = StringVar()
    player_list_var = StringVar()
    output_line1_var = StringVar()
    include_players_entry = Entry(root, width=25)
    exclude_players_entry = Entry(root, width=25)
    quarterback_entry = Entry(root, width=10)
    dst_entry = Entry(root, width=10)
    output_line1_var.set("                           Welcome to Stack Builder                        ")
    last_updated_var.set("Last Updated: " + str(get_last_updated() + "    "))
    number_of_rosters_var.set("Number of Rosters:      ")
    number_of_players_var.set("Number of Players:      " + str(get_count("players")))
    player_list_var.set(show_players_as_list())
    max_ratio_var.set("Highest Ratio:      ")
    max_projection_var.set("Highest Projection:      ")
    last_updated_label = Label(root, textvariable=last_updated_var)
    number_of_players_label = Label(root, textvariable=number_of_players_var)
    player_list_label = Label(root, textvariable=player_list_var)
    number_of_rosters_label = Label(root, textvariable=number_of_rosters_var)
    max_ratio_label = Label(root, textvariable=max_ratio_var)
    max_projection_label = Label(root, textvariable=max_projection_var)
    quarterback_label = Label(root, text="QB:  ")
    dst_label = Label(root, text="DST:  ")
    include_players_label = Label(root, text="Players that must be included:")
    exclude_players_label = Label(root, text="Players that must be excluded:")
    output_line1_label = Label(root, textvariable=output_line1_var, padx=10, pady=20)

    def create_rosters():
        output_line1_var.set("")
        start = time.time()
        create_rosters_table()
        last_updated_var.set("Last Updated: " + str(get_last_updated() + "    "))
        player_list_var.set(show_players_as_list())
        number_of_rosters_var.set("Number of Rosters:      ")
        number_of_players_var.set("Number of Players:      " + str(get_count("players")))
        max_ratio_var.set("Highest Ratio:      ")
        max_projection_var.set("Highest Projection:      ")
        now = time.time()
        output_statement = "It took " + get_time(start, now) + " seconds to write all the valid rosters to the database"
        output_line1_var.set(output_statement)
        print(output_statement)

    def get_statistics():
        print("Getting the Statistics")
        start = time.time()
        table = "rosters"
        if table_exists("stacks"):
            table = "stacks"
        number_of_rosters_var.set("Number of Rosters:      " + str(get_count(table)))
        number_of_players_var.set("Number of Players:      " + str(get_count("players")))
        player_list_var.set(show_players_as_list())
        max_ratio_var.set("Highest Ratio:      " + str(get_max(table, "ratio")))
        max_projection_var.set("Highest Projection:      " + str(get_max(table, "projection")))
        now = time.time()
        output_message = "It took " + get_time(start, now) + " seconds to get the stats from the " + table + " table"
        output_line1_var.set(output_message)
        print(output_message)

    def create_stacks():
        print("Building the Stacks")
        if not table_exists("rosters"):
            output_statement = "There are no tables"
            print(output_statement)
            output_line1_var.set(output_statement)
            return False
        start = time.time()
        quarterback = ""
        dst = ""
        included_player_numbers = []
        excluded_player_numbers = []

        if quarterback_entry.get():
            quarterback = int(quarterback_entry.get()) - 1
        if dst_entry.get():
            dst = int(dst_entry.get()) - 1
        if include_players_entry.get():
            included_player_numbers = include_players_entry.get().split(", ")
        if exclude_players_entry.get():
            excluded_player_numbers = exclude_players_entry.get().split(", ")
        success = create_stacks_table(quarterback, dst, included_player_numbers, excluded_player_numbers)
        now = time.time()
        if not success:
            output_statement = "You must select a quarterback to build a stack"
        else:
            output_statement = "  This script took " + get_time(start, now) + " seconds to build all valid stacks."

        output_line1_var.set(output_statement)
        print(output_statement)

    def write_stacks():
        if table_exists("stacks"):
            start = time.time()
            write_rosters_to_csv()
            now = time.time()
            output_statement = "  This script took " + get_time(start, now) + " seconds to write the CSV file."
        else:
            output_statement = "There are no stacks to write"
        output_line1_var.set(output_statement)
        print(output_statement)

    style = Style()
    style.configure('W.TButton', font=('calibri', 10, 'bold', 'underline'), foreground='blue')

    create_rosters_button = ttk.Button(root, text="Reset Rosters", style='W.TButton', command=create_rosters)
    get_statistics_button = ttk.Button(root, text="Get Statistics", style='W.TButton', command=get_statistics)
    build_stacks_button = ttk.Button(root, text="Build Stacks", style='W.TButton', command=create_stacks)
    filter_players_button = ttk.Button(root, text="Write CSV File", style='W.TButton', command=write_stacks)

    output_line1_label.grid(row=0, column=0)
    create_rosters_button.grid(row=1, column=0)
    last_updated_label.grid(row=2, column=0)
    get_statistics_button.grid(row=3, column=0)
    number_of_rosters_label.grid(row=4, column=0)
    max_ratio_label.grid(row=5, column=0)
    max_projection_label.grid(row=6, column=0)
    build_stacks_button.grid(row=7, column=0)
    quarterback_label.grid(row=8, column=0)
    quarterback_entry.grid(row=9, column=0)
    dst_label.grid(row=10, column=0)
    dst_entry.grid(row=11, column=0)
    include_players_label.grid(row=12, column=0)
    include_players_entry.grid(row=13, column=0)
    exclude_players_label.grid(row=14, column=0)
    exclude_players_entry.grid(row=15, column=0)
    filter_players_button.grid(row=16, column=0)
    number_of_players_label.grid(row=17, column=0)
    player_list_label.grid(row=18, column=0)

    mainloop()
