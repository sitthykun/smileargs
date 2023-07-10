# built-in
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

	class OptionPrefixSymbol:
		"""

		"""
		SHORT   = '-'
		LONG    = '--'

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
		self.__commandAssignedSymbol= ''
		self.__commandFound         = []
		self.__commandList          = []
		self.__commandMinNum        = 2
		## commands
		self.__args                 = []

	def __isLongCommandOption(self, command: str) -> bool:
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

	def __isShortCommandOption(self, command: str) -> bool:
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

	def __isValidCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		# valid
		isValid = False

		# check short and long
		if self.__isShortCommandOption(command) or self.__isLongCommandOption(command):
			#
			pass

		#
		return isValid

	def addElement(self, shortCommand: str, longCommand: str, description: str, num: int= 0, priority: int= Priority.IGNORE) -> None:
		"""

		:param shortCommand:
		:param longCommand:
		:param description:
		:param num:
		:param priority:
		:return:
		"""
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
				, self.Key.NUM          : num
			}
		)

	def findElement(self, command: str= '') -> bool:
		"""
		@search command
		:param command:
		:return:
		"""
		#
		found       = False
		# command
		commandLong = ''
		commandShort= ''
		commandKey  = ''

		# check short or long
		if self.__isShortCommandOption(command):
			# loop to check command
			for c in self.__commandList:
				# command with value
				if c.get(self.Key.SHORT) == command.split(self.__commandAssignedSymbol)[0]:
					# .s == a, .l == alphabet
					found   = True

		elif self.__isLongCommandOption(command):
			# loop to check command
			for c in self.__commandList:
				# command with value
				if c.get(self.Key.SHORT) == command.split(self.__commandAssignedSymbol)[0]:
					# .s == a, .l == alphabet
					found = True

		# after filter and calculation
		return found

		# #
		# try:
		# 	# loop list to find item
		# 	for index in range(len(self.__commandList)):
		# 		#
		# 		for key in self.__commandList[index]:
		# 			# find short command by each element
		# 			if self.__commandList[index]:
		# 				# del element
		# 				self.__commandFound.append(shortCommand)
		#
		# 			elif longCommand and self.__commandList[index].get(self.Key.LONG) == longCommand:
		# 				self.__commandFound.append(shortCommand)
		#
		# except Exception as e:
		# 	print(f'{str(e)}')
		# 	found   = False
		#
		# #
		# return found

	def getElement(self) -> list:
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

	def listElement(self) -> None:
		"""

		:return:
		"""
		pass

	def removeElement(self, shortCommand: str, longCommand: str= '') -> None:
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

	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol
