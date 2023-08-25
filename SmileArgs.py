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


class CommandAdd(CommandBase):
	def __init__(self):
		"""

		"""
		super().__init__()
		self.description    = ''


class CommandArgs(CommandBase):
	def __init__(self):
		"""

		"""
		super().__init__()
		self.isLong         = False


# class CommandHatch:


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

	def __init__(self, allowNoValue: bool= False, duplicated: bool= False, console: bool= True, debug: bool= False):
		"""

		:param allowNoValue:
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
		self.__isAllowedNoValue     = allowNoValue
		self.__isCmdLong            = False
		self.__isConsole            = console
		self.__isDebug              = debug
		## value
		self.__number               = 1
		## pattern
		self.__patternCommand       = '([(\-\-)(\-)]+\w+)'
		self.__patternFull          = '([(\-\-)(\-)]+\w+)(=?(\w+)?)'

	def __appendPrefixLong(self, command: str = None) -> Union[str | None]:
		"""

		:param command:
		:return:
		"""
		return f'{self.OptionPrefixSymbol.LONG}{command}' if command else None

	def __appendPrefixShort(self, command: str= None) -> Union[str | None]:
		"""

		:param command:
		:return:
		"""
		return f'{self.OptionPrefixSymbol.SHORT}{command}' if command else None

	def __console(self, func: str, content: str= None) -> None:
		"""

		:param func:
		:param content:
		:return:
		"""
		if self.__isConsole:
			print(f'{self.__class__.__name__}.{func}: {content}')

	def __debug(self, func: str, content: str) -> None:
		"""

		:param func:
		:param content:
		:return:
		"""
		if self.__isDebug:
			print(f'{self.__class__.__name__}.{func} Debug: {content}')

	def __hatchArg(self, arg: str) -> None:
		"""

		:param arg:
		:return:
		"""
		# pattern
		_pW     = '([(\-\-)(\-)]+\w+)(=?(\w+)?)'  # --mom=miss or -m=miss
		_pS     = '(^\-\w{1}$)'  # -m len(m) == 1
		_pL     = '(\-\-\w.{1,})'  # --mom len(mom) > 1

		#
		cmd     = ''
		command = ''
		isLong  = False
		value   = ''

		# round 1
		try:
			round1      = re.match(_pW, arg)
			#
			command     = round1.groups()[0]
			value       = round1.groups()[2]

			# round 2
			try:
				isLong  = True
				round2  = re.match(_pL, command)
				cmd     = round2.groups()[0]

			except Exception as e:
				self.__console(func= f'__hatchArg round 2 {command=}', content= f'Exception: {str(e)}')
				# round 3
				try:
					isLong  = False
					round3  = re.match(_pS, command)
					cmd     = round3.groups()[0]

				except Exception as e:
					self.__console(func= f'__hatchArg round 3 {command=}', content= f'Exception: {str(e)}')
					cmd     = ''

			# valid command, and continue to find in the exist command
			if cmd and not self.__isDuplicatedOnHatch(cmd):
				# loop to find
				for i in range(self.__commandList.__len__()):
					# long condition
					if isLong and self.__commandList[i].cmdLong == cmd:
						item        = CommandArgs()
						item.cmdLong    = cmd
						item.isLong     = isLong
						item.num        = self.__commandList[i].num
						item.priority   = self.__commandList[i].priority
						item.value      = value
						# add to list
						self.__args.append(item)

					# short condition
					elif isLong is False and self.__commandList[i].cmdShort == cmd:
						item        = CommandArgs()
						item.cmdLong    = cmd
						item.isLong     = isLong
						item.num        = self.__commandList[i].num
						item.priority   = self.__commandList[i].priority
						item.value      = value
						# add to list
						self.__args.append(item)

		except Exception as e:
			self.__console(func= '__hatchArg round 1', content= f'Exception: {str(e)}')

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

	def __isDuplicatedOnHatch(self, command: str) -> bool:
		"""

		:param command:
		:return:
		"""
		#
		for i in range(self.__args.__len__()):
			return command in [self.__args[i].cmdShort or self.__args[i].cmdLong]
		#
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
				#
				if self.__acceptedDuplication:
					# accept
					_continue   = True

			# not exist
			else:
				_continue   = True

			#
			if _continue:
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
			self.__console(func= 'removeCommand', content= f'Exception: {str(e)}')

	def run(self) -> None:
		"""

		:return:
		"""
		for arg in sys.argv[1:]:
			self.__hatchArg(arg)

	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol
