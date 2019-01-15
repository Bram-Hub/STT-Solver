# Jonathan Michaels
# 5/6/14

import sys

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
	global changedLiterals
	changedLiterals = dict()

	for statement in statements[:-1]:
		statement.assignment = True
	statements[-1].assignment = False

	print('Original Statements:')
	for statement in range(len(statements)):
		print(str(statement + 1) + ': ' + str(statements[statement]))

	count = 0
	while True:
		# look for contradiction
		for statement in range(len(statements)):
			if not statements[statement].isValid():
				print('\nContradiction found in Statement ' + str(statement + 1) + '! Therefore, this is valid.')
				return

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
					print('\nNo contradiction found! Therefore, this is invalid.')
				else:
					print('\nNo forced move')
				return

		input()
		count += 1
		print('\nStep ' + str(count) + ' - ' + toPrint)
		for statement in range(len(statements)):
			print(str(statement + 1) + ': ' + str(statements[statement]))
	

if len(sys.argv) != 2:
	# ask for input file if none is provided
	if len(sys.argv) == 1:
		sys.argv.append(input("Enter input file: "))
	else:
		print('Invalid command line arguments.')
		sys.exit()

f = open(sys.argv[1]).readlines()
statements = parseInput(f)
solveTable(statements)





