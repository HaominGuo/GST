# -*- coding: utf-8 -*-
# @Time       : 2024/1/30 20:53
# @Author     : 郭豪敏
# @FileName   : import_xmi.py
# @Software   : PyCharm
# @Description：

from lxml import etree
import random
import numpy as np

# 命名空间映射字典
NSMAP = {
        'DSL_Customization': 'http://www.magicdraw.com/schemas/DSL_Customization.xmi',
        'Validation_Profile': 'http://www.magicdraw.com/schemas/Validation_Profile.xmi',
        'diagram': 'http://www.nomagic.com/ns/magicdraw/core/diagram/1.0',
        'Dependency_Matrix_Profile': 'http://www.magicdraw.com/schemas/Dependency_Matrix_Profile.xmi',
        'MD_Customization_for_SysML__additional_stereotypes': 'http://www.magicdraw.com/spec/Customization/180/SysML',
        'StandardProfile': 'http://www.omg.org/spec/UML/20131001/StandardProfile',
        'project': 'http://www.nomagic.com/ns/cameo/client/project/1.0',
        'UI_Prototyping_Profile': 'http://www.magicdraw.com/schemas/UI_Prototyping_Profile.xmi',
        'uml': 'http://www.omg.org/spec/UML/20131001',
        'project.options': 'http://www.nomagic.com/ns/magicdraw/core/project/options/1.0',
        'SimulationProfile': 'http://www.magicdraw.com/schemas/SimulationProfile.xmi',
        'xmi': 'http://www.omg.org/spec/XMI/20131001',
        'sysml': 'http://www.omg.org/spec/SysML/20150709/SysML',
        'ns14': 'http://www.omg.org/XMI',
        'MagicDraw_Profile': 'http://www.omg.org/spec/UML/20131001/MagicDrawProfile',
        'ns17': 'http://www.omg.org/spec/UML/20161101',
        'ns18': 'http://www.omg.org/spec/SysML/20131001/SysML',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'ns20': 'http://www.omg.org/spec/MOF/20131001',
        'ns21': 'http://www.omg.org/spec/UML/20161101/StandardProfile',
        "binary" : "http://www.nomagic.com/ns/cameo/client/binary/1.0"
    }

# 生成一个17位xmi:id
xmi_id_init = random.randint(10**16, 10**17 - 1)

# 全局唯一17位xmi:id
def generate_xmi_id():
    global xmi_id_init
    xmi_id_init += 1

    return xmi_id_init


# 设置geometry横纵坐标以及长宽
def set_geometry_coordinate_lenth_heigh(geometry_node, x, y, l, h):
    new_geometry = f"{x}, {y}, {l}, {h}"
    geometry_node.text = new_geometry


# 设置geometry两个横纵坐标，箭头到的一端坐标，和箭头来的一端坐标
def set_geometry_coordinate_to_from(geometry_node, to_x, to_y, from_x, from_y):
    new_geometry = f"{to_x}, {to_y}; {from_x}, {from_y};"
    geometry_node.text = new_geometry

# 判断节点下是否存在模块即部件属性
def exist_property(node):
    if len(node) == 0:
        return False

    for child in node:
        if child.tag != "to":
            return True
    return False


# 判断BDDxml的节点下是否存在to标签即连接器的标签
def exist_to_tag(node):
    if len(node) == 0:
        return False
    else:
        for child in node:
            if child.tag == "to":
                return True
        return False


# 判断节点下的子模块是否存在连接关系
def exist_connector(node):
    if exist_property(node) == 0:
        return False
    else:
        for child in node:
            if exist_to_tag(child) == True:
                return True
        return False
def create_element(label_name):
    element = etree.Element(label_name)

    return element


# 创建可打包元素
def create_packagedElement(xmi_type, name='', visibility='public'):
    packagedElement = etree.Element("packagedElement")

    packagedElement.set("name", name)
    packagedElement.set("visibility", visibility)
    packagedElement.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    packagedElement.set("{%s}type" % NSMAP["xmi"], xmi_type)

    return packagedElement


def create_xmi_extension():
    xmi_extension = etree.Element("{%s}Extension" % NSMAP["xmi"])
    xmi_extension.set("extender", "MagicDraw UML 2021x")

    return xmi_extension


def create_stereotype(name, stereotypeHREF):
    stereotype = etree.Element("stereotype")

    stereotype.set("name", name)
    stereotype.set("stereotypeHREF", stereotypeHREF)

    return stereotype


def create_tag(name, tagID):
    tag = etree.Element("tag")

    tag.set("name", name)
    tag.set("tagID", tagID)

    return tag


# 固定信息，导出器及版本
def create_xmi_documentation():
    xmi_documentation = etree.Element("{%s}documentation" % NSMAP["xmi"])
    exporter = etree.SubElement(xmi_documentation, 'exporter')
    exporter.text = 'MagicDraw UML'
    exporterVersion = etree.SubElement(xmi_documentation, 'exporterVersion')
    exporterVersion.text = '19.0 v9'

    return xmi_documentation


def create_ownedDiagram_bdd(name, ownerOfDiagram, visibility):
    ownedDiagram = etree.Element("ownedDiagram")
    ownedDiagram.set("context", str(ownerOfDiagram))
    ownedDiagram.set("name", name)
    ownedDiagram.set("ownerOfDiagram", str(ownerOfDiagram))
    ownedDiagram.set("visibility", visibility)
    ownedDiagram.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    ownedDiagram.set("{%s}type" % NSMAP["xmi"], "uml:Diagram")

    return ownedDiagram

def create_ownedDiagram_ibd(name, ownerOfDiagram, visibility):
    ownedDiagram = etree.Element("ownedDiagram")
    ownedDiagram.set("context", str(ownerOfDiagram))
    ownedDiagram.set("name", name)
    ownedDiagram.set("ownerDiagram", str(ownerOfDiagram))
    ownedDiagram.set("ownerOfDiagram", str(ownerOfDiagram))
    ownedDiagram.set("visibility", visibility)
    ownedDiagram.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    ownedDiagram.set("{%s}type" % NSMAP["xmi"], "uml:Diagram")

    return ownedDiagram


