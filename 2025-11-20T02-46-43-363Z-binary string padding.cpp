#include <iostream>
#include <string>

// Function to manually pad a string on the left
std::string pad_left(const std::string& a, int width, char pad_char) {
    // Check if the current string length is already greater than or equal to the desired width
    if (a.length() >= width) {
        return a;
    }

    // Calculate how many padding characters are needed
    int pad_count = width - a.length();

    // Create a new string with the padding characters, then append the original string
    std::string padded_string(pad_count, pad_char);
    padded_string.append(a);

    return padded_string;
}

// Function to manually pad a string on the right
std::string pad_right(const std::string& a, int width, char pad_char) {
    if (a.length() >= width) {
        return a;
    }

    int pad_count = width - a.length();
    std::string padded_string = a;
    padded_string.append(pad_count, pad_char);

    return padded_string;
}

int main() {
    std::string text = "111";
    int target_width = 10;
    char padding_character = '0';

    // Demonstrate left padding
    std::string left_padded = pad_left(text, target_width, padding_character);
    std::cout << "Original: " << text << std::endl;
    std::cout << "Left padded: " << left_padded << std::endl;

    // Demonstrate right padding
    std::string right_padded = pad_right(text, target_width, padding_character);
    std::cout << "Right padded: " << right_padded << std::endl;

    return 0;
}