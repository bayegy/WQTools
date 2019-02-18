#!python3
# -*- coding: utf-8 -*-
"""
本脚本可以获取QQ2017(v8.9.4)群所有成员详细资料，请根据提示做对应的操作
作者：yinkaisheng@foxmail.com
"""
import time,os,re
import uiautomation as automation


def GetPersonDetail():
    detailWindow = automation.WindowControl(searchDepth= 1, ClassName = 'TXGuiFoundation', SubName = '的资料')
    details = ''
    for control, depth in automation.WalkControl(detailWindow):
        if isinstance(control, automation.EditControl):
            details += control.Name + control.CurrentValue() + '\n'
    details += 'eachpersonend\n'
    detailWindow.Click(-10, 10)
    return details


def main():
    automation.Logger.WriteLine('请把鼠标放在QQ群聊天窗口中的一个成员上面，3秒后获取\n')
    time.sleep(3)
    listItem = automation.ControlFromCursor()
    if listItem.ControlType != automation.ControlType.ListItemControl:
        automation.Logger.WriteLine('没有放在群成员上面，程序退出！')
        return
    consoleWindow = automation.GetConsoleWindow()
    if consoleWindow:
        consoleWindow.SetActive()
    qqWindow = listItem.GetTopWindow()
    list = listItem.GetParentControl()
    allListItems = list.GetChildren()
    for listItem in allListItems:
        automation.Logger.WriteLine(listItem.Name)
    answer = 'n'
    if answer.lower() == 'y':
        automation.Logger.WriteLine('\n3秒后开始获取QQ群成员详细资料，您可以一直按住F10键暂停脚本')
        time.sleep(3)
        qqWindow.SetActive()
        #确保群里第一个成员可见在最上面
        left, top, right, bottom = list.BoundingRectangle
        while allListItems[0].BoundingRectangle[1] < top:
            automation.Win32API.MouseClick(right - 5, top + 20)
        for listItem in allListItems:
            if listItem.ControlType == automation.ControlType.ListItemControl:
                if automation.Win32API.IsKeyPressed(automation.Keys.VK_F10):
                    if consoleWindow:
                        consoleWindow.SetActive()
                    input('\n您暂停了脚本，按Enter继续\n')
                    qqWindow.SetActive()
                listItem.RightClick()
                menu = automation.MenuControl(searchDepth= 1, ClassName = 'TXGuiFoundation')
                menuItems = menu.GetChildren()
                for menuItem in menuItems:
                    if menuItem.Name == '查看资料':
                        menuItem.Click()
                        break
                automation.Logger.WriteLine('eachpersonstart')
                automation.Logger.WriteLine(listItem.Name, automation.ConsoleColor.Green)
                
                automation.Logger.WriteLine(GetPersonDetail())
                listItem.Click()
                automation.SendKeys('{Down}')

				
				
#writed by zhangguoxing 
def formtable(qun,savefile):
    savefile='results/'+savefile
    with open(savefile,'a',encoding='utf-8') as fout,open('@AutomationLog.txt','r',encoding='utf-8') as fin:
        fout.write('QQ号\tQQ邮箱\t\群内备注\t来源\n')
        for line in fin:
            if re.search('\)$',line):
                line=re.sub('\n$','',line)
                qqn=re.search('\d{4,100}',line).group()
                sl=qqn+'\t'+qqn+'@qq.com'+'\t'+line+'\t'+qun+'\n'
                fout.write(sl)



if __name__ == '__main__':
    from datetime import datetime
    import sys,os
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-g', '--group', dest='group', metavar='<str>', help='提供QQ号的分组名字，默认每次用时间为组名', default=False)
    p.add_argument('-n', '--new', dest='new', metavar='<path>', help='另外建文件存储结果，指明新文件的名字', default=False)
    options = p.parse_args()

    if os.path.exists('@AutomationLog.txt'):
        os.remove('@AutomationLog.txt')
    qun = options.group if options.group else str(datetime.now())
    if options.new:
        savefile=options.new+'.txt'
        with open('config/filename.txt','w') as f:
            f.write(savefile)
        main()
        formtable(qun,savefile)
    else:
        with open('config/filename.txt','r') as f:
            savefile=f.read().strip()
        main()
        formtable(qun,savefile)
