from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# contoh endpoint POST
@app.route("/generate-barcode", methods=["POST"])
def generate_barcode():
    # logika kamu di sini
    return "Barcode PDF generated!"

# jika kamu pakai NPB juga
@app.route("/generate-npb", methods=["POST"])
def generate_npb():
    # logika kamu di sini
    return "NPB PDF generated!"

# penting agar bisa dipanggil Vercel
def handler(event, context):
    from mangum import Mangum
    asgi_app = Mangum(app)
    return asgi_app(event, context)
