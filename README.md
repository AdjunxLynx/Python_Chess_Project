# Python_Chess_Project

Simple chess project for A-Level Computer Science NEA (Non-Exam Assessmsent)

### board layout
This project uses PyGame to display a chess board defined as a 2 dimensional array in the format of an integer 0-63 representing the position from the top left to the top right, then the data of said piece.
the data is of format ```["colour", "piece type", "image name", "x coordinate", "y coordinate", "visibility", "has not moved" ```
`colour` is either `black` or `white`
`piece type` is all the different pieces from Pawn, Rook, Knight, Bishop, Queen and King
`image name` is the file name of the png file storing the image and is named with colours first letter, so `b_` or `w_` for black or white and then the piece name, finally ending with .png for the file type
`x coordinate` is the current x coordinate of the piece from 0-7, 0 being the left most position and 7 being the right
`y coorindate` is the same as `x coordinate` but 0 being the top most square and 7 being the bottom
`visibility` is either `life` or `dead` and if life, will call the `loadPictures()` function to ensure the script is not trying to draw an empty piece
`has not moved` is a boolean that changes if the piece has moved yet. defaults to `True` on startup. used to check wether castling is a legal option (as you cannot if either the king or rook you are trying to castle has moved


<img width="722" alt="image" src="https://github.com/AdjunxLynx/Python_Chess_Project/assets/117390288/8487bd36-dfe9-41e5-aedd-660fa5bf0959">
A variable is created if the user left clicks, and stores temporary data on the piece the mouse is over. this then calls a function that shows all possible moves of that piece, and indicates to user and script what piece is moving.

### rundown of the script with examples
the script then goes through a loop untill no valid moves are left, letting white start first and moving each piece legally. for example the bishop moves by adding or subtracting the values 7 or 9. In the image below, assuming a bishop is on square 36, to move to square 50, it would have to move down the array by 7, twice. This means i can check wether there are any pieces inbetween these 2 positions by checking the squares from (1 to x) lots of 7 where x is the number of diagonal spaces im trying to move the bishop. There is also another check to see if, by moving x\*7, the bishop has gone off the grid. since this is a 1d array, the bishop would 'teleport' to the other side of the board which isnt a legal move, so it needs to see wether its gone past a multiple of 8, or 8 + 1

![explolarge1](https://github.com/AdjunxLynx/Python_Chess_Project/assets/117390288/b17e503e-0d27-4164-a1dc-05ddbf27e4ba)

since the position of the pieces are in 1 dimension, you can split the data within the board into 8 equal sections, as shown in the `board.py` file



### login details
Username: kamil

Password: 1234

<img width="721" alt="image" src="https://github.com/AdjunxLynx/Python_Chess_Project/assets/117390288/659502f8-2122-4ac2-9a8c-e54572e22438">

these username and passwords are not stored securely.
If i were to ensure secure password, I would not upload to github and i would also hash them and read them through a safe function in the python script

