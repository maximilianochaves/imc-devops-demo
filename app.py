from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de IMC</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gauge.js/1.3.7/gauge.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: #fff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        .input-group {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], button {
            padding: 12px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 10px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
        }
        .error {
            color: #e74c3c;
            text-align: center;
            margin-top: 10px;
        }
        .info {
            margin-top: 30px;
            font-size: 14px;
            color: #555;
        }
        .info ul {
            padding-left: 20px;
        }
        .gauge-container {
            width: 100%;
            height: 200px;
            margin: 30px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .gauge-labels {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 300px;
            margin-top: 10px;
            font-size: 12px;
            color: #555;
        }
        .result-details {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .result-category {
            font-size: 20px;
            margin-bottom: 10px;
        }
        .gauge-legend {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            font-size: 12px;
            margin-right: 10px;
        }
        .legend-color {
            width: 15px;
            height: 15px;
            margin-right: 5px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculadora de IMC</h1>
        <h3>Indice de Massa Corporea</h3>
        <form method="POST">
            <div class="input-group">
                <label for="peso">Peso (kg)</label>
                <input type="text" id="peso" name="peso" placeholder="Ex: 70.5" required>
            </div>
            <div class="input-group">
                <label for="altura">Altura (m)</label>
                <input type="text" id="altura" name="altura" placeholder="Ex: 1.75" required>
            </div>
            <button type="submit">Calcular IMC</button>
        </form>
        
        {% if resultado %}
        <div class="result">{{ resultado }}</div>
        
        <div class="gauge-container">
            <canvas id="gauge"></canvas>
            <div class="gauge-legend">
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #3498db;"></div>
                    <span>Abaixo do peso</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #2ecc71;"></div>
                    <span>Normal</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #f1c40f;"></div>
                    <span>Sobrepeso</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #e67e22;"></div>
                    <span>Obesidade I</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #e74c3c;"></div>
                    <span>Obesidade II</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #c0392b;"></div>
                    <span>Obesidade III</span>
                </div>
            </div>
        </div>
        
        <div class="result-details" id="resultDetails">
            <div class="result-category">{{ classificacao }}</div>
            {% if grau_obesidade %}<div>{{ grau_obesidade }}</div>{% endif %}
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const imc = {{ imc|default(0) }};
                if (imc > 0) {
                    // Configurar o medidor
                    const opts = {
                        angle: 0,
                        lineWidth: 0.3,
                        radiusScale: 1,
                        pointer: {
                            length: 0.6,
                            strokeWidth: 0.03,
                            color: '#000000'
                        },
                        limitMax: false,
                        limitMin: false,
                        colorStart: '#3498db',
                        colorStop: '#c0392b',
                        strokeColor: '#E0E0E0',
                        generateGradient: true,
                        highDpiSupport: true,
                        staticZones: [
                            {strokeStyle: "#3498db", min: 0, max: 18.5}, // Abaixo do peso
                            {strokeStyle: "#2ecc71", min: 18.5, max: 25}, // Normal
                            {strokeStyle: "#f1c40f", min: 25, max: 30}, // Sobrepeso
                            {strokeStyle: "#e67e22", min: 30, max: 35}, // Obesidade I
                            {strokeStyle: "#e74c3c", min: 35, max: 40}, // Obesidade II
                            {strokeStyle: "#c0392b", min: 40, max: 50}  // Obesidade III
                        ],
                    };

                    const target = document.getElementById('gauge');
                    const gauge = new Gauge(target).setOptions(opts);
                    gauge.maxValue = 50;
                    gauge.setMinValue(0);
                    gauge.animationSpeed = 32;
                    gauge.set(imc);
                    
                    // Ajustar cor do resultado baseado na classificação
                    const resultDetails = document.getElementById('resultDetails');
                    {% if classificacao == "Abaixo do peso" %}
                        resultDetails.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
                    {% elif classificacao == "Peso normal" %}
                        resultDetails.style.backgroundColor = 'rgba(46, 204, 113, 0.2)';
                    {% elif classificacao == "Sobrepeso" %}
                        resultDetails.style.backgroundColor = 'rgba(241, 196, 15, 0.2)';
                    {% elif classificacao == "Obesidade" and grau_obesidade == "Grau I" %}
                        resultDetails.style.backgroundColor = 'rgba(230, 126, 34, 0.2)';
                    {% elif classificacao == "Obesidade" and grau_obesidade == "Grau II" %}
                        resultDetails.style.backgroundColor = 'rgba(231, 76, 60, 0.2)';
                    {% elif classificacao == "Obesidade" and grau_obesidade == "Grau III" %}
                        resultDetails.style.backgroundColor = 'rgba(192, 57, 43, 0.2)';
                    {% endif %}
                }
            });
        </script>
        {% endif %}
        
        {% if erro %}<div class="error">{{ erro }}</div>{% endif %}
        
        <div class="info">
            <h3>Classificações de IMC:</h3>
            <ul>
                <li><strong>Abaixo de 18.5:</strong> Abaixo do peso</li>
                <li><strong>18.5 a 24.9:</strong> Peso normal</li>
                <li><strong>25.0 a 29.9:</strong> Sobrepeso</li>
                <li><strong>30.0 a 34.9:</strong> Obesidade Grau I</li>
                <li><strong>35.0 a 39.9:</strong> Obesidade Grau II</li>
                <li><strong>40.0 ou mais:</strong> Obesidade Grau III</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    classificacao = None
    grau_obesidade = None
    erro = None
    imc = None
    
    if request.method == 'POST':
        try:
            peso_str = request.form['peso'].replace(',', '.')
            altura_str = request.form['altura'].replace(',', '.')
            peso = float(peso_str)
            altura = float(altura_str)
            
            if altura <= 0 or peso <= 0:
                erro = "Peso e altura devem ser maiores que zero."
            else:
                imc = peso / (altura ** 2)
                resultado = f"Seu IMC é {imc:.2f}"
                
                if imc < 18.5:
                    classificacao = "Abaixo do peso"
                elif imc < 25:
                    classificacao = "Peso normal"
                elif imc < 30:
                    classificacao = "Sobrepeso"
                elif imc < 35:
                    classificacao = "Obesidade"
                    grau_obesidade = "Grau I"
                elif imc < 40:
                    classificacao = "Obesidade"
                    grau_obesidade = "Grau II"
                else:
                    classificacao = "Obesidade"
                    grau_obesidade = "Grau III"
        except ValueError:
            erro = "Por favor, insira valores numéricos válidos."
        except Exception as e:
            erro = f"Erro inesperado: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, 
                                  resultado=resultado, 
                                  classificacao=classificacao, 
                                  grau_obesidade=grau_obesidade, 
                                  erro=erro, 
                                  imc=imc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)