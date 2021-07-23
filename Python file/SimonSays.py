"""
Simon Says
Written by Santiago Reyes

"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import tkinter.ttk as ttk
import os
import sys
import time
from pathlib import Path
import numpy
import random
import re

# We place everything inside a main function so we can restart the program upon theme change


def main():
    # Main window is created
    root = tk.Tk()
    root.geometry('1000x800')
    root.title("Simon Says")

    # We use a Try except to read/create the file
    # First we read the high score, then we read the current game theme
    try:
        cosa = open("simonsays_highscore.txt")
        contenido = cosa.read()
        var = contenido.split(",")
        hs = var[0]
        on_theme = var[1]
    except:
        cosa = open("simonsays_highscore.txt", "w")
        cosa.write("0,Lavander")
        cosa.close()
        hs = "0"
        on_theme = "Lavander"
    # We create the global variables for high_score and game_theme
    global high_score
    high_score = hs
    global game_theme
    game_theme = on_theme
    # We assign hexadecimal color codes depending on the game theme that is specified in the txt file
    if game_theme == "Lavander":
        background_color = "#272727"
        button_pressed = "#7715DA"
        button_passive = "#9F43FC"
        text_color = "#ffffff"
        pattern_color = "#9DE96B"
        number_color = "#000000"
    elif game_theme == "Noir":
        background_color = "#909195"
        button_pressed = "#3A383B"
        button_passive = "#4F4F51"
        text_color = "#E2E3E5"
        pattern_color = "#EBEBEB"
        number_color = "#000000"
    elif game_theme == "Royale":
        background_color = "#F0FAEF"
        button_pressed = "#47799C"
        button_passive = "#A6D9DC"
        text_color = "#243859"
        pattern_color = "#E63C49"
        number_color = "#243859"
    elif game_theme == "Custom":
        cosa = open("simonsays_highscore.txt")
        contenido = cosa.read()
        var = contenido.split(",")
        # backg,button,buttonpress,pattern,text,number
        background_color = var[2]
        button_pressed = var[4]
        button_passive = var[3]
        text_color = var[6]
        pattern_color = var[5]
        number_color = var[7]

    root.config(bg=background_color)

    level = 1
    score = 1
    valoractx = 10
    valoracty = 10
    carry_on = IntVar()
    # new_sequence is the sequence of buttons that need to be pressed for a specific level
    global new_sequence
    new_sequence = []
    global keep_playing
    keep_playing = None

    # We use this function for whenever the player loses
    def gameover():
        score = str(len(new_sequence))
        message = "The game is over, you got to level "+score+"\nThank you for playing!"
        gg = messagebox.showinfo("GAME OVER", message)

    # This is the function that is called whenever the player opens the settings
    def open_settings():
        font_submit = tkFont.Font(family="Lucida Grande", size=10)
        settings_window = Toplevel()
        settings_window.geometry("500x500")
        settings_window.config(bg=background_color)

        def reset_theme():
            cosa = open("simonsays_highscore.txt", "w")
            cosa.write(str(high_score)+",Lavander")
            cosa.close()
            settings_window.destroy()
            root.destroy()
            main()

        # A function is defined for whener the actual game theme changes
        def submit_theme(type_theme, backg, button, buttonpress, pattern, text, number):
            global game_theme
            # Whenever the game theme is not Custom, we only need to rewrite the name of the theme (Lavander,Noir,Royale)
            if type_theme != "Custom":
                if type_theme == "Lavander":
                    game_theme = "Lavander"
                    cosa = open("simonsays_highscore.txt", "w")
                    cosa.write(str(high_score)+",Lavander")
                    cosa.close()
                    settings_window.destroy()
                    root.destroy()
                    main()
                elif type_theme == "Noir":
                    game_theme = "Noir"
                    cosa = open("simonsays_highscore.txt", "w")
                    cosa.write(str(high_score)+",Noir")
                    cosa.close()
                    settings_window.destroy()
                    root.destroy()
                    main()
                elif type_theme == "Royale":
                    game_theme = "Royale"
                    cosa = open("simonsays_highscore.txt", "w")
                    cosa.write(str(high_score)+",Royale")
                    cosa.close()
                    settings_window.destroy()
                    root.destroy()
                    main()
            #If the game theme IS custom, then we need to do a bit more work to validate the colors and assign them to the txt file
            else:
                game_theme = "Custom"
                # Confirm all options are available:
                valid_backg = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', backg)
                valid_button = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', button)
                valid_buttonpress = re.search(
                    r'^#(?:[0-9a-fA-F]{3}){1,2}$', buttonpress)
                valid_pattern = re.search(
                    r'^#(?:[0-9a-fA-F]{3}){1,2}$', pattern)
                valid_text = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', text)
                valid_number = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', number)
                valid_attributes = True

                if not valid_backg:
                    invalid_backgmsg = "We're sorry, but "+backg + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_backg_box = messagebox.showerror(
                        "Invalid Background Color", invalid_backgmsg)
                    valid_attributes = False
                if not valid_button:
                    invalid_buttonmsg = "We're sorry, but "+button + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_button_box = messagebox.showerror(
                        "Invalid Button Color", invalid_buttonmsg)
                    valid_attributes = False
                if not valid_buttonpress:
                    invalid_buttonpressmsg = "We're sorry, but "+buttonpress + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_buttonpress_box = messagebox.showerror(
                        "Invalid Pressed Button Color", invalid_buttonpressmsg)
                    valid_attributes = False
                if not valid_pattern:
                    invalid_patternmsg = "We're sorry, but "+pattern + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_pattern_box = messagebox.showerror(
                        "Invalid Pattern Color", invalid_patternmsg)
                    valid_attributes = False
                if not valid_text:
                    invalid_textmsg = "We're sorry, but "+text + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_backg_box = messagebox.showerror(
                        "Invalid Text Color", invalid_textmsg)
                    valid_attributes = False
                if not valid_number:
                    invalid_numbermsg = "We're sorry, but "+text + \
                        " is not a valir color.\nRemember the color needs to be a hexadecimal color code, try again!"
                    invalid_number_box = messagebox.showerror(
                        "Invalid Text Color", invalid_numbermsg)
                    valid_attributes = False

                if valid_attributes:
                    custom_settings = backg+","+button+"," + \
                        buttonpress+","+pattern+","+text+","+number
                    cosa = open("simonsays_highscore.txt", "w")
                    cosa.write(str(high_score)+",Custom,"+custom_settings)
                    cosa.close()
                    settings_window.destroy()
                    root.destroy()
                    main()

        #We call this function whenever one of the radio buttons in the settings menu is pressed (used to display the current theme colors)
        def change_theme(new_theme):
            if new_theme != "Custom":
                background_color_entry.config(state='normal')
                button_color_entry.config(state='normal')
                button_press_entry.config(state='normal')
                pattern_color_entry.config(state='normal')
                number_color_entry.config(state='normal')
                text_color_entry.config(state='normal')

                background_color_entry.delete(0, END)
                button_color_entry.delete(0, END)
                button_press_entry.delete(0, END)
                pattern_color_entry.delete(0, END)
                number_color_entry.delete(0, END)
                text_color_entry.delete(0, END)
                if new_theme == "Lavander":
                    background_color_entry.insert(0, "#272727")
                    button_color_entry.insert(0, "#9F43FC")
                    button_press_entry.insert(0, "#7715DA")
                    pattern_color_entry.insert(0, "#9DE96B")
                    number_color_entry.insert(0, "#000000")
                    text_color_entry.insert(0, "#ffffff")
                elif new_theme == "Noir":
                    background_color_entry.insert(0, "#909195")
                    button_color_entry.insert(0, "#4F4F51")
                    button_press_entry.insert(0, "#3A383B")
                    pattern_color_entry.insert(0, "#EBEBEB")
                    number_color_entry.insert(0, "#000000")
                    text_color_entry.insert(0, "#E2E3E5")
                elif new_theme == "Royale":
                    background_color_entry.insert(0, "#F0FAEF")
                    button_color_entry.insert(0, "#A6D9DC")
                    button_press_entry.insert(0, "#47799C")
                    pattern_color_entry.insert(0, "#E63C49")
                    number_color_entry.insert(0, "#243859")
                    text_color_entry.insert(0, "#243859")
                background_color_entry.config(state='disabled')
                button_color_entry.config(state='disabled')
                button_press_entry.config(state='disabled')
                pattern_color_entry.config(state='disabled')
                number_color_entry.config(state='disabled')
                text_color_entry.config(state='disabled')
            else:
                background_color_entry.config(state='normal')
                button_color_entry.config(state='normal')
                button_press_entry.config(state='normal')
                pattern_color_entry.config(state='normal')
                number_color_entry.config(state='normal')
                text_color_entry.config(state='normal')
                background_color_entry.delete(0, END)
                button_color_entry.delete(0, END)
                button_press_entry.delete(0, END)
                pattern_color_entry.delete(0, END)
                number_color_entry.delete(0, END)
                text_color_entry.delete(0, END)
                try:
                    cosa = open("simonsays_highscore.txt")
                    contenido = cosa.read()
                    var = contenido.split(",")
                    # backg,button,buttonpress,pattern,text,number
                    background_color_entry.insert(0, var[2])
                    button_color_entry.insert(0, var[3])
                    button_press_entry.insert(0, var[4])
                    pattern_color_entry.insert(0, var[5])
                    number_color_entry.insert(0, var[7])
                    text_color_entry.insert(0, var[6])
                except:
                    background_color_entry.insert(0, "#")
                    button_color_entry.insert(0, "#")
                    button_press_entry.insert(0, "#")
                    pattern_color_entry.insert(0, "#")
                    number_color_entry.insert(0, "#")
                    text_color_entry.insert(0, "#")

        #Here is where the settings menu is actually displayed/created
        theme_text = Label(settings_window, text="Theme:",
                           bg=background_color, fg=text_color)
        theme_text.place(x=5, y=11)
        theme = StringVar()
        theme.set("Lavander")
        if game_theme == "Lavander":
            theme.set("Lavander")
        elif game_theme == "Noir":
            theme.set("Noir")
        elif game_theme == "Royale":
            theme.set("Royale")
        elif game_theme == "Custom":
            theme.set("Custom")
        # Radio buttons to choose theme
        lavander_button = Radiobutton(settings_window, text="Lavander", variable=theme, value="Lavander", selectcolor=background_color,
                                      activebackground=background_color, command=lambda: change_theme(theme.get()), activeforeground=text_color)
        lavander_button.config(bg=background_color, fg=text_color)
        lavander_button.place(x=60, y=10)

        noir_button = Radiobutton(settings_window, text="Noir", variable=theme, value="Noir", selectcolor=background_color,
                                  activebackground=background_color, command=lambda: change_theme(theme.get()), activeforeground=text_color)
        noir_button.config(bg=background_color, fg=text_color)
        noir_button.place(x=140, y=10)

        french_button = Radiobutton(settings_window, text="Royale", variable=theme, value="Royale", selectcolor=background_color,
                                    activebackground=background_color, command=lambda: change_theme(theme.get()), activeforeground=text_color)
        french_button.config(bg=background_color, fg=text_color)
        french_button.place(x=220, y=10)

        custom_button = Radiobutton(settings_window, text="Custom", variable=theme, value="Custom", selectcolor=background_color,
                                    activebackground=background_color, command=lambda: change_theme(theme.get()), activeforeground=text_color)
        custom_button.config(bg=background_color, fg=text_color)
        custom_button.place(x=300, y=10)

        # Entry fields for colors
        background_color_text = Label(
            settings_window, text="Background Color:", fg=text_color, bg=background_color)
        background_color_text.place(x=5, y=90)
        background_color_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        background_color_entry.place(x=200, y=90)

        button_color_text = Label(
            settings_window, text="Button Color:", fg=text_color, bg=background_color)
        button_color_text.place(x=5, y=140)
        button_color_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        button_color_entry.place(x=200, y=140)

        button_press_text = Label(
            settings_window, text="Pressed Button Color:", fg=text_color, bg=background_color)
        button_press_text.place(x=5, y=190)
        button_press_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        button_press_entry.place(x=200, y=190)

        pattern_color_text = Label(
            settings_window, text="Pattern Color:", fg=text_color, bg=background_color)
        pattern_color_text.place(x=5, y=240)
        pattern_color_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        pattern_color_entry.place(x=200, y=240)

        number_color_text = Label(
            settings_window, text="Number Color:", fg=text_color, bg=background_color)
        number_color_text.place(x=5, y=290)
        number_color_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        number_color_entry.place(x=200, y=290)

        text_color_text = Label(
            settings_window, text="Text Color:", fg=text_color, bg=background_color)
        text_color_text.place(x=5, y=340)
        text_color_entry = Entry(
            settings_window, width=15, bg=pattern_color, fg=number_color)
        text_color_entry.place(x=200, y=340)

        if game_theme == "Lavander":
            background_color_entry.insert(0, "#272727")
            button_color_entry.insert(0, "#9F43FC")
            button_press_entry.insert(0, "#7715DA")
            pattern_color_entry.insert(0, "#9DE96B")
            number_color_entry.insert(0, "#000000")
            text_color_entry.insert(0, "#ffffff")

            background_color_entry.config(state='disabled')
            button_color_entry.config(state='disabled')
            button_press_entry.config(state='disabled')
            pattern_color_entry.config(state='disabled')
            number_color_entry.config(state='disabled')
            text_color_entry.config(state='disabled')
        elif game_theme == "Noir":
            background_color_entry.insert(0, "#909195")
            button_color_entry.insert(0, "#4F4F51")
            button_press_entry.insert(0, "#3A383B")
            pattern_color_entry.insert(0, "#EBEBEB")
            number_color_entry.insert(0, "#000000")
            text_color_entry.insert(0, "#E2E3E5")

            background_color_entry.config(state='disabled')
            button_color_entry.config(state='disabled')
            button_press_entry.config(state='disabled')
            pattern_color_entry.config(state='disabled')
            number_color_entry.config(state='disabled')
            text_color_entry.config(state='disabled')
        elif game_theme == "Royale":
            background_color_entry.insert(0, "#F0FAEF")
            button_color_entry.insert(0, "#A6D9DC")
            button_press_entry.insert(0, "#47799C")
            pattern_color_entry.insert(0, "#E63C49")
            number_color_entry.insert(0, "#243859")
            text_color_entry.insert(0, "#243859")

            background_color_entry.config(state='disabled')
            button_color_entry.config(state='disabled')
            button_press_entry.config(state='disabled')
            pattern_color_entry.config(state='disabled')
            number_color_entry.config(state='disabled')
            text_color_entry.config(state='disabled')
        elif game_theme == "Custom":
            try:
                cosa = open("simonsays_highscore.txt")
                contenido = cosa.read()
                var = contenido.split(",")
                # backg,button,buttonpress,pattern,text,number
                background_color_entry.insert(0, var[2])
                button_color_entry.insert(0, var[3])
                button_press_entry.insert(0, var[4])
                pattern_color_entry.insert(0, var[5])
                number_color_entry.insert(0, var[7])
                text_color_entry.insert(0, var[6])
            except:
                background_color_entry.insert(0, "#")
                button_color_entry.insert(0, "#")
                button_press_entry.insert(0, "#")
                pattern_color_entry.insert(0, "#")
                number_color_entry.insert(0, "#")
                text_color_entry.insert(0, "#")

        submit_changes_button = Button(settings_window, text="SUBMIT CHANGES", font=font_submit, fg=number_color, bg=button_passive, width=15, height=3, command=lambda: submit_theme(
            theme.get(),
            str(background_color_entry.get()),
            str(button_color_entry.get()),
            str(button_press_entry.get()),
            str(pattern_color_entry.get()),
            str(text_color_entry.get()),
            str(number_color_entry.get())
        ))  # Submit Changes Button
        submit_changes_button.place(anchor=CENTER, x=250, y=450)

        reset_settings_button = Button(settings_window, text="Reset settings",
                                       fg="#000000", bg="#ffffff", width=10, height=2, command=reset_theme)
        reset_settings_button.place(anchor=CENTER, x=60, y=450)
        settings_window.mainloop()

    # This function is called when one of the game tiles (squares) is clicked
    # A comparison is made between the pressed tile and the next tile in the sequence
    # If the button you pressed does not match the next button in the sequence, the game is over

    def click_cuadro(s, number, seq):
        global new_sequence
        global high_score
        if len(seq) == 0:
            keep_playing = False
        else:
            if seq[0] == number:
                seq.pop(0)
                if len(seq) == 0:
                    # We add a new element to the sequence when the length of the sequence gets to zero (all of the sequence has been replicated by the player)
                    num = random.randint(1, 25)
                    new_sequence.append(num)
                    current_score_text.config(
                        text="Level: "+str(len(new_sequence)))
                    begin_game(sequence)

            else:
                # We update the high score to whatever the new score is (if it surpasses the value of the previous high score)
                if len(new_sequence) > int(high_score):
                    cosa = open("simonsays_highscore.txt", "w")
                    high_score = str(len(new_sequence))
                    if game_theme != "Custom":
                        newFileText = high_score+","+game_theme
                        cosa.write(newFileText)
                    else:
                        custom_settings = background_color+","+button_passive+"," + \
                        button_pressed+","+pattern_color+","+text_color+","+number_color
                        newFileText = high_score+",Custom,"+custom_settings
                        cosa.write(newFileText)
                    cosa.close()
                    high_score_text.config(text="High Score: "+high_score)
                gameover()
                num = random.randint(1, 25)
                new_sequence.clear()
                new_sequence.append(num)
                seq.clear()
                keep_playing = False
                play.config(state=NORMAL)
                current_score_text.config(
                    text="Level: "+str(len(new_sequence)))

    # begin_game shows the actual sequence of the game tiles

    def begin_game(sequence):
        cuadro1.config(state=DISABLED)
        cuadro2.config(state=DISABLED)
        cuadro3.config(state=DISABLED)
        cuadro4.config(state=DISABLED)
        cuadro5.config(state=DISABLED)
        cuadro6.config(state=DISABLED)
        cuadro7.config(state=DISABLED)
        cuadro8.config(state=DISABLED)
        cuadro9.config(state=DISABLED)
        cuadro10.config(state=DISABLED)
        cuadro11.config(state=DISABLED)
        cuadro12.config(state=DISABLED)
        cuadro13.config(state=DISABLED)
        cuadro14.config(state=DISABLED)
        cuadro15.config(state=DISABLED)
        cuadro16.config(state=DISABLED)
        cuadro17.config(state=DISABLED)
        cuadro18.config(state=DISABLED)
        cuadro19.config(state=DISABLED)
        cuadro20.config(state=DISABLED)
        cuadro21.config(state=DISABLED)
        cuadro22.config(state=DISABLED)
        cuadro23.config(state=DISABLED)
        cuadro24.config(state=DISABLED)
        cuadro25.config(state=DISABLED)
        # All of the buttons are disabled while the sequence is playing
        # Then, we "animate" the sequence using time.sleep()
        if sequence == []:
            if new_sequence == []:
                num = random.randint(1, 25)
                new_sequence.append(num)
            for j in new_sequence:
                sequence.append(j)
        for i in sequence:
            if i == 1:
                cuadro1.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro1.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 2:
                cuadro2.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro2.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 3:
                cuadro3.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro3.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 4:
                cuadro4.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro4.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 5:
                cuadro5.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro5.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            if i == 6:
                cuadro6.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro6.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 7:
                cuadro7.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro7.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 8:
                cuadro8.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro8.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 9:
                cuadro9.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro9.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 10:
                cuadro10.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro10.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            if i == 11:
                cuadro11.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro11.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 12:
                cuadro12.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro12.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 13:
                cuadro13.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro13.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 14:
                cuadro14.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro14.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 15:
                cuadro15.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro15.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            if i == 16:
                cuadro16.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro16.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 17:
                cuadro17.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro17.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 18:
                cuadro18.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro18.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 19:
                cuadro19.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro19.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 20:
                cuadro20.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro20.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            if i == 21:
                cuadro21.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro21.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 22:
                cuadro22.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro22.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 23:
                cuadro23.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro23.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 24:
                cuadro24.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro24.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
            elif i == 25:
                cuadro25.config(bg=pattern_color)
                root.update()
                time.sleep(0.75)
                cuadro25.config(bg=button_passive)
                root.update()
                time.sleep(0.25)
        cuadro1.config(state=NORMAL)
        cuadro2.config(state=NORMAL)
        cuadro3.config(state=NORMAL)
        cuadro4.config(state=NORMAL)
        cuadro5.config(state=NORMAL)
        cuadro6.config(state=NORMAL)
        cuadro7.config(state=NORMAL)
        cuadro8.config(state=NORMAL)
        cuadro9.config(state=NORMAL)
        cuadro10.config(state=NORMAL)
        cuadro11.config(state=NORMAL)
        cuadro12.config(state=NORMAL)
        cuadro13.config(state=NORMAL)
        cuadro14.config(state=NORMAL)
        cuadro15.config(state=NORMAL)
        cuadro16.config(state=NORMAL)
        cuadro17.config(state=NORMAL)
        cuadro18.config(state=NORMAL)
        cuadro19.config(state=NORMAL)
        cuadro20.config(state=NORMAL)
        cuadro21.config(state=NORMAL)
        cuadro22.config(state=NORMAL)
        cuadro23.config(state=NORMAL)
        cuadro24.config(state=NORMAL)
        cuadro25.config(state=NORMAL)
        play.config(state=DISABLED)

    # Here we create the "board" composed of 25 buttons, which all call the same function but with different arguments
    cuadro1 = tk.Button(root, text="1", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 1, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro1.place(anchor=CENTER, relx=0.2, rely=0.15, width=100, height=100)
    cuadro2 = tk.Button(root, text="2", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 2, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro2.place(anchor=CENTER, relx=0.35, rely=0.15, width=100, height=100)
    cuadro3 = tk.Button(root, text="3", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 3, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro3.place(anchor=CENTER, relx=0.5, rely=0.15, width=100, height=100)
    cuadro4 = tk.Button(root, text="4", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 4, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro4.place(anchor=CENTER, relx=0.65, rely=0.15, width=100, height=100)
    cuadro5 = tk.Button(root, text="5", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 5, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro5.place(anchor=CENTER, relx=0.8, rely=0.15, width=100, height=100)
    # Second Row
    cuadro6 = tk.Button(root, text="6", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 6, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro6.place(anchor=CENTER, relx=0.2, rely=0.3, width=100, height=100)
    cuadro7 = tk.Button(root, text="7", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 7, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro7.place(anchor=CENTER, relx=0.35, rely=0.3, width=100, height=100)
    cuadro8 = tk.Button(root, text="8", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 8, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro8.place(anchor=CENTER, relx=0.5, rely=0.3, width=100, height=100)
    cuadro9 = tk.Button(root, text="9", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                        command=lambda: click_cuadro(score, 9, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro9.place(anchor=CENTER, relx=0.65, rely=0.3, width=100, height=100)
    cuadro10 = tk.Button(root, text="10", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 10, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro10.place(anchor=CENTER, relx=0.8, rely=0.3, width=100, height=100)
    # Third Row
    cuadro11 = tk.Button(root, text="11", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 11, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro11.place(anchor=CENTER, relx=0.2, rely=0.45, width=100, height=100)
    cuadro12 = tk.Button(root, text="12", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 12, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro12.place(anchor=CENTER, relx=0.35, rely=0.45, width=100, height=100)
    cuadro13 = tk.Button(root, text="13", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 13, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro13.place(anchor=CENTER, relx=0.5, rely=0.45, width=100, height=100)
    cuadro14 = tk.Button(root, text="14", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 14, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro14.place(anchor=CENTER, relx=0.65, rely=0.45, width=100, height=100)
    cuadro15 = tk.Button(root, text="15", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 15, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro15.place(anchor=CENTER, relx=0.8, rely=0.45, width=100, height=100)
    # Fourth Row
    cuadro16 = tk.Button(root, text="16", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 16, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro16.place(anchor=CENTER, relx=0.2, rely=0.6, width=100, height=100)
    cuadro17 = tk.Button(root, text="17", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 17, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro17.place(anchor=CENTER, relx=0.35, rely=0.6, width=100, height=100)
    cuadro18 = tk.Button(root, text="18", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 18, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro18.place(anchor=CENTER, relx=0.5, rely=0.6, width=100, height=100)
    cuadro19 = tk.Button(root, text="19", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 19, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro19.place(anchor=CENTER, relx=0.65, rely=0.6, width=100, height=100)
    cuadro20 = tk.Button(root, text="20", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 20, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro20.place(anchor=CENTER, relx=0.8, rely=0.6, width=100, height=100)
    # Fifth Row
    cuadro21 = tk.Button(root, text="21", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 21, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro21.place(anchor=CENTER, relx=0.2, rely=0.75, width=100, height=100)
    cuadro22 = tk.Button(root, text="22", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 22, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro22.place(anchor=CENTER, relx=0.35, rely=0.75, width=100, height=100)
    cuadro23 = tk.Button(root, text="23", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 23, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro23.place(anchor=CENTER, relx=0.5, rely=0.75, width=100, height=100)
    cuadro24 = tk.Button(root, text="24", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 24, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro24.place(anchor=CENTER, relx=0.65, rely=0.75, width=100, height=100)
    cuadro25 = tk.Button(root, text="25", width=10, pady=10, fg=number_color, bg=button_passive, activebackground=button_pressed,
                         command=lambda: click_cuadro(score, 25, sequence), disabledforeground=number_color, borderwidth=0, activeforeground=number_color)
    cuadro25.place(anchor=CENTER, relx=0.8, rely=0.75, width=100, height=100)
    root.update()

    # This is the very last piece of code, which is where the rest of the objects are created (like the high score text and settings button)
    sequence = []
    new_sequence = sequence.copy()
    font_nombre = tkFont.Font(family="Lucida Grande", size=10)
    font_settings = tkFont.Font(family="Lucida Grande", size=25)
    font_play = tkFont.Font(family="Lucida Grande", size=15)
    name = Label(root, text="Developed by Santiago Reyes",
                 fg=text_color, bg=background_color, font=font_nombre)
    name.place(anchor=CENTER, relx=0.5, rely=0.95)
    play = tk.Button(root, text="Play", padx=10, pady=5, fg="#000000", bg="#84CF3C",
                     command=lambda: begin_game(sequence), font=font_play, disabledforeground="#000000")
    play.place(anchor=CENTER, relx=0.5, rely=0.9)
    settings = tk.Button(root, text="⚙️", padx=10, pady=5, fg="#000000", bg="#909090",
                         command=open_settings, font=font_settings, disabledforeground="#000000", borderwidth=0)
    settings.place(x=0, y=0)
    current_score = 1
    high_score_text = Label(root, text="High Score: "+str(high_score),
                            font=font_nombre, bg=background_color, fg=text_color)
    high_score_text.place(anchor=CENTER, relx=0.5, rely=0.01)
    current_score_text = Label(root, text="Level: "+str(len(new_sequence)),
                               font=font_nombre, bg=background_color, fg=text_color)
    current_score_text.place(anchor=CENTER, relx=0.5, rely=0.05)
    root.mainloop()


main()
