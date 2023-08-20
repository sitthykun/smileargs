# built-in
import re
import sys
from typing import Any, Union


class SmileArgs:
	"""

	"""
	class CommandCollection:
		def __init__(self):
			"""

			"""
			# public
			self.description    = ''
			self.cmdLong        = None
			self.cmdShort       = None
			self.num            = 0
			self.priority       = 0
			self.value          = None

	class Key:
		"""

		"""
		# key
		DESCRIPTION = 'd'
		LONG        = 'l'
		NUM         = 'n'
		PRIORITY    = 'p'
		SHORT       = 's'
		VALUE       = 'v'

	class OptionPrefixSymbol:
		"""

		"""
		LONG    = '--'
		SHORT   = '-'

	class OptionDelimiterSymbol:
		"""

		"""
		COLON   = ':'
		EQUAL   = '='

	class Priority:
		"""

		"""
		IGNORE  = 0
		LOW     = 1
		MEDIUM  = 2
		HIGH    = 3

	def __init__(self):
		"""

		"""
		# private
		self.__commandAssignedSymbol= self.OptionDelimiterSymbol.EQUAL
		self.__commandFound         = []
		self.__commandList          = []
		self.__commandMinNum        = 2
		## command
		self.__args                 = []
		## value
		self.__number               = 1
		## pattern
		self.__patternBase          = '([(\-\-)(\-)]+\w+)(=?(\w+)?)'

	def __appearCollection(self, arg: str) -> None:
		"""

		:param arg:
		:return:
		"""
		if self.__isValidValue(arg):
			#
			result = re.match(self.__patternBase, arg)
			# command value
			# result[0] result[2]
			if self.__isLongCommand(result[0]):
				# long command
				self.__args.append({
					self.Key.LONG   : result[0]
					, self.Key.SHORT: ''
					, self.Key.VALUE: result[2]
				})

			else:
				# short command
				self.__args.append({
					self.Key.LONG   : ''
					, self.Key.SHORT: result[0]
					, self.Key.VALUE: result[2]
				})

		else:
			result = re.match(self.__patternBase, arg)
			# result[0]
			if self.__isLongCommand(result[0]):
				#
				self.__args.append({
					self.Key.LONG   : result[0]
					, self.Key.SHORT: ''
					, self.Key.VALUE: ''
				})

			else:
				#
				self.__args.append({
					self.Key.LONG   : ''
					, self.Key.SHORT: result[0]
					, self.Key.VALUE: ''
				})

	def __cleanArg(self) -> list:
		"""

		:return:
		"""
		#
		validList   = []

		# scan valid list
		# start from argv
		for t in sys.argv[1:]:
			#
			if t.split(self.__commandAssignedSymbol):
				pass

		#
		return validList

	def __foundCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		for i in range(self.__commandList.__len__()):
			print(self.__commandList[i].cmdShort)
			# short
			if self.__isShortCommand(command):
				#
				if self.__commandList[i].cmdShort and command == self.__commandList[i].cmdShort:
					# add found
					self.__commandFound.append(self.__commandList[i].num)
					return True
			# long
			elif self.__isLongCommand(command):
				#
				if self.__commandList[i].cmdLong and command == self.__commandList[i].cmdLong:
					# add found
					self.__commandFound.append(self.__commandList[i].num)
					return True

		# nothing
		return False

	def __hasNoValue(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		try:
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '-e')
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '--engine')
			result  = re.match(self.__patternBase, command)

			# ('--engine', '', None)
			return (result.groups()[0]) and (result.groups()[1] == '' and result.groups()[2] is None)

		except Exception as e:
			return False

	def __isLongCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		#
		found   = False

		#
		if command and len(command) >= self.__commandMinNum:
			# --
			if command[:self.__commandMinNum] == self.OptionPrefixSymbol.LONG:
				# 	pass
				found   = True
		#
		return found

	def __isShortCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		#
		found   = False

		#
		if command and len(command) >= self.__commandMinNum:
			# -
			if command[:self.__commandMinNum -1] == self.OptionPrefixSymbol.SHORT:
				# prefix
				# if command[self.__commandMinNum -1:]:
				# 	pass
				found   = True

		#
		return found

	# def __isLong(self, command: str) -> bool:
	# 	"""
	#
	# 	:param command:
	# 	:return:
	# 	"""
	# 	command = f'{self.OptionPrefixSymbol.LONG}{command}'
	# 	# verify len and match
	# 	return len(command) > self.__commandMinNum and command.find(self.OptionPrefixSymbol.LONG) != -1
	#
	# def __isShort(self, command: str) -> bool:
	# 	"""
	#
	# 	:param command:
	# 	:return:
	# 	"""
	# 	command = f'{self.OptionPrefixSymbol.SHORT}{command}'
	# 	# verify len and match
	# 	return len(command) == self.__commandMinNum and command.find(self.OptionPrefixSymbol.SHORT) != -1

	def __isValidFormatCommand(self, args: str) -> bool:
		"""

		:param args:
		:return:
		"""
		try:
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '-e')
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '--engine')
			result = re.match(self.__patternBase, args)

			# --engine => ('--engine', '', None)
			return (result.groups()[0]) and (result.groups()[1] == '' and result.groups()[2] is None)

		except Exception as e:
			return False

	def __isValidValue(self, args: str) -> bool:
		"""

		:param args:
		:return:
		"""
		try:
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '-e')
			# re.match('([(\-\-)(\-)]+\w+)(=?(\w+)?)', '--engine')
			result = re.match(self.__patternBase, args)

			# --engine=dsffads => ('--engine', '=dsffads', 'dsffads')
			return (result.groups()[0] and result.groups()[1] and result.groups()[2])

		except Exception as e:
			return False

	def addCommand(self, shortCommand: str= None, longCommand: str= None, description: str= None, priority: int= Priority.IGNORE, overrideNum: list= []) -> None:
		"""

		:param shortCommand:
		:param longCommand:
		:param description:
		:param priority:
		:param overrideNum:
		:return:
		"""
		# valid that
		if longCommand or shortCommand:
			# increase power by 2
			self.__number *= 2

			# object
			item    = self.CommandCollection()
			# item
			item.description= description
			# main key
			item.cmdLong    = f'{self.OptionPrefixSymbol.LONG}{longCommand}'  if longCommand else None
			item.cmdShort   = f'{self.OptionPrefixSymbol.SHORT}{shortCommand}'  if shortCommand else None
			# special value
			item.num        = self.__number
			item.priority   = priority
			# add to list
			self.__commandList.append(item)

	def findCommand(self, args: str= '') -> bool:
		"""
		@search command
		:param args:
		:return:
		"""
		# command
		commandKey  = ''
		commandLong = ''
		commandShort= ''
		#
		found       = False

		# ([(\-\-)(\-)]+\w+)(=?(\w+)?)
		# after filter and calculation
		return found

	def getCommand(self) -> list:
		"""

		:return:
		"""
		return self.__commandList

	def getNumByCommand(self, command: str) -> int:
		"""

		:param command:
		:return:
		"""
		temp    = 0

		#
		return temp

	def printCommand(self) -> None:
		"""

		:return:
		"""
		print(self.__commandList)

	def removeCommand(self, shortCommand: str, longCommand: str= '') -> None:
		"""

		:param shortCommand:
		:param longCommand:
		:return:
		"""
		# remove short command from list
		try:
			# loop list to find item
			for index in range(len(self.__commandList)):
				#
				for key in self.__commandList[index]:
					# find short command by each element
					if (self.__commandList[index].get(self.Key.SHORT) == shortCommand) or (longCommand and self.__commandList[index].get(self.Key.LONG) == longCommand):
						# del element
						del self.__commandList[index]

		except Exception as e:
			print(f'{str(e)}')

	def run(self) -> None:
		"""

		:return:
		"""
		#
		for a in sys.argv[1:]:
			# print(f'run {a=}')
			if self.__isValidFormatCommand(a) and self.__foundCommand(a):
				self.__appearCollection(a)

		print(f'run appear command: {self.__args}, {self.__commandFound}')
	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol
