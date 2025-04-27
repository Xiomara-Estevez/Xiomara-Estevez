// Header file: Oop Design for Calculator Program using simple Math Operations held in classes:
// STRATEGY DESIGN PATTERN:
#ifndef STRATEGY_H
#define STRATEGY_H
#include <iostream>
#include <string>
#include <sstream>
using namespace std;
namespace oopn 
{
    class Object 
    {
        public:
        virtual string toString() const = 0;    // pure virtual method:

        friend ostream& operator<<(ostream& out,const Object& obj)
        {
            return out << obj.toString();
        }
    };

    //Strategy Interface
    class Operation
    {
        public:
        // Pure virtual methods for Interface Operation:
        virtual string symbol() const = 0;
        virtual string execute(int,int) = 0;    // parameters: int, int:
    };
    
    //Context Class
    class Calculator : public Object
    {
        private:
        Operation* op;
        int a;
        int b;

        public:
        // Default constructor:
        Calculator() : Calculator(0,0) {}
        // Parametized constructor: assigns default of a to a, and b to b parameter:
        Calculator(int a,int b) : a(a), b(b) {}
        
        // setter method for set(Operation* pointer) points to an assignment of the paramater argument:
        void set(Operation* value)
        {
            this->op = value;
        }

        // string getter method excute() = returns op->this pointer execute with parameters a, b:
        string execute() 
        {
            if(op == nullptr) {return string();}
            return op->execute(a,b);
        }

        // x () getter returns a:
        int x() const {return a;}

        // x setter sets parameter value,  assigns a to value
        void x(int value) {a = value;}

        // y() geter const method = returns b:
        int y() const {return b;}

        // y() setter() method, assigns parameter value to b:
        void y(int value) {b = value;}

        // Overridden toString method const returns a:, or op->symbol() else b:
        string toString() const override 
        {
            std::stringstream out;

            out << a << " ";

            if(op != nullptr)
            {
                out << op->symbol() << " ";
            }
            out << b;
            return out.str();
        }
    };

    class Addition : public Operation
    {
        public:
        string symbol() const override {return "+";}

        string execute(int a,int b) override 
        {
            return to_string(a + b);
        }
    };


    class Subtraction : public Operation
    {
        public:
        string symbol() const override {return "-";}

        string execute(int a,int b) override 
        {
            return to_string(a - b);
        }
    };
    
    class Multiplication : public Operation
    {
        public:
        string symbol() const override {return "*";}

        string execute(int a,int b) override 
        {
            return to_string(a * b);
        }
    };
    
    class Division : public Operation
    {
        public:
        string symbol() const override {return "//";}

        string execute(int a,int b) override 
        {
            if(b == 0) {return "error";}
            return to_string(a / b);
        }
    };
}
#endif