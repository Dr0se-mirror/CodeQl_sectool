from flask import Blueprint, jsonify, request, send_file
import os
import subprocess
import glob
import time
from tqdm import tqdm  # 导入 tqdm 库

choose_analyze_bp = Blueprint('choose_analyze', __name__)

DATABASE_FOLDER = './databases/'
QL_RULES_FOLDER = './ql/java/ql/src/codeql-suites/'

@choose_analyze_bp.route('/choose_databases', methods=['GET'])
def choose_databases():
    databases_folder = './databases/'
    databases = [d for d in os.listdir(databases_folder) if os.path.isdir(os.path.join(databases_folder, d))]
    return jsonify(databases), 200

@choose_analyze_bp.route('/choose_query_suites', methods=['GET'])
def choose_query_suites():
    ql_rules_folder = './ql/java/ql/src/codeql-suites/'
    query_suites = [f for f in os.listdir(ql_rules_folder) if f.endswith('.qls')]
    return jsonify(query_suites), 200

@choose_analyze_bp.route('/analyze_database', methods=['POST'])
def analyze_database_route():
    data = request.json
    database_name = data.get('database')
    query_suite = data.get('query_suite')

    if not query_suite:
        return {'error': '未选择查询套件'}, 400

    results_folder = './results/'
    os.makedirs(results_folder, exist_ok=True)

    output_file_name = f"{database_name}_{os.path.splitext(query_suite)[0]}_代码分析结果.csv"
    output_file_path = os.path.join(results_folder, output_file_name)

    database_path = os.path.join(DATABASE_FOLDER, database_name)
    if not os.path.exists(database_path):
        return {'error': '数据库不存在'}, 400

    query_suite_path = os.path.join(QL_RULES_FOLDER, query_suite)
    if not os.path.exists(query_suite_path):
        return {'error': '查询套件文件不存在'}, 400

    start_time = time.time()

    codeql_path = os.path.expanduser("~/codeql-tools/codeql-2.13.0/codeql/codeql")
    command = f'{codeql_path} database analyze "{database_path}" "{query_suite_path}" --format=csv --output="{output_file_path}" --sarif-add-baseline-file-info'
    print(command)

    with tqdm(total=100, desc="分析进度", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pbar.update(100)
            elapsed_time = time.time() - start_time
            print(f"分析成功，结果已生成，耗时: {elapsed_time:.2f}秒")
            return {'message': '分析成功，结果已生成'}, 200
        except subprocess.CalledProcessError as e:
            error_message = f"分析失败: {e.stderr.decode()}"
            print(error_message)
            return {'error': error_message}, 400

@choose_analyze_bp.route('/download_result/<path:filename>', methods=['GET'])
def download_result(filename):
    results_folder = './results/'
    file_path = os.path.join(results_folder, filename)
    if not os.path.exists(file_path):
        return {'error': '文件不存在'}, 404
    return send_file(file_path, as_attachment=True)