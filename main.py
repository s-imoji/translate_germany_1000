import os
from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

@app.route('/')
def index():
    """
    トップページを表示します。
    """
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    """
    フロントエンドから送られてきたテキストを翻訳するAPIエンドポイント。
    """
    try:
        # リクエストからJSONデータを取得
        data = request.get_json()
        text_to_translate = data.get('text', '')

        # 入力テキストが空の場合は、空の応答を返す
        if not text_to_translate.strip():
            # 初期状態としてドイツの国旗を表示させるため 'de' を返す
            return jsonify({'translation': '', 'source_lang': 'de'})

        # 入力言語を自動検出
        # deep-translatorは検出結果をリストで返すため、最初の要素を取得
        detected_lang_code = GoogleTranslator().detect(text_to_translate)[0]

        # サポートする言語（日本語、英語）以外は英語として扱う
        source_language = 'ja' if detected_lang_code == 'ja' else 'en'
        
        # ドイツ語に翻訳
        translated_text = GoogleTranslator(source=source_language, target='de').translate(text_to_translate)
        
        # 翻訳結果と検出した言語コードをJSONで返す
        return jsonify({
            'translation': translated_text,
            'source_lang': source_language
        })
    except Exception as e:
        print(f"Error during translation: {e}")
        # エラー発生時も空の応答を返す
        return jsonify({'translation': '翻訳中にエラーが発生しました。', 'source_lang': 'de'}), 500

if __name__ == '__main__':
    # Cloud Runが要求する環境変数PORTからポート番号を取得。
    # ローカルで実行する場合はデフォルトで8080ポートを使用。
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
    