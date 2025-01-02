from flask import jsonify
import os
import zipfile
import subprocess

UPLOAD_FOLDER = './uploads/'
EXTRACT_FOLDER = './extracted/'
DATABASE_FOLDER = './databases/'

# 确保上传、解压和数据库目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

def upload_file(file, language):
    if file.filename == '':
        return {'error': '没有选择文件'}, 400

    # 生成数据库名称，确保唯一性
    database_name = os.path.splitext(file.filename)[0] + 'database'
    database_path = os.path.join(DATABASE_FOLDER, database_name)

    # 检查数据库是否已存在
    if os.path.exists(database_path):
        return {'error': '数据库已存在'}, 400

    # 保存上传的zip文件
    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(zip_path)

    # 创建以 ZIP 文件命名的文件夹
    zip_folder_name = os.path.splitext(file.filename)[0]  # 去掉扩展名
    extract_path = os.path.join(EXTRACT_FOLDER, zip_folder_name)
    os.makedirs(extract_path, exist_ok=True)  # 创建解压文件夹

    # 解压zip文件
    print(f"正在解压文件: {file.filename} 到 {extract_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("解压完成。")

    # 调用 CodeQL 创建数据库
    command = f'codeql database create "{database_path}" --language={language} --source-root="{extract_path}"'
    print(f"正在生成数据库: {database_name}...")
    print("创建数据库命令:", command)  # 打印创建数据库命令以调试
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("数据库生成成功。")
        return {'message': '解析成功，数据库已创建', 'database_name': database_name}, 200
    except subprocess.CalledProcessError as e:
        # 解析失败，删除上传的 ZIP 文件
        cleanup(zip_path)
        error_message = f"解析失败: {e.stderr.decode()}"
        print(error_message)
        return {'error': error_message}, 400  # 返回解析错误信息

def cleanup(zip_path):
    """删除上传失败的相关文件"""
    if os.path.exists(zip_path):
        os.remove(zip_path)  # 删除上传的 ZIP 文件

def list_databases():
    databases = [d for d in os.listdir(DATABASE_FOLDER) if os.path.isdir(os.path.join(DATABASE_FOLDER, d))]
    return databases

def analyze_database(database_name, queries_path):
    database_path = os.path.join(DATABASE_FOLDER, database_name)

    if not os.path.exists(database_path):
        return {'error': '数据库不存在'}, 400

    # 调用 CodeQL 分析
    command = f'codeql database analyze "{database_path}" "{queries_path}" --format=sarif --output=results.sarif'
    print(f"正在分析数据库: {database_name}...")
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("分析成功，结果已生成。")
        return {'message': '分析成功，结果已生成'}, 200
    except subprocess.CalledProcessError as e:
        error_message = f"分析失败: {e.stderr.decode()}"
        print(error_message)
        return {'error': error_message}, 400  # 返回分析错误信息