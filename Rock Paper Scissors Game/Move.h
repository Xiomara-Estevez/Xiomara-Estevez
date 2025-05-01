// ROCK, PAPER, SCISSORS GAME:
// Header file for the move functions:
#ifndef MOVE_H
#define MOVE_H
#include <iostream>
#include <ctime>
#include <cstdlib>
using namespace std;

namespace move
{
    class Move
    {
        public:
        Move() 
        {
            cout << "Rock, Paper, Scissors Game:\n";
            cout << "Enter: 'r' for Rock, 'p' for Paper, 's', for Scissors:\n";
        }

        char getComputerMoves()
        {
            int move;
            srand(time(nullptr));   // generates random number from 0-2: because there are 3 moves: rock, paper, scissors:
            move = rand() % 3;

            if (move == 0)
            {
            // 0 = Tie/Draw, 1 = Win, -1 = Lose:
            return 'p'; // 'p' = Paper: 
            }
            else if (move == 1)
            {
                return 's'; // 's' = scissors:
            }
            return 'r';     // 'r' = rock:
        }
        int getResults(char player, char computer)
        {
            int result = getResults(player, computer);
            // Draw condition:
            if (player == computer)
            {
                cout << "It's a draw!\n";
                return 0;
            }

            // paper win and lose condition:
            // Rules:
            // Rock vs. Paper = Paper WINS
            // Paper vs. Scissor = Scissor WINS
            // Scissor vs. Rock = Rock WINS
            if (player == 's' && computer == 'p')
            {
                // Scissors beats paper: true
                return 1;   // 1 = win:
            }
            if (player == 's' && computer == 'r')
            {
                // scissors beats rock = false
                return -1; // -1 = Lose:
            }
            if (player == 'p' && computer == 'r')
            {
                // paper beats rock = true
                return 1;
            }
            if (player == 'p' && computer == 's')
            {
                // paper beats scissors = false:
                return -1;
            }
            if (player == 'r' && computer == 'p')
            {
                // Rock beats paper = false
                return -1;
            }
            if (player == 'r' && computer == 's')
            {
                // rock beats scissor = true
                return 1;
            }
            return 0;
        }
    };
}
#endif