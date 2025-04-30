#include "Strategy.h"
// non-user -input: Calculator operation program: MULTIPLICATION, DIVISION, ADDITION, SUBTRACTION:
int main()
{
    oopn::Operation* a;
    oopn::Calculator c;
    c.x(3);
    c.y(2);

    cout << "Addition Operation\n";         // Outputs: 3 + 2 = 5
    a = new oopn::Addition;
    c.set(a);
    std::cout << c << " = " << c.execute() << "\n";
    delete a;
 
    cout << "Subtraction Operation\n";      // Outputs: 3-2 = 1
    a = new oopn::Subtraction;
    c.set(a);
    cout << c << " = " << c.execute() << "\n";
    delete a;

    cout << "Multiplication Operation\n";   // Outputs: 3 * 2 = 6
    a = new oopn::Multiplication;
    c.set(a);
    cout << c << " = " << c.execute() << "\n";
    delete a;
 
    cout << "Division Operation\n";         // Outputs: 3 divided by 2 = 1
    a = new oopn::Division;
    c.set(a);
    cout << c << " = " << c.execute() << "\n";
    delete a;    

    return 0;
}