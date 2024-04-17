# Text-Chess

`Welcome to text chess!
8 '♜' '♞' '♝' '♛' '♚' '♝' '♞' '♜'
7 '♟' '♟' '♟' '♟' '♟' '♟' '♟' '♟'
6 ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '
5 ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '
4 ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '
3 ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '
2 '♙' '♙' '♙' '♙' '♙' '♙' '♙' '♙'
1 '♖' '♘' '♗' '♕' '♔' '♗' '♘' '♖'
   a   b   c   d   e   f   g   h
White, it's your turn! Please enter your move ('h' for help):`

Here is how you can enter a move. 
First, enter the piece you are trying to move. 
This will just be one letter. 
Type K for king, Q for queen, R for rook, B for bishop, N for knight, and P for pawn. 
You MUST type a P for any pawn move (unlike algebraic notation, if you know it).
Next, enter the starting square that your piece is currently on. 
This will be a letter [a-h] for the file (column) 
and a number [1-8] for the rank (row) where your piece is. 
Then, enter the ending square where you want to move your piece. 
This will again be a letter [a-h] and a number [1-8] for the file and rank.

There is no need to include any extra symbols or characters 
unless you are castling or promoting a pawn to a new major piece. 
Sometimes chess players write 'x', '+', '#' (again from algebraic notation)
to indicate a capture, check, or checkmate respectively, 
but please don't include those when entering a move.

Examples:
To move your queen from d1 to e2, type 'Qd1e2'.
To move your bishop from g7 to f6, type 'Bg7f6'.
To move your knight from f3 to d4, type 'Nf3d4'.
To move your pawn forward one square to a5, type 'Pa4a5'.
To capture en passant on c6 from the b file, type 'Pb5c6'.
To capture a knight on e4 with your king on d5, type 'Kd5e4'.
To capture a rook on e8 with your rook on e1, type 'Re1e8'.
To capture a queen on c1 with your pawn on b2 and promote to a knight, type 'Pb2c1=N'. 
If instead you wanted to just promote to a queen and not capture, you should type 'Pb2b1=Q'.
To castle kingside, type '0-0'. To castle queenside, type '0-0-0'.
Using either the upper case letter O or the number 0 will be accepted for castling.