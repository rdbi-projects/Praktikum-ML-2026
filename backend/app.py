import os
import joblib
import pickle
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# TODO  Inisialisasi aplikasi Flask


CORS(app)

# TODO Konfigurasi nama dan path file model machine learning


# Variabel global untuk menyimpan model Decision Tree di memori
tree_model = None



def load_model():
    global tree_model
    
    # TODO load model
    

    return tree_model


# Memuat model saat server pertama kali dijalankan
load_model()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "service": "Iris Decision Tree Classification API",
        "model_loaded": tree_model is not None,
        "model_file": MODEL_FILENAME
    })

@app.route('/predict', methods=['POST'])
def predict():
    global tree_model

    # Pastikan model sudah termuat di memori
    if tree_model is None:
        tree_model = load_model()
        if tree_model is None:
            return jsonify({
                "success": False,
                "error": f"Model '{MODEL_FILENAME}' belum berhasil dimuat. Pastikan file model ada di folder backend."
            }), 500

    try:
        # TODO ambil data dari json
        data = request.get_json(silent=True)
        

        # TODO ambil nilai fitur dari json
        

        # memastikan semua fitur terisi
        if any(v is None or str(v).strip() == '' for v in [sepal_length_raw, sepal_width_raw, petal_length_raw, petal_width_raw]):
            return jsonify({
                "success": False,
                "error": "Semua fitur harus diisi: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm"
            }), 400


        # TODO konversi nilai ke float

        # memastikan tidak ada nilai fitur yang negatif
        if any(val < 0 for val in [SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm]):
            return jsonify({
                "success": False,
                "error": "Nilai ukuran tidak boleh bernilai negatif."
            }), 400

        

        # TODO pembuatan DataFrame dan pemanggilan model.predict()
        

        # menghitung probabilitas prediksi
        probabilities = []
        if hasattr(tree_model, 'predict_proba') and hasattr(tree_model, 'classes_'):
            try:
                proba_arr = tree_model.predict_proba(input_data)[0]
                classes = list(tree_model.classes_)
                for cls, p in zip(classes, proba_arr):
                    cls_str = str(cls)
                    norm_label = cls_str if cls_str.startswith("Iris-") else f"Iris-{cls_str}"
                    probabilities.append({
                        "species": norm_label,
                        "percentage": round(float(p) * 100, 1)
                    })
                probabilities.sort(key=lambda x: x["percentage"], reverse=True)
            except Exception as e_proba:
                print(f"[WARN] Gagal menghitung probabilitas: {e_proba}")

        # TODO return respons jsonify

        
        return jsonify({"success": False, "error": "Fungsi prediksi belum dilengkapi."}), 501

    except ValueError as ve:
        return jsonify({
            "success": False,
            "error": f"Format input angka tidak valid: {str(ve)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Terjadi kesalahan saat memproses prediksi: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Server Flask berjalan di http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)