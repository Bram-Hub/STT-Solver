# Jonathan Michaels
# 5/6/14
#Edited by Cameron Arsenault and Quin Emerling 
#for UI and additional comments 4/30/21

import tkinter as tk
from tkinter import ttk, Button, Frame, Toplevel, Label, Scale, LEFT, SOLID, SUNKEN, DoubleVar, PhotoImage, Text, messagebox, filedialog
import sys
import math
import urllib.request
import os


class STTUI:
    #Initializing the base Ui, including view (which will be the textbox)
    #and sidebar (which will be the buttons)
    #We also create some flags to be used later. 
    #A flag for autocomplete, reset, a count, and an error flag. 
    #We then run functions to make the buttons and the textbox
    def __init__(self, master):
        self.master = master
        master.title("STT Solver")

        self.view = Frame(self.master, width=450, height=450)
        self.sidebar = Frame(self.master, relief=SUNKEN, bd=2, width=100, height=450)

        #Flag initialization
        self.com = tk.IntVar()
        self.rest = tk.IntVar()
        self.count = tk.IntVar()
        self.error = tk.IntVar()
        self.error.set(0)
        self.statements = []

        #Sidebar and View Positioning
        self.textsize = 60
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)
        
        self.sidebar.grid(row=0, column=1, sticky="e")
        self.view.grid(row=0, column=0, sticky="nsew")

        #Creating buttons and editable textbox
        self.create_buttons(self.sidebar)
        self.create_text_box(self.view)
        self.filename = ''
        self._filetypes = [
        ('Text', '*.txt'),
            ('All files', '*'),
            ]


        #initializing all of the buttons with their default commands
    def create_buttons(self, parent):
        
        self.fileo = Button(parent, text="File Import", justify = "center", width = 14, font=("Questiral, 16"), command=self.import_file)
        self.fileo.grid(row=0, column=0, sticky="nse")
        self.ghelp = Button(parent, text="Gurl Help", justify = "center", width = 14, font=("Questiral, 16"), command=self.girl_help)
        self.ghelp.grid(row=0, column=1, sticky="nse")
        self.start = Button(parent, text="Start", justify = "center", width = 14, font=("Questiral, 16"), command=self.start_solving)
        self.start.grid(row=1, column=0, sticky="nse")
        self.auto = Button(parent, text="Auto-complete", justify = "center", width = 14, font=("Questiral, 16"), command=self.autocom)
        self.auto.grid(row=1, column=1, sticky="nse")
        self.reset = Button(parent, text="Reset", justify = "center", width = 14, font=("Questiral, 16"), command=self.reset_text)
        self.reset.grid(row=2, column=0, sticky="nse")
        self.options = Button(parent, text="Save", justify = "center", width = 14, font=("Questiral, 16"), command=self.save_file)
        self.options.grid(row=2, column=1, sticky="nse")
        self.auto.config(state='disabled')

       #Initialized the textbox into view 
    def create_text_box(self, parent):
        self.view.rowconfigure(0, weight=1) # make textbox expandable
        self.view.columnconfigure(0, weight=1)
        self.entry = Text(parent)
        self.entry.grid(row=0, column=0, sticky = "nsew")


    # parse the input line, giving an error if the input is incorrect 
    # Walks through input line character by character
    # If it encounters a known character, it will assume subsequent known groups of characters
    # to make a valid Statement()
    # If valid pattern is not followed it will give an error 
    def getStatement(self, line, i):
        s = Statement()
        while i < len(line):
            if line[i] == ' ': #Skips new lines
                pass
            elif line[i] == '~' and line[i+1] == '(': 
                result, i = self.getStatement(line, i + 2)
                if s.operation == '':
                    s.first = Statement()
                    s.first.operation = '~'
                    s.first.first = result
                else:
                    s.second = Statement()
                    s.second.operation = '~'
                    
                    s.second.first = result
            elif line[i] == '(':
                result, i = self.getStatement(line, i + 1)
                if s.operation == '':
                    s.first = result
                else:
                    s.second = result

            elif line[i] == ')':
                if s.first == '':
                    tk.messagebox.showerror("error","Invalid input. Check your paranthesese.")
                    self.error.set(1)
                    break
                return s, i
            elif line[i] == '&' or line[i] == '|':
                s.operation = line[i]
            elif line[i] == '<' and line[i+1] == '-' and line[i+2] == '>':
                s.operation = line[i:i+3]
                i += 2
            elif line[i] == '-' and line[i+1] == '>':
                s.operation = line[i:i+2]
                i += 1

            elif line[i] == '~' and line[i+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if s.operation == '' and s.first == '':
                    s.first = Statement()
                    s.first.operation = line[i]
                    s.first.first = Statement(line[i+1])
                elif s.second == '':
                    s.second = Statement()
                    s.second.operation = line[i]
                    s.second.first = Statement(line[i+1])
                else:
                    tk.messagebox.showerror("error", "Invalid input. Check ~ in statements.")
                    self.error.set(1)
                    break
                i += 1
            elif line[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if s.operation == '' and s.first == '':
                    s.first = Statement(line[i])
                elif s.second == '':
                    s.second = Statement(line[i])
                else:
                    tk.messagebox.showerror("error","Invalid input. Unknown literal/Incorrect operations.")
                    self.error.set(1)
                    break
            else:
                tk.messagebox.showerror("error", "Invalid input. Unknown symbol/incorrect syntax")
                self.error.set(1)
                break

            i += 1
        if s.second == '':
            return s.first, i
        else:
            return s, i

    #Parses each line, translating it into a Statement and adds it to a statement list.
    def parseInput(self, f):
        self.statements = []
        self.starting_truth_vars = ''
        for line in f:
            input_line = line.strip()
            if input_line == '' or input_line == '\n' or input_line == ' ': #Skips new lines
                continue
            if input_line[0] == '=':
                self.starting_truth_vars = False
                input_line = input_line[1:]
            elif input_line[0] == '+':
                self.starting_truth_vars = True
                input_line = input_line[1:]
            else:
                tk.messagebox.showerror("error", "Invalid input. Please include initial truth values.")
                self.error.set(1)
                break
            s, temp = self.getStatement(input_line, 0)
            if self.error.get() == 1:
                break
            s.starting_value = self.starting_truth_vars
            self.statements.append(s)
        return self.statements


    # assign all instances of a given literal in all statements to a given truth value
    def assignLiteral(self, statements, literal, assignment):
        returnVal = False
        for statement in statements:
            if statement.assignLiteral(literal, assignment):
                returnVal = True
        return returnVal


    # try to force an assignment in any statement
    def forceAssignment(self, statements):
        for statement in range(len(statements)):
            if statements[statement].forceAssignment():
                return statement
        return -1


    # checks to see if all literals in all statements have been assigned truth values
    def isComplete(self, statements):
        for statement in statements:
            if not statement.isComplete():
                return False
        return True


    #The nitty gritty solving of the short truth table
    def solveTable(self, statements):
        global changedLiterals
        changedLiterals = dict()

        #Setting the final statement as false, and the premises as true
        for statement in statements:
            statement.assignment = statement.starting_value

        #Print opening statement
        self.entry.config(state='normal')
        self.entry.delete("1.0", tk.END)
        self.entry.insert(tk.END, 'Original Statements:\n')
        for statement in range(len(statements)):
            self.entry.insert(tk.END, (str(statement + 1) + ': ' + str(statements[statement]) + '\n' ))
        self.entry.see("end")

        self.entry.config(state='disabled')

        #Setting flags to 0.
        self.count.set(0)
        self.com.set(0)
        self.rest.set(0)
        while True: #Begin main loop

            # look for contradiction, ending if we found one, since we then know it is a valid argument
            for statement in range(len(statements)):
                if not statements[statement].isValid():
                    self.entry.config(state='normal')
                    self.entry.insert(tk.END, 'Contradiction found in Statement ' + str(statement + 1) + '\n')
                    self.entry.config(state='disabled')
                    self.start.config(state='disabled')
                    self.auto.config(state='disabled')
                    self.com.set(0)
                    self.entry.see("end")
                    return

            # see if any literal's truth value needs to be propogated to all statements
            if len(changedLiterals) > 0:
                literal, assignment = changedLiterals.popitem()
                if self.assignLiteral(statements, literal, assignment):
                    toPrint = 'Distributed ' + str(assignment) + ' to all ' + literal + 's'
                else:
                    continue
                if literal in changedLiterals:
                    del changedLiterals[literal]

            # try to force an assignment
            else:
                statement = self.forceAssignment(statements)
                if statement != -1:
                    toPrint = 'Forced assignment in Statement ' + str(statement + 1) + '\n'

                # no assignment was forced. check if the statements are complete
                else:
                    if self.isComplete(statements):
                        self.entry.config(state='normal')
                        self.entry.insert(tk.END,'\nNo contradiction found!\n')
                        self.entry.config(state='disabled')
                        self.start.config(state='disabled')
                        self.auto.config(state='disabled')
                        self.com.set(0)
                        self.entry.see("end")
                    else:
                        self.entry.config(state='normal')
                        self.entry.insert(tk.END,'\nNo forced move.\n')
                        self.entry.config(state='disabled')
                        self.start.config(state='disabled')
                        self.auto.config(state='disabled')
                        self.com.set(0)
                        self.entry.see("end")
                    return

            if self.com.get() == 0: #Check to see if we are autocompleting or not
                self.start.wait_variable(self.count) #Here is what makes us wait for a user input between steps 
            else:
                self.count.set(self.count.get() + 1)

            #Printing the next step
            self.entry.config(state='normal')
            self.entry.insert(tk.END,'\nStep ' + str(self.count.get()) + ' - ' + toPrint +'\n')
            for statement in range(len(statements)):
                self.entry.insert(tk.END, str(statement + 1) + ': ' + str(statements[statement]) + '\n')
            self.entry.config(state='disabled')
            self.entry.see("end")



        #This function uses tkinter to open a file explorer and allow a user to input a file.
        #The file goes directly to the textbox
    def import_file(self):
        self.reset_text()
        fil =  filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        file = open(fil, mode = 'r')
        lines = file.readlines()
        for line in lines:
            self.entry.insert(tk.END, line)
        self.entry.see("end")


        #This function initializes the solving sequence by making the textbox non-changable
    def start_solving(self):
        text = self.entry.get(1.0, tk.END)
        parsed = text.splitlines(keepends=True)
        self.entry.config(state='disabled')

        #parses and creates the statements, unless we encountered an error during parsing
        self.statements.clear()
        self.statements = self.parseInput(parsed)
        if self.error.get() == 1:
            self.entry.config(state='normal')
            self.error.set(0)
            return

        #Removing extra new line characters
        space_counter = 0
        for statement in self.statements:
            if statement == '':
               space_counter += 1

        while space_counter > 0:
            self.statements.remove('')
            space_counter = space_counter - 1

        #check for empty text box
        if len(self.statements) == 0:
                tk.messagebox.showerror("error", "Invalid input. Please write something!")
                self.entry.config(state='normal')
                return

        #We change the start button to the next button and then start solving the table
        self.auto.config(state='normal')
        self.start.config(text="Next", command=self.next_step)
        self.solveTable(self.statements)
        if self.rest.get() == 1:
            self.rest.set(0)
            self.reset_text()


    #This function moves the solve table function to its next step
    def next_step(self):
        self.count.set(self.count.get()+1)

    #This function creates the help window when the help button is pressed. This is simply a textbox that cannot be changed with some pre-written text there
    def girl_help(self):
        self.help_window = tk.Toplevel(self.master)
        self.help_window.grid()
        self.help_window.resizable(False, False)
        self.help_text = tk.Text(self.help_window, bg="lightgray")
        self.help_text.grid()
        self.help_text.insert("1.0", '''Valid Input Symbols:\nNOT : ~\nAND : &\nOR : |\nCONDITIONAL : ->\nBICONDITIONAL : <->\n
Possible literals are any capital letter\nSeparate premises with newline characters. 
Denote starting truth values using + for true and = for false. Put these at the start of each expression.\nUse the scrollwheel to see next steps that go beyond the box.\n\nFILE IMPORT: Select a txt file to put in the entry box\nGURL HELP: Finds this window (you already did it!)
START: Press start after inputing premises and conclusion to begin.\nNEXT: Procedes to the next step.\nAUTO-COMPLETE: Automatically displays all steps.
RESET: Sets the program to its default state, removing any current text.\nDo this especially when in the middle of a proof.\nSAVE: Saves anything in the text box to a desired location as a txt file.''')
        self.help_text.config(state="disabled")


    #saves file, keeping same name as before if it has been named, or calls save_file_as if there is no name
    def save_file(self, whatever = None):
        if (self.filename == ''):
            self.save_file_as()
        else:
            f = open(self.filename, 'w')
            f.write(self.entry.get('1.0', 'end'))
            f.close()

    #asks user for name of file and location before saving the file.
    def save_file_as(self, whatever = None):
        self.filename = tk.filedialog.asksaveasfilename(defaultextension='.txt',
                                                             filetypes = self._filetypes)
        f = open(self.filename, 'w')
        f.write(self.entry.get('1.0', 'end'))
        f.close()

    #This function deletes all text in the text box, reenables typing and changes the "start" button back to its inital state.
    #Additionally flags the restart variable, which will allow us to finish the current table without sending it to the user.
    def reset_text(self):
        self.com.set(1)
        self.rest.set(1)
        self.count.set(self.count.get() + 1)
        self.auto.config(state='disabled')
        self.entry.config(state="normal")
        self.entry.delete("1.0", tk.END)
        self.start.config(text="Start", command=self.start_solving, state='normal')

    #This function turns on the autocomplete flag, which will no longer ask for the user to click the next button 
    def autocom(self):
        self.com.set(1)
        self.count.set(self.count.get() + 1)


#The statement class represents each individual premise and conclusion. 
#A statement is comprised of a first and second section. This assignment recursses until we reach a literal statement 
class Statement:
    def __init__(self, first=''):
        if first != '':
            self.type = 'literal'
        else:
            self.type = 'expression'
        self.first = first
        self.second = ''
        self.operation = ''
        self._assignment = ''
        self.starting_value = ''

    @property
    def assignment(self):
        return self._assignment

    @assignment.setter
    def assignment(self, value):
        if self.type == 'literal':
            global changedLiterals
            changedLiterals[self.first] = value
        self._assignment = value


    # checks to see if there are any contradictions in the statement
    def isValid(self):
        if self.second == '': #This is the case where we have a literal (our base case) It's false if there's a not unside while the assignments match.
            if self.operation == '~' and self.assignment != '' and self.first.assignment != '' and self.assignment == self.first.assignment:
                return False  
            else:
                return True
        elif not (self.first.isValid() and self.second.isValid()): #This checks inner assignments
            return False

        elif self.assignment == '' or (self.first.assignment == '' and self.second.assignment == ''): #If they currently have no assignment, they do not contradict
            return True

        elif self.operation == '|': #Or operation passes if...
            if self.assignment: #the or itself has a value, either side of statement is true/has no current value or...
                return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == True or self.second.assignment == True
            else: #if or does not have a value it passes if either side of the statement is true
                return not (self.first.assignment == True or self.second.assignment == True)

        elif self.operation == '&': #And operation passes if...
            if self.assignment: #it has an assignment and both sides of it are true
                return not (self.first.assignment == False or self.second.assignment == False)
            else: #or both sides have an assignment of true
                return not (self.first.assignment == True and self.second.assignment == True)

        elif self.operation == '->': #The implication passes if....
            if self.assignment: #It has an assignment and either side has no value, or the first value is false or the second value is true
                return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == False or self.second.assignment == True
            else: #If it does not have an assignment, it passes only if the right is false or the right is true. 
                return not (self.first.assignment == False or self.second.assignment == True)

        elif self.operation == '<->': #The biconditional passes if....
            if self.assignment: #it has an assignment and either side doesnt have an assignment or if both sides match each other
                return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == self.second.assignment
            else: #or if both sides match each other
                return not (self.first.assignment == self.second.assignment)


    # try to force an assignment based on logical rules. 
    # We go over every possible situation for each operator, assigning a value where possible
    # If no situations match what we currently have, we make our success flag False, which means we must go deeper into the statement
    def forceAssignment(self):
        success = True

        if self.type == 'literal': #This means there are no possible assignments left for this statement
            return False


        #Handles OR Operation
        elif self.operation == '|': 
            if self.assignment == True and self.first.assignment == False and self.second.assignment == '':
                self.second.assignment = True
            elif self.assignment == True and self.second.assignment == False and self.first.assignment == '':
                self.first.assignment = True
            elif self.assignment == False and (self.first.assignment == '' or self.second.assignment == ''):
                self.first.assignment = False
                self.second.assignment = False
            elif (self.first.assignment == True or self.second.assignment == True) and self.assignment == '':
                self.assignment = True
            elif self.first.assignment == False and self.second.assignment == False and self.assignment == '':
                self.assignment = False
            else:
                success = False

        #Handles AND Operation
        elif self.operation == '&':
            if self.assignment == True and (self.first.assignment == '' or self.second.assignment == ''):
                self.first.assignment = True
                self.second.assignment = True
            elif self.assignment == False and self.first.assignment == True and self.second.assignment == '':
                self.second.assignment = False
            elif self.assignment == False and self.second.assignment == True and self.first.assignment == '':
                self.first.assignment = True
            elif self.first.assignment == True and self.second.assignment == True and self.assignment == '':
                self.assignment = True
            elif (self.first.assignment == False or self.second.assignment == False) and self.assignment == '':
                self.assignment = False
            else:
                success = False

        #Handles COND Operation
        elif self.operation == '->':
            if self.assignment == True and self.first.assignment == True and self.second.assignment == '':
                self.second.assignment = True
            elif self.assignment == True and self.second.assignment == False and self.first.assignment == '':
                self.first.assignment = False
            elif self.assignment == False and (self.first.assignment == '' or self.second.assignment == ''):
                self.first.assignment = True
                self.second.assignment = False
            elif (self.first.assignment == False or self.second.assignment == True) and self.assignment == '':
                self.assignment = True
            elif self.first.assignment == True and self.second.assignment == False and self.assignment == '':
                self.assignment = False
            else:
                success = False

        #BICOND
        elif self.operation == '<->':
            if self.assignment == True and self.first.assignment != '' and self.second.assignment == '':
                self.second.assignment = self.first.assignment
            elif self.assignment == True and self.second.assignment != '' and self.first.assignment == '':
                self.first.assignment = self.second.assignment
            elif self.assignment == False and self.first.assignment != '' and self.second.assignment == '':
                self.second.assignment = not self.first.assignment
            elif self.assignment == False and self.second.assignment != '' and self.first.assignment == '':
                self.first.assignment = not self.second.assignment
            elif self.first.assignment != '' and self.second.assignment != '' and self.first.assignment == self.second.assignment and self.assignment == '':
                self.assignment = True
            elif self.first.assignment != '' and self.second.assignment != '' and self.first.assignment != self.second.assignment and self.assignment == '':
                self.assignment = False
            else:
                success = False

        #Handles NOT Operation
        elif self.operation == '~':
            if self.assignment == True and self.first.assignment == '':
                self.first.assignment = False
            elif self.assignment == False and self.first.assignment == '':
                self.first.assignment = True
            elif self.first.assignment == True and self.assignment == '':
                self.assignment = False
            elif self.first.assignment == False and self.assignment == '':
                self.assignment = True
            else:
                success = False

        if success:
            return True
        if self.second != '': #If we didnt find something then we need to force assignments. (on both if this is an expression)
            return self.first.forceAssignment() or self.second.forceAssignment()
        else: #Or on just one if this is a literal
            return self.first.forceAssignment()
                

    # assign all instances of a given literal to a given truth value
    def assignLiteral(self, literal, assignment):
        if self.type == 'literal':
            if self.first == literal and self.assignment == '':
                self.assignment = assignment #If literal matches current literal and does not have an assignment, match the current assignment
                return True
        elif self.second == '':
            return self.first.assignLiteral(literal, assignment)
        else:
            return self.first.assignLiteral(literal, assignment) or self.second.assignLiteral(literal, assignment)

        return False


    # checks to see if all litearls have been assigned a truth value
    def isComplete(self):
        if self.type == 'literal' and self.assignment != '':
            return True
        elif self.second == '':
            return self.assignment != '' and self.first.isComplete()
        else:
            return self.assignment != '' and self.first.isComplete() and self.second.isComplete()


    # Getting truth values from statement objects to be used in printing
    def getAssignmentText(self):
        if self.assignment == True:
            return 'T'
        elif self.assignment == False:
            return 'F'
        else:
            return ' '

    #Assembles the text to be printed including the assigned truth values.
    def getText(self):  
        if self.operation == '~':
            firstLine, secondLine = self.first.getText()
            firstLine = '~' + firstLine
            secondLine = self.getAssignmentText() + secondLine
            return firstLine, secondLine
        elif self.second == '':
            if self.type == 'literal':
                return self.first, self.getAssignmentText()
            else:
                return self.first.getText()
        else:
            firstFirstLine, firstSecondLine = self.first.getText()
            secondFirstLine, secondSecondLine = self.second.getText()
            firstLine = '(' + firstFirstLine + ' ' + self.operation + ' ' + secondFirstLine + ')'
            secondLine = ' ' + firstSecondLine + ' ' + self.getAssignmentText() + ' '*len(self.operation) + secondSecondLine + ' '
            return firstLine, secondLine

    #Defines a string that represents this class
    def __repr__(self):
        firstLine, secondLine = self.getText()
        return firstLine + '\n   ' + secondLine
    

#Main begins here

#We create a root window, and initialize the mainloop using our STTUI class
root = tk.Tk()
root.minsize(450, 200)
app = STTUI(root)
root.mainloop()