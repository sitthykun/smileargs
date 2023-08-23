It is a modern args catching with python3 and OOP
## example 
create a test.py
```
from SmileArgs import SmileArgs
smile   = SmileArgs()

smile.addCommand('a', 'alphabet', 'show alphabet')
smile.addCommand('b', 'baby', 'miss mom by her baby')
smile.run()
print(smile.catchCommand()[0].num)
```

## cli
```
$ python test.py -a -ab -a
```
it will catch only one is '-a' as a short command