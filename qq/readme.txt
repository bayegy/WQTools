#用这个命令进入脚本所在位置，记得把F:\qq\qq-grabber改为你自己的路径
cd /d F:\qq\qq-grabber 
#用这个命令 新建一个文件，存储爬取结果，--group 后面跟群名字（不能有空格），--new 后面跟 文件名字，相应去修改
python get_qqinfo.py --group inature官方文献群 --new test
#用这个命令继续爬取另外一个群，爬取结果存储在上一次新建的文件里面，关键就是不要加--new
python get_qqinfo.py --group 大数据学习交流 
