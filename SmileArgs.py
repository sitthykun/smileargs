"""
Author: masakokh
Year: 2023
Package: library
Note:
Version: 1.1.2
"""
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
		self.id         = 0
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

	def __init__(self, isAllowedNoValue: bool= False, isDuplicated: bool= False, console: bool= True, debug: bool= False):
		"""

		:param isAllowedNoValue:
		:param isDuplicated:
		:param console:
		:param debug:
		"""
		# private
		self.__commandAssignedSymbol= self.OptionDelimiterSymbol.EQUAL
		self.__commandList          = []
		## command
		self.__acceptedDuplicate    = isDuplicated
		self.__args                 = []
		self.__isAllowedNoValue     = isAllowedNoValue
		self.__isCmdLong            = False
		self.__isConsole            = console
		self.__isDebug              = debug
		## value
		self.__id                   = 1
		self.__numIncrease          = 2

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
			self.__print(f'{self.__class__.__name__}.{func}: {content}')

	def __debug(self, func: str, content: str) -> None:
		"""

		:param func:
		:param content:
		:return:
		"""
		if self.__isDebug:
			self.__print(f'{self.__class__.__name__}.{func} Debug: {content}')

	def __hatchArg(self, arg: str, length: int= 1) -> None:
		"""

		:param arg:
		:param length:
		:return:
		"""
		# pattern
		## equal --mom=miss or -m=miss or
		## colom --mom:miss or -m:miss
		_pW     = '([(\-\-)(\-)]+\w+)(' + self.__commandAssignedSymbol + '?(\w+)?)'
		_pS     = '(^\-\w{' + str(length) + '}$)'  # -m len(m) == 1
		_pL     = '(^\-\-\w.{' + str(length) + ',}$)'  # --mom len(mom) > 1

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
				# set long command
				isLong  = True
				round2  = re.match(_pL, command)
				cmd     = round2.groups()[0]

			except Exception as e:
				# round 3
				try:
					# set short command
					isLong  = False
					round3  = re.match(_pS, command)
					cmd     = round3.groups()[0]

				except Exception as e:
					self.__debug(func= f'__hatchArg round 3 {command=}', content= f'Exception: {str(e)}')
					cmd     = ''

			# valid command, and continue to find in the exist command
			if cmd and not self.__isDuplicatedOnHatch(cmd):
				# loop to find
				for i in range(self.__commandList.__len__()):
					# long condition
					if isLong and self.__commandList[i].cmdLong == cmd:
						item            = CommandArgs()
						# detail
						item.cmdLong    = cmd
						item.id         = self.__commandList[i].id
						item.isLong     = isLong
						item.priority   = self.__commandList[i].priority
						item.value      = value
						# add to list
						self.__args.append(item)

					# short condition
					elif isLong is False and self.__commandList[i].cmdShort == cmd:
						item            = CommandArgs()
						# detail
						item.cmdShort   = cmd
						item.id        = self.__commandList[i].id
						item.isLong     = isLong
						item.priority   = self.__commandList[i].priority
						item.value      = value
						# add to list
						self.__args.append(item)

		except Exception as e:
			self.__debug(func= '__hatchArg round 1', content= f'Exception: {str(e)}')

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

	def __print(self, message: str) -> None:
		"""

		:param message:
		:return:
		"""
		print(message)

	def addCommand(self, shortCommand: str= None, longCommand: str= None, description: str= '', priority: int= Priority.IGNORE, overrideNum: list= []) -> None:
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
				if self.__acceptedDuplicate:
					# accept
					_continue   = True

			# not exist
			else:
				_continue   = True

			#
			if _continue:
				# increase power by 2
				self.__id   *= self.__numIncrease

				# object
				item            = CommandAdd()
				# item
				item.description= description
				# main key
				item.cmdLong    = f'{self.OptionPrefixSymbol.LONG}{longCommand}'  if longCommand else None
				item.cmdShort   = f'{self.OptionPrefixSymbol.SHORT}{shortCommand}'  if shortCommand else None
				# special value
				item.id         = self.__id
				item.priority   = priority
				# add to list
				self.__commandList.append(item)
				self.__console(f'Command Addition')
				self.__console(f'short: {item.cmdShort}, long: {item.cmdLong}, description: {item.description=}')

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
					return self.__commandList[i].id
			#
			else:
				# check with short and long command
				if command in [self.__commandList[i].cmdShort, self.__commandList[i].cmdLong]:
					# num or id
					return self.__commandList[i].id
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
				# found
				found   = False
				# with prefix - or --
				if appendPrefix:
					if (self.__appendPrefixShort(command) == self.__commandList[i].cmdShort):
						found   = True
					elif (self.__appendPrefixLong(command) == self.__commandList[i].cmdLong):
						found   = True
				#
				else:
					if command == self.__commandList[i].cmdShort or command == self.__commandList[i].cmdLong:
						found   = True
				#
				if found:
					self.__console(f'Command Removing')
					self.__console(f'short: {self.__commandList[i].cmdShort}, long: {self.__commandList[i].cmdLong}, description: {self.__commandList[i].description=}')

		except Exception as e:
			self.__debug(func= 'removeCommand', content= f'Exception: {str(e)}')

	def run(self) -> None:
		"""

		:return:
		"""
		# string token
		for arg in sys.argv[1:]:
			# verify
			self.__hatchArg(arg)

	def setAssignSymbol(self, symbol: str= OptionDelimiterSymbol.EQUAL) -> None:
		"""

		:param symbol:
		:return:
		"""
		self.__commandAssignedSymbol  = symbol

	def show(self) -> None:
		"""

		:return:
		"""
		lineTable   = '=========================================================='
		lineRowFirst= '+--------------+------------------------------------------'
		lineRowNext = '+--------------+---------------------'
		# added
		self.__print(f'{lineTable}')
		self.__print(f'Print all added commands')
		self.__print(f'Short Command \tLong Command \t\tDescription')
		self.__print(f'{lineRowFirst}')
		# loop to print all element
		for a in self.getCommand():
			self.__print(f'  {a.cmdShort} \t\t{a.cmdLong} \n description: {a.description}')
			self.__print(f'{lineRowNext if a != self.getCommand()[-1] else ""}')
		self.__print(f'{lineRowFirst}')

		#
		if len(self.catchCommand()) > 0:
			# caught
			self.__print(f'{lineTable}')
			self.__print(f'Print all caught commands')
			self.__print(f'Short/Long Command \tValue')
			self.__print(f'{lineRowFirst}')
			# loop to print all element
			for c in self.catchCommand():
				self.__print(f'  {c.cmdShort or c.cmdLong} \t\t{c.value or ""}')
				self.__print(f'{lineRowNext if c != self.catchCommand()[-1] else ""}')
			self.__print(f'{lineRowFirst}')