def create_diagramRepresentationObject(requiredFeature, type, umlType):
    create_diagramRepresentation = etree.Element("{%s}DiagramRepresentationObject" % NSMAP["diagram"])
    create_diagramRepresentation.set("requiredFeature", requiredFeature)
    create_diagramRepresentation.set("type", type)
    create_diagramRepresentation.set("umlType", umlType)

    return create_diagramRepresentation


def create_binaryObject(diagram_ID):
    binaryObject = etree.Element("binaryObject")
    binaryObject.set("streamContentID", str("BINARY-"+str(diagram_ID)))
    binaryObject.set("{%s}type" % NSMAP["xsi"], "binary:StreamIdentityBinaryObject")

    return binaryObject


def create_memberEnd(id):
    memberEnd = etree.Element("memberEnd")
    memberEnd.set("{%s}idref" % NSMAP["xmi"], str(id))

    return memberEnd


def create_ownedEnd(owningAssociation, memberEnd_from_type):
    ownedEnd = etree.Element("ownedEnd")
    ownedEnd.set("aggregation", "none")
    ownedEnd.set("isUnique", "true")
    ownedEnd.set("name", "")
    ownedEnd.set("owningAssociation", str(owningAssociation))
    ownedEnd.set("type", str(memberEnd_from_type))
    ownedEnd.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    ownedEnd.set("{%s}type" % NSMAP["xmi"], "uml:Property")

    return ownedEnd


# 创建BDD的xmi_Extension索引部分的标签
def create_xmi_Extension_of_BDD(id, name, visibility="public"):
    xmi_extension = create_xmi_extension()
    modelExtension = create_element("modelExtension")
    ownedDiagram = create_ownedDiagram_bdd(name, id, visibility)
    diagram_ID = ownedDiagram.get("{%s}id" % NSMAP["xmi"])
    xmi_extension1 = create_xmi_extension()
    diagramRepresentation = create_element("diagramRepresentation")
    diagramRepresentationObject = create_diagramRepresentationObject(
        "com.nomagic.magicdraw.plugins.impl.sysml#SysML;UML_Standard_Profile.mdzip;MD_customization_for_SysML.mdzip",
        "SysML Block Definition Diagram",
        "Class Diagram")
    diagramContents = create_element("diagramContents")
    binaryObject = create_binaryObject(diagram_ID)

    diagramContents.append(binaryObject)
    diagramRepresentationObject.append(diagramContents)
    diagramRepresentation.append(diagramRepresentationObject)
    xmi_extension1.append(diagramRepresentation)
    ownedDiagram.append(xmi_extension1)
    modelExtension.append(ownedDiagram)
    xmi_extension.append(modelExtension)

    return xmi_extension


# 创建模块下的ibd的xmi_Extension索引部分的标签
def create_xmi_Extension_of_ibd(owner_id, name, visibility="public"):
    xmi_extension = create_xmi_extension()
    modelExtension = create_element("modelExtension")
    ownedDiagram = create_ownedDiagram_ibd(name + "内部结构", owner_id, visibility)
    diagram_ID = ownedDiagram.get("{%s}id" % NSMAP["xmi"])
    xmi_extension1 = create_xmi_extension()
    diagramRepresentation = create_element("diagramRepresentation")
    diagramRepresentationObject = create_diagramRepresentationObject(
        "com.nomagic.magicdraw.plugins.impl.sysml#SysML;MD_customization_for_SysML.mdzip;UML_Standard_Profile.mdzip",
        "SysML Internal Block Diagram",
        "Composite Structure Diagram")
    diagramContents = create_element("diagramContents")
    binaryObject = create_binaryObject(diagram_ID)

    diagramContents.append(binaryObject)
    diagramRepresentationObject.append(diagramContents)
    diagramRepresentation.append(diagramRepresentationObject)
    xmi_extension1.append(diagramRepresentation)
    ownedDiagram.append(xmi_extension1)
    modelExtension.append(ownedDiagram)
    xmi_extension.append(modelExtension)

    return xmi_extension


# 构建ownAttribute标签
def create_ownAttribute(name, packagedElement_of_system, aggregation="composite", isUnique="true"):
    element = etree.Element("ownedAttribute")
    element.set("aggregation", aggregation)
    element.set("isUnique", isUnique)
    element.set("name", name)

    # 找到部件属性对应的模块的xmi：id
    xpath = f"./packagedElement[@name='{name}']"
    element_of_block = packagedElement_of_system.find(xpath)
    element.set("type", str(element_of_block.get("{%s}id" % NSMAP["xmi"])))

    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    element.set("{%s}type" % NSMAP["xmi"], "uml:Property")

    return element


# 创建ownedConnector标签
def create_ownedConnector(name=""):
    element = etree.Element("ownedConnector")
    element.set("name", name)
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    element.set("{%s}type" % NSMAP["xmi"], "uml:Connector")

    return  element


# 创建ownedConnector下的end标签
def create_ownedConnector_end(role, isUnique="true"):
    element = etree.Element("end")
    element.set("isUnique", isUnique)
    element.set("role", role)
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    element.set("{%s}type" % NSMAP["xmi"], "uml:ConnectorEnd")

    return element



# 创建sysml:block标签
def create_sysml_block(base_class_id):
    element = etree.Element("{%s}Block" % NSMAP["sysml"])
    element.set("base_Class", base_class_id)
    element.set("{%s}id" % NSMAP["xmi"], str(base_class_id)+"_application")

    return element


# 创建MD_Customization_for_SysML__additional_stereotypes:PartProperty标签
def create_MD_Customization_for_SysML__additional_stereotypes_PartProperty(base_class_id):
    element = etree.Element("{%s}PartProperty" % NSMAP["MD_Customization_for_SysML__additional_stereotypes"])
    element.set("base_Class", base_class_id)
    element.set("{%s}id" % NSMAP["xmi"], str(base_class_id)+"_application")

    return element


# 创建diagram的xmi:extension下面的filePart标签
def create_filePart(name):
    element = etree.Element("filePart")
    element.set("name", name)
    element.set("type", "XML")
    element.set("header", "<?xml version='1.0' encoding='UTF-8'?>")

    return element


