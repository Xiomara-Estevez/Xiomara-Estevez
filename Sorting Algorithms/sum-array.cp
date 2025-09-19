// program that sums every array element using for loop and sum asisgnment.\
#include <iostream>

int sum_array (const int arr[], int size)
{
    int sum = 0;    // sentinel will sum assign a[i]:

    // condition for loop iterates and increments through array subscript element arr[i]:
    for (int i = 0; i < size; i++)
    {
        sum += arr[i];
    }
    return sum;
}
int main()
{
    // define the actual elements with a new declarative array:
    int array = {29, 12, 1993, 04, 2023, 11, 1968, 08, 12, 2001, 02, 09};

    cout << "Original elements unsorted: " << array << endl;
    return 0;
}