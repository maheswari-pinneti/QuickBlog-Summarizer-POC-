import logging
import time 
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from summarizer import BlogSummarizer
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from deep_translator import GoogleTranslator
from model_utils import get_model

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

LANGUAGE_MODEL_MAP = {
    'en': 'facebook/bart-large-cnn',
    'multilingual': 'facebook/mbart-large-50-many-to-many-mmt',
    'mT5': 'google/mt5-small',
}

def get_model(language=None, model_name=None):
    if language:
        return LANGUAGE_MODEL_MAP.get(language, LANGUAGE_MODEL_MAP['multilingual'])
    return model_name or LANGUAGE_MODEL_MAP['en']

@app.route('/summarize', methods=['POST'])
@limiter.limit("5 per minute")
def summarize():
    data = request.get_json()
    url = data.get('url')
    max_length = data.get('max_length', 130)
    min_length = data.get('min_length', 30)
    model_name = get_model(data.get('language'), data.get('model_name'))

    if not url:
        logging.warning('No URL provided.')
        return jsonify({'error': 'No URL provided.'}), 400

    try:
        logging.info(f'Request: {url}, model={model_name}')
        temp_summarizer = BlogSummarizer(model_name=model_name)

        extracted_text = temp_summarizer.extract_text(url)
        summary = temp_summarizer.summarize(extracted_text, max_length=max_length, min_length=min_length)

        return jsonify({
            'summary': summary
        })

    except ValueError as ve:
        logging.error(f'ValueError: {ve}')
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.exception('Unexpected error')
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@app.route('/summarize/pdf', methods=['POST'])
@limiter.limit("5 per minute")
def summarize_pdf():
    data = request.get_json()
    url = data.get('url')
    max_length = data.get('max_length', 130)
    min_length = data.get('min_length', 30)
    translated_text = data.get('translated_summary')  # Optional

    model_name = get_model(data.get('language'), data.get('model_name'))

    if not url:
        logging.warning('No URL provided.')
        return jsonify({'error': 'No URL provided.'}), 400

    try:
        temp_summarizer = BlogSummarizer(model_name=model_name)
        summary = temp_summarizer.summarize_url(url, max_length=max_length, min_length=min_length)

        # Start creating PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40

        # Title
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, y, "📰 Blog Summary (English)")
        y -= 30
        p.setFont("Helvetica", 11)

        # English summary
        for line in summary.split('. '):
            if y < 40:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica", 11)
            p.drawString(40, y, line.strip())
            y -= 18

        # Optional Translated summary
        if translated_text:
            if y < 80:
                p.showPage()
                y = height - 40

            y -= 20
            p.setFont("Helvetica-Bold", 14)
            p.drawString(40, y, "🌍 Translated Summary")
            y -= 30
            p.setFont("Helvetica", 11)

            for line in translated_text.split('. '):
                if y < 40:
                    p.showPage()
                    y = height - 40
                    p.setFont("Helvetica", 11)
                p.drawString(40, y, line.strip())
                y -= 18

        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="summary.pdf", mimetype='application/pdf')

    except ValueError as ve:
        logging.error(f'ValueError: {ve}')
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.exception('Unexpected error')
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Backend is running.'})


@app.route('/translate', methods=['POST'])
def translate_summary():
    data = request.get_json()
    text = data.get('text')
    target_lang = data.get('target_lang')

    if not text or not target_lang:
        return jsonify({'error': 'Missing text or target language'}), 400

    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        logging.error(f'Translation error: {e}')
        return jsonify({'error': 'Translation failed'}), 500


if __name__ == '__main__':
    app.run(debug=True)
