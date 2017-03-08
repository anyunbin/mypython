#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,datetime
mydir = sys.path[0]
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append(mydir+"/tools/")
import sendMail
import MySQLdb
from operator import itemgetter, attrgetter
       #------------------------------------------------------ start  tools ---------------------------------------------------------------#
def render(title,header,objs,rowcss):
    content = '<h2>'+title+'</h2>'
    content = content + '<table width="100%" align="center" border="1" cellpadding="2" cellspacing="0" bordercolor="#00BFFF">'
    if rowcss == 1:
        preStatisDate = ''
        preStatisColor = '<tr align="center">'
        for index,obj in enumerate(objs):
            if index%20==0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>'+header[i]+'</th>'
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
    elif rowcss == 2:
        for index,obj in enumerate(objs):
            if index%10==0:
                content = content + '<tr style="background:#00BFFF">'
                for i in range(len(header)):
                    content = content + '<th>'+header[i]+'</th>'
                content = content + '</tr>'
            if index%2==0:
                content = content + '<tr align="center">'
            else:
                content = content + '<tr align="center" style="background:#EAF2D3">'
            content = content + str(obj)
            content = content + '</tr>'
    content = content + '</tbody></table>'
    return content
       #------------------------------------------------------ end  tools ---------------------------------------------------------------#
       #------------------------------------------------------ start  bean ---------------------------------------------------------------#
class CategoryReport:
    def __init__(self,statisDate,statisCategory,planSend,factSend,successSend,coverEmail,evryPv,evryPvDisEmail,evryClick,evryClickDisEmail,historyPv,historyPvDisEmail,historyClick,historyClickDisEmail):
        self.statisDate = statisDate
        self.statisCategory = statisCategory
        self.planSend = planSend
        self.factSend = factSend
        self.successSend = successSend
        self.coverEmail = coverEmail
        self.evryPv = evryPv
        self.evryPvDisEmail = evryPvDisEmail
        self.evryClick = evryClick
        self.evryClickDisEmail = evryClickDisEmail
        self.historyPv = historyPv
        self.historyPvDisEmail = historyPvDisEmail
        self.historyClick = historyClick
        self.historyClickDisEmail = historyClickDisEmail
    def __str__(self):
        self.evryPv_successSend = '0%'
        self.evryClick_successSend = '0%'
        if int(self.successSend) != 0:
            self.evryPv_successSend = str(round(float(self.evryPv)/self.successSend,3)*100)+'%'
            self.evryClick_successSend = str(round(float(self.evryClick)/self.successSend,3)*100)+'%'
        self.allDayPv = self.evryPv + self.historyPv
        self.allDayPvDisEmail = self.evryPvDisEmail + self.historyPvDisEmail
        self.allDayClick = self.evryClick + self.historyClick
        self.allDayClickDisEmail = self.evryClickDisEmail + self.historyClickDisEmail
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.statisCategory,self.planSend,self.factSend,self.successSend,self.coverEmail,self.evryPv,self.evryPvDisEmail,self.evryPv_successSend,self.evryClick,self.evryClickDisEmail,self.evryClick_successSend,self.historyPv,self.historyPvDisEmail,self.historyClick,self.historyClickDisEmail,self.allDayPv,self.allDayPvDisEmail,self.allDayClick,self.allDayClickDisEmail)

class AlgorithmContrast(CategoryReport):
    def __init__(self,statisDate,statisCategory,statisDept,successSend,coverEmail,evryPv,evryPvDisEmail,evryClick,evryClickDisEmail,historyPv,historyPvDisEmail,historyClick,historyClickDisEmail,allDayPvDisEmail,allDayClickDisEmail):
        CategoryReport.__init__(self,statisDate,statisCategory,0,0,successSend,coverEmail,evryPv,evryPvDisEmail,evryClick,evryClickDisEmail,historyPv,historyPvDisEmail,historyClick,historyClickDisEmail)
        self.statisDept = statisDept
        self.allDayPvDisEmail = allDayPvDisEmail
        self.allDayClickDisEmail = allDayClickDisEmail
        self.pv_send = '0%'
        self.click_send = '0%'
        self.click_pv = '0%'
    def __str__(self):
        if int(self.successSend) !=0 :
            self.pv_send = str(round(float(self.evryPv)/self.successSend,4)*100)+'%'
            self.click_send = str(round(float(self.evryClick)/self.successSend,4)*100)+'%'
        if int(self.historyPv) !=0 and int(self.evryPv) !=0:
            self.click_pv = str(round(float(int(self.evryClick))/int(self.evryPv),4)*100)+'%'
        header = ["日期","统计类型","算法分支","发送总量","覆盖独立人数","当日阅读量","当日阅读人数","当日点击量","当日点击人数","当日阅读/发送","当日点击/发送","当日点击/当日阅读"]
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.statisCategory,self.statisDept,self.successSend,self.coverEmail,self.evryPv,self.evryPvDisEmail,self.evryClick,self.evryClickDisEmail,self.pv_send,self.click_send,self.click_pv) 

