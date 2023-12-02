## Why SmileArgs
It is a modern args catching with python3 and OOP structure and implementation.
## Optional
Some parameters will clarify more, when instance starting
```
smile = SmileArgs(isAllowedNoValue= False, isDuplicated= False, console= True, debug= False)
```
- allowNoValue: bool= False | True
  - No require value on args 
  - -c command does not need any assign value (Ex: python test.py -c)
- duplicated: bool= False | True
  - Allowing a user types many times of any command on args (Ex: python test.py -b -b -b)
  - Will execute 3 times of the command "-b" regarding to the above example
- console: bool= False | True
  - A method will print error when the system catches and throw a particular error
- debug bool= False | True
  - This property will track any prompt while working

## getCommand()
- show all added commands
- return list

## run()
- find and match command via cli
- Ex: python test.py -a=Miss -b=Mom

## catchCommand()
- after executed run() method, it allows us to get catch command list
- show all cli command that matched to the added command
- return list


## Example 1
Create a test.py
```
from SmileArgs import SmileArgs
smile   = SmileArgs(console= True, debug= True)
# add command to list
smile.addCommand('a', 'alphabet', 'show alphabet')
smile.addCommand('b', 'baby', 'miss mom by her baby')
smile.addCommand('m', 'miss', 'miss mom everyday')

print(f'Print all added commands')
print(f'Short Command \tLong Command \t\tDescription')
print(f'+--------------+-----------------------------------------')
for a in smile.getCommand():
	print(f'{a.cmdShort} \t\t{a.cmdLong} \ndescription: {a.description}')
	print(f'+--------------+---------------------')

# catch cli command
print(f'\nFound commands via cli')
smile.run()

# show
print(f'Short/Long Command \tValue')
print(f'+--------------+-----------------------------------------')
for f in smile.catchCommand():
	print(f'{f.cmdShort or f.cmdLong} \t\t{f.value}')
	print(f'+--------------+---------------------')

```
On terminal try with this
```
$ python3.10 test.py -a -ab -a --miss=mom
```
<img width="853" alt="test-smileargs" src="https://github.com/sitthykun/smileargs/assets/227092/9855c13c-7400-4d2c-94ff-7c0508b7981a">

# Example 2

create a testclass.py
```
from SmileArgs import SmileArgs

class TestClass:
  def __init__(self):
    """
    """
    # private
    self.__smile   = SmileArgs()
    self.__load()
  
  def __load(self) -> None:
    """
    """
    self.__smile.addCommand('a', 'alphabet', 'show alphabet')
    self.__smile.addCommand('b', 'barbie', 'Wow, movies')
    self.__smile.addCommand('m', 'miss', 'miss mom everyday')
  
  def checkCLI(self) -> None:
    """
    """
    self.__smile.run()

  def executeCLICommand(self) -> None:
    """
    """
    #
    self.checkCLI()
    # 
    for s in self.__smile.catchCommand():
      print(f'{f.cmdShort or f.cmdLong} \t\t{f.value}')
    

testClass = TestClass()
testClass.executeCLICommand()
```

## cli
```
$ python3.10 testclass.py -a -ab -a --miss=mom
```
it will catch '-a' as a short command, and '--miss' as a long command;
then use match or if statement to control those states.
