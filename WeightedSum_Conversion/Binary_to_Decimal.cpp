// Program that uses Wieghted Sum Algorithm to convert from: Binary to Decimal:
#include <iostream>
#include <string>
#include <cmath>    // For pow.

// Using long long:
long long binary_to_decimal(std::string binarystring)
{
    // Declare and initialize a decimalvalue= 0, power which represents base = 0;
    long long decimalvalue = 0;
    int power = 0;  // represents base

    // Iterate from right to left (int in = 0; so binarystring.length() - 1; i >= 0;, pre-decrement i )
    for (int i = binarystring.length() - 1; i >= 0; --i)
    {
        // Condition for if binarystring[i] == a string '1' you add decimal value to formula for pow(2, pow) base:
        if (binarystring[i] == '1')
        {
            decimalvalue += std::pow(2, power);
        }
        power++;
    }
    return decimalvalue;
}
// Main driver Test: Create string literal
int main()
{
    std::string binarynum = "110101";
    long long decimalresult = binary_to_decimal(binarynum); // call function with parameter binarynum:

    std::cout << "Binary number: " << binarynum << " in decimal equivalent is: " << decimalresult << std::endl;
    return 0;
}