class TplReport:
    def __init__(self,statisDate,tplId,tplName,statisCategory,factSend,successSend,coverEmail,evryPv,evryPvDisEmail,evryClick,evryClickDisEmail,historyPv,historyPvDisEmail,historyClick,historyClickDisEmail):
        self.statisDate = statisDate
        self.tplId = tplId
        self.tplName = tplName
        self.statisCategory = statisCategory
        self.factSend = factSend
        self.successSend = successSend
        self.coverEmail = coverEmail
        self.evryPv = evryPv
        self.evryPvDisEmail = evryPvDisEmail
        self.evryClick = evryClick
        self.evryClickDisEmail = evryClickDisEmail
        self.historyPv = historyPv
        self.historyPvDisEmail = historyPvDisEmail
        self.historyClick = historyClick
        self.historyClickDisEmail = historyClickDisEmail
    def __str__(self):
        self.evryPv_successSend = "0%"
        self.evryClick_successSend = "0%"
        if self.successSend != 0 :
            self.evryPv_successSend = str(round(float(self.evryPv)/self.successSend,3)*100)+'%'
            self.evryClick_successSend = str(round(float(self.evryClick)/self.successSend,3)*100)+'%'
        self.allDayPv = self.evryPv + self.historyPv
        self.allDayPvDisEmail = self.evryPvDisEmail + self.historyPvDisEmail
        self.allDayClick = self.evryClick + self.historyClick
        self.allDayClickDisEmail = self.evryClickDisEmail + self.historyClickDisEmail
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.tplId,self.tplName,self.statisCategory,self.factSend,self.successSend,self.coverEmail,self.evryPv,self.evryPvDisEmail,self.evryPv_successSend,self.evryClick,self.evryClickDisEmail,self.evryClick_successSend,self.historyPv,self.historyPvDisEmail,self.historyClick,self.historyClickDisEmail,self.allDayPv,self.allDayPvDisEmail,self.allDayClick,self.allDayClickDisEmail)

class DomainReport:
    def __init__(self,statisDate,domain,sendCount,successCount,allDayPv,allDayClick,nDayPv,nDayClick):
        self.statisDate = statisDate
        self.domain = domain
        self.sendCount = sendCount
        self.successCount = successCount
        self.allDayPv = allDayPv
        self.allDayClick = allDayClick
        self.nDayPv = nDayPv
        self.nDayClick = nDayClick
        self.allDaySendCount = 0
    def __str__(self):        
        self.allDayPv_successCount = "0%"
        Click_successCount = "0%"
        self.sendRatio = "0%"
        if int(self.successCount) != 0:
            self.allDayPv_successCount = str(round(float(self.allDayPv)/self.successCount,3)*100) + "%"
            self.allDayClick_successCount = str(round(float(self.allDayClick)/self.successCount,3)*100) + "%"
        '''
        if int(self.allDayPv) != 0 :
            self.nDayPv_allDayPv = str(round(float(self.nDayPv)/self.allDayPv,3)*100) + "%"
        if int(self.allDayClick) != 0:
            self.nDayClick_allDayClick = str(round(float(self.nDayClick)/self.allDayClick,3)*100) + "%"
        '''
        if int(self.allDaySendCount) != 0 :
            self.sendRatio = round(float(self.sendCount)/self.allDaySendCount,3)*100
            if self.sendRatio >= 5:
                self.domain = '<span style="font-weight:bold;color:red">'+self.domain+'<span>'
            self.sendRatio = str(self.sendRatio)+'%'
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.allDaySendCount,self.domain,self.sendRatio,self.successCount,self.allDayPv,self.allDayClick,self.allDayPv_successCount,self.allDayClick_successCount,self.nDayPv,self.nDayClick)
class CategoryInvite:
    def __init__(self,statisDate,statisCategory,sendCount,uidCount,readCount,acceptCount,deliverCount):
        self.statisDate = statisDate
        self.statisCategory = statisCategory
        self.uidCount = uidCount
        self.sendCount = sendCount
        self.readCount = readCount
        self.acceptCount = acceptCount
        self.deliverCount = deliverCount
        self.read_send = '-'
        self.accept_read = '-'
        self.deliver_accept = '-'
        self.deliver_send = '-'
        self.send_uid = '-'
    def __str__(self):
        if int(self.sendCount) != 0:
            self.read_send = str(round(float(self.readCount)/self.sendCount,4)*100)+"%"
            self.deliver_send = str(round(float(self.deliverCount)/self.sendCount,4)*100)+"%"
        if int(self.readCount) != 0:
            self.accept_read = str(round(float(self.acceptCount)/self.readCount,4)*100)+"%"
        if int(self.acceptCount) != 0:
            self.deliver_accept = str(round(float(self.deliverCount)/self.acceptCount,4)*100)+"%"
            if int(self.deliverCount) == 0 :
                self.deliver_accept = '-'
                self.deliver_send = '-'
        if int(self.uidCount) != 0:
            self.send_uid = str(round(float(self.sendCount)/self.uidCount,2)) 
        if int(self.deliverCount) == 0 :
            self.deliverCount = '-'
	return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.statisCategory,self.sendCount,self.uidCount,self.send_uid,self.readCount,self.acceptCount,self.deliverCount,self.read_send,self.accept_read,self.deliver_send)
