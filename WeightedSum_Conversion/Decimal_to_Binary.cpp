// Repeated Division Algorithm: for decimal (base 10) to binary (base 2):
#include <iostream>
#include <string>

std::string decimal_to_binary( int decimalnum)
{
    // if condition for special case "0", return. decimal == 0
    if (decimalnum == 0)
    {
        return "0";
    }
    // Initialize a new string (binarystr) to == "" empty string.
    std::string binarystr = "";
    // How to get int remainder when divided by 2: decimalnum % 2: while condition for decimalnum > 0:
    while (decimalnum > 0)
    {
        int remainder = decimalnum % 2; //2 = binary.
        // Build in reverse order: decimalnum /= 2
        binarystr = std::to_string(remainder) + binarystr;

        // Divide by 2 for the next iteration:
        decimalnum /= 2;
    }
    return binarystr;
}
int main()
{
    // declare decimalnum:
    int decimalnum = 31;
    std::string binary_result = decimal_to_binary(decimalnum);
    std::cout << " The decimal " << decimalnum << " in binary equivalent is: " << binary_result << std::endl; 
    return 0;
}


