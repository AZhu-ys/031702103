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
    name= NAME.findall(address)

#获取手机号码
    telephone = re.compile(r'\d{11}')      #连续11位数字即是手机号码
    telephone_num = telephone.findall(address)

#获取地址
    list_address = address.split(',')      #以逗号为分隔符分开名字和后面信息，并返回分割后列表
    if(len(list_address) == 2):
        address=list_address[1]
    list_address = list_address.split(str(telephone_num[0]))      #以电话号码为分隔符
    address = list_address[0]+list_address[1]

#用cpca模块提取省、市、区
    address1 = address.split()
    DataFrame = cpca.transform(address1,cut = False,lookahead = 12)
    listaddress = DataFrame.values[0]
    if(listaddress[0][0:2] != address1[0][0:2]):
         DataFrame = cpca.transform(address1,cut=False,lookahead = 12)
         listaddress = DataFrame.values[0]
    ADDRESS = listaddress[-1]
    listaddress = list(listaddress)
    listaddress.pop()
    if(listaddress[0] == '北京市'or'上海市'or'天津市'or'重庆市'):
        listladdress[0] = str(listaddress[0]).strip('市')         #直辖市第一级时要去掉'市'


#提取详细地址

    ADDRESS = ADDRESS.strip('.')
    TOWN = re.compile(r'(.*?)镇')
    town = TOWN.findall(ADDRESS)
    STEEET= re.compile(r'(.*?)街道')
    street = STREET.findall(ADDRESS)
    XIANG = re.compile(r'(.*?)乡')
    village = XIANG.findall(ADDRESS)
    zonepattern = re.compile(r'(.*?)开发区')
    zone = zonepattern.findall(ADDRESS)
    coozonepattern = re.compile(r'(.*?)合作区')
    coozone = coozonepattern.findall(ADDRESS)


    if (len(STREET) != 0):
        ADDRESS = ADDRESS.split('街道')
        ADDRESS[0] += '街道'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(TOWN) != 0):
        ADDRESS = ADDRESS.split('镇')
        ADDRESS[0] += '镇'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(xiang) != 0):
        ADDRESS = ADDRESS.split('乡')
        ADDRESS[0] += '乡'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    elif (len(zone) != 0):
        ADDRESS = ADDRESS.split('开发区')
        ADDRESS[0] += '开发区'
        list_address += ADDRESS
        address = address[1]
    elif (len(coozone) != 0):
        ADDRESS = ADDRESS.split('合作区')
        ADDRESS[0] += '合作区'
        list_address += ADDRESS
        ADDRESS = ADDRESS[1]
    else:
        ADDRESS = ADDRESS.split()
        list_address += ADDRESS
        list_address.insert(3, '')
        ADDRESS = ADDRESS[0]
    # 提取完第四级地址


    if (flag == 2):
        list_address.pop()
        road = re.search(r'(.*?港路)|(.*?[路街港道])|(.*胡同)|(.*?庭)|(.*?区)|(.*?里)', ADDRESS)
        if (road == None):
            list_address.insert(4, '')
        else:
            road = road.group(0)
            road = road.split()
            list_address += road
            road = road[0]
            ADDRESS = ADDRESS.replace(road, '', 1)

     #门牌号
        door_number = re.search(r'(.*?[号弄])|(.*?[乡道])', ADDRESS)
        if (door_number == None):
            list_address.insert(5, '')
        else:
            door_number = door_number.group(0)
            door_number = door_number.split()
            list_address += door_number
            door_number = door_number[0]
            ADDRESS = ADDRESS.replace(door_number, '', 1)
        if (len(address) != 0):
            ADDRESS = ADDRESS.split()
            list_address += ADDRESS
        else:
            list_address .insert(6, '')



    ANS={'姓名':name[0],'手机':telephone_num [0],'地址':list_address }
    print(json.dumps(ANS,ensure_ascii=False))





