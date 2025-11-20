#ifndef HEAP_H
#define HEAP_H
#include <iostream>
#include <algorithm>
using namespace std;

int parent(int i) { return (i - 1) / 2; }   // 0 indexed
int left(int i)   { return 2 * i + 1; }
int right(int i)  { return 2 * i + 2; }

void Max_Heapify(int arr[], int i, int n)  // max heap property:
{
    int L = left(i);
    int R = right(i);
    int largest = i;

    if(L < n && arr[L] > arr[largest])
    {
        largest = L;
    }
    if(R < n && arr[R] > arr[largest])
    {
        largest = R;
    }
    
    if(largest != i)
    {
        swap(arr[i], arr[largest]);
        Max_Heapify(arr, largest, n);
    }
}

void Build_Max_Heap(int arr[], int n)
{
    for (int i = n / 2 - 1; i >=  0; i--)
    {
        Max_Heapify(arr, i, n);
    }
}

void Heap_Sort(int arr[], int n)
{
    Build_Max_Heap(arr, n);

    // One by one extract an element from heap
    for (int i = n - 1; i > 0; i--)
    {
        // Move current root to end
        swap(arr[0], arr[i]);
        // Call Max_Heapify on the reduced heap
        Max_Heapify(arr, 0, i);
    }
}

void print(int arr[], int n)
{
    
    for(int i = 0; i < n; i++)
    {
        cout << arr[i] << ", ";
    }
    cout << endl;
}
#endif