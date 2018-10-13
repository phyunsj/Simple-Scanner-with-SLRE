
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

# [Hadoop Configuration Parameter Example](https://github.com/phyunsj/simple-configuration-setter-getter-SLRE-sqlite/tree/master/example)

- Save Non-default Configuration Parameters & Apply thsoe again. (Perhapse going back to working condition?)

- Hadoop Configuration parameters are defined : http://ercoppa.github.io/HadoopInternals/HadoopConfigurationParameters.html.

- `generator.py` generates C++ class identical to a table definition. 

_**This example is nothing to do with Hadoop**_ 

## Quick Start

> $ ./create_hadoop_db.py for a smaple sqlite database. 

> $ ./generator.py or python ./generator.py
> $ make
> $ ./scanner  [direction]  [filename]

###### **sqlite-3.22** is used for database management

## Code Generator 


`generator.py` creates the following files
- db_class_types.include 
- db_read_from_map.include
- db_read_from_record.include
- db_write_to_map.include
- Mapreduce.cpp
- Mapreduce.h

`Mapreduce` class is from `database.xlsx` (`Mapreduce` tab represents a table.)

`database.xlsx` contains `min`,`max`,`default`, `private`. 

The outcomes are: 

```
#define MAPREDUCE_TASK_IO_SORT_MB_MIN 0
#define MAPREDUCE_TASK_IO_SORT_MB_MAX 255
#define MAPREDUCE_TASK_IO_SORT_MB_DEFAULT 100
#define MAPREDUCE_TASK_IO_SORT_MB_VALID_FLAG   (0x1 << 0)
#define MAPREDUCE_TASK_IO_SORT_MB_RANGE_ERROR 301

```

`db_class_types.include`, `db_read_from_map.include`, `db_read_from_record.include` and `db_write_to_map.include` are helper utility functions. 


## Saving Operation 

Extract all records from MAPREDUCE table and save non-default values only. 
