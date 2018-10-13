
# Hadoop Configuration Parameter Example

- Save Non-default Configuration Parameters & Apply thsoe again. (Perhapse going back to working condition?)

- Hadoop Configuration parameters are defined : http://ercoppa.github.io/HadoopInternals/HadoopConfigurationParameters.html.

- `generator.py` generates C++ class identical to a table definition. 

- _**This example is nothing to do with Hadoop**_ 


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


> ./scanner 1  hadoop_022818.map

Format `parameter_name=parameter_value`
```
task.io.sort.mb=77
map.sort.spill.percent=55
task.io.sort.factor=245
```

## Write Operation

Default settings + new settings from .map will be applied to MAPREDUCE table.

> ./scanner 0 hadoop_032418.map

