#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import json
import cpca


while (1):
    try:
        address = input()
        if(address == "END"):
            break
    except EOFError:
        break
    if(address[0:2] == '1!'):             #划分等级后删除标识符
          flag = 1
          address = address.strip('1!')
    elif(address[0:2] == '2!'):
        flag = 2
        address = address.strip('2!')
    else:
        flag = 3
        address = address.strip('3!')


#获取姓名
    NAME = re.compile(r'(.*),')
    name = NAME.findall(address)

#获取手机号码
    telephone = re.compile(r'\d{11}')      #连续11位数字即是手机号码
    telephone_num = telephone.findall(address)

#获取地址
    list_address = address.split(',')      #以逗号为分隔符,将名字和剩余的信息分开
    if(len(list_address) > 1):
        address = list_address[1]
    list_address = address.split(str(telephone_num[0]))      #以电话号码为分隔符，分割该字符串中的地址信息
    address = list_address[0] + list_address[1]

#用cpca模块提取省市区信息（前三级）
    address1 = address.split()
    df = cpca.transform(address1, cut = False, lookahead = 13)        #DataFrame
    list_address = df.values[0]
    if(list_address[0][0:2] != address1[0][0:2]):
         df = cpca.transform(address, cut=False, lookahead = 13)
         list_address = df.values[0]
    ADDRESS = list_address[-1]                                        #取列表最后一个元素
    list_address = list(list_address)
    list_address.pop()
    if(list_address[0] == '北京市'or'上海市'or'天津市'or'重庆市'):
        list_address[0] = str(list_address[0]).strip('市')         #直辖市在第一级时要去掉'市'


#提取详细地址

    ADDRESS = ADDRESS.strip('.')           #去掉句号
#提取第四级
    TOWN = re.compile(r'(.*?)镇')
    town = TOWN.findall(ADDRESS)
    STREET = re.compile(r'(.*?)街道')
    street = STREET.findall(ADDRESS)
    XIANG = re.compile(r'(.*?)乡')
    xiang = XIANG.findall(ADDRESS)
    QU = re.compile(r'(.*?)开发区')
    qu = QU.findall(ADDRESS)
    coopqu = re.compile(r'(.*?)合作区')
    coop_qu = coopqu.findall(ADDRESS)



    if (len(town) != 0):
        ADDRESS = ADDRESS.split('镇')
        ADDRESS[0] += '镇'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(street) != 0):
        ADDRESS = ADDRESS.split('街道')
        ADDRESS[0] += '街道'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(xiang) != 0):
        ADDRESS = ADDRESS.split('乡')
        ADDRESS[0] += '乡'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(qu) != 0):
        ADDRESS = ADDRESS.split('开发区')
        address[0] += '开发区'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(coop_qu) != 0):
        ADDRESS = ADDRESS.split('合作区')
        ADDRESS[0] += '合作区'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    else:
        ADDRESS = ADDRESS.split()
        list_address += ADDRESS
        list_address.insert(3, '')
        ADDRESS = ADDRESS[0]

#提取第六级
    if (flag == 2):
        list_address.pop()                      #删掉最后一个元素
        road = re.search(r'(.*胡同)|(.*?弄)|(.*?大街)|(.*?巷)|(.*?[路街港道])|(.*?庭)', ADDRESS)
        if (road == None):
            list_address.insert(4, '')  # 缺失的道路位置保留空字符串
        else:
            road = road.group(0)
            road = road.split()
            list_address += road
            road = road[0]
            ADDRESS = ADDRESS.replace(road, '', 1)

#门牌号
        door_number = re.search(r'(.*?号)|(.*?弄)|(.*?[乡道])', ADDRESS)
        if (door_number == None):
            list_address.insert(5, '')              #缺失的门牌号位置保留空字符串
        else:
            door_number = door_number.group(0)
            door_number = door_number.split()
            list_address += door_number
            door_number = door_number[0]
            ADDRESS = ADDRESS.replace(door_number, '', 1)
        if (len(ADDRESS) != 0):
            ADDRESS = ADDRESS.split()
            list_address += ADDRESS
        else:
            list_address .insert(6, '')            #第七级详细信息缺失置空字符串



    result = {'姓名':name[0],'手机':telephone_num [0],'地址':list_address}
    dict = json.dumps(result, ensure_ascii=False)        #将dict转换为json
    print(dict)





