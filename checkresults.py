import os
import csv
from threading import Thread

import openai
from openai import OpenAI
import requests
from flask import Blueprint, jsonify, request, send_file
from multiprocessing import Process
check_results_bp = Blueprint('check_results', __name__)


@check_results_bp.route('/choose_results', methods=['GET'])
def choose_results():
    """列出所有分析结果文件"""
    results_folder = './results/'
    if not os.path.exists(results_folder):
        return jsonify({'error': '结果文件夹不存在'}), 400
    results = [f for f in os.listdir(results_folder) if f.endswith('.csv')]
    # 调用 ai_analyze()，但不阻塞当前请求
    Process(target=ai_analyze).start()  # 使用线程异步执行 ai_analyze()
    return jsonify({'results': results}), 200


@check_results_bp.route('/preview_result', methods=['GET'])
def preview_result():
    """预览指定的分析结果文件内容（通过查询参数）"""
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': '未提供文件名参数'}), 400
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
        "ai_analyze",
        "Start Column",
        "End Line",
        "End Column"
    ]
    # 读取CSV文件内容并转换为JSON
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        data = [row for row in reader]
    return jsonify(data), 200

@check_results_bp.route('/preview_result/<path:filename>', methods=['GET'])
def preview_result_with_filename(filename):
    """预览指定的分析结果文件内容（通过URL路径参数）"""
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
        "ai_analyze",
        "Start Column",
        "End Line",
        "End Column"
    ]
    # 读取CSV文件内容并转换为JSON
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        data = [row for row in reader]
    return jsonify(data), 200

def ai_analyze():
    """对./results/中的CSV文件进行AI分析并覆盖原文件"""

    results_folder = './results/'
    if not os.path.exists(results_folder):
        print('结果文件夹不存在')
        return
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
        "End Column",
        "ai_analyze"
    ]
    # 遍历文件夹中的所有CSV文件
    for filename in os.listdir(results_folder):
        if filename.endswith('.csv') and '已生成ai分析' not in filename:
            print("开始ai分析")
            file_path = os.path.join(results_folder, filename)
            # 读取CSV文件内容
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, fieldnames=fieldnames)
                data = [row for row in reader]
            # 跳过标题行
            if data[0]["Vulnerability Name"] == "Vulnerability Name":
                data = data[1:]
            # 处理每一行数据
            for row in data:
                vulnerability_name = row.get("Vulnerability Name", "")
                description = row.get("Description", "")
                severity = row.get("Severity", "")
                details = row.get("Details", "")
                file_path_vuln = row.get("File Path", "")
                line_number = row.get("Line Number", "")

                # 构造相对文件路径
                # 假设项目名称在文件名中，且文件名格式为"项目名称_其他信息.csv"
                project_name = filename.split('database')[0]
                
                # 尝试多种路径构建方式
                # 1. 直接使用文件路径，去掉开头的斜杠
                file_path_clean = file_path_vuln.lstrip('/')
                local_file_path = os.path.join('./extracted', project_name, file_path_clean)
                
                # 规范化路径（处理不同操作系统的路径分隔符）
                local_file_path = os.path.normpath(local_file_path)
                
                print(f"尝试读取文件: {local_file_path}")
                
                # 如果文件不存在，尝试其他路径构建方式
                if not os.path.exists(local_file_path):
                    # 2. 尝试直接在extracted/project_name下查找
                    local_file_path = os.path.join('./extracted', project_name, 'src', file_path_clean.split('src/')[-1] if 'src/' in file_path_clean else file_path_clean)
                    local_file_path = os.path.normpath(local_file_path)
                    print(f"尝试备选路径1: {local_file_path}")
                
                # 如果文件仍不存在，尝试第三种方式
                if not os.path.exists(local_file_path):
                    # 3. 尝试在extracted目录下直接查找，不使用project_name
                    local_file_path = os.path.join('./extracted', file_path_clean)
                    local_file_path = os.path.normpath(local_file_path)
                    print(f"尝试备选路径2: {local_file_path}")
                
                if os.path.exists(local_file_path):
                    try:
                        with open(local_file_path, 'r', encoding='utf-8') as code_file:
                            code_content = code_file.read()
                    except Exception as e:
                        code_content = f"读取代码文件失败: {str(e)}"
                else:
                    code_content = f"代码文件不存在: {local_file_path}"

                    # 调用DeepSeek v3 API进行分析
                    # 调用 DeepSeek API 进行分析
                try:
                    client=openai.OpenAI(api_key="sk-da0d74cd445d4e70b03dd7d02e324621", base_url="https://api.deepseek.com")
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant"},
                            {"role": "user",
                                "content": f"Analyze the following vulnerability:\n\nVulnerability Name: {vulnerability_name}\nDescription: {description}\nSeverity: {severity}\nDetails: {details}\n漏洞点位于：{line_number}\nCode Content: {code_content},使用中文进行分析回复，返回的数据绝对不使用markdown格式"},
                            ],
                        stream=False
                        )
                    print(f"prompt:\nAnalyze the following vulnerability:\n\nVulnerability Name: {vulnerability_name}\nDescription: {description}\nSeverity: {severity}\nDetails: {details}\nCode Content: {code_content},使用中文进行分析回复")
                    ai_response = response.choices[0].message.content
                    print("\n返回：\n"+ai_response)
                except Exception as e:
                    ai_response = f'API调用错误: {str(e)}'

                    # 将ai分析结果添加到数据中
                row['ai_analyze'] = ai_response
                print(ai_response)
            # 将处理后的数据写入原文件，覆盖原文件
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f'处理完成并覆盖: {filename}')

            # 修改文件名，添加 "_已生成ai分析"
            new_filename = filename.replace('.csv', '_已生成ai分析.csv')  # 在文件名后添加后缀
            new_file_path = os.path.join(results_folder, new_filename)  # 构造新文件路径
            os.rename(file_path, new_file_path)  # 重命名文件
            print(f'文件已重命名为: {new_filename}')