#职位邀约对比
class JobInvitationContrast(CategoryInvite):
    def __init__(self,statisDate,dept,isRealTime,sendCount,uidCount,readCount,acceptCount,deliverCount,loginSendCount):
        CategoryInvite.__init__(self,statisDate,'职位',sendCount,uidCount,readCount,acceptCount,deliverCount)
        self.dept = dept
        self.isRealTime = isRealTime
        self.read_send = '-'
        self.accept_read = '-'
        self.deliver_accept = '-'
        self.deliver_send = '-'
        self.send_uid = '-'
        self.read_login_send_count = '-'
        self.deliver_login_send_count = '-'
        self.loginSendCount = loginSendCount
    def __str__(self):
        if int(self.sendCount) != 0:
            self.read_send = str(round(float(self.readCount)/self.sendCount,4)*100)+"%"
            self.deliver_send = str(round(float(self.deliverCount)/self.sendCount,4)*100)+"%"
        if int(self.readCount) != 0:
            self.accept_read = str(round(float(self.acceptCount)/self.readCount,4)*100)+"%"
        if int(self.acceptCount) != 0:
            self.deliver_accept = str(round(float(self.deliverCount)/self.acceptCount,4)*100)+"%"
            if int(self.deliverCount) == 0 :
                self.deliver_accept = '-'
                self.deliver_send = '-'
        if int(self.uidCount) != 0:
            self.send_uid = str(round(float(self.sendCount)/self.uidCount,2))
        if int(self.deliverCount) == 0 :
            self.deliverCount = '-'
        if int(self.loginSendCount) != 0 and self.deliverCount != '-':
            self.read_login_send_count = str(round(float(self.readCount)/self.loginSendCount,4)*100)+"%"
            self.deliver_login_send_count = str(round(float(self.deliverCount)/self.loginSendCount,4)*100)+"%"
        if int(self.loginSendCount) == 0 :
            self.loginSendCount = '-'
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.dept,self.isRealTime,self.sendCount,self.loginSendCount,self.uidCount,self.send_uid,self.readCount,self.acceptCount,self.deliverCount,self.read_send,self.accept_read,self.deliver_accept,self.deliver_send,self.read_login_send_count,self.deliver_login_send_count)
        

