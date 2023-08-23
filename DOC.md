# smileargs
args library for modern python
### do.py --version => lowercase
### do.py -V  => capital letter
### do.py --man=value => with value and deli is equal symbol
### do.py --man:value => with value and deli is colon
## command
### do.py --man value

## Number Group

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