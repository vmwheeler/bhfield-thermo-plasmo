#include "config.h"

#define f_main FC_FUNC_(f_main, F_MAIN)

extern "C" void f_main();

/* int main() { */

/* suzuki gfortran fix: enables command-line intrinsics */
extern "C" void _gfortran_set_args(int argc, char *argv[]);
int main (int argc, char *argv[]) {
  /* Initialize libgfortran. */
  _gfortran_set_args(argc, argv);

  f_main();
  return 0;
}

