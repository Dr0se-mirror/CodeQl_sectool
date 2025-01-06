from flask import Blueprint, jsonify, request, send_file
import os
import csv

check_results_bp = Blueprint('check_results', __name__)

@check_results_bp.route('/choose_results', methods=['GET'])
def choose_results():
    """列出所有分析结果文件"""
    results_folder = './results/'
    if not os.path.exists(results_folder):
        return jsonify({'error': '结果文件夹不存在'}), 400
    # 只列出 CSV 文件
    results = [f for f in os.listdir(results_folder) if f.endswith('.csv')]
    return jsonify({'results': results}), 200

@check_results_bp.route('/preview_result/<filename>', methods=['GET'])
def preview_result(filename):
    """预览指定的分析结果文件内容"""
    results_folder = './results/'
    file_path = os.path.join(results_folder, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    # 定义CSV文件的字段名
    fieldnames = [
        "Vulnerability Name",
        "Description",
        "Severity",
        "Details",
        "File Path",
        "Line Number",
        "Start Column",
        "End Line",
        "End Column"
    ]
    # 读取CSV文件内容并转换为JSON
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        data = [row for row in reader]
    return jsonify(data), 200