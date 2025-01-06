from flask import Blueprint, jsonify, request, send_file
import os

check_results_bp = Blueprint('check_results', __name__)

@check_results_bp.route('/choose_results', methods=['GET'])
def choose_results():
    """列出所有分析结果文件"""
    results_folder = './results/'
    if not os.path.exists(results_folder):
        return jsonify({'error': '结果文件夹不存在'}), 400
    # 只列出 CSV 文件
    results = [f for f in os.listdir(results_folder) if f.endswith('.sarif')]
    return jsonify({'results': results}), 200

@check_results_bp.route('/preview_result/<filename>', methods=['GET'])
def preview_result(filename):
    """预览指定的分析结果文件内容"""
    results_folder = './results/'
    file_path = os.path.join(results_folder, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 返回内容，设置 MIME 类型
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}