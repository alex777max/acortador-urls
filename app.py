from flask import Flask, request, redirect, jsonify
import hashlib

app = Flask(__name__)

# Diccionario para almacenar las URLs (en producción, usa una base de datos)
url_map = {}

def generar_codigo(url):
    # Genera un hash de la URL y toma los primeros 6 caracteres
    return hashlib.md5(url.encode()).hexdigest()[:6]

@app.route('/acortar', methods=['POST'])
def acortar_url():
    url_larga = request.form.get('url')
    if not url_larga:
        return jsonify({'error': 'No se proporcionó una URL'}), 400
    codigo = generar_codigo(url_larga)
    url_map[codigo] = url_larga
    url_corta = f'http://anularsegurofactura.com/{codigo}'
    return jsonify({'url_corta': url_corta})

@app.route('/<codigo>')
def redirigir(codigo):
    url_larga = url_map.get(codigo)
    if url_larga:
        return redirect(url_larga)
    else:
        return 'URL no encontrada', 404

if __name__ == '__main__':
    app.run(debug=True)