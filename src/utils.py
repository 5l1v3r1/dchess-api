import chess
import chess.pgn
import chess.svg
import cairosvg
import berserk
import io


class ChessUtil:

    def __init__(self, token):
        session = berserk.TokenSession(token)
        self.client = berserk.Client(session=session)

    def get_svg_from_id(self, id: str, move_count: int):
        match_pgn = self.client.games.export(game_id=id, as_pgn=True, clocks=False)
        #print(match_pgn)
        m_counter = 0
        game = chess.pgn.read_game(io.StringIO(match_pgn))
        board = game.board()
        check = None
        if move_count >= 1:
            for move in game.mainline_moves():
                board.push(move)
                m_counter += 1
                if m_counter >= move_count:
                    break
        if board.is_check():
            check = board.king(board.turn)
        return chess.svg.board(board=board, check=check, coordinates=False)

    def svg_to_png(self, svg_data):
        file_obj = None
        try:
            file_obj = cairosvg.svg2png(bytestring=svg_data, output_width=512, output_height=512)
        except Exception as e:
            print(e)
            return None
        return io.BytesIO(file_obj)

    def get_game_data(self, id:str):
        return self.client.games.export(game_id=id)

    def get_image_from_id(self, id, move):
        svg = self.get_svg_from_id(id, move_count=move)
        return self.svg_to_png(svg)