#项目邀约报表
class ProjectInvitation(CategoryInvite):
    def __init__(self,statisDate,statisCategory,sendCount,uidCount,readCount,acceptCount):
        CategoryInvite.__init__(self,statisDate,statisCategory,sendCount,uidCount,readCount,acceptCount,0)
        self.accept_send = ''
        self.read_send = ''
        if int(self.sendCount) != 0:
            self.accept_send = str(round(float(self.acceptCount)/self.sendCount,3)*100)+"%"
            self.read_send = str(round(float(self.readCount)/self.sendCount,3)*100)+"%"
        if int(self.readCount) != 0:
            self.accept_read = str(round(float(self.acceptCount)/self.readCount,3)*100)+"%"
    def __str__(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (self.statisDate,self.statisCategory,self.sendCount,self.uidCount,self.readCount,self.acceptCount,self.read_send,self.accept_send,self.accept_read)
class MTAReport:
    leaderSend = 0
    leaderSuccess = 0
    leaderPv = 0
    leaderClick = 0
    def __init__(self,statisDate,statisMTA,sendCount,successCount,pvCount,clickCount):
        self.statisDate = statisDate
        self.statisMTA = statisMTA
        self.sendCount = sendCount
        self.successCount = successCount
        self.pvCount = pvCount
        self.clickCount = clickCount
    def __str__(self):
        if int(self.sendCount) !=0 :
            self.success_send = str(round(float(self.successCount)/self.sendCount,3)*100)+"%"
        if int(self.successCount) !=0:
            self.pv_success = str(round(float(self.pvCount)/self.successCount,3)*100)+"%"
            self.click_success = str(round(float(self.clickCount)/self.successCount,3)*100)+"%"
        rate = 0.92
        if float(self.sendCount)/MTAReport.leaderSend < rate or float(self.successCount)/MTAReport.leaderSuccess < rate or float(self.pvCount)/MTAReport.leaderPv < rate or float(self.clickCount)/MTAReport.leaderClick < rate:
            return '<td><span style="font-weight:bold;color:red">%s</span></td><td><span style="font-weight:bold;color:red">%s</span></td><td><span style="font-weight:bold;color:red">%s</span></td><td><span style="font-weight:bold;color:red">%s</span></td><td><span style="font-weight:bold;color:red">%s</span></td><td><span style="font-weight:bold;color:red">%s</span></td>' % (self.statisDate,self.statisMTA,self.sendCount,self.success_send,self.pv_success,self.click_success)
        else:
            return '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (self.statisDate,self.statisMTA,self.sendCount,self.success_send,self.pv_success,self.click_success)

class ProjectDetail:
    def __init__(self,statisDate,statisCategory,projectId,corpName,projectName,sendCount,readCount,acceptCount):
        self.statisDate = statisDate
        self.statisCategory = statisCategory
        self.projectId = projectId
        self.corpName = corpName 
        self.projectName = projectName
        self.sendCount = sendCount
        self.readCount = readCount
        self.acceptCount = acceptCount
        self.read_send = '-'
        self.accept_send = '-'
        self.accept_read = '-'
    def __str__(self):
        if int(self.sendCount) != 0 :
            self.read_send = str(round(float(self.readCount)/self.sendCount,3)*100)+"%"
            self.accept_send = str(round(float(self.acceptCount)/self.sendCount,3)*100)+"%"
        if int(self.readCount) != 0 : 
            self.accept_read = str(round(float(self.acceptCount)/self.readCount,3)*100)+"%"
        return '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (self.statisDate,self.projectId,self.corpName,self.projectName,self.sendCount,self.readCount,self.acceptCount,self.read_send,self.accept_send,self.accept_read)

class RTJobInvitationDelay:
    def __init__(self,statisDate,delay0_5,delay5_10,delay10_20,delay20_60,delay60,notSend):
        self.statisDate = statisDate
        self.delay0_5 = delay0_5
        self.delay5_10 = delay5_10
        self.delay10_20 = delay10_20
        self.delay20_60 = delay20_60
        self.delay60 = delay60
        self.notSend = notSend
        self.uidDisCount = 0
    def __str__(self):
        self.uidDisCount +=int(self.delay0_5)+int(self.delay5_10)+int(self.delay10_20) +int(self.delay20_60)+int(self.delay60) +int(self.notSend)
        return '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (self.statisDate,self.uidDisCount,self.delay0_5,self.delay5_10,self.delay10_20,self.delay20_60,self.delay60,self.notSend)

class MailStatusBase:
    def __init__(self,statisDate,tplId,success,bounced,renderError):
        self.statisDate = statisDate
        self.tplId = tplId
        self.success = success
        self.bounced = bounced
        self.renderError = renderError
        self.bounced_total = str(round(float(self.bounced)/float(self.bounced + self.success),3)*100)+'%'
    def __str__(self):
        return '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (self.statisDate,self.tplId,self.success,self.bounced,self.bounced_total,self.renderError)

class MailStatusForInvitation(MailStatusBase):
    def __init__(self,statisDate,inviteGroupId,tplId,success,bounced,renderError):
        MailStatusBase.__init__(self,statisDate,tplId,success,bounced,renderError)
        self.inviteGroupId = inviteGroupId
        self.bounced_total = str(round(float(self.bounced)/float(self.bounced + self.success),3)*100)+'%'
    def __str__(self):
        return '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (self.statisDate,self.inviteGroupId,self.tplId,self.success,self.bounced,self.bounced_total,self.renderError)
       #------------------------------------------------------ end  bean ---------------------------------------------------------------#
       #------------------------------------------------------ start  dao and service  ---------------------------------------------------------------#
def getCategoryReport(statisDate):
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor = db.cursor()
    sql = "select statis_date,statis_category,plan_count,send_count,success_count,email_count,evry_pv_count,evry_pv_email_count,evry_click_count,evry_click_email_count,history_pv_count,history_pv_email_count,history_click_count,history_click_email_count from tb_rptdash_email_category where statis_date = '%s' order by statis_category,success_count desc;" % (statisDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        if line[3] == 0:
            continue
        else:
            resList.append(CategoryReport(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13]))
    '''
    allCategoryReport = CategoryReport(results[0][0],"汇总数据",results[0][2],0,0,0,0,0,0,0,0,0,0,0) 
    for line in resList:
        allCategoryReport.factSend = allCategoryReport.factSend + line.factSend
        allCategoryReport.successSend = allCategoryReport.successSend + line.successSend
        allCategoryReport.coverEmail = allCategoryReport.coverEmail + line.coverEmail
        allCategoryReport.evryPv = allCategoryReport.evryPv + int(line.evryPv)
        allCategoryReport.evryPvDisEmail = allCategoryReport.evryPvDisEmail + line.evryPvDisEmail
        allCategoryReport.evryClick = allCategoryReport.evryClick + line.evryClick
        allCategoryReport.evryClickDisEmail = allCategoryReport.evryClickDisEmail + line.evryClickDisEmail
        allCategoryReport.historyPv = allCategoryReport.historyPv + line.historyPv
        allCategoryReport.historyPvDisEmail = allCategoryReport.historyPvDisEmail + line.historyPvDisEmail
        allCategoryReport.historyClick = allCategoryReport.historyClick + line.historyClick
        allCategoryReport.historyClickDisEmail = allCategoryReport.historyClickDisEmail + line.historyClickDisEmail
    resList.insert(0,allCategoryReport)
    '''
    return resList

def getTplReport(statisDate):
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_tpl_id,statis_tpl_name,statis_category,send_count,success_count,email_count,evry_pv_count,evry_pv_email_count,evry_click_count,evry_click_email_count,history_pv_count,history_pv_email_count,history_click_count,history_click_email_count from tb_rptdash_email_tpl where statis_date = '%s' and (success_count != 0 or evry_click_count !=0 or history_pv_count !=0 ) order by success_count desc limit 20; " % (statisDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        #if line[4] ==0 and line[7] == 0 and line[11] == 0:
        if line[4] == 0:
            continue
        else:
            resList.append(TplReport(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]))
    return resList

def getDomainReport(statisDate):
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_domain,send_count,success_count,evry_pv_count,evry_click_count,nday_pv_count,nday_click_count from tb_rptdash_email_domain where statis_date = '%s' order by send_count desc limit 15;" % (statisDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    sendCount = 0
    for line in results:
        beforeDate = time.strftime('%Y-%m-%d',time.localtime((time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6)))
        sql = "select sum(success_count) from tb_rptdash_email_domain where statis_domain = '%s' and statis_date <='%s' and statis_date >='%s';" % (line[1],statisDate,beforeDate)
        cursor.execute(sql)
        nDaySendCount = cursor.fetchone()
        nDaySendCount = nDaySendCount[0]
        pv = 0
        click = 0
        if int(nDaySendCount) !=0:
            pv = str(round(line[6]/nDaySendCount,3)*100)+"%"
            click = str(round(line[7]/nDaySendCount,3)*100)+"%"
        if line[2] == 0:
        #if line[2] == 0 and line[4] == 0 and line[6] == 0:
            continue
        else:
            resList.append(DomainReport(line[0],line[1],line[2],line[3],line[4],line[5],pv,click))
        sendCount = sendCount + line[2]
    for line in resList:
        line.allDaySendCount = sendCount
    return resList

