# Jonathan Michaels
# 5/6/14

from tkinter import *

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
		if self.second == '':
			if self.operation == '~' and self.assignment != '' and self.first.assignment != '' and self.assignment == self.first.assignment:
				return False
			else:
				return True
		elif not (self.first.isValid() and self.second.isValid()):
			return False
		elif self.assignment == '' or (self.first.assignment == '' and self.second.assignment == ''):
			return True
		elif self.operation == '|':
			if self.assignment:
				return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == True or self.second.assignment == True
			else:
				return not (self.first.assignment == True or self.second.assignment == True)
		elif self.operation == '&':
			if self.assignment:
				return not (self.first.assignment == False or self.second.assignment == False)
			else:
				return not (self.first.assignment == True and self.second.assignment == True)
		elif self.operation == '->':
			if self.assignment:
				return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == False or self.second.assignment == True
			else:
				return not (self.first.assignment == False or self.second.assignment == True)
		elif self.operation == '<->':
			if self.assignment:
				return self.first.assignment == '' or self.second.assignment == '' or self.first.assignment == self.second.assignment
			else:
				return not (self.first.assignment == self.second.assignment)


	# try to force an assignment
	def forceAssignment(self):
		success = True

		if self.type == 'literal':
			return False
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
		if self.second != '':
			return self.first.forceAssignment() or self.second.forceAssignment()
		else:
			return self.first.forceAssignment()
				

	# assign all instances of a given literal to a given truth value
	def assignLiteral(self, literal, assignment):
		if self.type == 'literal':
			if self.first == literal and self.assignment == '':
				self.assignment = assignment
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


	# printing functions
	def getAssignmentText(self):
		if self.assignment == True:
			return 'T'
		elif self.assignment == False:
			return 'F'
		else:
			return ' '

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

	def __repr__(self):
		firstLine, secondLine = self.getText()
		return firstLine + '\n   ' + secondLine


