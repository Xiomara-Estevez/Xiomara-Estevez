// Header file: holds a function that prints 1 to n numbers WITHOUT USING A LOOP:
// Constraints: 1 to n: n >= 1
// Using recursion:
#ifndef NO_LOOP_NUMBER_PRINTS_H
#define NO_LOOP_NUMBER_PRINTS_H
#include <iostream>
using namespace std;
namespace n
{
    class Print
    {
        public:
        void printNumbers(int n)
        {
            if (n >= 1)
            {
                printNumbers(n - 1);
                cout << n << " ";
            }
        }
    };
}
#endif