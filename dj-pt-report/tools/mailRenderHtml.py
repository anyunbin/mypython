__author__ = 'yunbinan'
# coding:utf-8
import os, sys, time
from operator import itemgetter, attrgetter


def render(title, header, objs, rowcss):
    content = '<h2>' + title + '</h2>'
    content = content + '<table width="100%" align="center" border="1" cellpadding="2" cellspacing="0" bordercolor="#00BFFF">'
    #必须有statisDate属性，该属性相同的记录同色在一起
    if rowcss == 1:
        preStatisDate = ''
        preStatisColor = '<tr align="center">'
        for index, obj in enumerate(objs):
            if index % 20 == 0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>' + header[i] + '</th>'
                content = content + '</tr>'
            if objs[index].statisDate == preStatisDate:
                content = content + preStatisColor
            else:
                preStatisDate = objs[index].statisDate
                if preStatisColor == '<tr align="center" style="background:#EAF2D3">':
                    preStatisColor = '<tr align="center">'
                else:
                    preStatisColor = '<tr align="center" style="background:#EAF2D3">'
            content = content + preStatisColor
            content = content + str(obj)
            content = content + '</tr>'
    #颜色交替
    elif rowcss == 2:
        for index, obj in enumerate(objs):
            if index % 10 == 0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>' + header[i] + '</th>'
                content = content + '</tr>'
            if index % 2 == 0:
                content = content + '<tr align="center">'
            else:
                content = content + '<tr align="center" style="background:#EAF2D3">'
            content = content + str(obj)
            content = content + '</tr>'
    elif rowcss == 3:
        preBizCode = ''
        preStatisColor = '<tr align="center">'
        for index, obj in enumerate(objs):
            if index % 20 == 0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>' + header[i] + '</th>'
                content = content + '</tr>'
            if objs[index].bizCode == preBizCode:
                content = content + preStatisColor
            else:
                preBizCode = objs[index].bizCode
                if preStatisColor == '<tr align="center" style="background:#EAF2D3">':
                    preStatisColor = '<tr align="center">'
                else:
                    preStatisColor = '<tr align="center" style="background:#EAF2D3">'
            content = content + preStatisColor
            content = content + str(obj)
            content = content + '</tr>'
    elif rowcss == 4:
        preTplId = ''
        preStatisColor = '<tr align="center">'
        for index, obj in enumerate(objs):
            if index % 20 == 0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>' + header[i] + '</th>'
                content = content + '</tr>'
            if objs[index].tplId == preTplId:
                content = content + preStatisColor
            else:
                preTplId = objs[index].tplId
                if preStatisColor == '<tr align="center" style="background:#EAF2D3">':
                    preStatisColor = '<tr align="center">'
                else:
                    preStatisColor = '<tr align="center" style="background:#EAF2D3">'
            content = content + preStatisColor
            content = content + str(obj)
            content = content + '</tr>'
    content = content + '</tbody></table>'
    return content



#测试
class User:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return '<td>%s</td><td>%s</td><td>%s</td>' % (self.id, self.name, self.age)


if __name__ == '__main__':
    header = ["A", "B", "C"]
    data = list()
    data.append(User(1,'AYB',18))
    data.append(User(2,'ABC',19))
    data.append(User(3,'JNH',20))
    print render("你好", header, data, 3)
