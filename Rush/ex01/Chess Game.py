class ChessPiece:
    def __init__(self, name, color):
        # กำหนดชื่อและสีของตัวหมาก
        self.name = name  # ชื่อของตัวหมาก เช่น 'K' สำหรับ King, 'Q' สำหรับ Queen
        self.color = color  # สีของตัวหมาก เช่น 'W' สำหรับ White, 'B' สำหรับ Black

    def __str__(self):
        # คืนค่าสตริงที่ประกอบด้วยตัวอักษรแรกของสีและชื่อของตัวหมาก
        return f"{self.color[0]}{self.name}"  # เช่น 'WK' สำหรับ White King, 'BQ' สำหรับ Black Queen

class ChessBoard:
    def __init__(self):
        # สร้างกระดานหมากรุกและกำหนดให้เริ่มต้นด้วยฝั่งสีขาว
        self.board = self.create_board()  # สร้างกระดานหมากรุก
        self.turn = 'W'  # เริ่มต้นด้วยฝั่งสีขาว

    def create_board(self):
        # สร้างกระดานขนาด 8x8 ที่เต็มไปด้วยช่องว่าง
        board = [[' ' for _ in range(8)] for _ in range(8)]
        # กำหนดลำดับของตัวหมากในแถวแรกและแถวสุดท้าย
        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i in range(8):
            # วางตัวหมากสีดำในแถวแรก
            board[0][i] = ChessPiece(pieces[i], 'B')
            # วางเบี้ยสีดำในแถวที่สอง
            board[1][i] = ChessPiece('P', 'B')
            # วางเบี้ยสีขาวในแถวที่เจ็ด
            board[6][i] = ChessPiece('P', 'W')
            # วางตัวหมากสีขาวในแถวสุดท้าย
            board[7][i] = ChessPiece(pieces[i], 'W')
        return board  # คืนค่ากระดานหมากรุกที่สร้างเสร็จแล้ว

    def print_board(self):
        # พิมพ์กระดานหมากรุกออกมา
        for i, row in enumerate(self.board):
            # พิมพ์แถวของกระดานพร้อมตัวหมาก
            print(f"{8-i} " + ' '.join(str(piece).ljust(2) if piece != ' ' else '. ' for piece in row))
        # พิมพ์ท้ายกระดาน
        print("  a  b  c  d  e  f  g  h")

    def move_piece(self, start, end):
        # แปลงตำแหน่งเริ่มต้นจากรูปแบบตัวอักษรและตัวเลขเป็นพิกัดในกระดาน
        start_x, start_y = self.convert_position(start)
        # แปลงตำแหน่งปลายทางจากรูปแบบตัวอักษรและตัวเลขเป็นพิกัดในกระดาน
        end_x, end_y = self.convert_position(end)
        # ดึงตัวหมากจากตำแหน่งเริ่มต้น
        piece = self.board[start_x][start_y]
        if piece == ' ':
            # ถ้าไม่มีตัวหมากที่ตำแหน่งเริ่มต้น ให้พิมพ์ข้อความแจ้งเตือน
            print("No piece at start position!")
            return
        if self.board[end_x][end_y] != ' ' and self.board[end_x][end_y].color == piece.color:
            # ถ้ามีตัวหมากของฝั่งเดียวกันที่ตำแหน่งปลายทาง ให้พิมพ์ข้อความแจ้งเตือน
            print("Cannot capture your own piece!")
            return
        # ย้ายตัวหมากไปยังตำแหน่งปลายทาง
        self.board[end_x][end_y] = piece
        # ลบตัวหมากจากตำแหน่งเริ่มต้น
        self.board[start_x][start_y] = ' '
        # กำหนดสีของฝั่งตรงข้าม
        opponent_color = 'B' if piece.color == 'W' else 'W'
        if self.is_in_check(opponent_color):
            # ถ้าฝั่งตรงข้ามถูกเช็ค ให้พิมพ์ข้อความแจ้งเตือน
            print(f"{opponent_color} King is in check by {piece.color}{piece.name} at {end}!!!")
        # สลับฝั่งที่เดินหมาก
        self.turn = '------------Black' if self.turn == 'W' else 'W'
        # พิมพ์ข้อความแจ้งเตือนว่าฝั่งไหนเป็นฝั่งที่ต้องเดินหมาก
        print(f"{self.turn} Turn------------")

    def convert_position(self, pos):
        # แปลงตัวอักษรเป็นตัวเลข
        letters_to_numbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        # แปลงแถวจากตัวเลขในรูปแบบกระดานหมากรุกเป็นพิกัดในกระดาน
        row = 8 - int(pos[1])
        # แปลงคอลัมน์จากตัวอักษรเป็นตัวเลข
        col = letters_to_numbers[pos[0]]
        return row, col  # คืนค่าพิกัดในกระดาน

    def find_king(self, color):
        # ค้นหาตำแหน่งของ King ตามสีที่กำหนด
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != ' ' and piece.name == 'K' and piece.color == color:
                    return i, j  # คืนค่าตำแหน่งของ King
        return None

    def is_in_check(self, color):
        # ตรวจสอบว่า King ของสีที่กำหนดถูกเช็คหรือไม่
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        king_x, king_y = king_pos
        opponent_color = 'W' if color == 'B' else 'B'
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != ' ' and piece.color == opponent_color:
                    if self.can_attack(i, j, king_x, king_y):
                        return True  # คืนค่า True ถ้า King ถูกเช็ค
        return False

    def can_attack(self, start_x, start_y, end_x, end_y):
        # ตรวจสอบว่าตัวหมากสามารถโจมตีตำแหน่งที่กำหนดได้หรือไม่
        piece = self.board[start_x][start_y]
        if piece.name == 'P':
            # ตรวจสอบการเคลื่อนที่ของเบี้ย
            direction = 1 if piece.color == 'W' else -1
            if start_x + direction == end_x and abs(start_y - end_y) == 1:
                return True
        elif piece.name == 'R':
            # ตรวจสอบการเคลื่อนที่ของเรือ
            if start_x == end_x or start_y == end_y:
                return True
        elif piece.name == 'N':
            # ตรวจสอบการเคลื่อนที่ของม้า
            if abs(start_x - end_x) == 2 and abs(start_y - end_y) == 1 or abs(start_x - end_x) == 1 and abs(start_y - end_y) == 2:
                return True
        elif piece.name == 'B':
            # ตรวจสอบการเคลื่อนที่ของบิชอป
            if abs(start_x - end_x) == abs(start_y - end_y):
                return True
        elif piece.name == 'Q':
            # ตรวจสอบการเคลื่อนที่ของควีน
            if start_x == end_x or start_y == end_y or abs(start_x - end_x) == abs(start_y - end_y):
                return True
        elif piece.name == 'K':
            # ตรวจสอบการเคลื่อนที่ของคิง
            if abs(start_x - end_x) <= 1 and abs(start_y - end_y) <= 1:
                return True
        return False

def main():
    # สร้างกระดานหมากรุกและพิมพ์กระดาน
    board = ChessBoard()
    board.print_board()
    print("------------White Turn------------")  # เริ่มต้นด้วยฝั่งสีขาว

    while True:
        # รับตำแหน่งเริ่มต้นและตำแหน่งปลายทางจากผู้ใช้
        start = input("Enter the start position: ")
        end = input("Enter the end position: ")
        # ย้ายตัวหมากและพิมพ์กระดานใหม่
        board.move_piece(start, end)
        board.print_board()



if __name__ == "__main__":
    main()