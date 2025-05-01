#include <iostream>
#include <cstdlib> // For rand() and srand()
#include <ctime>   // For time()
#include <limits>  // For numeric_limits
#include "Move.h"

// Function declaration for getResults
int getResults(char player, char computer);
using namespace move;

int main()
{
    char player;
    char computer;
    Move prompt;
    int choice;

    // Seed the random number generator
    srand(static_cast<unsigned int>(time(0)));

    while (true) // Loop the game
    {
        cout << "Rock-Paper-Scissors Game\n";
        cout << "1. Play\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";

        if (!(cin >> choice)) // Check if input is invalid
        {
            cout << "Invalid input! Please enter a number (1 to play or 4 to exit).\n";
            cin.clear(); // Clear the fail state
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Discard invalid input:
            continue;
        }

        if (choice == 4)
        {
            cout << "Exiting the game. Thank you for playing! Goodbye!\n";
            break; // Exit the loop
        }
        else if (choice != 1)
        {
            cout << "Invalid choice! Please enter 1 to play or 4 to exit.\n";
            continue;
        }

        // User input:
        while (true)
        {
            cout << "Enter your move (r for rock, p for paper, s for scissors): ";
            cin >> player;

            // If player equals any of the 3 moves:
            if (player == 'p' || player == 'r' || player == 's')
            {
                break;
            }
            else
            {
                cout << "Invalid move! Please enter r, p, or s.\n";
                continue;
            }
        }

        // Generate computer's move randomly
        int randomMove = rand() % 3; // Generates 0, 1, or 2
        if (randomMove == 0)
            computer = 'r'; // Rock
        else if (randomMove == 1)
            computer = 'p'; // Paper
        else
            computer = 's'; // Scissors

        // Display computer's move
        cout << "Computer's move: ";
        if (computer == 'r')
            cout << "Rock\n";
        else if (computer == 'p')
            cout << "Paper\n";
        else
            cout << "Scissors\n";

        // Determine the result
        int result = getResults(player, computer);
        if (result == 0)
        {
            cout << "Draw\n";
        }
        else if (result == 1)
        {
            cout << "You win!\n";
        }
        else
        {
            cout << "Computer won.\n";
        }
    }

    return 0;
}

// Function definition for getResults
int getResults(char player, char computer)
{
    if (player == computer)
        return 0; // Tie
    else if ((player == 'r' && computer == 's') || 
             (player == 'p' && computer == 'r') || 
             (player == 's' && computer == 'p'))
        return 1; // Player wins
    else
        return -1; // Computer wins
}