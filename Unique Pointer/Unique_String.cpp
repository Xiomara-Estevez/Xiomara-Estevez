// A program consisting of unique pointer string arrays for displaying words:
#include <iostream>
#include <string>
#include <memory> // Include memory for unique_ptr
using namespace std;

int main()
{
    int max; // Initialize max with a valid integer value
    cout << "How many words do you want to type in?: ";
    cin >> max;

    unique_ptr<string[]> ptr(new string[max]); // Initialize after max is assigned

    for (int i = 0; i < max; i++)
    {
        cout << "Enter any word that comes to mind: ";
        cin >> ptr[i];
    }

    // display the contents of the array with cout:
    cout << "Here is what you entered: ";
    for (int i= 0; i < max; i++)
    {
        cout << ptr[i] << " ";
    }
    return 0;    
}