# 创建描述图框信息的mdElement
def create_mdElement_diagramFrame(xmi_idref):
    element = etree.Element("mdElement")
    element.set("elementClass", "DiagramFrame")
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID = etree.SubElement(element, "elementID")
    elementID.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    geometry = etree.SubElement(element, "geometry")
    geometry.text = "12, 5, 951, 584"# 默认的图框左上角坐标、图框的大小

    compartment = etree.SubElement(element, "compartment")
    compartment.set("compartmentID", "TAGGED_VALUES")
    compartment.set("isContentLocked", "false")

    etree.SubElement(element, "mdOwnedViews")

    return element

def create_mdElement_ColorProperty(color_value_text):
    mdElement_color_property = etree.Element("mdElement")
    mdElement_color_property.set("elementClass", "ColorProperty")

    property_ID = etree.SubElement(mdElement_color_property, "propertyID")
    property_ID.text = "PEN_COLOR"

    property_description_ID = etree.SubElement(mdElement_color_property, "propertyDescriptionID")
    property_description_ID.text = "PEN_COLOR_DESCRIPTION"

    color_value = etree.SubElement(mdElement_color_property, "value")
    color_value.text = color_value_text

    etree.SubElement(mdElement_color_property, "mdOwnedViews")

    return mdElement_color_property


# 创建描述BDD图中模块信息的mdElement，xmi_idref是模块的id，不是部件属性的id
def create_mdElement_class(xmi_idref, x, y, l, h):# x横坐标，y纵坐标，l为模块图框长度，h为模块图框宽
    element = etree.Element("mdElement")
    element.set("elementClass", "Class")
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID = etree.SubElement(element, "elementID")
    elementID.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    properties = etree.SubElement(element, "properties")

    properties.append(create_mdElement_ColorProperty("-5399163"))

    geometry = etree.SubElement(element, "geometry")
    set_geometry_coordinate_lenth_heigh(geometry, x, y, l, h)

    compartment = etree.SubElement(element, "compartment")
    compartment.set("compartmentID", "TAGGED_VALUES")
    compartment.set("isContentLocked", "false")

    etree.SubElement(element, "mdOwnedViews")

    return element

# 创建描述IBD图中部件属性part模块信息的mdElement，xmi_idref是前面uml:model下的packagedElement下的ownedAttribute的id
def create_mdElement_part(xmi_idref, x, y, l, h):# x横坐标，y纵坐标，l为模块图框长度，h为模块图框宽
    element = etree.Element("mdElement")
    element.set("elementClass", "Part")
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID = etree.SubElement(element, "elementID")
    elementID.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    properties = etree.SubElement(element, "properties")

    properties.append(create_mdElement_ColorProperty("-6055837"))

    geometry = etree.SubElement(element, "geometry")
    set_geometry_coordinate_lenth_heigh(geometry, x, y, l, h)

    compartment = etree.SubElement(element, "compartment")
    compartment.set("compartmentID", "TAGGED_VALUES")
    compartment.set("isContentLocked", "false")

    etree.SubElement(element, "mdOwnedViews")

    return element


# 创建choiceProperty这个mdElement
def create_md_element_choice_property(propertyID_text, propertyDescriptionID_text, value_text, choice_text, index_text):
    mdElement_choice_property = etree.Element("mdElement")
    mdElement_choice_property.set("elementClass", "ChoiceProperty")

    propertyID = etree.SubElement(mdElement_choice_property, "propertyID")
    propertyID.text = propertyID_text

    propertyDescriptionID = etree.SubElement(mdElement_choice_property, "propertyDescriptionID")
    propertyDescriptionID.text = propertyDescriptionID_text

    value = etree.SubElement(mdElement_choice_property, "value")
    value.text = value_text

    choice = etree.SubElement(mdElement_choice_property, "choice")
    choice.text = choice_text

    index = etree.SubElement(mdElement_choice_property, "index")
    index.text = index_text

    etree.SubElement(mdElement_choice_property, "mdOwnedViews")

    return mdElement_choice_property

# 创建BooleanProperty这个mdElement
def create_mdElement_BooleanProperty(propertyID_text, propertyDescriptionID_text):
    mdElement_choice_property = etree.Element("mdElement")
    mdElement_choice_property.set("elementClass", "BooleanProperty")

    propertyID = etree.SubElement(mdElement_choice_property, "propertyID")
    propertyID.text = propertyID_text

    propertyDescriptionID = etree.SubElement(mdElement_choice_property, "propertyDescriptionID")
    propertyDescriptionID.text = propertyDescriptionID_text

    etree.SubElement(mdElement_choice_property, "mdOwnedViews")

    return mdElement_choice_property

# 创建compartment标签
def create_compartment_tag(compartmentID, isContentLocked):
    compartment = etree.Element("compartment")
    compartment.set("compartmentID", compartmentID)
    compartment.set("isContentLocked", isContentLocked)

    return compartment

# 创建mdOwnedViews下的elementClass为Role的mdElement, to的那端，
def create_mdElement_role_to(xmi_idref, x, y):
    mdElement_role = etree.Element("mdElement")
    mdElement_role.set("elementClass", "Role")
    mdElement_role.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID_memberEnd_to = etree.SubElement(mdElement_role, "elementID")
    elementID_memberEnd_to.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    properties = etree.SubElement(mdElement_role, "properties")

    properties.append(create_md_element_choice_property("STEREOTYPES_DISPLAY_MODE",
                                                        "STEREOTYPES_DISPLAY_MODE_DESCRIPTION",
                                                        "STEREOTYPE_DISPLAY_MODE_DO_NOT_DISPLAY_STEREOTYPES",
                                                        "STEREOTYPE_DISPLAY_MODE_TEXT_AND_ICON^STEREOTYPE_DISPLAY_MODE_TEXT^STEREOTYPE_DISPLAY_MODE_ICON^STEREOTYPE_DISPLAY_MODE_DO_NOT_DISPLAY_STEREOTYPES",
                                                        "3"))
    properties.append(create_mdElement_BooleanProperty("SHOW_ROLE_MULTIPLICITY",
                                                       "SHOW_ROLE_MULTIPLICITY_DESCRIPTION"))

    geometry = etree.SubElement(mdElement_role, "geometry")
    set_geometry_coordinate_lenth_heigh(geometry, x, y, 10, 10)

    mdElement_role.append(create_compartment_tag("TAGGED_VALUES",
                                                 "false"))

    etree.SubElement(mdElement_role, "mdOwnedViews")

    return mdElement_role

