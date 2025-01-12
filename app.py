from flask import Flask, request, send_from_directory, jsonify

from custom_ql import custom_ql_bp
from uploadCreateDatabase import upload_file, list_databases, analyze_database
from chooseAnalyzeDatabase import choose_analyze_bp  # 导入新的蓝图
from checkresults import check_results_bp  # 导入新的蓝图
import os

app = Flask(__name__)
app.register_blueprint(choose_analyze_bp)  # 注册蓝图
app.register_blueprint(check_results_bp)  # 注册蓝图
app.register_blueprint(custom_ql_bp)
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')  # 返回前端页面

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    language = request.form['language']
    return upload_file(file, language)

@app.route('/databases', methods=['GET'])
def databases():
    return {'databases': list_databases()}

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    database_name = data.get('database')
    queries_path = data.get('queries_path')
    return analyze_database(database_name, queries_path)

@app.route('/results', methods=['GET'])
def list_results():
    """列出所有分析结果文件"""
    results_folder = './results/'
    if not os.path.exists(results_folder):
        return jsonify({'error': '结果文件夹不存在'}), 400
    results = [f for f in os.listdir(results_folder) if os.path.isfile(os.path.join(results_folder, f))]
    return jsonify({'results': results}), 200

if __name__ == '__main__':
    app.run(port=5000)