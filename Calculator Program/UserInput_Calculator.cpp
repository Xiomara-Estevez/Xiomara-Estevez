// This is the user-input version of the calculator program:
#include <iostream>
#include <memory> // smart pointers:
#include "Strategy.h"
using namespace std;

int main()
{
    // assign Operation* pointer nullptr:
    oopn::Operation* operations= nullptr;
    oopn::Calculator calculator;
    int x, y;
    char operation;

    cout << 
    "Enter the first number: ";
    cin >> x;
    calculator.x(x);

    cout << "Enter the second number: ";
    cin >> y;
    calculator.y(y);

    // choose operation:
    cout << "What operation will you perform?: +, /, *, -: ";
    cin >> operation;

    while (true)
    {
        // switch statement for the different operation's symbols:
        switch (operation)
        {
            // ADDITION:
            case '+':
            operations = new oopn::Addition;
            break;

            // SUBTRACTION:
            case '-':
            operations = new oopn::Subtraction;
            break;

            // MULTIPLICATION:
            case '*':
            operations = new oopn::Multiplication;
            break;

            // DIVISION:
            case '/':
            operations = new oopn::Division;
            break;

            default:
            cout << "Invalid operation! Re-enter: " << endl;
            cin >> operation;
            continue;   // loop until correct
        }
        // while true scope : use break here:
        // if correct operation symbol:
        break;  // exit the loop if valid operation choosen
    }
    // calls caluclator with the operations and their results:
    calculator.set(operations);
    cout << "Result: " << calculator.execute() << endl; // displays the operation results:

    // clean up dynamically allocated memory!!!
    delete operations;
    return 0;
}