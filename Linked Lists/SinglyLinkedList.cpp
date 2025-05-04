#include <iostream>
#include <limits> // to use numeric_limits
using namespace std;

class Node
{
private:
    int data;
    Node* next;

    friend class LinkedList;

public:
    Node(int value) : data(value), next(nullptr) {}
};

class LinkedList
{
private:
    Node* head;

public:
    LinkedList()
    {
        head = nullptr;
        cout << "Choose from the menu:\n";
        cout << "1. Insert at the beginning.\n";
        cout << "2. Insert at the middle.\n";
        cout << "3. Insert at the end.\n";
        cout << "4. Delete from the beginning.\n";
        cout << "5. Delete from the middle.\n";
        cout << "6. Delete from the end.\n";
        cout << "7. Exit the program.\n";
    }

    void InsertBeginning()
    {
        int data;
        cout << "Enter the value to insert at the beginning: ";
        cin >> data;

        Node* newnode = new Node(data);
        newnode->next = head;
        head = newnode;
    }

    void InsertAtEnd()
    {
        int data;
        cout << "Enter a value to insert at the end: ";
        cin >> data;

        Node* newnode = new Node(data);

        if (head == nullptr)
        {
            head = newnode;
            return;
        }

        Node* last = head;
        while (last->next != nullptr)
        {
            last = last->next;
        }

        last->next = newnode;
    }

    Node* InsertAtMiddle(int x)
    {
        if (head == nullptr)
        {
            return new Node(x);
        }

        Node* newnode = new Node(x);
        Node* current = head;

        int length = 0;
        while (current != nullptr)
        {
            length++;
            current = current->next;
        }

        int mid = length / 2;
        if (length % 2 != 0)
        {
            mid += 1;
        }

        current = head;
        while (mid > 1)
        {
            current = current->next;
            mid--;
        }

        newnode->next = current->next;
        current->next = newnode;
        return head;
    }

    Node* DeleteEnd()
    {
        if (head == nullptr)
        {
            cout << "The list is empty. Nothing to delete." << endl;
            return nullptr;
        }

        if (head->next == nullptr)
        {
            delete head;
            head = nullptr;
            return nullptr;
        }

        Node* temp = head;
        while (temp->next->next != nullptr)
        {
            temp = temp->next;
        }

        delete temp->next;
        temp->next = nullptr;

        return head;
    }

    Node* DeleteBeginning()
    {
        if (head == nullptr)
        {
            cout << "The list is empty. There is nothing to delete.\n";
            return nullptr;
        }

        Node* temp = head;
        head = head->next;
        delete temp;
        return head;
    }

    Node* DeleteMiddle()
    {
        if (head == nullptr)
        {
            cout << "The list is empty, nothing to currently delete.\n";
            return nullptr;
        }

        if (head->next == nullptr)
        {
            delete head;
            head = nullptr;
            return nullptr;
        }

        if (head->next->next == nullptr)
        {
            delete head->next;
            head->next = nullptr;
            return head;
        }

        Node* current = head;
        int length = 0;

        while (current != nullptr)
        {
            length++;
            current = current->next;
        }

        int mid = length / 2;
        if (length % 2 != 0)
        {
            mid += 1;
        }

        current = head;
        for (int i = 0; i < mid - 1; i++)
        {
            current = current->next;
        }

        Node* temp = current->next;
        current->next = temp->next;
        delete temp;

        return head;
    }

    void Print()
    {
        if (head == nullptr)
        {
            cout << "The list is currently empty." << endl;
            return;
        }

        Node* temp = head;
        while (temp != nullptr)
        {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }
};

int main()
{
    LinkedList list;
    int choice;

    while (true)
    {
        cout << "Please pick from the menu: ";
        cin >> choice;

        if (cin.fail())
        {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Please enter a valid choice from the menu: ";
            continue;
        }

        switch (choice)
        {
        case 1:
            cout << "1. Insert at the beginning.\n";
            list.InsertBeginning();
            cout << "Current list: ";
            list.Print();
            break;

        case 2:
            cout << "2. Insert at the middle.\n";
            int value;
            cout << "Enter the value to insert at the middle: ";
            while (!(cin >> value))
            {
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                cout << "Invalid input! Please enter an integer: ";
            }
            list.InsertAtMiddle(value);
            cout << "Current list: ";
            list.Print();
            break;

        case 3:
            cout << "3. Insert at the end.\n";
            list.InsertAtEnd();
            cout << "Current list: ";
            list.Print();
            break;

        case 4:
            cout << "4. Delete from the beginning.\n";
            list.DeleteBeginning();
            cout << "Current list: ";
            list.Print();
            break;

        case 5:
            cout << "5. Delete from the middle.\n";
            list.DeleteMiddle();
            cout << "Current list: ";
            list.Print();
            break;

        case 6:
            cout << "6. Delete from the end.\n";
            list.DeleteEnd();
            cout << "Current list: ";
            list.Print();
            break;

        case 7:
            cout << "Exiting the program.\n";
            return 0;

        default:
            cout << "Invalid input, please pick from the menu.\n";
            break;
        }

        char continueChoice;
        cout << "\nDo you wish to continue through the menu? y/n: ";
        cin >> continueChoice;

        if (continueChoice == 'y' || continueChoice == 'Y')
        {
            continue;
        }
        else if (continueChoice == 'n' || continueChoice == 'N')
        {
            cout << "Exiting the program. Goodbye.\n";
            return 0;
        }
        else
        {
            cout << "Invalid input, please enter 'y' or 'n'.\n";
            continue;
        }
    }

    return 0;
}