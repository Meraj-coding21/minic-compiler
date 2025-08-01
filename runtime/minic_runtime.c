// minic_compiler/runtime/minic_runtime.c
#include <stdio.h>

// A simple runtime function to print an integer.
// We can call this from our compiled Mini-C code.
void print_int(int x) {
    printf("%d\n", x);
}