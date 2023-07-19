# built-in
import re
import sys


class SmileArgs:
	"""

	"""
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
		self.__number               = 0
		## pattern
		self.__patternBase          = '([(\-\-)(\-)]+\w+)(=?(\w+)?)'

	def __addCollection(self, arg: str) -> None:
		"""

		:param arg:
		:return:
		"""
		if self.__isValidValue(arg):
			#
			result = re.match(self.__patternBase, arg)
			# command value
			# result[0] result[2]
			if self.__isLong(result[0]):
				#
				self.__args.append({
					self.Key.LONG   : result[0]
					, self.Key.SHORT: ''
					, self.Key.VALUE: result[2]
				})

			else:
				#
				self.__args.append({
					self.Key.LONG   : ''
					, self.Key.SHORT: result[0]
					, self.Key.VALUE: result[2]
				})

		else:
			result = re.match(self.__patternBase, arg)
			# result[0]
			if self.__isLong(result[0]):
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

			# -
			elif command[:self.__commandMinNum -1] == self.OptionPrefixSymbol.SHORT:
				# 	pass
				found   = False

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
			# --
			if command[:self.__commandMinNum] == self.OptionPrefixSymbol.LONG:
				# prefix
				# if command[self.__commandMinNum:]:
				# 	pass
				found   = False

			# -
			elif command[:self.__commandMinNum -1] == self.OptionPrefixSymbol.SHORT:
				# prefix
				# if command[self.__commandMinNum -1:]:
				# 	pass
				found   = True

		#
		return found

	def __isLong(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		return command.find(self.OptionPrefixSymbol.LONG) != -1

	def __isShort(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		return  command.find(self.OptionPrefixSymbol.SHORT) != -1

	def __isValidCommand(self, args: str) -> bool:
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

	def addCommand(self, shortCommand: str, longCommand: str, description: str, priority: int= Priority.IGNORE, overrideNum: list= []) -> None:
		"""

		:param shortCommand:
		:param longCommand:
		:param description:
		:param priority:
		:param overrideNum:
		:return:
		"""
		# increase power by 2
		self.__number   *= 2

		#
		self.__commandList.append(
			{
				# main key
				self.Key.SHORT          : f'{self.OptionPrefixSymbol.SHORT}{shortCommand}'
				, self.Key.LONG         : f'{self.OptionPrefixSymbol.LONG}{longCommand}'
				#
				, self.Key.DESCRIPTION  : description
				, self.Key.PRIORITY     : priority
				# special value
				, self.Key.NUM          : self.__number
			}
		)

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

	def listCommand(self) -> None:
		"""

		:return:
		"""
		pass

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
			if self.__isValidCommand(a):
				self.__addCollection(a)

	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol