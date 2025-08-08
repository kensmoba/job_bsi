from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from generate_labels import generate_labels
from npb import generate_npb_labels

app = Flask(__name__)
OUTPUT_FOLDER = "static"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    # Ambil nama file PDF dari query string (jika ada)
    barcode_file = request.args.get("barcode_file")
    npb_file = request.args.get("npb_file")
    return render_template("index.html", barcode_file=barcode_file, npb_file=npb_file)

@app.route("/generate-barcode", methods=["POST"])
def generate_barcode():
    start = int(request.form["start"])
    end = int(request.form["end"])
    prefix = request.form.get("prefix", "D")

    output_filename = "barcode_output.pdf"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    generate_labels(start=start, end=end, output_file=output_path, prefix=prefix)

    # Kirim ke template dalam format URL yang valid
    return redirect(url_for("index", barcode_file=f"static/{output_filename}"))


@app.route("/generate-npb", methods=["POST"])
def generate_npb():
    start = int(request.form["start"])
    end = int(request.form["end"])
    prefix = request.form.get("prefix", "B09925")

    output_filename = "npb_output.pdf"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    header_img_path = os.path.join("static", "header.png")
    generate_npb_labels(start=start, end=end, prefix=prefix, output_file=output_path, header_img_path=header_img_path)

    return redirect(url_for("index", npb_file=f"static/{output_filename}"))


if __name__ == "__main__":
    app.run(debug=True)
