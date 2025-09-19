// Bubble Sort Algorithm
// psuedo code:
#include<iostream>
//function bubblesort(array A)
//{
    // n = length(A): n assigned to the length of A input
    // for int i from 1 to n-1: inner loop iterates n-1 times:
        //  if A[j] > A[j + 1]
            // for (int j = 0; j < n - i - 1; i++)
                // swap (a[j], a[j + 1]): inner loop swaps two adjacent elements
                // int temp = arr[j] assign a temp variable to a[j]
                // arr[j] = arr[j + 1]
                 // arr[j + 1 ] = temp
                // end for
            // end for
        // end if
    // end for
//}

// manually implement function:
void bubblesort (int arr[], int n)
{
    for (int i = 0; i < n - 1; i++) // j variable - 3 variables: n i  1
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            // swap adjacents:  uses condition if
            if (arr[j] > arr[j + 1])
            {
                // use a temp variable to swap with arr[j]
                int temp = arr[j];

                // assign arr[j] to arr[j + 1]
                arr[j] = arr[j + 1];
                // assign arr[j + 1] to temp
                arr[j + 1] = temp;
            }
        }
    }
}

// print function:
void print (int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        std::cout << arr[i] << " "; 
    }
    std::cout << std::endl;
}
// main driver test:
int main()
{
    // make a defintition of an array with data in it:
    int array[] {2, 1, 5, 4, 3, 6};

    // sort through array with formula: sizeof(array) / sizeof(array[0])
    int n = sizeof(array) / sizeof(array[0]); // parameter from function defined here!

    // call original:
    std::cout << "Original array: ";
    print(array, n);
    bubblesort(array, n);

    std::cout << "Sorted: ";
    print(array, n);
    return 0;
}