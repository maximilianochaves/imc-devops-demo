from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    imc = None
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = round(peso / (altura ** 2), 2)
    return render_template('index.html', imc=imc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
