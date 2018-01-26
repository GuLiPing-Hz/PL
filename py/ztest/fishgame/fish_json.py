
import json
import os

#当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
#然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
#正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append("..")
import file_helper

def ChangePosition(src_name,out_name,isReverse=False):
    try:
        with open(src_name,"r") as file:
            routes = json.load(file)
            #print(routes,type(routes))

            route = routes[0]
            # print(route,type(route))
            # print(route["points"])
            for route in routes:
                for point in route["points"]:
                    if(isReverse):
                        point["x"] += 560
                        point["y"] += 315
                    else:
                        point["x"] -= 560
                        point["y"] -= 315

            # print(routes[0],type(routes[0]))

            with open(out_name,"w") as file2:
                json.dump(routes,file2)

    except FileNotFoundError:
        print("not find file=",src_name)
        pass


RESOURCE = "res";
PUSHCNT = 0

def printSpace4(msg):
    print("    "+msg);

def printSpace8(msg):
    print("        "+msg);

"""
    {
        "AnchorPoint": {
          "ScaleX": 1.0,
          "ScaleY": 0.5
        },
        "Position": {
          "X": -1.91,
          "Y": 65.2554
        },
        "Scale": {
          "ScaleX": 1.0,
          "ScaleY": 1.0
        },
        "RotationSkewX": 20.0,
        "RotationSkewY": 20.0,
        "CColor": {
          "G": 16,
          "B": 32
        },
        "Size": {
          "X": 0.0,
          "Y": 0.0
        },
        "VisibleForFrame": false,
        "Alpha": 200,
        "Name": "Node_1",
        "Children":[],
        "ctype": "SingleNodeObjectData"
    }
"""
def ParseCCSNodeProp(json_content,str_node,is_node = False,is_text=False,has_blend=False,no_color=False,no_size=False):
    #设置颜色混合
    if(has_blend and "BlendFunc" in json_content):
        json_blend = json_content["BlendFunc"];
        blend_src = 1 if "Src" not in json_blend else json_blend["Src"];
        blend_dst = 771 if "Dst" not in json_blend else json_blend["Dst"];
        printSpace8(str_node+".setBlendFunc("+str(blend_src)+", "+str(blend_dst)+");");

    #设置锚点
    if(not is_node and "AnchorPoint" in json_content):
        json_anchor = json_content["AnchorPoint"];
        anchor_x = 0 if "ScaleX" not in json_anchor else json_anchor["ScaleX"];
        anchor_y = 0 if "ScaleY" not in json_anchor else json_anchor["ScaleY"];
        printSpace8(str_node+".setAnchorPoint(cc.p("+str(anchor_x)+", "+str(anchor_y)+"));");

    #设置位置
    if("Position" in json_content):
        json_position = json_content["Position"];
        position_x = json_position["X"];
        position_y = json_position["Y"];

        if(position_x == 0 and position_y == 0):
            pass
        else:
            printSpace8(str_node+".setPosition(cc.p("+str(position_x)+", "+str(position_y)+"));");
    #设置缩放
    if("Scale" in json_content):
        json_scale = json_content["Scale"];
        scale_x = json_scale["ScaleX"];
        scale_y = json_scale["ScaleY"];

        if(scale_x == 1 and scale_y == 1):
            pass
        elif(scale_x == scale_y):
            printSpace8(str_node+".setScale("+str(scale_x)+");");
        else:
            printSpace8(str_node+".setScaleX("+str(scale_x)+");");
            printSpace8(str_node+".setScaleY("+str(scale_y)+");");
    #设置旋转角度
    if("RotationSkewX" in json_content):
        printSpace8(str_node+".setRotationX("+str(json_content["RotationSkewX"])+");");
        printSpace8(str_node+".setRotationY("+str(json_content["RotationSkewY"])+");");

    if(not no_color and "CColor" in json_content):
        json_color = json_content["CColor"];#设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"];
        if("G" in json_color):
            g = json_color["G"];
        if("B" in json_color):
            b = json_color["B"];

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            if(is_text):#如果是文字节点，则设置文字颜色
                printSpace8(str_node+".setTextColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));");
            else:
                printSpace8(str_node+".setColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));");

    if("VisibleForFrame" in json_content):#设置可见性
        printSpace8(str_node+".setVisible(false);");

    if("Alpha" in json_content):#设置alpha值
        printSpace8(str_node+".setOpacity("+str(json_content["Alpha"])+");");

    if(is_node or is_text):
        no_size = True;
    if(not no_size and "Size" in json_content):#设置非节点的内容大小
        json_size = json_content["Size"];
        printSpace8(str_node+".setContentSize(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"));");

    #解析子节点
    if("Children" in json_content):
        ParseCCSChildren(json_content["Children"],str_node);