# 创建mdOwnedViews下的elementClass为Role的mdElement, from的那端
def create_mdElement_role_from(xmi_idref, x, y):
    mdElement_role = etree.Element("mdElement")
    mdElement_role.set("elementClass", "Role")
    mdElement_role.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID_memberEnd_to = etree.SubElement(mdElement_role, "elementID")
    elementID_memberEnd_to.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    properties = etree.SubElement(mdElement_role, "properties")

    properties.append(create_mdElement_BooleanProperty("SHOW_ROLE_NAME",
                                                       "SHOW_ROLE_NAME_DESCRIPTION"))
    properties.append(create_mdElement_BooleanProperty("SHOW_ROLE_MULTIPLICITY",
                                                       "SHOW_ROLE_MULTIPLICITY_DESCRIPTION"))

    geometry = etree.SubElement(mdElement_role, "geometry")
    set_geometry_coordinate_lenth_heigh(geometry, x, y, 10, 10)

    mdElement_role.append(create_compartment_tag("TAGGED_VALUES",
                                                 "false"))

    etree.SubElement(mdElement_role, "mdOwnedViews")

    return mdElement_role

# 创建描述定向组合关系的mdElement
# xmi_idref是前面创建的模型中的这个定向组合关系的ID，linkFirstEnd_ID, linkSecondEnd_ID是前面刚创建的MD中模块图元素的ID，to_x, to_y, from_x, from_y是连线的两端坐标
# xmi_idref_memberEnd_to, xmi_idref_memberEnd_from是前面uml:model里面创建的定向组合关联两端的ID
def create_mdElement_association(xmi_idref, linkFirstEnd_ID, linkSecondEnd_ID, to_x, to_y, from_x, from_y, xmi_idref_memberEnd_to, xmi_idref_memberEnd_from):
    element = etree.Element("mdElement")
    element.set("elementClass", "Association")
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID = etree.SubElement(element, "elementID")
    elementID.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    #创建连接线的properties
    properties = etree.SubElement(element, "properties")
    mdElement_choice_property = create_md_element_choice_property("LINK_LINE_STYLE",
                                                                  "LINK_LINE_STYLE_DESCRIPTION",
                                                                  "RECTILINEAR",
                                                                  "RECTILINEAR^OBLIQUE^BEZIER",
                                                                  "0")
    properties.append(mdElement_choice_property)

    linkFirstEndID = etree.SubElement(element, "linkFirstEndID")
    linkFirstEndID.set("{%s}idref" % NSMAP["xmi"], linkFirstEnd_ID)

    linkSecondEndID = etree.SubElement(element, "linkSecondEndID")
    linkSecondEndID.set("{%s}idref" % NSMAP["xmi"], linkSecondEnd_ID)

    # 连线的两端坐标（不包含折线，全部都用直线连接，从from到to，从上到下连接）
    geometry = etree.SubElement(element, "geometry")
    set_geometry_coordinate_to_from(geometry, to_x, to_y, from_x, from_y)

    element.append(create_compartment_tag("TAGGED_VALUES", "false"))
    element.append(create_compartment_tag("CONVEYED_INFORMATION_A", "true"))
    element.append(create_compartment_tag("CONVEYED_INFORMATION_B", "true"))

    nameVisible = etree.SubElement(element, "nameVisible")
    nameVisible.set("{%s}value" % NSMAP["xmi"], "true")

    # 计算连线两端小方块的坐标
    mdElement_role_to_x = to_x - 5
    mdElement_role_to_y = to_y - 10
    mdElement_role_from_x = from_x - 10
    mdElement_role_from_y = from_y - 5

    # 创建mdOwnedViews标签，即是连接线两端的两个小方块
    mdOwnedViews = etree.SubElement(element, "mdOwnedViews")
    mdElement_role_to = create_mdElement_role_to(xmi_idref_memberEnd_to, mdElement_role_to_x, mdElement_role_to_y)
    mdElement_role_from = create_mdElement_role_from(xmi_idref_memberEnd_from, mdElement_role_from_x, mdElement_role_from_y)
    mdElement_role_to_ID = mdElement_role_to.get("{%s}id" % NSMAP["xmi"])
    mdElement_role_from_ID = mdElement_role_from.get("{%s}id" % NSMAP["xmi"])
    mdOwnedViews.append(mdElement_role_to)
    mdOwnedViews.append(mdElement_role_from)

    associationFirstEndID = etree.SubElement(element, "associationFirstEndID")
    associationFirstEndID.set("{%s}idref" % NSMAP["xmi"], mdElement_role_to_ID)

    associationSecondEndID = etree.SubElement(element, "associationSecondEndID")
    associationSecondEndID.set("{%s}idref" % NSMAP["xmi"], mdElement_role_from_ID)

    return element

# 创建mdOwnedViews下的elementClass为ConnectorEnd的mdElement, 连接线两端的小方块，是一样的
def create_mdElement_ConnectorEnd(xmi_idref, x, y):
    mdElement_ConnectorEnd = etree.Element("mdElement")
    mdElement_ConnectorEnd.set("elementClass", "ConnectorEnd")
    mdElement_ConnectorEnd.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID_memberEnd_to = etree.SubElement(mdElement_ConnectorEnd, "elementID")
    elementID_memberEnd_to.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    properties = etree.SubElement(mdElement_ConnectorEnd, "properties")

    properties.append(create_mdElement_ColorProperty("-5399163"))

    geometry = etree.SubElement(mdElement_ConnectorEnd, "geometry")
    set_geometry_coordinate_lenth_heigh(geometry, x, y, 14, 14)

    mdElement_ConnectorEnd.append(create_compartment_tag("TAGGED_VALUES",
                                                 "false"))

    etree.SubElement(mdElement_ConnectorEnd, "mdOwnedViews")

    return mdElement_ConnectorEnd


