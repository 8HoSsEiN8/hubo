default: all

CFLAGS := -I./include -g --std=gnu99
CC := gcc

BINARIES := HW1_HelloWorld_RobotSimulation
all : $(BINARIES)

LIBS := -lach 

HW1_HelloWorld_RobotSimulation: src/HW1_HelloWorld_RobotSimulation.o
	gcc -o $@ $< $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(BINARIES) src/*.o
