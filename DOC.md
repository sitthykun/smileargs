
** Pattern and Sample
```
([(\-\-)(\-)]+\w+)(=?(\w+)?)
```

** test sample on below
```
--engine=dsffads
--version=
--value==
--pen==kok
--world
-na
-
```

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

## above
it will catch only one is '-a' as a short command
