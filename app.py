from flask import Flask, request, send_from_directory
from uploadCreateDatabase import upload_file, list_databases, analyze_database
from chooseAnalyzeDatabase import choose_analyze_bp  # 导入新的蓝图

app = Flask(__name__)
app.register_blueprint(choose_analyze_bp)  # 注册蓝图

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

if __name__ == '__main__':
    app.run(port=3000)