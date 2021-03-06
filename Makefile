# Sample Makefile for compiling Fortran programs using ARPREC library. (mingw/msys)
# Make sure the script arprec-config (installed during "make install") 
# is in your path.

# Fortran compiler.  Should be whatever  "arprec-config --fc"  returns.
FC=$(shell arprec-config --fc)

# C++ compiler.  Used for linking.
# Should be whatever  "arprec-config --cxx"  returns.
CXX=$(shell arprec-config --cxx)

LIBLOCS = -L/usr/lib64 -L/home/vmwheeler/Software/local/lib
LIBS = -lcuba -lm
GSLSTUFF = $(shell pkg-config --cflags fgsl) $(LIBLOCS) $(shell pkg-config --libs fgsl)

CUBASTUFF = -L/home/vmwheeler/Software/local/lib -lcuba -lm

# Fortran compiler flags.  Should be whatever  "arprec-config --fcflags"  
# returns, but some items (like optimization levels) # can be 
# tweaked if desired.
FCFLAGS=$(shell arprec-config --fcflags)

# Linker flags.  Includes the Quad-Double library and any Fortran
# libraries that needs to be linked in.  Should be whatever  
# "arprec-config --fclibs"  returns
# FCLIBS=$(shell arprec-config --fclibs) $(shell arprec-config --fmainlib)
# cygwin
# FCLIBS=-Wl,--enable-auto-import -static $(shell arprec-config --fmainlib) $(shell arprec-config --fclibs)
# mingw
FCLIBS=-static $(shell arprec-config --fmainlib) $(shell arprec-config --fclibs)

# Your main program.  Note that you main program should be declared
# as "subroutine f_main", not "program myprog", since the C++ linker
# must find the C++ main entry.

# ftnchek path
#FTNCHEK = C:/Winapp/ftnchek/ftnchek-3_3_1-win32.exe

# common defs
#DEFINES = -DNMAX_COEFFS=500 -DCHECK_SURFACE_MODE -DDATA_DIR="'./'"
DEFINES = -DNMAX_COEFFS=700 -DCHECK_SURFACE_MODE -DDATA_DIR="'/home/vmwheeler/Code/bhfield-121005/src/nkdata/'"
#DEFINES = -DNMAX_COEFFS=700 -DCHECK_SURFACE_MODE -DDATA_DIR="'/home/vmwheeler/Code/bhfield-thermo-plasmo/nkdata/'"

# ARP options
#DARP = -DUSE_ARPREC -DUSE_ARPREC_LEGENDRE

# debug options: -fcheck=all -> "error: unrecognized option"; why?
# DBOPT = -DCHECK_UNDERFLOW -DCHECK_TANGENTIAL_CONTINUITY -DDEBUG_BESSEL -DOUTPUT_YBESSE -fbounds-check -O -Wuninitialized -ffpe-trap=invalid,zero,overflow -fbacktrace -g
DBOPT = -DCHECK_UNDERFLOW -DCHECK_TANGENTIAL_CONTINUITY -DDEBUG_BESSEL -fbounds-check


# clear up the default gnu make
.DEFAULT:
.SUFFIXES:
.SUFFIXES: .f .o .exe
# .PRECIOUS: %.o %-arp.o %-arp-bd.o
.PHONY: all clean ftnchek allclean
%.o: %.f
%.exe: %.o

# all: bhfield-arp.exe bhfield-std.exe bhfield-arp-db.exe bhfield-std-db.exe
all: bhfield-std-db.exe

# standard version: one-step compilation
%-std.exe: %.f
	$(FC) -cpp $(DEFINES) $(GSLSTUFF)       -O2 -Wall -static -o $@ $+

%-std-db.exe: %.f
	$(FC) -cpp $(DEFINES) $(LIBLOCS) $(LIBS) $(DBOPT) -g -static -O2 -Wall -o $@ $+ libcuba.a
#	$(FC) -cpp $(DEFINES) $(CUBASTUFF) $(DBOPT) -static -O2 -Wall -o $@ $+

# arprec version: two-step
%.exe: %.o
	$(CXX) -O2 -Wall -o $@ $+ $(FCLIBS)

%-arp.o: %.f
	$(FC) -cpp $(DARP) $(DEFINES)          -O2 -Wall -c -o $@ $< $(FCFLAGS)

%-arp-db.o: %.f
	$(FC) -cpp $(DARP) $(DEFINES) $(DBOPT) -O2 -Wall -c -o $@ $< $(FCFLAGS)

clean:
	rm -f *o *exe

allclean:
	rm -f *o *exe *dat *log
	
# gfortran warning not enough!!! do ftnchek too!!!
# ftnchek doesn't support preprocessing, so do cpp first (-E: preprocessing only)

ftnchek: bhfield.f
	$(FC) -cpp -E $(DEFINES)                  -O2 -Wall -static -o std-cpp.f $<
	$(FC) -cpp -E $(DEFINES) $(DBOPT)         -O2 -Wall -static -o std-db-cpp.f $<
	$(FC) -cpp -E $(DARP) $(DEFINES)          -O2 -Wall -c -o arp-cpp.f $<
	$(FC) -cpp -E $(DARP) $(DEFINES) $(DBOPT) -O2 -Wall -c -o arp-db-cpp.f $<
	$(FTNCHEK) -wrap=0 std-cpp.f    >00ftnchek-std.txt
	$(FTNCHEK) -wrap=0 std-db-cpp.f >00ftnchek-std-db.txt
	$(FTNCHEK) -wrap=0 arp-cpp.f    >00ftnchek-arp.txt
	$(FTNCHEK) -wrap=0 arp-db-cpp.f >00ftnchek-arp-db.txt
	mv 00ftnchek* ftnchek
	rm -f std-cpp.f std-db-cpp.f arp-cpp.f arp-db-cpp.f
	diff -c ./ftnchek/old ./ftnchek >ftnchek-dif.txt

