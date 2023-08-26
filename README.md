## Why SmileArgs
It is a modern args catching with python3 and OOP structure and implementation.
## Optional
Some parameters will clarify more, when instance starting
```
smile = SmileArgs(allowNoValue= False, duplicated= False, console= True, debug= False)
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

## Example 
create a test.py
```
from SmileArgs import SmileArgs
smile   = SmileArgs()

smile.addCommand('a', 'alphabet', 'show alphabet')
smile.addCommand('b', 'barbie', 'Wow, movies')
smile.addCommand('m', 'miss', 'miss mom everyday')
smile.run()
```

## cli
```
$ python test.py -a -ab -a --miss=mom
```
it will catch '-a' as a short command, and '--miss' as a long command;
then use match or if statement to control those states.
