========2022.5.25 Cbyto========
      "CmBrowser" ver 1.2.2
========2022.11.3 Cbyto========

#Book Folder Format:
 
Book_Name
----Chapter_Names
	----Images
	----Images

[Book_Name(Folder) > Chapter_Name(Folder) > Images(Files)]
[书名(文件夹) > 章节名(文件夹) > 图片(文件)]
=========================

软件适配的字体:
"Cascadia Code SemiBold"
"Open Sans Semibold"
"Comic Sans MS Bold"(默认)
> 可以在app/fontset.txt中改变字体, 请确保字体已装载在C:/Windows/Font中（系统字体文件夹）
更改字体可能导致按钮变形或错位，同样请谅解
(Tkinter不支持外置自定义字体我真的好**啊)

PS：
> 竖屏版本里的放大模块有些瑕疵，见谅
> 请不要随意删除或篡改app和save文件夹下的文件，以免发生严重的bug或无法挽回的错误！
-
===========================
错误处理（重要）：
（已知可能会发生的bug）

*请不要在翻页界面输入不合理的数字与字母，以免发生无法预料的bug（已经在1.2.2解决）
  如果进入阅读界面时黑屏或无法打开书籍，请选中书籍后点击“Check Save”并检查当前页码是否正确（第二行的数字）

*如果发现进入library界面后没有显示指定的书库的书，而是显示save目录下的书库名称且窗口名为空，那么证明app/current_lib.dat文档里内容为空。请尝试重新切换当前书库或修改curren_lib.dat(疑似已经解决)

*在改完屏幕方向设置后请重新启动Cmbrowser
==========================
Click "Help" Button in home page for more information.
点击Help按钮阅读软件使用教程（英文）
教程文档存放在Manual.txt里面，请不要给它删了
==========================

Code By Cbyto
"普通至极的低技术力"
CmBrowser ver 1.2.4 / Packed with pyinstaller

==========================

PS: tkinter显示出来的图片分辨率一坨答辩，我也没办法，见谅。。
还有就是不要把图片放太大（尤其是针对2k/4k显示器的用户），不然会导致严重的性能负担。





