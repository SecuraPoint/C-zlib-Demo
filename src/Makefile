CC=cc
CFLAGS=-I$(CONDA_PREFIX)/include
LDFLAGS=-L$(CONDA_PREFIX)/lib -lpng -lz

all: main

main: main.c
	$(CC) $(CFLAGS) main.c -o main $(LDFLAGS)

clean:
	rm -f main