def getCategoryInviteForJob(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,send_count,read_count,accept_count,post_deliver_count,mtype,uid_count from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'job' order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(CategoryInvite(line[0],line[1]+'-'+line[6],line[2],line[7],line[3],line[4],line[5]))
    '''
    sql = "select statis_date,'当日汇总数据',sum(send_count),sum(read_count),sum(accept_count),sum(post_deliver_count),'job',sum(uid_count) from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'job' group by statis_date order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    totalList = []
    for line in results:
        totalList.append(CategoryInvite(line[0],line[1],int(line[2]),int(line[7]),int(line[3]),int(line[4]),line[5]))
    i = 0
    for index,line in enumerate(resList):
        if len(totalList) <= i:
            break
        if line.statisDate == totalList[i].statisDate:
            resList.insert(index,totalList[i])
            i = i + 1
    '''
    return resList

def getCategoryInviteForProject(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,send_count,read_count,accept_count,0,mtype,uid_count from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'project' order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(CategoryInvite(line[0],line[1]+'-'+line[6],line[2],line[7],line[3],line[4],line[5]))
    '''
    sql = "select statis_date,'当日汇总数据',sum(send_count),sum(read_count),sum(accept_count),sum(post_deliver_count),'project',sum(uid_count) from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'project' group by statis_date order by statis_date desc,statis_category desc;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    totalList = []
    for line in results:
        totalList.append(CategoryInvite(line[0],line[1],int(line[2]),int(line[7]),int(line[3]),int(line[4]),line[5]))
    i = 0
    for index,line in enumerate(resList):
        if len(totalList) <= i:
            break
        if line.statisDate == totalList[i].statisDate:
            resList.insert(index,totalList[i])
            i = i + 1
    '''
    return resList

def getCategoryInviteForCampus(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,send_count,read_count,accept_count,0,mtype,uid_count from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'campus' order by statis_date desc,statis_category desc;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(CategoryInvite(line[0],line[1]+'-'+line[6],line[2],line[7],line[3],line[4],line[5]))
    '''
    sql = "select statis_date,'当日汇总数据',sum(send_count),sum(read_count),sum(accept_count),sum(post_deliver_count),'campus',sum(uid_count) from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'campus' group by statis_date order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    totalList = []
    for line in results:
        totalList.append(CategoryInvite(line[0],line[1],int(line[2]),int(line[7]),int(line[3]),int(line[4]),line[5]))
    i = 0
    for index,line in enumerate(resList):
        if len(totalList) <= i:
            break
        if line.statisDate == totalList[i].statisDate:
            resList.insert(index,totalList[i])
            i = i + 1
    '''
    return resList
def getMTA(statisDate):
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor = db.cursor()
    sql = "select count(1),sum(send_count),sum(success_count),sum(pv_count),sum(click_count) from tb_rptdash_email_mta where statis_date = '%s' and statis_mta not in ('mx347.dajie-mail.com','mx37.dajie.com');" % (statisDate)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results[0] == 0:
        return resList
    resList.append(MTAReport(statisDate,'在用MTA:'+str(results[0]+2)+'台 平均数据',int(results[1]/results[0]),int(results[2]/results[0]),int(results[3]/results[0]),int(results[4]/results[0])))
    MTAReport.leaderSend = int(results[1]/results[0])
    MTAReport.leaderSuccess = int(results[2]/results[0])
    MTAReport.leaderPv = int(results[3]/results[0])
    MTAReport.leaderClick = int(results[4]/results[0])
    sql = "select statis_mta,send_count,success_count,pv_count,click_count from tb_rptdash_email_mta where statis_date = '%s' and statis_mta not in ('mx347.dajie-mail.com','mx37.dajie.com') order by statis_mta;" % (statisDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    leader = resList[0]
    rate = 0.91
    for line in results:
        mtaReport = MTAReport(statisDate,line[0],line[1],line[2],line[3],line[4])
        resList.append(mtaReport)
    return resList
#为项目需求，单独查询7日内的数据
def getProjectInvitation(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,max(send_count),max(uid_count),max(read_count),max(accept_count) from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and mtype = 'project' group by statis_date,statis_category order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(ProjectInvitation(line[0],line[1],line[2],line[3],line[4],line[5]))
    return resList
 
#为项目需求，查询项目详情    
def getProjectDetail(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor = db.cursor()
    sql = "select statis_date,statis_category,project_id,corp_name,project_name,max(send_count),max(read_count),max(accept_count) from tb_rptdash_email_project_detail where statis_category = 4003 and statis_date <= '%s' and statis_date > '%s' group by statis_date,statis_category,project_id,corp_name,project_name order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(ProjectDetail(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]))
    return resList
#实时邀约发送延时时间统计
def getRTJobInvitationDelay(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*30))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor = db.cursor()
    sql = "select statis_date,delay_0_5,delay_5_10,delay_10_20,delay_20_60,delay_60,notsend from tb_rptdash_email_rt_invitation_job_delay where type = 1 and statis_date <='%s' and statis_date >= '%s' order by statis_date desc;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(RTJobInvitationDelay(line[0],line[1],line[2],line[3],line[4],line[5],line[6]))
    return resList

#邀约算法站内信对比报表
def getInvitationAlogrithmContrast(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,'邀约算法',if(substring(statis_category,1,3)='101','基础平台','数据部门'),sum(send_count),sum(read_count),sum(accept_count),sum(post_deliver_count),mtype,sum(uid_count),sum(if(statis_category='101140112' or statis_category='101140131' or statis_category='101140141',0,login_send_count)) from tb_rptdash_email_invite_bizcode where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite_bizcode) and mtype = 'job' and substring(statis_category,1,2) ='10' group by statis_date,substring(statis_category,1,3) order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(JobInvitationContrast(line[0],line[1],line[2],int(line[3]),int(line[8]),int(line[4]),int(line[5]),int(line[6]),int(line[9])))
    return resList

#内部邀约算法站内信对比报表
def getJobInvitationContrast(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,case when statis_category='101140108' then '平台-新算法' when statis_category='101140106' then '人才流动-应届' when statis_category='101140101' then '平台-协同过滤' when statis_category='101140102' then '平台-add_rec' when statis_category='101140103' then '平台-社招add_rec' when statis_category='101140104' then '平台-校招add_rec' when statis_category='101010701' then '平台-add_rec_old' when statis_category='101010501' then '平台-活跃用户' when statis_category='101010401' then '平台-协同过滤_old' when statis_category='101140111' then '平台-协同过滤权重' when statis_category='101020101' then '平台-邀约算法' when statis_category='101140112' then '协同过滤算法-邀约箱' when statis_category='101140131' then '社招add_rec-邀约箱' when statis_category='101140141' then '校招add_rec-邀约箱' when substring(statis_category,1,3)='102' then '数据-邀约算法' when statis_category='101140105' then '平台-新职位' when statis_category='101140151' then '新职位-模糊' else '其他' end,if(substring(statis_category,4,2)='02','实时','离线'),sum(send_count),sum(read_count),sum(accept_count),sum(post_deliver_count),mtype,sum(uid_count),if(statis_category='101140112' or statis_category='101140131' or statis_category='101140141',0,sum(login_send_count)) from tb_rptdash_email_invite_bizcode where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite_bizcode) and mtype = 'job' and substring(statis_category,1,2) ='10' group by statis_date,substring(statis_category,1,3),substring(statis_category,4,6),substring(statis_category,6,2) order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(JobInvitationContrast(line[0],line[1],line[2],int(line[3]),int(line[8]),int(line[4]),int(line[5]),int(line[6]),int(line[9])))
    return resList

#邀约算法邮件对比报表
def getAlgorithmEmailContrast(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,statis_dept,success_count,email_count,evry_pv_count,evry_pv_email_count,evry_click_count,evry_click_email_count,history_pv_count,history_pv_email_count,history_click_count,history_click_email_count,allday_pv_email_count,allday_click_email_count from tb_rptdash_email_contrast where statis_date <= '%s' and statis_date >= '%s' order by statis_date desc,statis_dept;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(AlgorithmContrast(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]))
    return resList

#邮件状态报表
def getMailStatusData(statisDate):
    resList = []
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    endDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))+60*60*24*1))
    db = MySQLdb.connect('10.10.67.62','platform_sel','dajie.platform)-','DB_MAIL',3308,charset='utf8')
    cursor = db.cursor()
    sql = "select left(create_date,10),tpl_version_id,count(distinct if(status=0,mail_data_id,0))-1 success,count(distinct if(status=5,mail_data_id,0))-1 bounced,count(distinct if(status=19,mail_data_id,0))-1 rendererror from tb_send_record where create_date > '%s' and create_date < '%s' and status in (0,5,19) group by left(create_date,10),tpl_version_id having success > 100;" % (startDate,endDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(MailStatusBase(line[0],line[1],line[2],line[3],line[4]))
    sortedResList =  sorted(resList,key=attrgetter('statisDate','bounced'),reverse=True)
    return sortedResList

def getMailStatusForInviteGroupIdData(statisDate):
    resList = []
    serialIdSet = set()
    serialIdInviteGroupId = dict()
    endDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))+60*60*24*1))
    db = MySQLdb.connect('10.10.67.62','platform_sel','dajie.platform)-','DB_MAIL',3308,charset='utf8')
    cursor = db.cursor()
    sql = "select left(create_date,10),serial_id,tpl_version_id,count(distinct if(status=0,mail_data_id,0))-1 success,count(distinct if(status=5,mail_data_id,0))-1 bounced,count(distinct if(status=19,mail_data_id,0))-1 rendererror from tb_send_record where create_date >= '%s' and create_date < '%s' and status in (0,5,19) and serial_id > 0 group by serial_id having success > 100;" % (statisDate,endDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(MailStatusForInvitation(line[0],line[1],line[2],line[3],line[4],line[5]))
        serialIdSet.add(int(line[1]))
    db = MySQLdb.connect('10.10.67.62','platform_sel','dajie.platform)-','DB_MAIL',3308,charset='utf8')
    cursor = db.cursor()
    sql = "select id,invite_group_id from engine_center_indentify_info where id in (%s);" % (str(serialIdSet)[5:len(str(serialIdSet))-2])
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        serialIdInviteGroupId[str(line[0])] = str(line[1])
    resMap = dict()
    for line in resList:
        if line.inviteGroupId in resMap:
           resMap[line.inviteGroupId].success = resMap[line.inviteGroupId].success + line.success
           resMap[line.inviteGroupId].success = resMap[line.inviteGroupId].bounced + line.bounced
           resMap[line.inviteGroupId].success = resMap[line.inviteGroupId].renderError + line.renderError
        else:
            line.inviteGroupId = serialIdInviteGroupId[str(line.inviteGroupId)]
            resMap[line.inviteGroupId] = line
    resList = []
    for line in resMap:
        resList.append(resMap[line])
    sortedResList = sorted(resList,key=attrgetter('tplId','bounced'),reverse=True)
    return sortedResList

def getCategoryInviteForTalentLibrary(statisDate):
    startDate = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(statisDate,'%Y-%m-%d'))-60*60*24*6))
    resList = []
    db = MySQLdb.connect('cobarVIP','platformol','platformol-3','DB_BSS',12001,charset='utf8')
    cursor =db.cursor()
    sql = "select statis_date,statis_category,send_count,read_count,accept_count,post_deliver_count,mtype,uid_count from tb_rptdash_email_invite where statis_date <= '%s' and statis_date >= '%s' and create_date = (select max(create_date) from tb_rptdash_email_invite) and mtype = 'talent' order by statis_date desc,statis_category;" % (statisDate,startDate)
    cursor.execute(sql)
    results = cursor.fetchall()
    for line in results:
        resList.append(CategoryInvite(line[0],line[1]+'-'+line[6],line[2],line[7],line[3],line[4],line[5]))
    return resList 
       #------------------------------------------------------ end  dao and service ---------------------------------------------------------------#
       #------------------------------------------------------ start  main ---------------------------------------------------------------#
