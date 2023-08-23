# built-in
import re
import sys
from typing import Any, Union


class CommandBase:
	def __init__(self):
		"""

		"""
		self.cmdLong    = None
		self.cmdShort   = None
		self.num        = 0
		self.priority   = 0
		self.value      = None


class CommandArgs(CommandBase):
	def __init__(self):
		"""

		"""
		super().__init__()
		self.isLong         = False


class CommandAdd(CommandBase):
	def __init__(self):
		"""

		"""
		super().__init__()
		self.description    = ''


class SmileArgs:
	"""

	"""
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

	def __init__(self, duplicated: bool= False, console: bool= True, debug: bool= False):
		"""

		:param duplicated:
		:param console:
		:param debug:
		"""
		# private
		self.__commandAssignedSymbol= self.OptionDelimiterSymbol.EQUAL
		self.__commandList          = []
		self.__commandMinNum        = 2
		## command
		self.__acceptedDuplication  = duplicated
		self.__args                 = []
		self.__isCmdLong            = False
		self.__isConsole            = console
		self.__isDebug              = debug
		## value
		self.__number               = 1
		## pattern
		self.__patternBase          = '([(\-\-)(\-)]+\w+)(=?(\w+)?)'

	def __appendPrefixLong(self, command: str = None) -> Union[str | None]:
		"""

		:param command:
		:return:
		"""
		if command:
			return f'{self.OptionPrefixSymbol.LONG}{command}'
		# nothing
		return None

	def __appendPrefixShort(self, command: str= None) -> Union[str | None]:
		"""

		:param command:
		:return:
		"""
		if command:
			return f'{self.OptionPrefixSymbol.SHORT}{command}'
		# nothing
		return None

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

	def __console(self, prefix: str= 'Error: ', content: str= None) -> None:
		"""

		:param prefix:
		:param content:
		:return:
		"""
		if self.__isConsole:
			print(f'{prefix}{content}')

	def __debug(self, content: str) -> None:
		"""

		:param content:
		:return:
		"""
		if self.__isDebug:
			print(f'Debug: {content}')

	def __findCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		for i in range(self.__commandList.__len__()):
			# short
			if self.__isShortCommand(command):
				#
				if self.__commandList[i].cmdShort and command == self.__commandList[i].cmdShort:
					# add found
					# self.__commandFound.append(self.__commandList[i].num)
					self.__isCmdLong    = False
					return True
			# long
			elif self.__isLongCommand(command):
				#
				if self.__commandList[i].cmdLong and command == self.__commandList[i].cmdLong:
					# add found
					# self.__commandFound.append(self.__commandList[i].num)
					self.__isCmdLong    = True
					return True
		# nothing
		return False

	def __grabCommand(self, arg: str) -> None:
		"""

		:param arg:
		:return:
		"""
		if self.__isValidValue(arg):
			self.__debug('__grabCommand is valid value')
			#
			result = re.match(self.__patternBase, arg)
			#
			if self.__isDuplicatedOnGrab(result[0]):
				self.__debug('----------------found duplicated arg')

			else:
				# command value
				# result[0] result[2]
				if self.__isLongCommand(result[0]):
					#
					item    = CommandArgs()
					for i in range(self.__commandList.__len__()):
						if result[0] == self.__commandList[i].cmdLong:
							#
							item.isLong     = True
							item.num        = self.__commandList[i].num
							item.priority   = self.__commandList[i].priority
							item.value      = result[2]
							# long command
							item.cmdLong    = result[0]
							self.__args.append(item)
							# exit loop
							break
				# double-check with short again
				elif self.__isShortCommand(result[0]):
					# short command
					item    = CommandArgs()
					for i in range(self.__commandList.__len__()):
						if result[0] == self.__commandList[i].cmdShort:
							#
							item.isLong     = False
							item.num        = self.__commandList[i].num
							item.priority   = self.__commandList[i].priority
							item.value      = result[2]
							# short command
							item.cmdShort   = result[0]
							self.__args.append(item)
							# exit loop
							break
				# nothing with value block
				else:
					pass
		#
		else:
			self.__debug('__grabCommand is no value')
			result = re.match(self.__patternBase, arg)
			#
			if self.__isDuplicatedOnGrab(result[0]):
				self.__debug('----------------found duplicated arg')

			else:
				# result[0]
				if self.__isLongCommand(result[0]):
					#
					item    = CommandArgs()
					for i in range(self.__commandList.__len__()):
						if result[0] == self.__commandList[i].cmdLong:
							#
							item.isLong     = True
							item.num        = self.__commandList[i].num
							item.priority   = self.__commandList[i].priority
							item.value      = result[2]
							# long command
							item.cmdLong    = result[0]
							self.__args.append(item)
							# exit loop
							break
				#
				elif self.__isShortCommand(result[0]):
					# short command
					item    = CommandArgs()
					for i in range(self.__commandList.__len__()):
						if result[0] == self.__commandList[i].cmdShort:
							#
							item.isLong     = False
							item.num        = self.__commandList[i].num
							item.priority   = self.__commandList[i].priority
							item.value      = ''
							# short command
							item.cmdShort   = result[0]
							self.__args.append(item)
							# exit loop
							break
				# nothing with no value block
				else:
					pass

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
			self.__console(content= f'{str(e)}')
			return False

	def __isDuplicatedOnAdd(self, shortCommand: str= None, longCommand: str= None, appendPrefix: bool= True) -> bool:
		"""

		:param shortCommand:
		:param longCommand:
		:param appendPrefix:
		:return:
		"""
		#
		for i in range(self.__commandList.__len__()):
			# with prefix - or --
			if appendPrefix:
				# self.__debug(f'__isDuplicatedOnAdd append prefix= {self.__appendPrefixShort(shortCommand)=}, {self.__commandList[i].cmdShort=}, {self.__commandList[i].cmdLong=} |  {self.__appendPrefixLong(longCommand)=}, {self.__commandList[i].cmdLong=}')
				return (self.__appendPrefixShort(shortCommand) == self.__commandList[i].cmdShort) or (self.__appendPrefixLong(longCommand) == self.__commandList[i].cmdLong)

			else:
				# self.__debug(f'__isDuplicatedOnAdd= {shortCommand=}, {self.__commandList[i].cmdShort=} | {longCommand=}, {self.__commandList[i].cmdLong=}')
				return shortCommand == self.__commandList[i].cmdShort or longCommand == self.__commandList[i].cmdLong
		#
		return False

	def __isDuplicatedOnGrab(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		#
		for i in range(self.__args.__len__()):
			self.__debug(f'__isDuplicatedOnGrab= {command=}, {self.__args[i].cmdShort=}, {self.__args[i].cmdLong=}')
			return command in [self.__args[i].cmdShort or self.__args[i].cmdLong]
		#
		return False

	def __isLongCommand(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		#
		found   = False
		self.__debug(f'__isLongCommand {command}')
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
		self.__debug(f'__isShortCommand {command}')
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
			self.__console(content= f'{str(e)}')
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
			self.__console(content= f'{str(e)}')
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
			# continue
			_continue   = False

			# find any existed
			if self.__isDuplicatedOnAdd(shortCommand= shortCommand, longCommand= longCommand):
				# self.__debug(f' addCommand duplication {longCommand=}, {shortCommand}')
				if self.__acceptedDuplication:
					# accept
					_continue   = True
					# self.__debug(f'addCommand duplication accepted')
			# not exist
			else:
				# self.__debug(f'addCommand not duplicated')
				_continue   = True

			#
			if _continue:
				# self.__debug(f'addCommand append')
				# increase power by 2
				self.__number *= 2

				# object
				item    = CommandAdd()
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

	def catchCommand(self) -> list:
		"""

		:return:
		"""
		return self.__args

	def getCommand(self) -> list:
		"""

		:return:
		"""
		return self.__commandList

	def getNumByCommand(self, command: str, addPrefix: bool= False) -> int:
		"""

		:param command:
		:param addPrefix:
		:return:
		"""
		for i in range(self.__commandList.__len__()):
			#
			if addPrefix:
				if (self.__appendPrefixShort(command) == self.__commandList[i].cmdShort) or \
						(self.__appendPrefixLong(command) == self.__commandList[i].cmdLong):
					#
					return self.__commandList[i].num
			else:
				if command in [self.__commandList[i].cmdShort, self.__commandList[i].cmdLong]:
					#
					return self.__commandList[i].num
		#
		return 0

	def removeCommand(self, command: str, appendPrefix: bool= True) -> None:
		"""

		:param command:
		:param appendPrefix:
		:return:
		"""
		# remove short or long command from list
		try:
			#
			for i in range(self.__commandList.__len__()):
				# with prefix - or --
				if appendPrefix:
					return (self.__appendPrefixShort(command) == self.__commandList[i].cmdShort) or \
						(self.__appendPrefixLong(command) == self.__commandList[i].cmdLong)
				#
				else:
					return command == self.__commandList[i].cmdShort or command == self.__commandList[i].cmdLong

		except Exception as e:
			self.__console(content= f'{str(e)}')

	def run(self) -> None:
		"""

		:return:
		"""
		#
		for a in sys.argv[1:]:
			if self.__isValidFormatCommand(a):
				self.__grabCommand(a)
		# self.__debug(f'>>>>>>>>>>>>>>>>>>>>> run: {self.__commandList=}')
		# self.__debug(f'>>>>>>>>>>>>>>>>>>>>> run: {self.__args=}')
		# for i in range(self.__args.__len__()):
		# 	self.__debug(f'{self.__args[i].num=}, {self.__args[i].value=}, {self.__args[i].priority=}, {self.__args[i].cmdLong=}, {self.__args[i].cmdShort=}')

	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol
