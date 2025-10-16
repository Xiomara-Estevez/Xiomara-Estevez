// modern sum array:
#include <iostream>
#include <numeric>   // accumulate()

// print array in ascending order:
void printarray(const int array[], int size)
{
    std::cout << "Sorted array in ascending order: ";
    for (int i = 0; i < size; ++i)
    {
        std::cout << array[i] << (i + 1 == size ? '\n' : ' ');
    }
}

void sort_array(int array[], int size)
{
    // Standard insertion sort
    for (int i = 1; i < size; ++i)
    {
        int key = array[i];
        int j = i - 1;
        while (j >= 0 && array[j] > key)
        {
            array[j + 1] = array[j];
            --j;
        }
        array[j + 1] = key;
    }
}

int main()
{
    int arr[] = {2, 20, 8}; // partially filled literal
    int size = static_cast<int>(sizeof(arr) / sizeof(arr[0]));
    int sum = std::accumulate(arr, arr + size, 0);

    sort_array(arr, size);
    printarray(arr, size);

    std::cout << "Sum of array is: " << sum << std::endl;
    return 0;
}