if __name__ == "__main__":
    while 1:
        flagLen = ''
        try:
            flagLen = len(open("reportMain.flag").readlines())
            print flagLen
            if int(flagLen) >= 1:
                break
            else:
                time.sleep(5)
        except Exception,e:
            print e
            time.sleep(5)

    args = sys.argv
    statisDate = ''
    if len(args) > 1:
        statisDate = args[1]
    else:
        statisDate = time.strftime('%Y-%m-%d',time.localtime(time.time()-60*60*24*1))
    print statisDate
    #-------------------------------------------------------------------对外发送报表----------------------------------------------------#
    to_email = ['yake.zheng@dajie-inc.com','jian.yin@dajie-inc.com','yunbin.an@dajie-inc.com','yanxiong.dong@dajie-inc.com','guanghe.ge@dajie-inc.com','shiqiang.wang@dajie-inc.com','dongcai.liu@dajie-inc.com','peipei.li@dajie-inc.com']
    #to_email = ['yunbin.an@dajie-inc.com']
    # 1.1.1 发送站内信报表 职位 项目 宣讲会 
    content = '<html><body>'
    header = ["日期","统计类别","站内信发送量","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读","累计投递/发送"]
    reports = getCategoryInviteForJob(statisDate)
    content = content + render('邀约箱-职位',header,reports,1)
    # 1.1.2
    header = ["日期","统计类别","站内信发送量","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读",">累计投递/发送"]
    reports = getCategoryInviteForTalentLibrary(statisDate)
    content = content + render('人才库-公司',header,reports,1)
    # 1.1.3
    header = ["日期","统计类别","站内信发送量","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读","累计投递/发送"]
    reports = getCategoryInviteForProject(statisDate)
    content = content + render('邀约箱-项目',header,reports,1)
    # 1.1.4
    header = ["日期","统计类别","站内信发送量","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读","累计投递/发送"]
    reports = getCategoryInviteForCampus(statisDate)
    content = content + render('邀约箱-宣讲会',header,reports,1)
    content = content + '</body></html>'
    print 'inviation report send:',sendMail.send_mail(to_email,'站内信日发送报表'+statisDate,content+ '</body></html>')

    '''
    to_email = ['yake.zheng@dajie-inc.com','jian.yin@dajie-inc.com','yunbin.an@dajie-inc.com','yanxiong.dong@dajie-inc.com','guanghe.ge@dajie-inc.com','linyan.wang@dajie-inc.com','shiqiang.wang@dajie-inc.com','dongcai.liu@dajie-inc.com']
    to_email = ['yunbin.an@dajie-inc.com']
    # 1.2.1 邮件类别报表 
    content = '<html><body>'
    header = ["日期","统计类别","资源分配量","试图发送量","成功发送量","发送人数","邮件打开次数","邮件打开人数","当日打开/实际发送","去重点击次数","点击人数","当日点击/实际发送","历史打开次数","历史打开人数","历史点击次数","历史点击人数","全天打开次数","全天打开人数","全天点击次数","全天点击人数"]
    reports = getCategoryReport(statisDate)
    content = content + render('业务线类别发送日报',header,reports,2)
    # 1.2.2 邮件模板报表 
    header = ["日期","模板Id","模板名称","统计类别","试图发送量","成功发送量","发送人数","邮件打开次数","邮件打开人数","当日打开/实际发送","去重点击次数","点击人数","当日点击/实际发送","历史打开次数","历史打开人数","历史点击次数","历史点击人数","全天打开次数","全天打开人数","全天点击次数","全天点击人数"]
    reports = getTplReport(statisDate)
    content = content + render('邮件模板发送日报',header,reports,2)
    content = content + '</body></html>'
    print 'email report send:',sendMail.send_mail(to_email,'邮件日发送报表'+statisDate,content+ '</body></html>')
    '''
    #-------------------------------------------------------------------------------------------------------------------------------------#
    # 1.3.1 邀约算法站内信对比报表
    #content = '<html><body>'
    #header = ["日期","统计类型","算法分支","站内信发送量","登录人覆盖邀约数","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读","累计投递/接受","累计投递/发送","累计阅读/登录","累计投递/登录"]
    #reports = getInvitationAlogrithmContrast(statisDate)
    #content = content + render('邀约算法站内信对比报表',header,reports,1)

    # 1.3.2 邀约算法邮件对比报表
    #header = ["日期","统计类型","算法分支","发送总量","覆盖独立人数","当日阅读量","当日阅读人数","当日点击量","当日点击人数","当日阅读/发送","当日点击/发送","当日点击/当日阅读"]
    #reports = getAlgorithmEmailContrast(statisDate)
    #content = content + render('邀约算法邮件对比报表',header,reports,1)
    #print 'algorithm email contrast and algorithm invitation contrast report send:',sendMail.send_mail(to_email,'邀约算法对比报表'+statisDate,content+ '</body></html>')

    #----------------------------------------------------------内部邮件报表--------------------------------------------------------------#
    '''
    to_email = ['dongcai.liu@dajie-inc.com','yanxiong.dong@dajie-inc.com','yunbin.an@dajie-inc.com','shiqiang.wang@dajie-inc.com']
    #to_email = ['yunbin.an@dajie-inc.com']
    # 3.1.1 域名发送报表 
    content = '<html><body>'
    header = ["日期","全天实际发送量","域名","发送百分比","成功发送量","邮件打开人数","邮件点击人数","打开/实际发送","点击/实际发送","打开/发送(7日平均)","点击/发送(7日>平均)"]
    reports = getDomainReport(statisDate)
    content = content + render('邮件域名分析日报',header,reports,2)
    content = content + '</body></html>'
    print 'domain report send:',sendMail.send_mail(to_email,'邮件域名分析日报'+statisDate,content+ '</body></html>')
    #-----------------------------------------------------------------------------------------------------------------------------------#
    # 3.2.1 MTA 报表
    content = '<html><body>'
    header = ["日期","MTA域名","试图发送","成功/试图","打开/成功","点击/成功"]
    reports = getMTA(statisDate)
    content = content + '</body></html>'
    content = content + render('MTA分析日报',header,reports,2)
    print 'mta report send:',sendMail.send_mail(to_email,'MTA分析日报'+statisDate,content+ '</body></html>')
    #---------------------------------------------------------------------------------------------------------------------------------#
    '''
    # 3.3.1 内部邀约算法站内信对比报表
    to_email = ['dongcai.liu@dajie-inc.com','yanxiong.dong@dajie-inc.com','yunbin.an@dajie-inc.com','shiqiang.wang@dajie-inc.com']
    #to_email = ['yunbin.an@dajie-inc.com']
    content = '<html><body>'
    header = ["日期","部门","实时/离线","站内信发送量","登录人覆盖邀约数","独立覆盖人数","发送量/覆盖人数","累计阅读量","累计接受量","累计投递量","累计阅读/发送","累计接受/阅读","累计投递/接受","累计投递/发送","累计阅读/登录","累计投递/登录"]
    reports = getJobInvitationContrast(statisDate)
    content = content + render('内部邀约算法站内信对比报表',header,reports,1)

    # 3.3.2 实时职位邀约发送延时，从用户登录邀约箱到邀约发送的延时统计
    #header = ["日期","登录总人数","延时0-5秒","延时5-10秒","延时10-20秒","延时20-60秒","延时60秒以上","未发送"]
    #reports = getRTJobInvitationDelay(statisDate)
    #content = content + render('实时邀约算法发送延时报表',header,reports,2)
    print 'inside algorithm invitation contrast and real time job invitation delay report send:',sendMail.send_mail(to_email,'内部邀约算法对比报表'+statisDate,content+ '</body></html>')
    #---------------------------------------------------------------------------------------------------------------------------------#
    '''
    to_email = ['dongcai.liu@dajie-inc.com','yanxiong.dong@dajie-inc.com','yunbin.an@dajie-inc.com','shiqiang.wang@dajie-inc.com','li.han@dajie-inc.com','wei.pang@dajie-inc.com']
    #to_email = ['dongcai.liu@dajie-inc.com']
    #邮件发送状态报表
    content = '<html><body>'
    # 3.4.1 按邀约统计邮件模板状态报表
    header = ["日期","邀约ID","模板号","成功发送","被拒绝","被拒/总量","渲染异常"]
    reports = getMailStatusForInviteGroupIdData(statisDate)
    content = content + render('邮件邀约发送状态报表',header,reports,2)
    # 3.4.2 邮件模板状态报表
    header = ["日期","模板号","成功发送","被拒绝","被拒/总量","渲染异常"]
    reports = getMailStatusData(statisDate)
    content = content + render('模板发送状态报表',header,reports,1)
    print 'mail tpl status report send:',sendMail.send_mail(to_email,'邮件状态报表'+statisDate,content+ '</body></html>')
    '''
       #------------------------------------------------------ end  main ---------------------------------------------------------------#
