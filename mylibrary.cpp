#include <Python.h>
#include <iostream>

// Ensure that the function uses C linkage for Python compatibility
extern "C" {

    // Define the function that will be called from Python
    bool king_dead(PyObject* positions_dict) {
        // Check if the input dictionary is valid
        if (!PyDict_Check(positions_dict)) {
            std::cerr << "Input is not a valid Python dictionary." << std::endl;
            return true;  // Returning true as an error flag
        }

        // Iterate over each key-value pair in the dictionary
        PyObject* key;
        PyObject* value;
        Py_ssize_t pos = 0;

        bool found_black_king = false;
        bool found_white_king = false;

        while (PyDict_Next(positions_dict, &pos, &key, &value)) {
            // Convert the key to a string (chess position, e.g., "a3")
            const char* position = PyUnicode_AsUTF8(key);
            if (position == nullptr) {
                continue;  // Skip if the position is not a valid string
            }

            // Convert the value to a string (chess piece, e.g., "black_king")
            const char* piece = PyUnicode_AsUTF8(value);
            if (piece == nullptr) {
                continue;  // Skip if the piece is not a valid string
            }

            // Check for the kings
            if (strcmp(piece, "black_king") == 0) {
                found_black_king = true;
            } else if (strcmp(piece, "white_king") == 0) {
                found_white_king = true;
            }
        }

        // If both kings are found, return false, otherwise return true
        return !(found_black_king && found_white_king);
    }

}

