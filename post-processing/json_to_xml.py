# -*- coding: utf-8 -*-
# @Time       : 2024/1/31 12:19
# @Author     : 郭豪敏
# @FileName   : json_to_xml.py
# @Software   : PyCharm
# @Description：
import  json
from lxml import etree

# 同时记录BDD和IBD信息
def create_element(text):
    element = etree.Element(text)

    return element

with open("../DLmodel/output/test_predictions.json", "r", encoding="utf-8") as fp:
    lines = fp.readlines()

# 根据json中的内容，创建BDD的xml树结构
root = None
nodes = {}# 一个text_to_node的字典，储存每个已经建好的节点

for line in lines:
    data = json.loads(line)
    for spo in data["spo_list"]:
        # 如果导入的json文件中本身spo就有问题，需要额外处理
        if spo["subject"] == spo["object"]:
            continue
        if spo["subject"] == '' or spo["object"] == '':
            continue

        if spo["predicate"] == "定向组合" and spo["subject_type"] == "模块" and spo["object_type"] == "模块":
            # 创建第一个节点
            if root == None:
                root = create_element(spo["subject"])
                object_element = create_element(spo["object"])
                root.append(object_element)

                nodes[spo["subject"]] = root
                nodes[spo["object"]] = object_element

            # subject和object都未出现过
            elif spo["subject"] not in nodes and spo["object"] not in nodes:
                subject_element = create_element(spo["subject"])
                object_element = create_element(spo["object"])
                subject_element.append(object_element)
                root.append(subject_element)

                nodes[spo["subject"]] = subject_element
                nodes[spo["object"]] = object_element

            # subject已经出现过
            elif spo["subject"] in nodes and spo["object"] not in nodes:
                object_element = create_element(spo["object"])
                nodes[spo["subject"]].append(object_element)

                nodes[spo["object"]] = object_element

            # subject和object都已经出现过了
            else:
                continue

        # 根据连接器中的部件属性名称创建模块，并添加到BDD结构树的根节点
        elif spo["predicate"] == "连接器" and spo["subject_type"] == "部件属性" and spo["object_type"] == "部件属性":
            # subject和object都未出现过
            if spo["subject"] not in nodes and spo["object"] not in nodes:
                subject_element = create_element(spo["subject"])
                object_element = create_element(spo["object"])
                root.append(subject_element)
                root.append(object_element)

                nodes[spo["subject"]] = subject_element
                nodes[spo["object"]] = object_element

            # subject已经出现过
            elif spo["subject"] in nodes and spo["object"] not in nodes:
                object_element = create_element(spo["object"])
                root.append(object_element)

                nodes[spo["object"]] = object_element

            # object已经出现过
            elif spo["subject"] not in nodes and spo["object"] in nodes:
                subject_element = create_element(spo["subject"])
                root.append(subject_element)

                nodes[spo["subject"]] = subject_element

            else:
                continue


# 判断subject或object是否已有同样的连接关系
def to_element_node_exist(parent_node, exist_name):
    for child in parent_node.iterchildren(tag="to"):
        if child.get("element_name") == exist_name:
            return False
    else:
        return True


# 向BBD树结构中添加IBD信息，添加到子节点中
for line in lines:
    data = json.loads(line)
    for spo in data["spo_list"]:
        # 如果导入的json文件中本身spo就有问题，需要额外处理
        if spo["subject"] == spo["object"]:
            continue
        if spo["subject"] == '' or spo["object"] == '':
            continue

        if spo["predicate"] == "连接器" and spo["subject_type"] == "部件属性" and spo["object_type"] == "部件属性":
            # 判断BDD树中是否已有该连接关系
            if to_element_node_exist(nodes[spo["subject"]], spo["object"]) and to_element_node_exist(nodes[spo["object"]], spo["subject"]):
                # 判断subject和object是否为同级元素，不是同级元素暂时不做处理
                for sibling in nodes[spo["subject"]].itersiblings():
                    if sibling.tag == spo["object"]:
                        to_element = etree.Element("to")
                        to_element.set("element_name", spo["object"])
                        nodes[spo["subject"]].append(to_element)
                        break


tree = etree.ElementTree(root)
tree.write("BDD.xml", pretty_print=True, xml_declaration=True, encoding="utf-8")
