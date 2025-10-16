// program that sums every array element using for loop and sum asisgnment.
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

// to print the original unsorted array you need to travers through arr[i] with a for loop and cout statement:
void print_array (const int arr[], int size)
{
    std::cout << "The original unsorted array is: ";
    for (int i = 0; i < size; i++)
    {
        std::cout << arr[i];
        std::cout << " ";
    }
    std::cout << std::endl;
}

// function to sort array lowest to highest:
void sort_array (int arr[], int size)
{
    std::cout << "Sorting array by ascending using insertion sort: ";
    for (int i = 1; i < size; i++)
    {
        int key = arr[i];
        int j = i - 1;

        // Move elements of arr[0..i-1] that are greater than the key
        // to one position ahead of their current position + 1 to the right:
        for (int j = 1; j < size; j++)
        {
            while ( j >= 0 && arr[j] > key)
            {
                arr[ j + 1] = arr[j];
                j = j - 1;
            }
        }
    }
}

int main()
{
    // define the actual elements with a new declarative array:
    int array[] = {29, 12, 1993, 04, 2023, 11, 1968, 8, 12, 2001, 02, 9};
    // deifne int n:
    int size = 12;
    int totalSum = sum_array(array, size); // plugin main array defined, with n.

    std::cout << "The sum of array elements are: " << totalSum << std::endl;
    std::cout << "The original unsorted array is: ";
    print_array(array, size);
    
    std::cout << " Sort array by ascending order: ";
    sort_array(array, size);
    return 0;
}