// program for Weighted Sum Algorithm: Hexadecimal (base 16) to Decimal (base 10):
#include <iostream>
#include <string>
#include <sstream>  // for string stream out
#include <cmath>

int hexadecimal_to_decimal(char hex_char)   // a-f, A-F, 0-9
{
    if (hex_char >= '0' && hex_char <= '9')
    {
        // return hex_char - '0' for numerical.
        return hex_char - '0';
    }
    else if (hex_char >= 'A' && hex_char <= 'F')
    {
        // for alphanumerical UPPERCASE:
        return hex_char - 'A' + 10;
    }
    // lowercase alphanumerical:
    else if (hex_char >= 'a' && hex_char <= 'f')
    {
        return hex_char - 'a' + 10;
    }
    return 0;   // for invalid hex character.
}

// hexadecimal string to decimal int value: Reference parameter for hex_string
long long hex_string_to_decimal( std::string& hex_string)
{
    long long decimalvalue = 0;
    int power = 0;

    // since hexadecimal, going from right to left so hex_string.length() - 1; i >= 0; --i
    for (int i = hex_string.length() - 1; i >= 0; --i)
    {
        // assign anew declare int hexdigit = hexadecimal_to_decimal(hex_string[i])
        int hexdigit = hexadecimal_to_decimal(hex_string[i]);
        // add assignment from decimalvalue to formula: hexdigit * static_cast<long long> std::pow(16, power);
        decimalvalue += hexdigit * static_cast<long long>(std::pow(16, power));
        power++;
    }
    return decimalvalue;
}
// maind driver test:
int main()
{
    std::string hex_input = "4AF";
    long long decimal_result = hex_string_to_decimal(hex_input);

    // stringstream to print:
    std::stringstream out;
    out << "The hexadecimal " << hex_input << " to decimal equivalent is " << decimal_result << std::endl;
    // print string stream to console
    std::cout << out.str();
    return 0;
}