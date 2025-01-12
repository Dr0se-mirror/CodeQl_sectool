from flask import Blueprint, request, jsonify
import os

custom_ql_bp = Blueprint('custom_ql', __name__)

QL_FOLDER = os.path.join(os.getcwd(), 'ql/java')


# 确保get_directory_structure函数正确递归获取目录结构
def get_directory_structure(path, parent_path=''):
    structure = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        relative_path = os.path.join(parent_path, item).lstrip('/')
        if os.path.isdir(item_path):
            structure.append({
                'type': 'folder',
                'name': item,
                'path': relative_path,
                'children': get_directory_structure(item_path, relative_path)
            })
        else:
            structure.append({
                'type': 'file',
                'name': item,
                'path': relative_path
            })
    return structure

@custom_ql_bp.route('/get_ql_files', methods=['GET'])
def get_ql_files():
    structure = get_directory_structure(QL_FOLDER)
    print(structure)  # 打印结构数据
    return jsonify(structure), 200

@custom_ql_bp.route('/create_new_file', methods=['POST'])
def create_new_file():
    data = request.json
    folder_path = data.get('folder')
    file_name = data.get('name')
    if not folder_path or not file_name:
        return jsonify({'error': 'Folder path or file name missing'}), 400
    full_path = os.path.join(QL_FOLDER, folder_path, file_name)
    if os.path.exists(full_path):
        return jsonify({'error': 'File already exists'}), 409
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            pass  # 创建空文件
        return jsonify({'message': 'File created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@custom_ql_bp.route('/get_ql_content', methods=['GET'])
def get_ql_content():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({'error': 'File name not provided'}), 400
    file_path = os.path.join(QL_FOLDER, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File not found'}), 404

@custom_ql_bp.route('/save_ql_file', methods=['POST'])
def save_ql_file():
    data = request.json
    file_name = data.get('file')
    content = data.get('content')
    if not file_name or not content:
        return jsonify({'error': 'File name or content missing'}), 400
    file_path = os.path.join(QL_FOLDER, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'message': 'File saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500