# 创建描述连接器connector关系的mdElement
# xmi_idref是前面创建的模型中的这个连接器关系的ID，linkFirstEnd_ID, linkSecondEnd_ID是前面刚创建的MD中部件属性图元素的ID，to_x, to_y, from_x, from_y是连线的两端坐标
# xmi_idref_end_to, xmi_idref_end_from是前面uml:model里面创建的ownedConnector关联两端end的ID
def create_mdElement_connector(xmi_idref, linkFirstEnd_ID, linkSecondEnd_ID, to_x, to_y, from_x, from_y, xmi_idref_end_to, xmi_idref_end_from):
    element = etree.Element("mdElement")
    element.set("elementClass", "Connector")
    element.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))

    elementID = etree.SubElement(element, "elementID")
    elementID.set("{%s}idref" % NSMAP["xmi"], xmi_idref)

    #创建连接线的properties
    properties = etree.SubElement(element, "properties")
    mdElement_choice_property = create_md_element_choice_property("LINK_LINE_STYLE",
                                                                  "LINK_LINE_STYLE_DESCRIPTION",
                                                                  "RECTILINEAR",
                                                                  "RECTILINEAR^OBLIQUE^BEZIER",
                                                                  "0")
    properties.append(mdElement_choice_property)

    linkFirstEndID = etree.SubElement(element, "linkFirstEndID")
    linkFirstEndID.set("{%s}idref" % NSMAP["xmi"], linkFirstEnd_ID)

    linkSecondEndID = etree.SubElement(element, "linkSecondEndID")
    linkSecondEndID.set("{%s}idref" % NSMAP["xmi"], linkSecondEnd_ID)

    # 连线的两端坐标（不包含折线，全部都用直线连接，从from到to）
    geometry = etree.SubElement(element, "geometry")
    set_geometry_coordinate_to_from(geometry, to_x, to_y, from_x, from_y)

    element.append(create_compartment_tag("TAGGED_VALUES", "false"))
    element.append(create_compartment_tag("CONVEYED_INFORMATION_A", "true"))
    element.append(create_compartment_tag("CONVEYED_INFORMATION_B", "true"))

    nameVisible = etree.SubElement(element, "nameVisible")
    nameVisible.set("{%s}value" % NSMAP["xmi"], "true")

    # 计算连线两端小方块的坐标
    # mdElement_role_to_x = to_x - 5
    # mdElement_role_to_y = to_y - 10
    # mdElement_role_from_x = from_x - 10
    # mdElement_role_from_y = from_y - 5

    # 创建mdOwnedViews标签，即是连接线两端的两个小方块
    mdOwnedViews = etree.SubElement(element, "mdOwnedViews")
    mdElement_ConnectorEnd_to = create_mdElement_ConnectorEnd(xmi_idref_end_to, to_x, to_y)
    mdElement_ConnectorEnd_from = create_mdElement_ConnectorEnd(xmi_idref_end_from, from_x, from_y)
    mdOwnedViews.append(mdElement_ConnectorEnd_to)
    mdOwnedViews.append(mdElement_ConnectorEnd_from)

    mdElement_ConnectorEnd_to_ID = mdElement_ConnectorEnd_to.get("{%s}id" % NSMAP["xmi"])
    mdElement_ConnectorEnd_from_ID = mdElement_ConnectorEnd_from.get("{%s}id" % NSMAP["xmi"])

    associationFirstEndID = etree.SubElement(element, "associationFirstEndID")
    associationFirstEndID.set("{%s}idref" % NSMAP["xmi"], mdElement_ConnectorEnd_to_ID)

    associationSecondEndID = etree.SubElement(element, "associationSecondEndID")
    associationSecondEndID.set("{%s}idref" % NSMAP["xmi"], mdElement_ConnectorEnd_from_ID)

    return element

# 递归创建class并添加到XMI结构中，max_x_dict用来记录当前图中最右边的坐标，用dict可以在函数内部修改函数外部的值，以辅助创建模块的x坐标，row用来创建模块的y坐标
# 模块之间上下间隔50，左右间隔50，模块初始坐标为（50，50），模块初始长宽分别为100、50
def add_mdElement_class(mdOwnedViews, packageElement_of_system, packagedElement_root, max_x_dict, row, interval_x=50, interval_y=50, block_l=100, block_h=50):
    packagedElement_root_id = packagedElement_root.get("{%s}id" % NSMAP["xmi"])

    class_x = max_x_dict["max_x"] + interval_x
    class_y = 50 + row * (interval_y + block_h)
    mdElement_class = create_mdElement_class(packagedElement_root_id, class_x, class_y, block_l, block_h)
    mdOwnedViews.append(mdElement_class)

    # 到树叶节点更新max_x_dict
    if len(packagedElement_root) == 0: # 没有子节点
        current_x = class_x + block_l
        if current_x > max_x_dict["max_x"]:
            max_x_dict["max_x"] = current_x
        return

    for child in packagedElement_root:
        if child.tag == "ownedAttribute":
            ownedAttribute_type = child.get("type")
            packagedElement_block = packageElement_of_system.find(f"./packagedElement[@xmi:id = '{ownedAttribute_type}']", namespaces=NSMAP)
            add_mdElement_class(mdOwnedViews, packageElement_of_system, packagedElement_block, max_x_dict, row + 1)

# 确定连线上端的端点, 端点在模块的下方中间
def get_from_xy(mdElement):
    geometry_node = mdElement.find("./geometry")
    geometry_text = geometry_node.text
    values = geometry_text.split(",")
    coordinates = list(map(int, values))
    x, y, l, h = coordinates

    lower_bound_x = x
    upper_bound_x = x + l
    lower_bound_y = y
    upper_bound_y = y + h

    from_x = random.randint(lower_bound_x, upper_bound_x)
    from_y = random.randint(lower_bound_y, upper_bound_y)

    return from_x, from_y

# 确定连线下端的端点，端点在模块的上方中间
def get_to_xy(mdElement):
    geometry_node = mdElement.find("./geometry")
    geometry_text = geometry_node.text
    values = geometry_text.split(",")
    coordinates = list(map(int, values))
    x, y, l, h = coordinates

    # to_x = x + int(l/2)
    # to_y = y

    lower_bound_x = x
    upper_bound_x = x + l
    lower_bound_y = y
    upper_bound_y = y + h

    to_x = random.randint(lower_bound_x, upper_bound_x)
    to_y = random.randint(lower_bound_y, upper_bound_y)

    return to_x, to_y


