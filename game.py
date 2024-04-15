import re

help_message = """Here is how you can enter a move. 
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

Press Enter to return....
"""

#ep not working
#check castling rights, if white castles then dont clear black castling rights

def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

class Game:

	castle_strs = ["0-0","0-0-0","O-O","O-O-O"]
	cvt_prm_pce = {
		'Q': ('\u2655','\u265b'),
		'R': ('\u2656','\u265c'),
		'B': ('\u2657','\u265d'),
		'N': ('\u2658','\u265e'),
		None: (None,None)
	}

	def __init__(self):
		self.board = [
			['\u2656','\u2658','\u2657','\u2655','\u2654','\u2657','\u2658','\u2656'],
			['\u2659' for _ in range(8)],
			[' ' for _ in range(8)],
			[' ' for _ in range(8)],
			[' ' for _ in range(8)],
			[' ' for _ in range(8)],
			['\u265f' for _ in range(8)],	
			['\u265c','\u265e','\u265d','\u265b','\u265a','\u265d','\u265e','\u265c']
		]
		self.positions = {str(self.board):1}
		self.turn = 'White'
		self.white_castle_rights = [True, True] #[short, long]
		self.black_castle_rights = [True, True]
		# ...e_p_file holds the file (board[][j]) on which 
		# the enemy pawn just moved forward two squares
		self.white_e_p_file = float('inf')
		self.black_e_p_file = float('inf')
		self.king = '\u2654'
		self.king_i = 0
		self.king_j = 4
		self.result = None

	# potentially keep track of move # instead of always clearing ep variables
	# currently have to always set_e_p_file within each of the make_move functions

	def welcome_message(self):
		print("Welcome to text chess!")

	def get_move(self):
		while True:
			self.print_board()
			move_str = input("{}, it's your turn! Please enter your move ('h' for help): ".format(self.turn)).strip()
			if move_str == 'h':
				input(help_message)
			else:
				if self.is_well_formed(move_str):
					# breakpoint()
					msg = self.make_move(move_str)
					if msg:
						print(msg)
					else:
						break
				else:
					print("Moves must be in the format <piece><start sq><end sq> (unless castling). Please try again.")
		self.finish_move()

	def is_well_formed(self, text):
		pattern = "^[KQRBNP]([a-h][1-8]){2}((?<=^P.{4})=[QRBN])?$"
		return text in self.castle_strs or re.search(pattern, text)

	def make_move(self, move_str):
		if move_str in self.castle_strs:
			if self.is_check():
				return "You're in check; castling is not allowed."
			else:
				return self.make_castle_move(move_str)
		else:
			if move_str[1:3] != move_str[3:5]:
				pce = move_str[0]
				if len(move_str) > 5:
					return make_pawn_move(*self.process_move_sqs(move_str[1:5]), move_str[6])
				else:
					return {
						"K": self.make_king_move,
						"Q": self.make_queen_move,
						"R": self.make_rook_move,
						"B": self.make_bishop_move,
						"N": self.make_knight_move,
						"P": self.make_pawn_move
					}[pce](*self.process_move_sqs(move_str[1:5]))
			else:
				return "Starting and ending squares must be different."

	def process_move_sqs(self, squares_str):
		return (int(squares_str[1])-1, ord(squares_str[0])-97, int(squares_str[3])-1, ord(squares_str[2])-97)

	def make_castle_move(self, move_str):
		if self.king == '\u2654':
			rights = self.white_castle_rights
			rook = '\u2656'
		else:
			rights = self.black_castle_rights
			rook = '\u265c'
		if move_str in ["0-0","O-O"]:
			d_file = 1
			spaces = 2
			right = rights[0]
		else:
			d_file = -1
			spaces = 3
			right = rights[1]
		if right:
			if all([self.board[self.king_i][self.king_j + (dj+1)*d_file] == ' ' for dj in range(spaces)]):
				can_castle = True
				for _ in range(2):
					self.board[self.king_i][self.king_j] = ' '
					self.king_j += d_file
					self.board[self.king_i][self.king_j] = self.king
					can_castle = can_castle and not self.is_check()
				if can_castle:
					self.board[self.king_i][self.king_j + d_file*(spaces-1)] = ' '
					self.board[self.king_i][self.king_j - d_file] = rook
					rights[0] = False
					rights[1] = False
					self.set_e_p_file()
					return ''
				else:
					self.board[self.king_i][self.king_j] = ' '
					self.king_j -= 2*d_file
					self.board[self.king_i][self.king_j] = self.king
					return "You cannot castle through check."
			else:
				return "You cannot castle because there are pieces in the way."
		else:
			return "You lost castle rights by moving your king or rook on a previous turn."

	def make_king_move(self, srt_i, srt_j, end_i, end_j):
		if self.king == '\u2654':
			rights = self.white_castle_rights
			frly_pcs = ['\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			rights = self.black_castle_rights
			frly_pcs = ['\u265b','\u265c','\u265d','\u265e','\u265f']
		if self.king_i == srt_i and self.king_j == srt_j:
			if abs(end_i - srt_i) <= 1 and abs(end_j - srt_j) <= 1:
				if self.board[end_i][end_j] not in frly_pcs:
					self.board[self.king_i][self.king_j] = ' '
					self.king_i = end_i
					self.king_j = end_j
					old_pce = self.board[self.king_i][self.king_j]
					self.board[self.king_i][self.king_j] = self.king
					if not self.is_king_check() and not self.is_check():
						rights[0] = False
						rights[1] = False
						self.set_e_p_file()
						return ""
					else:
						self.board[self.king_i][self.king_j] = old_pce
						self.king_i = srt_i
						self.king_j = srt_j
						self.board[self.king_i][self.king_j] = self.king
						return "King cannot move into check."
				else:
					return "King cannot move to square with a friendly piece on it."
			else:
				return "King cannot move more than one square."
		else:
			return "King is not on the specified starting move square."

	def make_queen_move(self, srt_i, srt_j, end_i, end_j):
		if self.king == '\u2654':
			queen = '\u2655'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			queen = '\u265b'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		if self.board[srt_i][srt_j] == queen:
			di = end_i-srt_i
			dj = end_j-srt_j
			if di == 0 or dj == 0 or abs(di) == abs(dj):
				no_pce_blk = True
				sqr_is = range(end_i, srt_i, -sign(di)) if di != 0 else [end_i]*abs(dj)
				sqr_js = range(end_j, srt_j, -sign(dj)) if dj != 0 else [end_j]*abs(di)
				for i,j in zip(sqr_is, sqr_js):
					if self.board[i][j] in frly_pcs:
						no_pce_blk = False
						break
					elif self.board[i][j] != ' ' and (i != end_i or j != end_j):
						no_pce_blk = False
						break
				if no_pce_blk:
					self.board[srt_i][srt_j] = ' '
					old_pce = self.board[end_i][end_j]
					self.board[end_i][end_j] = queen
					if not self.is_check():
						self.set_e_p_file()
						return ""
					else:
						self.board[end_i][end_j] = old_pce
						self.board[srt_i][srt_j] = queen
						return "Queen cannot make a move that leaves own king in check."
				else:
					return "Queen cannot jump over pieces or land in a square occupied by a friendly piece."
			else:
				return "Queen can only move vertically, horizontally, or diagonally."
		else:
			return "There is no queen on the specified starting move square."

	def make_rook_move(self, srt_i, srt_j, end_i, end_j):
		if self.king == '\u2654':
			rook = '\u2656'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
			rights = self.white_castle_rights
		else:
			rook = '\u265c'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
			rights = self.black_castle_rights
		if self.board[srt_i][srt_j] == rook:
			di = end_i-srt_i
			dj = end_j-srt_j
			if di == 0 or dj == 0:
				no_pce_blk = True
				sqr_is = range(end_i, srt_i, -sign(di)) if di != 0 else [end_i]*abs(dj)
				sqr_js = range(end_j, srt_j, -sign(dj)) if dj != 0 else [end_j]*abs(di)
				for i,j in zip(sqr_is, sqr_js):
					if self.board[i][j] in frly_pcs:
						no_pce_blk = False
						break
					elif self.board[i][j] != ' ' and (i != end_i or j != end_j):
						no_pce_blk = False
						break
				if no_pce_blk:
					self.board[srt_i][srt_j] = ' '
					old_pce = self.board[end_i][end_j]
					self.board[end_i][end_j] = rook
					if not self.is_check():
						if srt_j == 7:
							rights[0] = False
						elif srt_j == 0:
							rights[1] = False
						self.set_e_p_file()
						return ""
					else:
						self.board[end_i][end_j] = old_pce
						self.board[srt_i][srt_j] = rook
						return "Rook cannot make a move that leaves own king in check."
				else:
					return "Rook cannot jump over pieces or land in a square occupied by a friendly piece."
			else:
				return "Rook can only move vertically or horizontally."
		else:
			return "There is no rook on the specified starting move square."

	def make_bishop_move(self, srt_i, srt_j, end_i, end_j):
		if self.king == '\u2654':
			bishop = '\u2657'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			bishop = '\u265d'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		if self.board[srt_i][srt_j] == bishop:
			di = end_i-srt_i
			dj = end_j-srt_j
			if abs(di) == abs(dj):
				no_pce_blk = True
				sqr_is = range(end_i, srt_i, -sign(di))
				sqr_js = range(end_j, srt_j, -sign(dj))
				for i,j in zip(sqr_is, sqr_js):
					if self.board[i][j] in frly_pcs:
						no_pce_blk = False
						break
					elif self.board[i][j] != ' ' and (i != end_i or j != end_j):
						no_pce_blk = False
						break
				if no_pce_blk:
					self.board[srt_i][srt_j] = ' '
					old_pce = self.board[end_i][end_j]
					self.board[end_i][end_j] = bishop
					if not self.is_check():
						self.set_e_p_file()
						return ""
					else:
						self.board[end_i][end_j] = old_pce
						self.board[srt_i][srt_j] = bishop
						return "Bishop cannot make a move that leaves own king in check."
				else:
					return "Bishop cannot jump over pieces or land in a square occupied by a friendly piece."
			else:
				return "Bishop can only move diagonally."
		else:
			return "There is no bishop on the specified starting move square."

	def make_knight_move(self, srt_i, srt_j, end_i, end_j):
		if self.king == '\u2654':
			knight = '\u2658'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			knight = '\u265e'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		if self.board[srt_i][srt_j] == knight:
			if (end_i-srt_i, end_j-srt_j) in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
				if self.board[end_i][end_j] not in frly_pcs:
					self.board[srt_i][srt_j] = ' '
					old_pce = self.board[end_i][end_j]
					self.board[end_i][end_j] = knight
					if not self.is_check():
						self.set_e_p_file()
						return ""
					else:
						self.board[end_i][end_j] = old_pce
						self.board[srt_i][srt_j] = knight
						return "Knight cannot make a move that leaves own king in check."
				else:
					return "Knight cannot move to square with a friendly piece on it."
			else:
				return "Knight can only move in a 1x2 L-shape."
		else:
			return "There is no knight on the specified starting move square."

	def make_pawn_move(self, srt_i, srt_j, end_i, end_j, prm_pce=None):
		if self.king == '\u2654':
			pawn = '\u2659'
			eny_pcs = ['\u265b','\u265c','\u265d','\u265e','\u265f']
			srt_r = 1
			prm_r = 7
			dir_r = 1
			prm_pce = self.cvt_prm_pce[prm_pce][0]
		else:
			pawn = '\u265f'
			eny_pcs = ['\u2655','\u2656','\u2657','\u2658','\u2659']
			srt_r = 6
			prm_r = 0
			dir_r = -1
			prm_pce = self.cvt_prm_pce[prm_pce][1]
		if prm_pce is not None:
			if end_i != prm_r:
				return "Pawns cannot promote until they reach the final rank."
		if end_i == prm_r:
			if prm_pce is None:
				return "Pawns must promote if they reach the final rank."
		if self.board[srt_i][srt_j] == pawn:
			di = end_i-srt_i
			dj = end_j-srt_j
			if di == dir_r:
				if dj == 0:
					if self.board[end_i][end_j] == ' ':
						self.board[srt_i][srt_j] = ' '
						self.board[end_i][end_j] = pawn if end_i != prm_r else prm_pce
						if not self.is_check():
							self.set_e_p_file()
							return ""
						else:
							self.board[end_i][end_j] = ' '
							self.board[srt_i][srt_j] = pawn
							return "Pawn cannot make a move that leaves own king in check."
				elif abs(dj) == 1:
					if self.board[end_i][end_j] in eny_pcs:
						self.board[srt_i][srt_j] = ' '
						old_pce = self.board[end_i][end_j]
						self.board[end_i][end_j] = pawn if end_i != prm_r else prm_pce
						if not self.is_check():
							self.set_e_p_file()
							return ""
						else:
							self.board[end_i][end_j] = old_pce
							self.board[srt_i][srt_j] = pawn
							return "Pawn cannot make a move that leaves own king in check."
					else:
						return "Pawns cannot move forward diagonally unless they are capturing an enemy piece."
				else:
					return "Pawns can only move straight forward unless capturing, in which case they move forward diagonally one square."
			elif di == 2*dir_r:
				if srt_i == srt_r:
					if dj == 0:
						# breakpoint()
						if self.board[srt_i+dir_r][end_j] == ' ' and self.board[end_i][end_j] == ' ':
							self.board[srt_i][srt_j] = ' '
							self.board[end_i][end_j] = pawn
							if not self.is_check():
								self.set_e_p_file(end_j)
								return ""
							else:
								self.board[end_i][end_j] = ' '
								self.board[srt_i][srt_j] = pawn
								return "Pawn cannot make a move that leaves own king in check."
						else:
							return "Pawn cannot move forward if blocked by other pieces."
					else:
						return "Pawns can only change files (columns) when capturing."
				else:
					return "Pawns can only move forward two squares on their first move."
			else:
				return "Pawns can only move forward one square, unless moving two squares forward on their first move."
		else:
			return "There is no pawn on the specified starting move square."
		# valid piece move (can piece move to target square)
			# is file the same
				# is it 1 rank change
				# is it 2
					# is it on starting sq
				# accessible piece move (anything blockign piece moving to target square)
			# is file one different
				# is there enemy piece there
				# is it en passant
		# does move result in check
		# if promotion, is 7 and 8 rank
		#update en passant if successful

	def set_e_p_file(self, file=None):
		if self.king == '\u2654':
			self.white_e_p_file = float('inf') if file is None else file
		else:
			self.black_e_p_file = float('inf') if file is None else file

	def is_over(self):
		if self.is_checkmate():
			if self.turn == 'White':
				self.result = '0-1'
			else:
				self.result = '1-0'
			return True
		elif self.is_stalemate():
			self.result = '1/2-1/2'
			return True
		elif self.is_threefold_repetition():
			self.result = '1/2-1/2'
			return True
		elif self.is_fifty_move_rule():
			self.result = '1/2-1/2'
			return True
		elif self.is_dead_position():
			self.result = '1/2-1/2'
			return True
		return False

	def is_checkmate(self):
		if not self.is_check():
			return False
		else:
			if self.has_move():
				return False
			else:
				return True

	def is_stalemate(self):
		if self.is_check():
			return False
		else:
			if self.has_move():
				return False
			else:
				return True

	def is_check(self):
		if self.is_pawn_check():
			return True
		elif self.is_knight_check():
			return True
		elif self.is_bishop_check():
			return True
		elif self.is_rook_check():
			return True
		elif self.is_queen_check():
			return True
		return False


	##### is_check subroutines #####
	################################

	def is_pawn_check(self):
		if self.king == '\u2654':
			eny_pawn = '\u265f'
			d_rank = 1
		else:
			eny_pawn = '\u2659'
			d_rank = -1
		for di,dj in [(1,-1),(1,1)]:
			i = self.king_i + d_rank*di
			j = self.king_j + dj
			if i in range(8) and j in range(8):
				if self.board[i][j] == eny_pawn:
					return True
		return False

	def is_knight_check(self):
		if self.king == '\u2654':
			eny_knight = '\u265e'
		else:
			eny_knight = '\u2658'
		for di,dj in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
			i = self.king_i + di
			j = self.king_j + dj
			if i in range(8) and j in range(8):
				if self.board[i][j] == eny_knight:
					return True
		return False

	def is_rook_check(self):
		if self.king == '\u2654':
			eny_rook = '\u265c'
		else:
			eny_rook = '\u2656'
		for di,dj in [(0,1), (1,0), (-1,0), (0,-1)]:
			for d in range(7):
				i = self.king_i + di*(d+1)
				j = self.king_j + dj*(d+1)
				if i in range(8) and j in range(8):
					if self.board[i][j] == eny_rook:
						return True
					elif self.board[i][j] != ' ':
						break
				else:
					break
		return False

	def is_bishop_check(self):
		if self.king == '\u2654':
			eny_bishop = '\u265d'
		else:
			eny_bishop = '\u2657'
		for di,dj in [(1,1), (1,-1), (-1,1), (-1,-1)]:
			for d in range(7):
				i = self.king_i + di*(d+1)
				j = self.king_j + dj*(d+1)
				if i in range(8) and j in range(8):
					if self.board[i][j] == eny_bishop:
						return True
					elif self.board[i][j] != ' ':
						break
				else:
					break
		return False

	def is_queen_check(self):
		if self.king == '\u2654':
			eny_queen = '\u265b'
		else:
			eny_queen = '\u2655'
		paths = []
		for di,dj in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
			for d in range(7):
				i = self.king_i + di*(d+1)
				j = self.king_j + dj*(d+1)
				if i in range(8) and j in range(8):
					if self.board[i][j] == eny_queen:
						return True
					elif self.board[i][j] != ' ':
						break
				else:
					break
		return False

	def is_king_check(self):
		if self.king == '\u2654':
			eny_king = '\u265a'
		else:
			eny_king = '\u2654'
		for di,dj in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
			i = self.king_i + di
			j = self.king_j + dj
			if i in range(8) and j in range(8):
				if self.board[i][j] == eny_king:
					return True
		return False


	##### is_checkmate/is_stalemate subroutines #####
	#################################################

	def has_move(self):
		if self.has_king_move():
			return True
		if self.has_nonking_move():
			return True
		return False
		
	def has_king_move(self):
		if self.king == '\u2654':
			eny_pcs = ['\u265b','\u265c','\u265d','\u265e','\u265f']
		else:
			eny_pcs = ['\u2655','\u2656','\u2657','\u2658','\u2659']
		has_legal_move = False
		for di,dj in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
			i = self.king_i + di
			j = self.king_j + dj
			if i in range(8) and j in range(8):
				old_pce = self.board[i][j]
				if old_pce in eny_pcs + [' ']:
					self.board[self.king_i][self.king_j] = ' '
					self.king_i += di
					self.king_j += dj
					self.board[self.king_i][self.king_j] = self.king
					if not self.is_king_check() and not self.is_check():
						has_legal_move = True
					self.board[self.king_i][self.king_j] = old_pce
					self.king_i -= di
					self.king_j -= dj
					self.board[self.king_i][self.king_j] = self.king
					if has_legal_move:
						return True
		return False

	def has_nonking_move(self):
		if self.king == '\u2654':
			frly_pcs = ['\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			frly_pcs = ['\u265b','\u265c','\u265d','\u265e','\u265f']
		for i in range(8):
			for j in range(8):
				if self.board[i][j] in frly_pcs:
					if self.board[i][j] in ['\u2655','\u265b']:
						if self.has_queen_move(i,j):
							return True
					elif self.board[i][j] in ['\u2656','\u265c']:
						if self.has_rook_move(i,j):
							return True
					elif self.board[i][j] in ['\u2657','\u265d']:
						if self.has_bishop_move(i,j):
							return True
					elif self.board[i][j] in ['\u2658','\u265e']:
						if self.has_knight_move(i,j):
							return True
					elif self.board[i][j] in ['\u2659','\u265f']:
						if self.has_pawn_move(i,j):
							return True
		return False

	def has_queen_move(self,i,j):
		if self.king == '\u2654':
			queen = '\u2655'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			queen = '\u265b'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		has_legal_move = False
		last_in_radius = False
		for di,dj in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
			for d in range(7):
				i_ = i + di*(d+1)
				j_ = j + dj*(d+1)
				if i_ in range(8) and j_ in range(8):
					old_pce = self.board[i_][j_]
					if old_pce in frly_pcs:
						break
					if old_pce != ' ':
						last_in_radius = True
					self.board[i_][j_] = queen
					self.board[i][j] = ' '
					if not self.is_check():
						legal_move = True
					self.board[i_][j_] = old_pce
					self.board[i][j] = queen
					if has_legal_move:
						return True
					if last_in_radius:
						break
				else:
					break
		return False

	def has_rook_move(self,i,j):
		if self.king == '\u2654':
			rook = '\u2656'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			rook = '\u265c'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		has_legal_move = False
		last_in_radius = False
		for di,dj in [(1,0),(0,1),(-1,0),(0,-1)]:
			for d in range(7):
				i_ = i + di*(d+1)
				j_ = j + dj*(d+1)
				if i_ in range(8) and j_ in range(8):
					old_pce = self.board[i_][j_]
					if old_pce in frly_pcs:
						break
					if old_pce != ' ':
						last_in_radius = True
					self.board[i_][j_] = rook
					self.board[i][j] = ' '
					if not self.is_check():
						legal_move = True
					self.board[i_][j_] = old_pce
					self.board[i][j] = rook
					if has_legal_move:
						return True
					if last_in_radius:
						break
				else:
					break
		return False

	def has_bishop_move(self,i,j):
		if self.king == '\u2654':
			bishop = '\u2657'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			bishop = '\u265d'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		has_legal_move = False
		last_in_radius = False
		for di,dj in [(1,1),(-1,1),(-1,-1),(1,-1)]:
			for d in range(7):
				i_ = i + di*(d+1)
				j_ = j + dj*(d+1)
				if i_ in range(8) and j_ in range(8):
					old_pce = self.board[i_][j_]
					if old_pce in frly_pcs:
						break
					if old_pce != ' ':
						last_in_radius = True
					self.board[i_][j_] = bishop
					self.board[i][j] = ' '
					if not self.is_check():
						legal_move = True
					self.board[i_][j_] = old_pce
					self.board[i][j] = bishop
					if has_legal_move:
						return True
					if last_in_radius:
						break
				else:
					break
		return False

	def has_knight_move(self,i,j):
		if self.king == '\u2654':
			knight = '\u2658'
			frly_pcs = ['\u2654','\u2655','\u2656','\u2657','\u2658','\u2659']
		else:
			knight = '\u265e'
			frly_pcs = ['\u265a','\u265b','\u265c','\u265d','\u265e','\u265f']
		has_legal_move = False
		for di,dj in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
			i_ = i + di
			j_ = j + dj
			if i_ in range(8) and j_ in range(8):
				old_pce = self.board[i_][j_]
				if old_pce in frly_pcs:
					continue
				self.board[i_][j_] = knight
				self.board[i][j] = ' '
				if not self.is_check():
					has_legal_move = True
				self.board[i_][j_] = old_pce
				self.board[i][j] = knight
				if has_legal_move:
					return True
		return False

	def has_pawn_move(self,i,j):
		if self.king == '\u2654':
			pawn = '\u2659'
			if i == 1:
				start_sq = True
			else:
				start_sq = False
			d_rank = 1
			eny_pcs = ['\u265b','\u265c','\u265d','\u265e','\u265f']
			e_p_move = []
			if abs(self.white_e_p_file - j) == 1 and i == 4:
				e_p_move.append((1,self.white_e_p_file - j))
		else:
			pawn = '\u265f'
			if i == 6:
				start_sq = True
			else:
				start_sq = False
			d_rank = -1
			eny_pcs = ['\u2655','\u2656','\u2657','\u2658','\u2659']
			e_p_move = []
			if abs(self.black_e_p_file - j) == 1 and i == 3:
				e_p_move.append((1,self.white_e_p_file - j))
		has_legal_move = False
		for di,dj in [(1,-1),(1,1),(1,0)] + [(2,0)] if start_sq else []:
			i_ = i + di*d_rank
			j_ = j + dj
			if i_ in range(8) and j_ in range(8):
				old_pce = self.board[i_][j_]
				if dj != 0:
					if old_pce not in eny_pcs:
						continue
				else:
					if old_pce != ' ':
						break
				self.board[i_][j_] = pawn
				self.board[i][j] = ' '
				if not self.is_check():
					has_legal_move = True
				self.board[i_][j_] = old_pce
				self.board[i][j] = pawn
				if has_legal_move:
					return True
		for di,dj in e_p_move:
			self.board[i + di*d_rank][j + dj] = pawn
			eny_pawn = self.board[i][j + dj]
			self.board[i][j + dj] = ' '
			self.board[i][j] = ' '
			if not self.is_check():
				has_legal_move = True
			self.board[i + di*d_rank][j + dj] = ' '
			self.board[i][j + dj] = eny_pawn
			self.board[i][j] = pawn
			if has_legal_move:
				return True
		return False

	###############

	def is_threefold_repetition(self):
		if 3 in self.positions.values():
			return True
		return False

	#todo implement
	def is_fifty_move_rule(self):
		return False
	
	#todo implement
	def is_dead_position(self):
		return False

	def print_board(self):
		for i in range(7, -1, -1):
			print(i+1, end=" ")
			for j in range(8):
				print("'{}'".format(self.board[i][j]), end=' ')
			print('')
			# print(self.board[i])
		out = '  '
		for ltr in range(ord('a'), ord('h')+1):
			out += " {}  ".format(chr(ltr))
		print(out)


	def is_legal_move(self, move):
		if move == "0-0" or move == "0-0-0":
			return is_legal_castle(move)
		else:
			#piece not on starting square
			#piece cannot move in that direction
			#there's a piece in the way of your move
			#that move would put you into check
			pass

	def update_king_loc(self):
		i = 0
		j = 0
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == self.king:
					self.king_i = i
					self.king_j = j
					return

	def finish_move(self):
		# update positions dictionary for 3fold repetition
		board = str(self.board)
		if board in self.positions:
			self.positions[board] += 1
		else:
			self.positions[board] = 1
		if self.turn == 'White':
			self.turn = 'Black'
			self.king = '\u265a'
		else:
			self.turn = 'White'
			self.king = '\u2654'
		self.update_king_loc()

	def exit_message(self):
		winner = ""
		phrase = " has won the game"
		if self.result == "1-0":
			winner = "White"
		elif self.result == "0-1":
			winner = "Black"
		else:
			phrase = "It's a draw"
		print("{}{}! Thanks for playing.".format(winner, phrase))


if __name__ == "__main__":

	game = Game()
	game.welcome_message()

	# breakpoint()
	while not game.is_over():
		game.get_move()

	game.exit_message()



