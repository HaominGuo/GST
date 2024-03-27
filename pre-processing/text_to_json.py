# -*- coding: utf-8 -*-
# @Time       : 2024/3/8 19:27
# @Author     : 郭豪敏
# @FileName   : text_to_json.py
# @Software   : PyCharm
# @Description：
import re
import os

# 自定义分句标记，包括英文和中文标点
def sentence_tokenize(text):
    sentence_enders = re.compile('[。\!\?；，\n\r]+|[.;?!]+')
    sentence_list = sentence_enders.split(text)
    return sentence_list

#将文本文档转化为实体关系提取阶段的输入的json文档
def to_json(content):
    return f'{{"text": "{content}"}}'


# 批量对文档进行分段分句
def process_text_files(input_folder_path, output_folder_path):
    # 读取文件夹中所有的文本文档
    text_files = [file for file in os.listdir(input_folder_path) if file.endswith('.txt')]

    for text_file in text_files:
        # 提取前缀
        file_prefix, _ = os.path.splitext(text_file)
        # 创建同名的分句后的json文件
        sen_file_path = os.path.join(output_folder_path, f'{file_prefix}.json')

        # 读取每个文本文档内容
        file_path = os.path.join(input_folder_path, text_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        paragraphs = content.split('\n')
        with open(sen_file_path, 'w', encoding='utf-8') as f:
            for paragraph in paragraphs:
                if paragraph.strip():
                    sentences = sentence_tokenize(paragraph)
                    for sentence in sentences:
                        if sentence.strip():
                            f.write(to_json(sentence.strip()) + '\n')
                        else:
                            continue
                continue

        # 处理最后多余的空白行
        with open(sen_file_path, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()

def main():
    input_folder_path = '../input/' # 要处理的txt文件目录
    output_folder_path = '.'
    process_text_files(input_folder_path, output_folder_path)

if __name__ == "__main__":
    main()