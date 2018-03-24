
APPL=scanner

all: $(APPL)

CXX=g++
CC=gcc

SOURCES = slre.c scanner.cpp Mapreduce.cpp sqlite3.c
OBJS = slre.o scanner.o Mapreduce.o sqlite3.o

PATH := $(TIMESYS_BIN):$(PATH)
BUILD_DIR = .

CPPFLAGS = -I. -O1 -Wall -Wformat -Wpointer-arith -Wswitch -Wunused  -DSQLITE_THREADSAFE=0 
# Targets

#compile C++ source files into object files.
%.o: %.cpp
	$(CXX) $(CPPFLAGS) -c $<  

%.o: %.c
	$(CC) $(CPPFLAGS) -c $<  


$(APPL): $(OBJS)
	$(CXX) $(CFLAGS)  $^ $(CE_LDFLAGS) -ldl -o $(APPL)

clean:
	-@$(RM) $(OBJS)
	-@$(RM) $(APPL)
