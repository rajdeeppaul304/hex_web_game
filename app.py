from flask import Flask, render_template, send_from_directory, jsonify
import os
from PIL import Image

app = Flask(__name__)

HEXAGON_FOLDER = "output/hexagons"
ROWS = list(range(3, 12)) 
COLS = list(range(1, 12)) 

def hex_filename(r, c):
    return f"hexagon_r{r}_c{c}.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hex-data")
def hex_data():
    sample_path = None
    for r in ROWS:
        for c in COLS:
            path = os.path.join(HEXAGON_FOLDER, hex_filename(r, c))
            if os.path.exists(path):
                sample_path = path
                break
        if sample_path:
            break

    if not sample_path:
        return jsonify({"error": "No hexagon images found"}), 500

    with Image.open(sample_path) as img:
        hex_w, hex_h = img.size

    y_offset = int(hex_h * 0.75)

    tiles = []

    for i, r in enumerate(ROWS):
        for j, c in enumerate(COLS):
            filename = hex_filename(r, c)
            path = os.path.join(HEXAGON_FOLDER, filename)
            if os.path.exists(path):
                x = j * hex_w + (0 if i % 2 == 1 else hex_w // 2)
                y = i * y_offset
                tiles.append({
                    "filename": filename,
                    "x": x,
                    "y": y,
                    "width": hex_w,
                    "height": hex_h,
                    "grid_x": j,  
                    "grid_y": i  
                })

    return jsonify(tiles)

@app.route("/hexagons/<filename>")
def serve_hex_tile(filename):
    return send_from_directory(HEXAGON_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)