def ParseCCSNode(json_content,str_parent):
    name = json_content["Name"]
    printSpace8("var "+name+" = new cc.Node();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    else:
        printSpace8("parent.addChild("+name+");");
        printSpace8(name+".setPosition(pos);");
    if(name.endswith("_use")):
        global PUSHCNT;#申明是全局变量
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");
    if(name.startswith("box_")):
        printSpace8(name+".setName('box');");

    ParseCCSNodeProp(json_content,name,True);

"""
    "FileData": {
      "Type": "Normal",
      "Path": "platform/btn_sure.png",
      "Plist": ""
    },
"""
def ParseCCSSpriteProp(json_content,name=None):
    if(not name):
        name = "FileData"
    #设置纹理
    str_sprite = json_content[name]["Path"];
    resource = "res"
    if(str_sprite.startswith("games")):
        pos_start = str_sprite.find("/")+1
        pos_end = str_sprite.find("/",pos_start)
        resource = str_sprite[pos_start:pos_end]+"Res"
    str_sprite = str_sprite[str_sprite.rfind("/")+1:];
    str_sprite = str_sprite.replace(".","_");

    return resource+"."+str_sprite;

def ParseCCSBtn(json_content,str_parent,str_node):
    printSpace8("var "+str_node+" = new ccui.Button();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+str_node+");");
    if(str_node.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+str_node+");");

    #设置按钮属性
    printSpace8(str_node+".setPressedActionEnabled(true);//--启用点击动作,只有当设置了按下的图片才有效果");
    printSpace8(str_node+".setZoomScale(-0.1);//--点击缩小,有点击就缩小，不用则置为0");
    printSpace8(str_node+".setTitleFontName(res.default_font);");
    printSpace8(str_node+".setTitleFontSize(32);");
    printSpace8(str_node+".setTitleText('');");
    printSpace8(str_node+".setTitleColor(cc.color('#ffffff'));");

    #设置纹理
    printSpace8(str_node+".loadTextureNormal("+ParseCCSSpriteProp(json_content)+", ccui.Widget.LOCAL_TEXTURE);");

def ParseCCSSprite(json_content,str_parent):
    name = json_content["Name"];

    is_btn = name.startswith("btn_");
    if(is_btn):
        ParseCCSBtn(json_content,str_parent,name);
    else:
        printSpace8("var "+name+" = new cc.Sprite();");
        if(str_parent):
            printSpace8(str_parent+".addChild("+name+");");
        if(name.endswith("_use")):
            global PUSHCNT;
            printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
            printSpace8("ret.push("+name+");");

        #设置纹理
        printSpace8(name+".initWithFile("+ParseCCSSpriteProp(json_content)+");");
    
    ParseCCSNodeProp(json_content,name,has_blend=not is_btn);

"""
    "Scale9Enable": true,
    "Scale9OriginX": 20,
    "Scale9OriginY": 18,
    "Scale9Width": 4,
    "Scale9Height": 19,
    "TouchEnable": true,
"""
def ParseCCSImage(json_content,str_parent):
    name = json_content["Name"]

    if(name.startswith("btn_")):
        ParseCCSBtn(json_content,str_parent,name);
    else:
        printSpace8("var "+name+" = new ccui.ImageView("+ParseCCSSpriteProp(json_content)+");");
        if(str_parent):
            printSpace8(str_parent+".addChild("+name+");");
        if(name.endswith("_use")):
            global PUSHCNT;
            printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
            printSpace8("ret.push("+name+");");

        #设置九宫格
        if("Scale9Enable" in json_content):
            scale9_x = 0 if("Scale9OriginX" not in json_content) else json_content["Scale9OriginX"];
            scale9_y = 0 if("Scale9OriginY" not in json_content) else json_content["Scale9OriginY"];
            printSpace8(name+".setScale9Enabled(true);");
            printSpace8(name+".setCapInsets(cc.rect("+str(scale9_x)+", "+str(scale9_y)+", 1, 1));");
        else:
            printSpace8(name+".ignoreContentAdaptWithSize(false);//图片这里需要做忽略大小设置");

        if("TouchEnable" in json_content):
            printSpace8(name+".setTouchEnabled(true);");

    ParseCCSNodeProp(json_content,name);
    
"""
    "IsCustomSize": true,
    "FontSize": 30,
    "LabelText": "2人",
    "HorizontalAlignmentType": "HT_Center",
    "VerticalAlignmentType": "VT_Center",
"""
def ParseCCSText(json_content,str_parent):
    name = json_content["Name"]
    printSpace8("var "+name+" = new ccui.Text();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    printSpace8(name+".setFontName(res.default_font);");
    if("IsCustomSize" in json_content):
        printSpace8(name+".ignoreContentAdaptWithSize(false);");

        json_size = json_content["Size"];
        printSpace8(name+".setTextAreaSize(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"));");
    if("FontSize" in json_content):
        printSpace8(name+".setFontSize("+str(json_content["FontSize"])+");");
    if("LabelText" in json_content):
        printSpace8(name+".setString("+repr(json_content["LabelText"])+");");

    if("HorizontalAlignmentType" in json_content):
        horizontal_align = json_content["HorizontalAlignmentType"];
        if(horizontal_align == "HT_Center"):
            printSpace8(name+".setTextVerticalAlignment(cc.TEXT_ALIGNMENT_CENTER);");
        elif(horizontal_align == "HT_Right"):
            printSpace8(name+".setTextVerticalAlignment(cc.TEXT_ALIGNMENT_RIGHT);");

    if("VerticalAlignmentType" in json_content):
        vertical_align = json_content["VerticalAlignmentType"];
        if(vertical_align == "VT_Center"):
            printSpace8(name+".setTextHorizontalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_CENTER);");
        elif(vertical_align == "VT_Bottom"):
            printSpace8(name+".setTextHorizontalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM);");

    if("TouchEnable" in json_content):
        printSpace8(name+".setTouchEnabled(true);");

    ParseCCSNodeProp(json_content,name,is_text = True);

"""
    "CharWidth": 18,
    "CharHeight": 22,
    "LabelText": "/123456",
    "StartChar": "/",
    "LabelAtlasFileImage_CNB": {
      "Type": "Normal",
      "Path": "platform/num_active.png",
      "Plist": ""
    },
"""
def ParseCCSTextAtlas(json_content,str_parent):
    name = json_content["Name"];

    printSpace8("var "+name+" = new ccui.TextAtlas('"+json_content["LabelText"]+"', "
        +ParseCCSSpriteProp(json_content,"LabelAtlasFileImage_CNB")
        +", "+str(json_content["CharWidth"])+", "+str(json_content["CharHeight"])
        +", '"+json_content["StartChar"]+"');");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    ParseCCSNodeProp(json_content,name,is_text = True);

"""
    "ProgressInfo": 50,
    "ImageFileData": {
      "Type": "Normal",
      "Path": "platform/shuzhitiao2.png",
      "Plist": ""
    },
"""
def ParseCCSLoadingBar(json_content,str_parent):
    name = json_content["Name"];

    printSpace8("var "+name+" = new ccui.LoadingBar("+ParseCCSSpriteProp(json_content,"ImageFileData")+", 0);");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    ParseCCSNodeProp(json_content,name);

def ParseCCSParticle(json_content,str_parent):
    name = json_content["Name"]
    printSpace8("var "+name+" = cc.ParticleSystem.create("+ParseCCSSpriteProp(json_content)+");");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");
        print(name+".stop();");

    ParseCCSNodeProp(json_content,name,is_node=True,has_blend=True);

"""
    "ClipAble": true,
    "BackColorAlpha": 0,
    "ComboBoxIndex": 1,
    "SingleColor": {
      "R": 0,
      "G": 0,
      "B": 0
    },
    "FirstColor": {
      "R": 150,
      "G": 200
    },
    "EndColor": {},
    "ColorVector": {
      "ScaleY": 1.0
    },
    "Scale9Width": 1,
    "Scale9Height": 1,
    "TouchEnable": true,
"""
def ParseCCSPanel(json_content,str_parent):
    name = json_content["Name"];
    printSpace8("var "+name+" = new ccui.Layout();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    #设定裁切
    printSpace8(name+".setClippingEnabled("+("true" if json_content["ClipAble"] else "false")+");");
    #设定点击
    if("TouchEnable" in json_content):
        printSpace8(name+".setTouchEnabled(true);");

    #设定背景图片
    bg_type = 0;
    if("ComboBoxIndex" in json_content):
        bg_type = json_content["ComboBoxIndex"];
    if(bg_type == 0):#只有图片
        if("FileData" in json_content):#检查纹理设置
            printSpace8(name+".setBackGroundImage("+ParseCCSSpriteProp(json_content)+");");

            #检查九宫格设置
            if("Scale9Enable" in json_content):
                scale9_x = 0 if("Scale9OriginX" not in json_content) else json_content["Scale9OriginX"];
                scale9_y = 0 if("Scale9OriginY" not in json_content) else json_content["Scale9OriginY"];
                printSpace8(name+".setBackGroundImageScale9Enabled(true);");
                printSpace8(name+".setBackGroundImageCapInsets(cc.rect("+str(scale9_x)+", "+str(scale9_y)+", 1, 1));");
    elif(bg_type == 1):#纯色

        json_color = json_content["SingleColor"];#设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"];
        if("G" in json_color):
            g = json_color["G"];
        if("B" in json_color):
            b = json_color["B"];

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            printSpace8(name+".setBackGroundColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));");

        if("BackColorAlpha" in json_content):
            printSpace8(name+".setBackGroundColorOpacity("+str(json_content["BackColorAlpha"])+");");
        printSpace8(name+".setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID);");
        
    else:#渐变色 不支持
        raise NotImplementedError();

    ParseCCSNodeProp(json_content,name);

"""
    "BackGroundData": {
      "Type": "Normal",
      "Path": "platform/B7.png",
      "Plist": ""
    },
    "ProgressBarData": {
      "Type": "Normal",
      "Path": "platform/B6.png",
      "Plist": ""
    },
    "BallNormalData": {
      "Type": "Normal",
      "Path": "platform/B5.png",
      "Plist": ""
    },
"""
def ParseCCSSlider(json_content,str_parent):
    name = json_content["Name"];
    printSpace8("var "+name+" = new ccui.Slider();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    printSpace8(name+".loadBarTexture("+ParseCCSSpriteProp(json_content,"BackGroundData")+");");
    printSpace8(name+".loadProgressBarTexture("+ParseCCSSpriteProp(json_content,"ProgressBarData")+");");
    printSpace8(name+".loadSlidBallTextures("+ParseCCSSpriteProp(json_content,"BallNormalData")+");");
    printSpace8(name+".setPercent(0);");

    ParseCCSNodeProp(json_content,name);

"""
    "NormalBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "PressedBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "DisableBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "NodeNormalFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_select.png",
      "Plist": ""
    },
    "NodeDisableFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_select.png",
      "Plist": ""
    },
    "TouchEnable": true,
"""
def ParseCCSCheckBox(json_content,str_parent):
    name = json_content["Name"];

    printSpace8("var "+name+" = new ccui.CheckBox("+ParseCCSSpriteProp(json_content,"NormalBackFileData")+", "
        +ParseCCSSpriteProp(json_content,"NodeNormalFileData")+");");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    ParseCCSNodeProp(json_content,name,no_size=True);

def ParseCCSTextField(json_content,str_parent,str_node):
    str_holder = json_content["PlaceHolderText"];
    printSpace8("var "+str_node+" = new ccui.TextField("+repr(str_holder)+", res.default_font, "
        +str(json_content["FontSize"])+");");
    if(str_parent):
        printSpace8(str_parent+".addChild("+str_node+");");
    if(str_node.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+str_node+");");

    json_color = json_content["CColor"];#设置颜色值
    r = 255
    g = 255
    b = 255
    if("R" in json_color):
        r = json_color["R"];
    if("G" in json_color):
        g = json_color["G"];
    if("B" in json_color):
        b = json_color["B"];

    if(r == 255 and g == 255 and b == 255):
        pass
    else:
        printSpace8(str_node+".setTextColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));");
    printSpace8(str_node+".setPlaceHolderColor(cc.color('#616161'));");
    
    printSpace8(str_node+".ignoreContentAdaptWithSize(false);");
    json_size = json_content["Size"];
    printSpace8(str_node+".setTextAreaSize(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"));");
    
    if("MaxLengthEnable" in json_content):
        printSpace8(str_node+".setMaxLengthEnabled(true);");
        printSpace8(str_node+".setMaxLength("+str(json_content["MaxLengthText"])+");");

    if("TouchEnable" in json_content):
        printSpace8(str_node+".setTouchEnabled(true);");

"""
    "FontSize": 26,
    "IsCustomSize": true,
    "LabelText": "input_png",
    "PlaceHolderText": "input_png",
    "MaxLengthEnable": true,
    "MaxLengthText": 10,
    "TouchEnable": true,
"""
def ParseCCSTextInput(json_content,str_parent):
    name = json_content["Name"];

    if(name.startswith("tf_")):
        ParseCCSTextField(json_content,str_parent,name);

    else:

        json_size = json_content["Size"];
        str_bg = json_content["PlaceHolderText"];
        printSpace8("var "+name+" = new cc.EditBox(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"), "
            +RESOURCE+"."+str_bg+");//label text的文字当作背景图片，不能为空，至少放个透明图片");
        if(str_parent):
            printSpace8(str_parent+".addChild("+name+");");
        if(name.endswith("_use")):
            global PUSHCNT;
            printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
            printSpace8("ret.push("+name+");");

        printSpace8(name+".setFontName(res.default_font);");
        printSpace8(name+".setFontSize("+str(json_content["FontSize"])+");");

        json_color = json_content["CColor"];#设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"];
        if("G" in json_color):
            g = json_color["G"];
        if("B" in json_color):
            b = json_color["B"];

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            printSpace8(name+".setFontColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));");
        printSpace8(name+".setPlaceholderFontColor(cc.color('#616161'));");

        printSpace8(name+".setInputFlag(cc.EDITBOX_INPUT_FLAG_SENSITIVE);");
        printSpace8(name+".setInputMode(cc.EDITBOX_INPUT_MODE_SINGLELINE);//单行输入");
    
        if("MaxLengthEnable" in json_content):
            printSpace8(name+".setMaxLength("+str(json_content["MaxLengthText"])+");");


    printSpace8(name+".setTextHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);//设置水平对齐");
    printSpace8(name+".setString('');");

    ParseCCSNodeProp(json_content,name,no_color=True);

"""
    "IsBounceEnabled": true,
    "InnerNodeSize": {
      "Width": 540,
      "Height": 2000
    },
    "ScrollDirectionType": "Vertical",Vertical_Horizontal
    "ClipAble": true,
    "BackColorAlpha": 0,
"""
def ParseCCSScrollView(json_content,str_parent):
    name = json_content["Name"];

    printSpace8("var "+name+" = new ccui.ScrollView();");
    if(str_parent):
        printSpace8(str_parent+".addChild("+name+");");
    if(name.endswith("_use")):
        global PUSHCNT;
        printSpace8("/**push node "+str(PUSHCNT)+" */");PUSHCNT+=1;
        printSpace8("ret.push("+name+");");

    if("IsBounceEnabled" in json_content):
        printSpace8(name+".setBounceEnabled(true);");

    direction = json_content["ScrollDirectionType"];
    if(direction == "Vertical"):
        printSpace8(name+".setDirection(cc.SCROLLVIEW_DIRECTION_VERTICAL);");
    elif(direction == "Horizontal"):
        printSpace8(name+".setDirection(cc.SCROLLVIEW_DIRECTION_HORIZONTAL);");
    else:
        printSpace8(name+".setDirection(cc.SCROLLVIEW_DIRECTION_BOTH);");

    #内部内容大小
    inner_size = json_content["InnerNodeSize"];
    printSpace8(name+".setInnerContainerSize(cc.size("+str(inner_size["Width"])+", "+str(inner_size["Height"])+"));");
    #设定裁切
    printSpace8(name+".setClippingEnabled("+("true" if json_content["ClipAble"] else "false")+");");

    ParseCCSNodeProp(json_content,name);


def ParseCCSChildren(json_children,str_parent):
    for i in range(len(json_children)):
        json_content = json_children[i];
        if(json_content["ctype"] == "SingleNodeObjectData"):
            ParseCCSNode(json_content,str_parent)
        elif(json_content["ctype"] == "SpriteObjectData"):
            ParseCCSSprite(json_content,str_parent)
        elif(json_content["ctype"] == "ImageViewObjectData"):
            ParseCCSImage(json_content,str_parent)
        elif(json_content["ctype"] == "TextObjectData"):
            ParseCCSText(json_content,str_parent)
        elif(json_content["ctype"] == "TextAtlasObjectData"):
            ParseCCSTextAtlas(json_content,str_parent)
        elif(json_content["ctype"] == "LoadingBarObjectData"):
            ParseCCSLoadingBar(json_content,str_parent)
        elif(json_content["ctype"] == "ParticleObjectData"):
            ParseCCSParticle(json_content,str_parent)
        elif(json_content["ctype"] == "PanelObjectData"):
            ParseCCSPanel(json_content,str_parent)
        elif(json_content["ctype"] == "SliderObjectData"):
            ParseCCSSlider(json_content,str_parent)
        elif(json_content["ctype"] == "CheckBoxObjectData"):
            ParseCCSCheckBox(json_content,str_parent)
        elif(json_content["ctype"] == "TextFieldObjectData"):
            ParseCCSTextInput(json_content,str_parent)
        elif(json_content["ctype"] == "ScrollViewObjectData"):
            ParseCCSScrollView(json_content,str_parent)


def ParseCCSJson(json_file):
    with open(json_file,"rb") as file:
        nodes = json.load(file);
        root = nodes["Content"]["Content"]["ObjectData"];
        # printSpace8(json_file);
        func_name = json_file[json_file.rfind("_")+1:json_file.rfind(".json")];
        func_name = "autoMakeFor"+ func_name.upper();
        printSpace4(func_name + ": function(parent, pos){");
        printSpace8("var ret = [];");
        ParseCCSNode(root,None);
        printSpace8("return ret;");
        printSpace4("},")


def JsonWalk(path,file):
    global PUSHCNT;
    PUSHCNT = 0;
    if(file.endswith(".json") and file.startswith("Node_")):
        ParseCCSJson(os.path.join(path,file))

def PrintComments():
    print("/**")
    print("This file is auto maked by python reading ccs json file!")
    print("Don't change it only the TEXT label")
    print()
    print("if you want a button, just rename the sprite/imageview name start with 'btn_'")
    print()
    print("if you want a node to be return, just rename the node name end with '_use'")
    print()
    print("if you want a loadingbar use scale9, just do :" + """
        
            ui.setScale9Enabled(true);
            ui.setCapInsets(capInset);
        
        """+" by yourself!")
    print()
    print("the default use of text input is EditBox,you can use TextField with name start with 'tf_'")
    print("*/")

def AutoParseJsonDirLobby(path):
    #解析节点json
    # ParseCCSJson("../../test/Node_yxjs.json")

    PrintComments()
    print("var AutoUiForMain = {")
    file_helper.Diskwalk(path).walk(JsonWalk)
    print("};")
    print()

def AutoParseJsonDirFish(path):
    #解析节点json
    # ParseCCSJson("../../test/Node_yxjs.json")

    PrintComments()
    print("var AutoUiForFish = {")
    file_helper.Diskwalk(path).walk(JsonWalk)
    print("};")
    print()

if __name__ == '__main__':
    #TestJson()

    #转化路径偏移
    # ChangePosition("../../test/pfishRoutes.json","../../test/pfishRoutes_new.json",False)

    #解析所有的node节点，转化成js函数

    #大厅
    AutoParseJsonDirLobby("D:\\glp\\GitHub\\fishjs\\res1\\scene_ext_ignore\\vip");

    #游戏
    # AutoParseJsonDirFish("D:\\glp\\GitHub\\fishjs\\res1\\scene_ext_ignore\\game")

