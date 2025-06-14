from flask import Flask, render_template, request
from utils import extract_sudoku_grid, recognize_digits
from solver import solve
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['sudoku']
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        try:
            grid_img = extract_sudoku_grid(path)
            board = recognize_digits(grid_img)
            original = [row.copy() for row in board]
            solve(board)
            return render_template('index.html', solved=board, original=original)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
