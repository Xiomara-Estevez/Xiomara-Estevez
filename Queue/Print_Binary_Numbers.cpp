#include <iostream>
#include <string>
#include <vector>
#include <queue>
using namespace std;

// create prints of binary numbers using vector and queue:
// ex: 1 10, 110, ... etc
vector<string> printBinary(int n)
{
    // create a vector and queue of string data type:
    queue<string> q;
    vector<string> s;

    // push "1" string to the top of the queue list:
    q.push("1");

    // while condition: while n--:
    while (n--)
    {
        // assign new string str to q.front(), which will push the value to the front of the list:
        string str = q.front();
        // remove:
        q.pop();
        // push str now to the back of the list:
        s.push_back(str);
        // concatenate with str + "0", and str + "1":, then outside scope of while, return s the vector:
        q.push(str + "0");
        q.push(str + "1");
    }
    return s;
    
}

int main()
{
    int n = 10;  // size of numbers to generate:
    // need to assign a vector<string> to printBinary function to print
    vector<string> binaryNumbers = printBinary(n);  

    // print using a loop and a const string& ref. to binary:
    cout << "here are the binary numbers: " << endl;
    for (const string& binary : binaryNumbers)
    {
        cout << binary << " ";
    }
    cout << endl;
    return 0;
}