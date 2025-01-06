from flask import Blueprint, jsonify, request, send_file
import os
import subprocess
import glob
import time
from tqdm import tqdm  # 导入 tqdm 库

choose_analyze_bp = Blueprint('choose_analyze', __name__)

DATABASE_FOLDER = './databases/'
QL_RULES_FOLDER = './ql/java/ql/src/codeql-suites/'


# 路由：获取可用的数据库列表
@choose_analyze_bp.route('/choose_databases', methods=['GET'])
def choose_databases():
    """返回可用的数据库列表"""
    databases_folder = './databases/'
    # 获取数据库文件夹中的所有子文件夹
    databases = [d for d in os.listdir(databases_folder) if os.path.isdir(os.path.join(databases_folder, d))]
    return jsonify(databases), 200  # 直接返回文件夹名称列表
@choose_analyze_bp.route('/analyze_database', methods=['POST'])
def analyze_database_route():
    """分析选定的数据库"""
    data = request.json
    database_name = data.get('database')

    # 创建结果文件夹（如果不存在）
    results_folder = './results/'
    os.makedirs(results_folder, exist_ok=True)

    # 根据数据库名称构建输出文件名
    output_file_name = f"{database_name}_代码分析结果.csv"
    output_file_path = os.path.join(results_folder, output_file_name)

    database_path = os.path.join(DATABASE_FOLDER, database_name)
    if not os.path.exists(database_path):
        return {'error': '数据库不存在'}, 400

    # 获取所有 QL 规则文件
    ql_files = glob.glob(os.path.join(QL_RULES_FOLDER, 'java-code-scanning.qls'))
    if not ql_files:
        print("没有找到QL规则文件")
        return {'error': '没有找到 QL 规则文件'}, 400

    # 开始计时
    start_time = time.time()

    # 构建分析命令
    ql_files_str = ' '.join(f'"{ql_file}"' for ql_file in ql_files)
    command = f'codeql database analyze "{database_path}" {ql_files_str} --format=csv --output="{output_file_path}" --sarif-add-baseline-file-info'
    print(command)

    # 使用 tqdm 显示进度条
    with tqdm(total=100, desc="分析进度", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        try:
            # 这里可以模拟进度更新，实际分析过程可能需要根据具体情况调整
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pbar.update(100)  # 完成时更新进度条
            elapsed_time = time.time() - start_time
            print(f"分析成功，结果已生成，耗时: {elapsed_time:.2f}秒")
            return {'message': '分析成功，结果已生成'}, 200
        except subprocess.CalledProcessError as e:
            error_message = f"分析失败: {e.stderr.decode()}"
            print(error_message)
            return {'message': '代码未发现问题'}, 400  # 返回分析错误信息

# 新增路由：下载结果文件
@choose_analyze_bp.route('/download_result/<filename>', methods=['GET'])
def download_result(filename):
    """下载指定的分析结果文件"""
    results_folder = './results/'
    file_path = os.path.join(results_folder, filename)
    if not os.path.exists(file_path):
        return {'error': '文件不存在'}, 404
    return send_file(file_path, as_attachment=True)