# parse the input file
def getStatement(line, i):
	s = Statement()
	while i < len(line):
		if line[i] == ' ':
			pass
		elif line[i] == '~' and line[i+1] == '(':
			result, i = getStatement(line, i + 2)
			if s.operation == '':
				s.first = Statement()
				s.first.operation = '~'
				s.first.first = result
			else:
				s.second = Statement()
				s.second.operation = '~'
				s.second.first = result
		elif line[i] == '(':
			result, i = getStatement(line, i + 1)
			if s.operation == '':
				s.first = result
			else:
				s.second = result
		elif line[i] == ')':
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
				print('Invalid input file.')
				sys.exit()
			i += 1
		elif line[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			if s.operation == '' and s.first == '':
				s.first = Statement(line[i])
			elif s.second == '':
				s.second = Statement(line[i])
			else:
				print('Invalid input file.')
				sys.exit()
		else:
			print('Invalid input file.')
			sys.exit()

		i += 1
	if s.second == '':
		return s.first, i
	else:
		return s, i


def parseInput(f):
	statements = []
	for line in f:
		s, temp = getStatement(line.strip(), 0)
		statements.append(s)
	return statements


# assign all instances of a given literal in all statements to a given truth value
def assignLiteral(statements, literal, assignment):
	returnVal = False
	for statement in statements:
		if statement.assignLiteral(literal, assignment):
			returnVal = True
	return returnVal


# try to force an assignment in any statement
def forceAssignment(statements):
	for statement in range(len(statements)):
		if statements[statement].forceAssignment():
			return statement
	return -1


# checks to see if all literals in all statements have been assigned truth values
def isComplete(statements):
	for statement in statements:
		if not statement.isComplete():
			return False
	return True


def solveTable(statements):
	result = []
	
	global changedLiterals
	changedLiterals = dict()

	for statement in statements[:-1]:
		statement.assignment = True
	statements[-1].assignment = False

	result.append('Original Statements:\n')
	for statement in range(len(statements)):
		result[0] += str(statement + 1) + ': ' + str(statements[statement]) + "\n"

	count = 0
	while True:
		# look for contradiction
		for statement in range(len(statements)):
			if not statements[statement].isValid():
				result[-1] += '\nContradiction found in Statement ' + str(statement + 1) + '! Therefore, this is valid.\n'
				return result

		# see if any literal's truth value needs to be propogated to all statements
		if len(changedLiterals) > 0:
			literal, assignment = changedLiterals.popitem()
			if assignLiteral(statements, literal, assignment):
				toPrint = 'Distributed ' + str(assignment) + ' to all ' + literal + 's'
			else:
				continue
			if literal in changedLiterals:
				del changedLiterals[literal]

		# try to force an assignment
		else:
			statement = forceAssignment(statements)
			if statement != -1:
				toPrint = 'Forced assignment in Statement ' + str(statement + 1)

			# no assignment was forced. check if the statements are complete
			else:
				if isComplete(statements):
					result[-1] += '\nNo contradiction found! Therefore, this is invalid.\n'
				else:
					result[-1] += '\nNo forced move\n'
				return result

		#input()
		count += 1
		result.append('Step ' + str(count) + ' - ' + toPrint + "\n")
		for statement in range(len(statements)):
			result[-1] += str(statement + 1) + ': ' + str(statements[statement]) + "\n"	


class GUI(object):
	def __init__(self, parent):
		self.parent = parent
		self.parent.title("STT-Solver")
		self.main_frame = Frame(self.parent)  ##parent of this frame
		self.main_frame.pack()  ##make this visible
		self.top_frame = Frame(self.main_frame)
		self.top_frame.pack(side=TOP)
		
		self.bottom_frame = Frame(self.main_frame)
		self.bottom_frame.pack(side=BOTTOM)
		
		self.scrollbar = Scrollbar(self.parent)
		self.scrollbar.pack( side = RIGHT, fill = Y )	
		
		self.text = Text(self.parent, yscrollcommand = self.scrollbar.set, state = DISABLED)
		self.text.pack()
		
		self.scrollbar.config( command = self.text.yview )		
		
		self.button1 = Button(self.top_frame, text="Enter File Name", command=self.enterFileName)
		self.button1.pack(side=LEFT)
		self.button2 = Button(self.top_frame, text="Prev Step", command=self.prevStep)
		self.button2.pack(side=LEFT)
		self.button3=Button(self.top_frame, text="Next Step", command=self.nextStep)
		self.button3.pack(side=LEFT)
		self.button4=Button(self.top_frame, text="Show All Steps", command=self.showAllSteps)
		self.button4.pack(side=LEFT)		
		self.button6 = Button(self.top_frame, text = "Last Step", command = self.lastStep)
		self.button6.pack(side = LEFT)
		
		self.button2.config(state = DISABLED)
		self.button3.config(state = DISABLED)
		self.button4.config(state = DISABLED)
		self.button6.config(state = DISABLED)
		
		self.e1 = ""
		self.file_window = ""
		self.button5 = ""
		self.fileName_error = ""
		self.fileName_entered = False
		
		self.table = []
		self.current = -1 #current represents the state just printed out		
		
		
	    
	def enterFileName(self):
		self.file_window = Toplevel(self.parent)
		self.file_window.title("Enter file name")
		self.file_window.protocol("WM_DELETE_WINDOW", self.callback_file_window)
		
		self.button1.config(state = DISABLED)
		self.button2.config(state = DISABLED)
		self.button3.config(state = DISABLED)
		self.button4.config(state = DISABLED)
		self.button6.config(state = DISABLED)
				
		l1 = Label(self.file_window, text="File Name")
		l1.pack( side = LEFT)		
		
		self.e1 = Entry(self.file_window, bd =5)
		self.e1.pack(side = LEFT)
		
		file_frame = Frame(self.file_window)
		file_frame.pack(side = BOTTOM)			
		
		self.button5 = Button(file_frame, text="Enter")
		self.file_window.bind('<Return>', self.enter_file)
		self.button5.bind('<Button-1>', self.enter_file)
		self.button5.pack(side = RIGHT)
		self.file_window.focus_force()
		self.e1.focus_set()


	def enter_file(self, self2):
		fileName = self.e1.get()
		try:
			f = open(fileName).readlines()
			statements = parseInput(f)
			self.table = solveTable(statements)	
			self.button1.config(state = NORMAL)
			#self.button2.config(state = NORMAL)
			self.button3.config(state = NORMAL)
			self.button4.config(state = NORMAL)
			self.button6.config(state = NORMAL)
			self.current = -1
			self.fileName_entered = True
			
			self.file_window.destroy()
			
			self.nextStep();

		except:
			self.fileName_error = Toplevel(self.parent)
			self.fileName_error.title("File not found")
			self.fileName_error.protocol("WM_DELETE_WINDOW", self.callback_fileName_error)
			l2 = Label(self.fileName_error, text="File does not exist. Close this window and enter a new file to continue")
			l2.pack()
			self.fileName_error.lift()
			self.fileName_error.focus_force()
			
			self.button5.config(state = DISABLED)
			self.file_window.unbind('<Return>')
			self.button5.unbind('<Button-1>')
			
			self.e1.config(state = DISABLED)
					
			
		
	def callback_fileName_error(self):
		self.button5.config(state = NORMAL)
		self.e1.config(state = NORMAL)
		self.file_window.bind('<Return>', self.enter_file)
		self.button5.bind('<Button-1>', self.enter_file)		
		self.fileName_error.destroy()
		
	def callback_file_window(self):
		self.button1.config(state = NORMAL)
		if self.fileName_entered == True:
			self.button3.config(state = NORMAL)
			self.button4.config(state = NORMAL)
			self.button6.config(state = NORMAL)
		try:
			self.fileName_error.destroy()
			self.file_window.destroy()
		except:
			self.file_window.destroy()
		

	def prevStep(self):
		self.current -= 2
		self.nextStep();
		self.button3.config(state = NORMAL)
		if self.current == 0:
			self.button2.config(state = DISABLED)
		
	
	def nextStep(self):
		self.current += 1
		self.text.config(state = NORMAL)
		self.text.delete(1.0,END)
		self.text.insert(END, self.table[self.current])
		self.text.config(state = DISABLED)
		self.button2.config(state = NORMAL)
		
		if self.current == 0:
			self.button2.config(state = DISABLED)
		if self.current == len(self.table)-1:
			self.button3.config(state = DISABLED)
		else:
			self.button3.config(state = NORMAL)		
		
	def lastStep(self):
		self.current = len(self.table) - 2
		self.nextStep();		
	
	def showAllSteps(self):
		self.current = len(self.table) - 1
		self.text.config(state = NORMAL)
		self.text.delete(1.0,END)
		for i in range(len(self.table)):
			self.text.insert(END, self.table[i])		
		self.text.config(state = DISABLED)
		self.button3.config(state = DISABLED)
		self.button2.config(state = NORMAL)
	

if __name__ == "__main__":
	root = Tk()
	gui = GUI(root)
	root.mainloop()	