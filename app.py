from flask import Flask, render_template, send_from_directory, jsonify, request
import os
from PIL import Image

app = Flask(__name__)

HEXAGON_FOLDER = "output/hexagons_set1"
ROWS = list(range(1, 20))  # r1 to r11
COLS = list(range(0, 23))  # c0 to c22



def hex_filename(r, c):
    return f"hexagon_r{r}_c{c}.png"

@app.route("/")
def index():
    dataset = request.args.get("set", "1")  # default to set1
    return render_template("index.html", dataset=dataset)


@app.route("/hex-data")
def hex_data():
    dataset = request.args.get("set", "1")
    hexagon_folder = f"output/hexagons_set{dataset}"
    HEXAGON_FOLDER = hexagon_folder
    sample_path = None
    for r in ROWS:
        for c in COLS:
            path = os.path.join(hexagon_folder, hex_filename(r, c))
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
            path = os.path.join(hexagon_folder, filename)
            if os.path.exists(path):
                x = j * hex_w + (0 if i % 2 == 1 else hex_w // 2)
                y = i * y_offset
                tiles.append({
                    "filename": f"/hexagons/{dataset}/{filename}",  # updated!
                    "x": x,
                    "y": y,
                    "width": hex_w,
                    "height": hex_h,
                    "grid_x": j,
                    "grid_y": i
                })

    return jsonify(tiles)

@app.route("/hexagons/<set_id>/<filename>")
def serve_hex_tile(set_id, filename):
    hexagon_folder = f"output/hexagons_set{set_id}"
    return send_from_directory(hexagon_folder, filename)


@app.route("/hex_visualizer")
def hex_visualizer():
    return render_template("hex_visualizer.html")

@app.route("/hex_grid_maker")
def hex_grid_maker():
    return render_template("hex_breaker_2.html")

if __name__ == "__main__":
    app.run(debug=True)