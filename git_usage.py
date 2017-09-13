# -*- coding: utf-8 -*-

'''
git使用方法

git bash进行操作

添加、提交、查看、删除文件：
$ git add <filename>
$ git commit
$ git rm <filename>
$ cat <filename>

$ git status  查看当前仓库的状态

控制版本：
$ git log     显示提交记录
$ git reflog  显示提交记录ID
$ git reset --hard <commit id>
($ git reset --hard HEAD^)  一个^表示退回上一个版本

撤销修改：
$ git checkout --<filename>


远程仓库——git hub：
创建ssh公共密匙并在git hub账号上添加该密匙
$ git remote add origin git@github.com:<my email>/<my project>.git  链接远程仓库
$ git push -u origin master   初始化
$ git push origin master      本地仓库修改后上传
$ git pull                    从远程仓库抓取变化，每次编辑本地仓库之前先pull一遍，保证后面能正常push


'''







