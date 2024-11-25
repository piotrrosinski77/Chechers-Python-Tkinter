def calculate_ai_move(board, possible_moves):
    # minimax lub uczenie maszynowe

    return possible_moves[0] if possible_moves else None

ai_move = calculate_ai_move(self.board, self.board.get_all_possible_moves("B"))
if ai_move:
    self.process_move(ai_move, "B")