
#!python3
# -*- coding: utf-8 -*-

import os,re,sys,codecs


fout1=open('media.txt','w',encoding='UTF-8')
for line in open('F:/qq/Python-UIAutomation-for-Windows-master/@AutomationLog.txt',encoding='UTF-8'):
	line=re.sub('\n','\t',line)
	line=re.sub('eachpersonend','\n',line)
	fout1.write(line)
fout1.close()

info={'群中备注':'未填写','备注':'未填写','昵称':'未填写','帐号':'未填写','邮箱':'未填写','可能邮箱':'未填写','学历':'未填写','学校':'未填写','职业':'未填写','公司':'未填写','故乡':'未填写','所在地':'未填写','电话':'未填写','主页':'未填写','Q龄':'未填写','语言':'未填写','姓名':'未填写','个人说明':'未填写','手机':'未填写'}
infok=list(info.keys())



fout=open('qqinfotab.csv','w',encoding='UTF-8')
for z in infok:
	fout.write(z+',')
fout.write('\n')
for line in open('F:/qq/Python-UIAutomation-for-Windows-master/media.txt',encoding='UTF-8'):
	if re.search('^\t+$',line)==None:
		line=re.sub('^.+eachpersonstart\t','',line)
		
		line=re.split('\t',line)
		
		info={'群中备注':'未填写','备注':'未填写','昵称':'未填写','帐号':'未填写','邮箱':'未填写','可能邮箱':'未填写','学历':'未填写','学校':'未填写','职业':'未填写','公司':'未填写','故乡':'未填写','所在地':'未填写','电话':'未填写','主页':'未填写','Q龄':'未填写','语言':'未填写','姓名':'未填写','个人说明':'未填写','手机':'未填写'}
		
		info['群中备注']=line[0]
		
		for li in line:
			for io in infok:
				if re.search(io,li)!=None:
					info[io]=re.sub(io,'',li)
		if re.search('\d{5,30}',info['帐号'])!=None:
			info['可能邮箱']=re.search('\d{5,30}',info['帐号']).group()+'@qq.com'
			info['帐号']=re.search('\d{5,30}',info['帐号']).group()
		for i in infok:
			fout.write(info[i]+',')
		fout.write('\n')
fout.close()


