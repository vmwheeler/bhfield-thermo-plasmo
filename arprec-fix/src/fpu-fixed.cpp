/*
 * src/fpu.cc
 *
 * This work was supported by the Director, Office of Science, Division
 * of Mathematical, Information, and Computational Sciences of the
 * U.S. Department of Energy under contract number DE-AC03-76SF00098.
 *
 * Copyright (c) 2000-2001
 *
 * Contains functions to set and restore the round-to-double flag in the
 * control word of a x86 FPU.
 */

#include "config.h"
#include <arprec/fpu.h>

#ifdef X86
#ifdef  _WIN32



/* fix for mingw - suzuki; '_control87' was not declared in this scope */
#include "C:\\MinGW\\include\\float.h"



#include <float.h>
#else

#ifdef HAVE_FPU_CONTROL
#include <fpu_control.h>
#endif

#ifndef _FPU_GETCW
#define _FPU_GETCW(x) asm volatile ("fnstcw %0":"=m" (x));
#endif

#ifndef _FPU_SETCW
#define _FPU_SETCW(x) asm volatile ("fldcw %0": :"m" (x));
#endif

#ifndef _FPU_EXTENDED
#define _FPU_EXTENDED 0x0300
#endif

#ifndef _FPU_DOUBLE
#define _FPU_DOUBLE 0x0200
#endif

#endif
#endif

extern "C" {

void fpu_fix_start(unsigned int *old_cw) {
#ifdef X86
#ifdef _WIN32
#ifdef __BORLANDC__
  /* Win 32 Borland C */
  unsigned short cw = _control87(0, 0);
  _control87(0x0200, 0x0300);
  if (old_cw) {
    *old_cw = cw;
  }
#else
  /* Win 32 MSVC */
  unsigned int cw = _control87(0, 0);
  _control87(0x00010000, 0x00030000);
  if (old_cw) {
    *old_cw = cw;
  }
#endif
#else
  /* Linux */
  volatile unsigned short cw, new_cw;
  _FPU_GETCW(cw);

  new_cw = (cw & ~_FPU_EXTENDED) | _FPU_DOUBLE;
  _FPU_SETCW(new_cw);
  
  if (old_cw) {
    *old_cw = cw;
  }
#endif
#endif
}

void fpu_fix_end(unsigned int *old_cw) {
#ifdef X86
#ifdef _WIN32

#ifdef __BORLANDC__
  /* Win 32 Borland C */
  if (old_cw) {
    unsigned short cw = (unsigned short) *old_cw;
    _control87(cw, 0xFFFF);
  }
#else
  /* Win 32 MSVC */
  if (old_cw) {
    _control87(*old_cw, 0xFFFFFFFF);
  }
#endif

#else
  /* Linux */
  if (old_cw) {
    volatile unsigned short cw;
    cw = (unsigned short) *old_cw;
    _FPU_SETCW(cw);
  }
#endif
#endif
}

}
 
