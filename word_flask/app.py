import os
import socket
from docx import Document
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # 导入 CORS 模块
from werkzeug.utils import secure_filename
import unicodedata
import openai  # 导入 OpenAI 包

# 在此填入您的 OpenAI API 密钥
openai.api_key = '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'

app = Flask(__name__)
CORS(app)  # 启用 CORS
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'docx', 'doc'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', title=None, directories=None, content=None)


@app.route('/get_all_contents', methods=['POST'])
def get_all_contents():
    """上传文件"""
    files = request.files.getlist('file')
    print(files)
    if 'file' not in request.files:
        return jsonify(error='No file part')

    file = request.files['file']
    print(file.filename)
    if file.filename == '':
        return jsonify(error='No selected file')

    if file and allowed_file(file.filename):
        # 清理并规范化文件名
        filename = secure_filename(file.filename)
        filename_normalized = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')

        # 构建文件路径
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename_normalized)

        file.save(file_path)

        # 获取文件内容
        # print(file_path)
        content = read_file_content(file_path)
        markdown_result = analyze_document(content)
        print('===============================================')
        print(markdown_result['content'])
        # 将文件内容传递给 get_file_content 函数
        return jsonify(markdown_result)


def read_file_content(file_path):
    """
    读取文档内容
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def analyze_document(document):
    # 定义您要进行分析的文档数据
    prompt = f"分析以下文档内容,只对正文内容分析，\n{document}\n\n### ，分析出的结果需要生成 Markdown 格式文本，格式以“#”为父节点，“##”为“#”的子节点，“###”为“##”的子节点，以此类推，生成的结果树不能出现遗漏情况，也就是每行必须含有至少一个#"
    # 调用GPT模型生成Markdown格式的分析结果
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "{}".format(prompt)}
        ]
    )

    # 获取生成的Markdown格式结果
    markdown_result = response.choices[0].message

    return markdown_result


if __name__ == '__main__':
    # 设置超时时间为 300 秒
    socket.setdefaulttimeout(300)
    app.run(debug=True, threaded=True, processes=1)
