// Program using Weighted Sum Algorithm to convert from: Octal(base 8) to Decimal(base10):
#include <iostream>
#include <cmath>    // for pow.

long long octal_to_decimal(int octalnum)
{
    // declare and initialize both blong long decimalnum and power to 0:
    long long decimalnum = 0;
    int power = 0;

    // Condition for octalnum is greater than 0, you  modulus %10 the last digit to extract.
    while (octalnum > 0)
    {
        // Declare an int last digit to extract using modulus %10:
        int lastdigit = octalnum % 10;

        // Add decimal num to formula lastdigit * pow(8, power); then post increment power++;
        // Afterwards you integer divide octalnum / 10;
        // return decimalnum; outside the iteration:
        decimalnum += lastdigit * std::pow(8, power);
        power++;
        octalnum /= 10;
    }
    return decimalnum;
}
// main driver test: Declare here octalnum and return function octal_to_decimal with parameter octalnum;
int main()
{
    int octalnum = 236; // octal = (0 - 7) should output 158 decimal:
    int octalnum2 = 157;    // should output 111 decimal:

    std::cout << "The octal number: " << octalnum << " in decimal equivalent is: " << octal_to_decimal(octalnum) << std::endl;  // should output 104 decimal.
    std::cout << "The second octal number: " << octalnum2 << "in decimal equivalent is: " << octal_to_decimal(octalnum2) << std::endl;  //should output 111
    return 0;
}