# 根据uml:model中的定向组合关系创建extension中的定向组合关系，并添加到XMI结构中
def add_mdElement_association(mdOwnedViews, packageElement_of_system):
    target_nodes = packageElement_of_system.findall("./packagedElement[@xmi:type = 'uml:Association']", namespaces=NSMAP)
    for node in target_nodes:
        xmi_idref = node.get("{%s}id" % NSMAP["xmi"])

        member_ends = node.findall('memberEnd')
        xmi_idref_memberEnd_to = member_ends[0].get("{%s}idref" % NSMAP["xmi"])
        xmi_idref_memberEnd_from = member_ends[1].get("{%s}idref" % NSMAP["xmi"])

        ownedAttribute_to = packageElement_of_system.find(f".//ownedAttribute[@xmi:id = '{xmi_idref_memberEnd_to}']", namespaces=NSMAP)
        ownedAttribute_to_type = ownedAttribute_to.get("type")
        linkFirstEnd_elementID = mdOwnedViews.find(f"./mdElement/elementID[@xmi:idref = '{ownedAttribute_to_type}']", namespaces=NSMAP)
        linkFirstEnd = linkFirstEnd_elementID.find('..')
        linkFirstEnd_ID = linkFirstEnd.get("{%s}id" % NSMAP["xmi"])

        ownedEnd = node.find("ownedEnd")
        ownedEnd_type = ownedEnd.get("type")
        linkSecondEnd_elementID = mdOwnedViews.find(f"./mdElement/elementID[@xmi:idref = '{ownedEnd_type}']", namespaces=NSMAP)
        linkSecondEnd = linkSecondEnd_elementID.find('..')
        linkSecondEnd_ID = linkSecondEnd.get("{%s}id" % NSMAP["xmi"])

        from_x, from_y = get_from_xy(linkSecondEnd)
        to_x, to_y = get_to_xy(linkFirstEnd)

        mdElement_association = create_mdElement_association(xmi_idref, linkFirstEnd_ID, linkSecondEnd_ID, to_x, to_y, from_x, from_y, xmi_idref_memberEnd_to, xmi_idref_memberEnd_from)
        mdOwnedViews.append(mdElement_association)


# 递归把BBDxml中的所有模块添加到左边导航栏系统架构下面
def process_bddxml_addblock(node, packageElement_of_system):
    element = create_packagedElement("uml:Class", str(node.tag))
    packageElement_of_system.append(element)


    if exist_property(node)  == 0:
        return

    for child in node:
        if child.tag != "to":
            process_bddxml_addblock(child, packageElement_of_system)


# 创建模块下面的部件属性
def create_part_property_of_block(node, element_of_node, packagedElement_of_system):
    if exist_property(node) == 0:
        return

    for child in node:
        if child.tag != "to":
            ownAttribute = create_ownAttribute(str(child.tag), packagedElement_of_system)
            element_of_node.append(ownAttribute)

            name = str(child.tag)
            element_of_child = packagedElement_of_system.find(f"./packagedElement[@name='{name}']")
            create_part_property_of_block(child, element_of_child, packagedElement_of_system)


# 递归创建所有含有子模块即部件属性的模块下的IBD标签索引，具体IBD图信息在后面的extension
def add_ibd_extension_to_block(node, element_of_node, packagedElement_of_system):
    # 节点下面没有模块不用创建ibd
    if exist_property(node) == 0:
        return

    name = str(node.tag)
    id = element_of_node.get("{%s}id" % NSMAP["xmi"])
    element_of_node.append(create_xmi_Extension_of_ibd(id, name))

    for child in node:
        if child.tag != "to":
            child_name = str(child.tag)
            element_of_child = packagedElement_of_system.find(f"./packagedElement[@name='{child_name}']")
            add_ibd_extension_to_block(child, element_of_child, packagedElement_of_system)


# 根据BDDxml中的连接器信息创建模块下的连接器
def add_connector_to_block(node, element_of_node, packagedElement_of_system):
    if exist_connector(node) == False:
        return

    for child in node:
        if exist_to_tag(child) == True:
            for subchild in child:
                if subchild.tag == "to":
                    child_name = str(child.tag)
                    element_of_end1 = element_of_node.find(f"./ownedAttribute[@name='{child_name}']")
                    end1_id = element_of_end1.get("{%s}id" % NSMAP["xmi"])

                    subchild_name = subchild.get("element_name")
                    element_of_end2 = element_of_node.find(f"./ownedAttribute[@name='{subchild_name}']")
                    end2_id = element_of_end2.get("{%s}id" % NSMAP["xmi"])

                    ownedConnector = create_ownedConnector()
                    connector_end1 = create_ownedConnector_end(end1_id)
                    connector_end2 = create_ownedConnector_end(end2_id)

                    ownedConnector.append(connector_end1)
                    ownedConnector.append(connector_end2)
                    element_of_node.append(ownedConnector)

    for child in node:
        if child.tag != "to":
            child_name = str(child.tag)
            element_of_child = packagedElement_of_system.find(f"./packagedElement[@name='{child_name}']")
            add_connector_to_block(child, element_of_child, packagedElement_of_system)


# 创建定向组合关系(在XMI中也是一个可打包元素）, memberEnd_to_id是部件属性的id，memberEnd_from_id是新建的id，
def create_composite_association(memberEnd_to_id, memberEnd_from_type_id):
    packageElement = create_packagedElement("uml:Association")
    packageElement_id = packageElement.get("{%s}id" % NSMAP["xmi"])

    memberEnd_to = create_memberEnd(memberEnd_to_id)

    # 定向组合关系拥有端的信息，type是所属block的id，xmi_id是对应部件属性的id，相当于新建了一个部件属性
    ownedEnd = create_ownedEnd(packageElement_id, memberEnd_from_type_id)
    memberEnd_from_id = ownedEnd.get("{%s}id" % NSMAP["xmi"])

    memberEnd_from = create_memberEnd(memberEnd_from_id)

    packageElement.append(memberEnd_to)
    packageElement.append(memberEnd_from)
    packageElement.append(ownedEnd)

    return packageElement


