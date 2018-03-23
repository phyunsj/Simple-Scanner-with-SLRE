
# Simple Scanner with SLRE

**S**uper **L**ight **R**egular **E**xpression library from http://slre.sourceforge.net/.

## Source

https://github.com/cesanta/slre
```
SLRE is released under commercial and GNU GPL v.2 open source licenses.
```

http://slre.sourceforge.net/ Version 1.0 
```
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * Sergey Lyubka wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.
 * ----------------------------------------------------------------------------
 */
```

## Usage 

##### with version 1.0 

Only need two files. `slre.h`, `slre.c` and your own scanner with rules. 

sightseeing.map
```
name=Aquarium
street=Atlantic Ave and State St
city=Boston
state=MA
zip=02120
```


> $ make

Remap to `struct _addr` for your future use.

> $ ./scanner sightseeing.map  


      
