
APPL=scanner

all: $(APPL)

CXX=g++
CC=gcc

SOURCES = slre.c scanner.cpp 
OBJS = slre.o scanner.o

PATH := $(TIMESYS_BIN):$(PATH)
BUILD_DIR = .

CPPFLAGS = -I. -O1 -Wall -Wformat -Wpointer-arith -Wswitch -Wunused  
# Targets

#compile C++ source files into object files.
%.o: %.cpp
	$(CXX) $(CPPFLAGS) -c $<  

%.o: %.c
	$(CC) $(CPPFLAGS) -c $<  


$(APPL): $(OBJS)
	$(CXX) $(CFLAGS)  $^ $(CE_LDFLAGS) -o $(APPL)

clean:
	-@$(RM) $(OBJS)
	-@$(RM) $(APPL)