# 递归的把BDDxml中的定向组合关系创建并添加到“系统架构”包下面
def add_composite_association(node, element_of_node, packagedElement_of_system):
    if exist_property(node) == 0:
        return

    for child in node:
        if child.tag != "to":
            child_name = str(child.tag)
            memberEnd_to = element_of_node.find(f"./ownedAttribute[@name='{child_name}']")
            memberEnd_to_id = memberEnd_to.get("{%s}id" % NSMAP["xmi"])

            node_name = str(node.tag)
            memberEnd_from_type = packagedElement_of_system.find(f"./packagedElement[@name='{node_name}']")
            memberEnd_from_type_id = memberEnd_from_type.get("{%s}id" % NSMAP["xmi"])

            packagedElement_of_composite_association = create_composite_association(memberEnd_to_id, memberEnd_from_type_id)

            packagedElement_of_system.append(packagedElement_of_composite_association)

    for child in node:
        if child.tag != "to":
            child_name = str(child.tag)
            element_of_child = packagedElement_of_system.find(f"./packagedElement[@name='{child_name}']")
            add_composite_association(child, element_of_child, packagedElement_of_system)


# M-Design左边导航栏的层级结构，“模型”是导航栏根节点
def create_uml_model(model_name, BDDxml_path):
    uml_model = etree.Element("{%s}Model" % NSMAP["uml"])

    uml_model.set("name", model_name)
    uml_model.set("{%s}id" % NSMAP["xmi"], str(generate_xmi_id()))
    uml_model.set("{%s}type" % NSMAP["xmi"], "uml:Model")

    # uml:model下的系统架构包，包含整个系统架构BDD图以及各大模块及其内部IBD图
    packagedElement_of_system = create_packagedElement("uml:Package", "系统架构")
    uml_model.append(packagedElement_of_system)
    system_id = packagedElement_of_system.get("{%s}id" % NSMAP["xmi"])

    # BDD图导航链接，具体图信息在后面的extension中
    modelExtension_of_bdd = create_xmi_Extension_of_BDD(id=system_id, name="总体架构")
    packagedElement_of_system.append(modelExtension_of_bdd)

    # 读取根据json生成的BDD图xml树结构信息并构造模块,必须要先完整构造所有模块，后面需要用到模块的id
    tree = etree.parse(BDDxml_path)
    root = tree.getroot()
    process_bddxml_addblock(root, packagedElement_of_system)

    # 生成模块下的部件属性
    root_name = str(root.tag)
    element_of_root = packagedElement_of_system.find(f"./packagedElement[@name='{root_name}']")
    create_part_property_of_block(root, element_of_root, packagedElement_of_system)

    # 生成模块下的IBD导航链接
    add_ibd_extension_to_block(root, element_of_root, packagedElement_of_system)

    # 生成模块下的Connector部分
    add_connector_to_block(root, element_of_root, packagedElement_of_system)

    # 生成模块下的定向组合部分
    add_composite_association(root, element_of_root, packagedElement_of_system)

    return uml_model


# 描述构造型的extension，root子节点第一个extension
def create_xmi_Extension1_of_stereotype():
    xmi_extension = create_xmi_extension()
    stereotypesHREFS = create_element("stereotypesHREFS")
    stereotype_Magic_Draw_Profile_DiagramInfo = create_stereotype("MagicDraw_Profile:DiagramInfo",
                                                                  "#_9_0_be00301_1108044380615_150487_0")
    stereotype_sysml_Block = create_stereotype("sysml:Block", "#_11_5EAPbeta_be00301_1147424179914_458922_958")
    tag_sysml_Block_isEncapsulated = create_tag("sysml:Block:isEncapsulated",
                                                "_11_5EAPbeta_be00301_1147424201876_860708_1049")
    tag_sysml_Block_usedAsType = create_tag("sysml:Block:usedAsType", "SysML.Block.usedAsType")
    stereotype_PartProperty = create_stereotype("MD_Customization_for_SysML__additional_stereotypes:PartProperty",
                                                "#_15_0_be00301_1199377756297_348405_2678")

    stereotypesHREFS.append(stereotype_Magic_Draw_Profile_DiagramInfo)
    stereotypesHREFS.append(stereotype_sysml_Block)
    stereotypesHREFS.append(tag_sysml_Block_isEncapsulated)
    stereotypesHREFS.append(tag_sysml_Block_usedAsType)
    stereotypesHREFS.append(stereotype_PartProperty)
    xmi_extension.append(stereotypesHREFS)

    return xmi_extension


# 创建uml:model同级后续的一系列的sysml:Block和MD_Customization_for_SysML__additional_stereotypes:PartProperty
def create_block_partproperty(root):
    target_nodes = root.xpath('./uml:Model/packagedElement/packagedElement[@xmi:type="uml:Class"]', namespaces=NSMAP)

    # 创建sysml:block
    for node in target_nodes:
        xmi_id = node.get("{%s}id" % NSMAP["xmi"])
        root.append(create_sysml_block(xmi_id))

        # 每个block下面还要判断并创建MD_Customization_for_SysML__additional_stereotypes:PartProperty
        own_attribute_nodes = node.findall("ownedAttribute")
        if own_attribute_nodes is not None:
            for subnode in own_attribute_nodes:
                own_attr_xmi_id = subnode.get("{%s}id" % NSMAP["xmi"])
                root.append(create_MD_Customization_for_SysML__additional_stereotypes_PartProperty(own_attr_xmi_id))


# 创建描述MD中BDD图详细信息的xmi:extension
def create_xmi_extension_of_BDDdiagram(root):
    packagedElement_of_system = root.find('./uml:Model/packagedElement', namespaces=NSMAP)# 找到“系统架构”这个包
    system_BDDdiagram = packagedElement_of_system.find('./xmi:Extension/modelExtension/ownedDiagram', namespaces=NSMAP)

    xmi_extension = etree.Element("{%s}Extension" % NSMAP["xmi"])

    BDD_xmi_id = system_BDDdiagram.get("{%s}id" % NSMAP["xmi"])
    filePart = create_filePart("BINARY-"+str(BDD_xmi_id))

    md_owned_views = etree.Element("mdOwnedViews")

    mdElement_diagramFrame = create_mdElement_diagramFrame(BDD_xmi_id)# 添加图框图元素

    md_owned_views.append(mdElement_diagramFrame)

    packagedElement = packagedElement_of_system.find('./packagedElement')# 匹配第一个packagedElement即BDD图的根节点模块
    max_x_dict = {"max_x" : 0}
    row = 0
    add_mdElement_class(md_owned_views, packagedElement_of_system, packagedElement, max_x_dict, row)# 添加所有的block图元素

    add_mdElement_association(md_owned_views, packagedElement_of_system) # 添加所有的定向组合图元素

    filePart.append(md_owned_views)
    xmi_extension.append(filePart)

    return xmi_extension

# 创建描述MD中IBD图详细信息的xmi:extension
def create_xmi_extension_of_IBDdiagram(root):
    ownedDiagrams = root.findall("./uml:Model/packagedElement//ownedDiagram[@xmi:type='uml:Diagram']", namespaces=NSMAP)
    for ownedDiagram in ownedDiagrams:
        DiagramRepresentationObject = ownedDiagram.find("./xmi:Extension/diagramRepresentation/diagram:DiagramRepresentationObject", namespaces=NSMAP)
        diagram_type = DiagramRepresentationObject.get("type")
        if diagram_type == "SysML Internal Block Diagram":
            xmi_extension = etree.Element("{%s}Extension" % NSMAP["xmi"])
            root.append(xmi_extension)

            ibd_ID = ownedDiagram.get("{%s}id" % NSMAP["xmi"])
            filePart = create_filePart("BINARY-" + str(ibd_ID))
            xmi_extension.append(filePart)

            md_owned_views = etree.Element("mdOwnedViews")
            filePart.append(md_owned_views)

            # 添加图框图元素
            mdElement_diagramFrame = create_mdElement_diagramFrame(ibd_ID)
            md_owned_views.append(mdElement_diagramFrame)

            ownerOfDiagram_id = ownedDiagram.get("ownerOfDiagram")
            ownerOfDiagram_packagedElement = root.find(f"./uml:Model/packagedElement/packagedElement[@xmi:id = '{ownerOfDiagram_id}']", namespaces=NSMAP)

            # 创建所有的部件属性图元素
            ownedAttribute_nodes = ownerOfDiagram_packagedElement.findall("./ownedAttribute")
            for ownedAttribute_node in ownedAttribute_nodes:
                ownedAttribute_node_xmi_id = ownedAttribute_node.get("{%s}id" % NSMAP["xmi"])

                # 定义一个区域随机生成部件属性的坐标，大小可设置
                lower_bound_x = 30
                lower_bound_y = 50
                upper_bound_x = 900
                upper_bound_y = 550
                part_x = int(np.random.uniform(lower_bound_x, upper_bound_x))
                part_y = int(np.random.uniform(lower_bound_y, upper_bound_y))

                mdElement_part = create_mdElement_part(ownedAttribute_node_xmi_id, part_x, part_y, 157, 38)
                md_owned_views.append(mdElement_part)

            # 创建部件属性之间连接器的图元素
            ownedConnector_nodes = ownerOfDiagram_packagedElement.findall("./ownedConnector")
            for ownedConnector_node in ownedConnector_nodes:
                ownedConnector_node_xmi_id = ownedConnector_node.get("{%s}id" % NSMAP["xmi"])

                ownedConnector_endA, ownedConnector_endB = ownedConnector_node.findall("./end")
                ownedConnector_endA_role = ownedConnector_endA.get("role")
                ownedConnector_endB_role = ownedConnector_endB.get("role")
                ownedConnector_endA_xmi_id = ownedConnector_endA.get("{%s}id" % NSMAP["xmi"])
                ownedConnector_endB_xmi_id = ownedConnector_endB.get("{%s}id" % NSMAP["xmi"])

                mdElement_partA_elementID = md_owned_views.find(f"./mdElement/elementID[@xmi:idref = '{ownedConnector_endA_role}']", namespaces=NSMAP)
                mdElement_partA = mdElement_partA_elementID.find("..")
                mdElement_partB_elementID = md_owned_views.find(f"./mdElement/elementID[@xmi:idref = '{ownedConnector_endB_role}']", namespaces=NSMAP)
                mdElement_partB = mdElement_partB_elementID.find("..")

                linkFirstEndID = mdElement_partA.get("{%s}id" % NSMAP["xmi"])
                linkSecondEndID = mdElement_partB.get("{%s}id" % NSMAP["xmi"])

                to_x, to_y = get_to_xy(mdElement_partA)
                from_x, from_y = get_from_xy(mdElement_partB)

                mdElement_Connector = create_mdElement_connector(ownedConnector_node_xmi_id, linkFirstEndID, linkSecondEndID, to_x, to_y, from_x, from_y, ownedConnector_endA_xmi_id, ownedConnector_endB_xmi_id)

                md_owned_views.append(mdElement_Connector)

def main():
    # xmi根节点
    root = etree.Element("{%s}XMI" % NSMAP["xmi"], nsmap=NSMAP)

    root.append(create_xmi_documentation())  # 固定信息，导出器及版本
    root.append(create_uml_model("Model", "./BDD.xml")) # M-Design左边导航栏的层级结构，“模型”是导航栏根节点，“BDD.XML”是由json生成的BDD结构树
    root.append(create_xmi_Extension1_of_stereotype())  # 描述构造型导航信息的extension，root下子节点第一个extension
    create_block_partproperty(root)# 创建uml:model同级后续的一系列的sysml:Block和MD_Customization_for_SysML__additional_stereotypes:PartProperty
    root.append(create_xmi_extension_of_BDDdiagram(root))# 创建描述MD中BDD图详细信息的xmi:extension
    create_xmi_extension_of_IBDdiagram(root)# 创建所有的IBD图详细信息的xmi:extension

    tree = etree.ElementTree(root)
    tree.write('../output/import_MD.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')

    print('-'*20)
    print("generated output successfully!")


if __name__ == "__main__":
    main()