#encoding: utf-8
import sys
from PIL import Image, ImageEnhance #,ImageTk
import os
#import random
import tkinter as tk
from tkinter import filedialog, PhotoImage
#from tkinter.ttk import *
from natsort import natsorted
import gc
from ast import literal_eval
from time import sleep
from keyboard import read_key








dimg=""  # 声明全局变量，确保图片不被python的gc清除

if getattr(sys, 'frozen', False):
    mainprogram = os.path.dirname(sys.executable)
elif __file__:
    mainprogram = os.path.dirname(__file__)
#print(mainprogram)

r_key = open(mainprogram+"/app/key_config.json","r",encoding="utf-8").read().strip() # 键位设置
key_dic = literal_eval(r_key)
#print(key_dic)

casfontdir = open(mainprogram+"/app/fontset.txt","r",encoding="utf-8").read().strip() # 字体设置

opclib = open(mainprogram+"/app/current_lib.dat","r",encoding="utf-8") # 当前目录设置
current_lib = opclib.read().strip()
opclib.close()

scdis = True # 是否可以打开目录页面
getis = True

def cmdisplay(book):
    pagecount = 0
    imgsize = 0
    avalibility = True # 文件是否可读
    

    # rdc = open(mainprogram+"/app/homecfg.dat","r",encoding="utf-8") #<<读取屏幕方向设置
    # displayMode = rdc.readline().strip()
    # rdc.close()
    displayMode = smode

    def show(dim):
        canv = tk.Canvas(root,width=screenwidth,height=screenheight,bd=0,bg="black")
        canv.place(x=-2,y=-2,anchor="nw")
        if displayMode == "Vertical":
            canvImage = canv.create_image(screenwidth/2,screenheight/2,anchor="center",image=dim)
        else:    
            canvImage = canv.create_image(screenwidth/2,0,anchor="n",image=dim)
        #canvImage.image = dimg
        canv.create_text(screenwidth-80,screenheight-30,text=str(pagecount+1)+"/"+str(len(piclist)),fill="white",font=(casfontdir,20))
        
        root.bind(f"{key_dic['cmb_scrollup']}", lambda *args:canv.move(1,0,50))
        root.bind(f"{key_dic['cmb_scrolldown']}", lambda *args:canv.move(1,0,-50))
        root.bind(f"{key_dic['cmb_scrollleft']}", lambda *args:canv.move(1,50,0))
        root.bind(f"{key_dic['cmb_scrollright']}", lambda *args:canv.move(1,-50,0))
        
    try:
        rd =  open(book,"r",encoding="utf-8")
        bookpath = rd.readline().strip()
        pagecount = int(rd.readline().strip())
        #print(pagecount)
        f=bookpath
        chapterlist = []
        piclist=[]
        chapterstart={}  # 注意看，这个字典叫chapterstart！
        rd.close()
    except:
        tk.messagebox.showwarning("Warning","Invalid Save!")
        avalibility = False
        home()
        
    try:
        folder = os.listdir(f)
        folder = natsorted(folder)
        contain_folder = False

        def appendImage(item):
            nonlocal piclist
            #count=0
            if item.endswith(("png","jpg","jpeg","webp","bmp","PNG","JPG","JPEG","WEBP","BMP")):
                ct = "/"+i+"/"+item
                piclist.append(ct) # ==这里==在路径前面已经有加<"/">
                #print(ct)
                
                

        for ij in folder:  # 先遍历一遍folder文件夹下的图片，再处理章节内的 (不调用appendImage函数直接操控piclist)
            if not os.path.isdir(os.path.join(f,ij)):
                if ij.endswith(("png","jpg","jpeg","webp","bmp","PNG","JPG","JPEG","WEBP","BMP")):
                    print(ij)
                    piclist.append("/"+ij)
                

        for i in folder:               # i 对应章节名称
            if os.path.isdir(f+"/"+i):  
                contain_folder = True
                chapterlist.append(i)
                pics = os.listdir(f +"/"+ i) 
                pics=natsorted(pics)          # pics 是一个列表，包含文件夹 i 中的所有文件（与文件夹）
                #print(pics)

                
                start_dir = ("/"+i+"/"+pics[0]) 
                chapterstart[i]=start_dir

                flst=[]
                for fold in pics:        
                    if os.path.isdir(f+"/"+i+"/"+fold):
                        flst.append(fold)
                    #print(flst)
                    flst=natsorted(flst)
                try:
                    under_pics = os.listdir(f+"/"+i+"/"+flst[0])
                    under_pics=natsorted(under_pics)
                    start_dir = ("/"+i+"/"+flst[0]+"/"+under_pics[0])
                    chapterstart[i]=start_dir
                except:pass #print("None!!")


                for j in pics:
                    fdpath = (f +"/"+ i +"/"+j)
                    #print(fdpath) 
                    if os.path.isdir(f +"/"+ i +"/"+j):
                        fd = os.listdir(f +"/"+ i +"/"+j)
                        #print(fd)
                        for pc in fd:
                            appendImage(j+"/"+pc)
                            #print(j+"/"+pc,"----1")
                    appendImage(j)
                    #print(j,"----2")
                    

        chapterlist = natsorted(chapterlist)
        
        #print(bookpath)
        #print(piclist)

        #print(chapterlist)
        #print(chapterstart)
        #print(len(piclist))
        
        #print(pics)

    except:
        avalibility = False
        tk.messagebox.showerror("An Error has occured!","Cannot recognize book directory!\n\nCheck your directory's format.\nCheck if the directory is loadable or not.")
        home()
        raise
        

    if avalibility: #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Start from here
        root = tk.Tk()
        
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()    
        
        canv = tk.Canvas(width=screenwidth,height=screenheight,bd=0,bg="black")
        canv.place(x=-2,y=-2,anchor="nw")
        
        root.title("CmBrowser")
        root.configure(bg="black")
        root.iconbitmap(mainprogram+"/app/book.ico")
        
        root.attributes("-fullscreen",True)

        root.focus_force()
        

        def flip(pic,ron): #切换到指定页 <<<<<<<<<<<<<<<<<<<<<<<<（dimg）
            global dimg
            nonlocal imgsize
            if ron == False:
                imgsize = 0
            canv.destroy()
            path = open(bookpath +"/"+pic,"rb")  # Binary mode 
            picload = Image.open(path)
            img_w = picload.width
            img_h = picload.height

            if displayMode == "Vertical":
                if img_w > img_h:
                    size_w = screenwidth+(imgsize*50)
                else:
                    size_w = screenwidth-50
                size_h=int(img_h * (size_w/img_w))
            else:
                size_h=screenheight+(imgsize*50)
                size_w=int(img_w * (size_h/img_h))

            picload = picload.resize((size_w,size_h),Image.ANTIALIAS)
            picload = ImageEnhance.Sharpness(picload)
            picload = picload.enhance(1.9)
            picload.save(mainprogram+"/app/temp.png","png")
            dimg = PhotoImage(file=mainprogram+"/app/temp.png")
            
            path.close()
            gc.collect() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            show(dimg)

        def magni(*args):
            nonlocal imgsize
            if imgsize < 117: #==================================HERE
                imgsize +=1
            flip(piclist[pagecount],True)
        def shrink(*args):
            nonlocal imgsize
            if imgsize > -6:
                imgsize -= 1
            flip(piclist[pagecount],True)
        def maxim(*args):
            nonlocal imgsize
            imgsize = 10
            flip(piclist[pagecount],True)
        root.bind(f"{key_dic['cmb_expand_img']}", magni)
        root.bind(f"{key_dic['cmb_shrink_img']}", shrink)
        root.bind(f"{key_dic['cmb_quick_expand']}",maxim)

        def selectChapter(*args):
            global scdis
            if scdis == True:
                scdis = False
                sc= tk.Tk()
                sc.title("Catalog")
                sc.attributes("-topmost",True)
                sc.resizable(False,False)
                sc.geometry("%dx%d+%d+%d"%(450,700,(screenwidth-500)/2,(screenheight-700)/2))
                sc.attributes("-toolwindow",2)
                sc.focus_force()


                def scexit(*args):
                    global scdis
                    scdis = True
                    sc.destroy()
                sc.protocol('WM_DELETE_WINDOW', scexit)

                scroller = tk.Scrollbar(sc)
                listbox1 = tk.Listbox(sc,height =27,width=47, yscrollcommand = scroller.set,font=("Calibri",12),exportselection=False)
                listbox1.place(x=35,y=100)
                for i in chapterlist:
                    listbox1.insert("end",i)
                def gotochapter(*args):
                    try:
                        index = listbox1.curselection()[0]
                        chapter = chapterlist[index]
                        nonlocal pagecount
                        pagecount = piclist.index(chapterstart[chapter])
                        flip(chapterstart[chapter],False)
                        scexit()
                    
                    except ValueError:
                        scexit()
                        tk.messagebox.showerror("An Error has occured!","<Cannot flip to chapter!>\nPlease check your chapter's folder format!\n(There should NOT be any empty folders)")
                        raise
                        
                    #except:pass
                
                gobt = tk.Button(sc,text="< Switch >",fg="brown",bg="white",font=(casfontdir,20),command=gotochapter,width=21,height=1)
                gobt.place(x=225,y=55,anchor="center")
                sc.bind("<Return>",gotochapter)
                sc.bind("<Escape>",scexit)
                sc.bind(f"<{key_dic['main_exit']}>",scexit)

                sc.mainloop()
            else:
                pass
        
        root.bind(f"{key_dic['cmb_chapter']}",selectChapter)


        def exitdisplay(*args):
            pagesave()
            root.destroy()
            sys.exit()
        def returnHome(*args):
            pagesave()
            root.destroy()
            home()
        def minidisplay(*args):
            root.iconify()
        root.bind(f"{key_dic['cmb_minimize']}",minidisplay)
        root.bind("<Escape>",exitdisplay)
        #root.bind("<Control-space>",exitdisplay)
        root.bind(f"{key_dic['main_exit']}",returnHome)

        
        
        def gotopage(page):
            nonlocal pagecount
            #print(page)
            try:
                page = int(page)
            except:tk.messagebox.showerror("Error...","Input something sensible!")
            try:
                # 1145141919810 <<marked a bug here
                if page - 1 < 0:
                    tk.messagebox.showerror("Error!","Page out of range")
                    return False
                if page-1 > len(piclist)-1:
                    tk.messagebox.showerror("Error!","Page out of range")
                    return False
            except:
                print("@")
            else:
                try:
                    if page > 0:
                        pagecount = page-1
                        flip(piclist[pagecount],False)
                except:
                    raise Exception("Unknown Error!!!")
                    return False
        def getPage(*args):
            global getis
            if getis:
                getwin = tk.Tk()
                getwin.lift()
                getwin.title("Flip to Page")
                getwin.geometry("%dx%d+%d+%d"%(295,60,(screenwidth-295)/2,(screenheight-70)/2))
                getwin.attributes("-toolwindow",2)
                getwin.focus_force()
                getwin.configure(bg="grey")
                getis = False
                getPage = tk.Entry(getwin,width=32)
                getPage.place(x=20,y=20)
                getPage.focus_set()                  #Recently Added
                def exitgetp(*args):
                    global getis
                    getis = True  
                    getwin.destroy()
                def finish(*args):
                    global getis
                    getis = True
                    gotopage(getPage.get()) 
                    getwin.destroy()
                    try:
                        getwin.lift()
                    except:pass
                gotopagebt = tk.Button(getwin,text="Enter",fg="brown",font=(casfontdir,10),command=finish,width=5,height=1)
                gotopagebt.place(x=223,y=14)       
                getwin.protocol('WM_DELETE_WINDOW',exitgetp)
                getwin.bind(f"{key_dic['main_exit']}",exitgetp)
                getwin.bind("<Escape>",exitgetp)
                getwin.bind("<Return>",finish)
            else:pass

        root.bind(f"{key_dic['cmb_flippage']}",getPage)
        #root.bind("<Shift_L>",getPage)

        def pagesave(*args):
            wr = open(book,"w",encoding="utf-8")
            wr.write(bookpath+"\n"+str(pagecount))



        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # 初始页
        print(pagecount)
        flip(piclist[pagecount],False)

        def pnext(*args):
            nonlocal pagecount
            pagecount+=1
            if pagecount > len(piclist)-1:
                pagecount = len(piclist)-1         # KKSK
            
            
            flip(piclist[pagecount],False)
            

        def plast(*args):
            nonlocal pagecount
            pagecount -= 1
            if pagecount < 0:
                pagecount = 0

            flip(piclist[pagecount],False)
        def pchk(key):
            coor = key.x
            if coor>= screenwidth/2:
                pnext()
            else: plast()
        flipmode = [plast,pnext]
        root.bind(f"{key_dic['cmb_previous']}",plast)
        root.bind("<Button-1>",pchk)
        root.bind(f"{key_dic['cmb_next']}",pnext)
        
        #root.bind("<b>",pagesave)
        

        def refresh(*args):
            flip(piclist[pagecount],False)
        #root.bind("<Shift_R>",refresh)
        #root.bind("<z>",refresh)
        root.bind(f"{key_dic['cmb_reload_img']}",refresh)

        refresh()
        #refresh() # testfor
        
        root.mainloop()
#cmdisplay()=====================================================================================================





#目录界面
def cmlibrary(*args):
    
    browsefile = ""

    def readpath(file):   # <<<This was changed!!! May cause some problems<<<
        with open (mainprogram + f"/save/{current_lib}/{file}","r")as r:
            result = r.readline().strip()
            r.close()
            return result

    lib = tk.Tk()
    lib.title(current_lib)
    lib.iconbitmap(mainprogram+"/app/folder.ico")

    screenwidth = lib.winfo_screenwidth()
    screenheight = lib.winfo_screenheight()
    lib.geometry("%dx%d+%d+%d"%(400,600,(screenwidth-400)/2,(screenheight-600)/2))
    lib.resizable(width = False,height = False)
    #lib.attributes("-topmost",True)

    lib.focus_force()


    def display():
        displaylist = []

        try:
            for i in os.listdir(mainprogram+f"/save/{current_lib}"):
                displaylist.append(i)
        except:
            tk.messagebox.showerror("ERROR","Library Do Not Exist!\nPlease click <Switch-Library> to change a library!")
        scroll = tk.Scrollbar(lib)
        listbox1 = tk.Listbox(lib,height =20,width=42, yscrollcommand = scroll.set,font=("Calibri",12),exportselection=False)
        listbox1.place(x=30,y=100)
        for count,i in enumerate(displaylist):
            item = i[:-4]
            listbox1.insert(count,item)

        def browse(*args): # =====从此开始======================
            ct = (listbox1.curselection())[0]
            rs = mainprogram+f"/save/{current_lib}/"+listbox1.get(ct)+".txt"
            lib.destroy()
            print(rs)
            cmdisplay(rs)
        #
        #  阅读按键
        browsebt = tk.Button(lib, text = "BROWSE", fg='brown',bg="#dfdfdf" , font=(casfontdir, 25), width=15, height=1,command=browse)
        browsebt.place(x=200,y=50,anchor="center")
                
        def keydel(*args): #删除内容=======已修改
            try:
                ct = (listbox1.curselection())[0]
                rs = listbox1.get(ct)
                #print(rs)
                
                listbox1.delete(ct)
                os.remove(mainprogram+f"/save/{current_lib}/{rs}.txt")
                if ct-1 < 0:
                    listbox1.selection_set(str(0))
                else:
                    listbox1.selection_set(str(ct-1))
            except: pass
        def configdel(*args):
            try:
                validity = tk.messagebox.askyesno("Configure",f"Are sure about removing \"{listbox1.get(listbox1.curselection()[0])}\" from your library?")
                if validity == True:
                    keydel()
            except:pass
        delbt = tk.Button(lib, text = "REMOVE", fg='brown',bg="#dfdfdf" , font=(casfontdir, 20), width=9, height=1,command=configdel)
        delbt.place(x=290,y=550,anchor="center")
        lib.bind("<BackSpace>",configdel)
        lib.bind("<Control-BackSpace>",keydel)
        lib.bind("<Return>",browse)

        def opsavelocation(*args):
            try:
                ct = (listbox1.curselection())[0]
                rs = mainprogram+f"/save/{current_lib}/"+listbox1.get(ct)+".txt"
                os.startfile(rs)
            except:pass
        opfbt = tk.Button(lib, text = "Check Save", fg='brown',bg="#dfdfdf" , font=(casfontdir, 10), width=20, height=1,command=opsavelocation)
        opfbt.place(x=115,y=535,anchor="center")

        def opdir(*args):
            ct = (listbox1.curselection())[0]
            rs = mainprogram+f"/save/{current_lib}/"+listbox1.get(ct)+".txt"
            with open(rs,"r",encoding="utf-8")as rdir:
                path = rdir.readline().strip()
                print(path)
                os.system('start "" "%s"' % path)   #============# Windows command!  Caution!!===============
                rdir.close()
        dirbt = tk.Button(lib, text = "Open Directory", fg='brown',bg="#dfdfdf" , font=(casfontdir, 10), width=20, height=1,command=opdir)
        dirbt.place(x=115,y=567,anchor="center")
    def libclose(*args):
        lib.destroy()
        home()
    lib.protocol('WM_DELETE_WINDOW', libclose)
    lib.bind(f"{key_dic['main_exit']}",libclose)
    lib.bind("<Escape>",libclose)
    display()
    lib.mainloop()  

#cmlibrary() #  ===========================================


r = open(mainprogram+"/app/homecfg.dat","r",encoding="utf-8") # 读取 home设置
smode = r.readline().strip()
pmode = r.readline().strip()
r.close()







def config(*args):                                                                                                                        # display设置
    imgpath = ""
    cfg=tk.Tk()
    r = open(mainprogram+"/app/homecfg.dat","r",encoding="utf-8")
    smode = r.readline().strip()
    pmode = r.readline().strip()
    r.close()
    screenwidth = cfg.winfo_screenwidth()
    screenheight = cfg.winfo_screenheight()
    cfg.geometry("%dx%d+%d+%d"%(620,270,(screenwidth-620)/2,(screenheight-270)/2))
    cfg.title("Setting")
    cfg.resizable(width = False,height = False)
    cfg.attributes("-topmost",True)
    text0=tk.Label(cfg,text="Display Mode:",font=(casfontdir,12),fg="black")
    text1=tk.Label(cfg,text="Do display background:",font=(casfontdir,11),fg="black")
    text0.place(x=10,y=6)
    text1.place(x=10,y=80)

    cfg.focus_force()

    selection=[]
    if smode == "Vertical":
        selection.append(1)
    else:selection.append(0)
    if pmode == "False":
        selection.append(1)
    else:selection.append(0)

    listbox1 = tk.Listbox(cfg,height=2,width=30,exportselection=False,font=("Calibri",13))
    listbox1.place(x=10,y=33)
    listbox1.insert("end","Horizontal","Vertical")
    listbox1.selection_set(selection[0])

    listbox2 = tk.Listbox(cfg,height=2,width=30,exportselection=False,font=("Calibri",13),selectmode="browse")
    listbox2.place(x=10,y=105)
    listbox2.insert("end","True","False")
    listbox2.selection_set(selection[1])

    var_stretch = tk.BooleanVar()
    radiobt = tk.Checkbutton(cfg,text="Auto\nStretch",variable=var_stretch)
    radiobt.place(x=205,y=160)

    def selectimg(*args):
        cfg.attributes("-topmost",False)
        global imgpath
        imgpath = tk.filedialog.askopenfilename()
        cfg.attributes("-topmost",True)

    selectimgbt = tk.Button(cfg,text="Select Background Image",fg="black",bg="#989898",height=1,width=20,font=("Calibri",13),command=selectimg)
    selectimgbt.place(x=10,y=160)

    def okay(*args):
        lb1=["Horizontal","Vertical"]
        lb2=["True","False"]
        line1=lb1[(listbox1.curselection())[0]]
        line2=lb2[(listbox2.curselection())[0]]
        global smode, pmode
        smode=line1
        pmode=line2
        configure = open(mainprogram+"/app/homecfg.dat","w",encoding="utf-8")
        configure.write(line1+"\n"+line2)
        configure.close()
        try:
            global imgpath
            image = Image.open(imgpath)
            size_h = 600
            size_w = int(image.width/(image.height/600))
            if var_stretch.get():
                size_w = 900
            image_size = image.resize((size_w, size_h),Image.LANCZOS)
            image_size.save(mainprogram+"/app/bg0.png")
            
        except: pass
            #tk.messagebox.showerror("ERROR!","Cannot Load Image")
        cfg.destroy()
        return home()

    finishbt = tk.Button(cfg,text="Finish",bg="#dedede",fg="brown",height=1,width=22,font=(casfontdir,15),command=okay)
    finishbt.place(x=10,y=210)
    def cfgex(*args):
        cfg.destroy()
        return home()
    cfg.protocol('WM_DELETE_WINDOW', cfgex)
    cfg.bind("<Return>",okay)
    cfg.bind(f"{key_dic['main_exit']}",cfgex)
    cfg.bind("<Escape>",cfgex)









def fontcfg(*args):                                                                                                                          # 自定义字体
    cf=tk.Tk()
    screenwidth = cf.winfo_screenwidth()
    screenheight = cf.winfo_screenheight()
    cf.geometry("%dx%d+%d+%d"%(300,350,(screenwidth-300)/2,(screenheight-270)/2))
    cf.title("Font Setting")
    cf.resizable(width = False,height = False)
    cf.attributes("-topmost",True)
    cf.config(bg="#c8c8c8")
    def setfont(fontname):
        op = open(mainprogram+"/app/fontset.txt","w",encoding="utf-8")
        op.write(fontname)
        op.close()
        global casfontdir
        casfontdir = fontname
        cf.destroy()
        home()
    def previewFont(ft):
        pre = tk.Label(cf,text="The quick brown fox jumps over the lazy dog.1234567890",font=(ft,10),fg="grey")
        pre.place(x=0,y=300,anchor="w")

    ComicSansMSBold = tk.Button(cf,text="Comic Sans MS Bold",bg="#dedede",fg="brown",height=1,width=22,font=("Comic Sans MS Bold",12),command=lambda *args:setfont("Comic Sans MS Bold"))
    OpenSansSemibold = tk.Button(cf,text="Open Sans Semibold",bg="#dedede",fg="brown",height=1,width=22,font=("Open Sans Semibold",12),command=lambda *args:setfont("Open Sans Semibold"))
    CascadiaCodeSemiBold = tk.Button(cf,text="Cascadia Code Semibold",bg="#dedede",fg="brown",height=1,width=25,font=("Cascadia Code SemiBold",12),command=lambda *args:setfont("Cascadia Code SemiBold"))
    TwCenMTBold = tk.Button(cf,text="Tw Cen MT Bold",bg="#dedede",fg="brown",height=1,width=25,font=("Tw Cen MT Bold",12),command=lambda *args:setfont("Tw Cen MT Bold"))
    text00=tk.Label(cf,text="Custom Font",font=(casfontdir,12),fg="black",bg="#c8c8c8")
    
    entBox = tk.Entry(cf,width=28)
    customize = tk.Button(cf,text="Set as Font",bg="#dedede",fg="brown",height=1,width=11,font=(casfontdir,11),command=lambda *args:setfont(entBox.get().strip()))
    preview = tk.Button(cf,text="Preview",bg="#dedede",fg="black",height=1,width=11,font=(casfontdir,11),command=lambda *args:previewFont(entBox.get().strip()))
    

    text00.place(x=11,y=225,anchor="w")
    entBox.place(x=117,y=225,anchor="w")
    entBox.insert("insert", casfontdir)
    
    OpenSansSemibold.place(x=150,y=30,anchor="center")
    ComicSansMSBold.place(x=150,y=80,anchor="center")
    CascadiaCodeSemiBold.place(x=150,y=130,anchor="center")
    TwCenMTBold.place(x=150,y=180,anchor="center")

    customize.place(x=30,y=280,anchor="sw")
    preview.place(x=160,y=280,anchor="sw")
    previewFont(casfontdir)

    cf.focus_force()
    entBox.focus_force()  
    cf.bind("<Return>",previewFont(entBox.get().strip()))

    def cfgex(*args):
        cf.destroy()
        return home()
    cf.protocol('WM_DELETE_WINDOW', cfgex)
    cf.bind(f"{key_dic['main_exit']}",cfgex)
    cf.bind("<Escape>",cfgex)
    
    #cf.bind("Control")





def callback(k,v):
    key_dic[k] = v
    print(key_dic)
    
    
def keyconfig_start(*args):                                                                                                             # 按键绑定
    global key_dic
    #keyset = open(mainprogram+"/app/key_config.json","r",encoding="utf-8")  
    #keys = keyset.read()
    #keyset.close()
    keycfg = tk.Tk()
    screenwidth = keycfg.winfo_screenwidth()
    screenheight = keycfg.winfo_screenheight()
    keycfg.title("Key Configure")
    keycfg.geometry(f"450x650+{int((screenwidth-450)/2)}+{int((screenheight-650)/2)}")
    keycfg.resizable(False,False)
    keycfg.configure(bg="grey")
    def cfgex(*args):
        keycfg.destroy()
        return home()
    keycfg.protocol('WM_DELETE_WINDOW', cfgex)
    #keycfg.bind(f"{key_dic['main_exit']}",cfgex)
    keycfg.bind("<Escape>",cfgex)
    info = tk.Label(keycfg, text="Click to configure key\n(Number or Letter Recommended)",bg="grey",fg="white",height=2,width=30,font=(casfontdir,18))
    info.pack(side=tk.BOTTOM,anchor="s")
    keycfg.focus_force()



    canv_k = tk.Canvas(keycfg, bg="grey",height=650, width=449)
    canv_k.pack(anchor="nw")


    klst = [
    "main_exit",
    "home_library",
    "home_book",
    "home_folder",
    "home_config",
    "home_switch",
    "cmb_minimize",
    "cmb_chapter",
    "cmb_flippage",
    "cmb_shrink_img",
    "cmb_expand_img",
    "cmb_quick_expand",
    "cmb_reload_img" ] # 不包含翻页/scroll按钮
 
    def keyref():
        for ins, k in enumerate(klst):
            kbt = tk.Button(keycfg, text=k,bg="#c8c8c8",fg="brown",height=1,width=20,font=(casfontdir,11),command=lambda arg=k:change_key(arg))
            kbt.place(x = 100,y=klst.index(k)*34+30,anchor="center")
    def valref(destroy):
        if destroy == True:
            canv_k.delete("all")
        for k in range(len(klst)):
            
            canv_k.create_text(230,k*34+30,text=key_dic[klst[k]],font=(casfontdir,12),fill="white")
            

    def change_key(keyname):
        def gohk(val):
            nonlocal keyname
            callback(keyname,val)
            
            valref(True)
        gohk(read_key().lower())  
    
    
    keyref()
    valref(False)

    keycfg.mainloop()






def switch_library(*args):                                                                                                                # 切换书库
    libc = tk.Tk()
    screenwidth = libc.winfo_screenwidth()
    screenheight = libc.winfo_screenheight()
    libc.geometry("%dx%d+%d+%d"%(400,490,(screenwidth-400)/2,(screenheight-490)/2))
    libc.resizable(width = False,height = False)
    libc.title("Switch-Library")
    libc.iconbitmap(mainprogram+"/app/folder.ico")
    libc.config(bg="#c8c8c8")
    
    

    libc.focus_force()

    def shut(*args):
        libc.destroy()
        home()
    def display():
        displaylist = []
        for i in os.listdir(mainprogram+"/save"):
            displaylist.append(i)

        scroll = tk.Scrollbar(libc)
        listbox1 = tk.Listbox(libc,height =14,width=42, yscrollcommand = scroll.set,font=("Calibri",12),exportselection=False)
        listbox1.place(x=30,y=100)
        for count,i in enumerate(displaylist):
            item = i
            listbox1.insert(count,item)
        try:
            listbox1.selection_set(str(displaylist.index(current_lib)))
        except:pass
        def change(*args): # =====     从此开始======================
            global current_lib
            ct = (listbox1.curselection())[0]
            rs = displaylist[int(ct)]
            current_lib = rs
            print(current_lib)
            wrfd = open(mainprogram+"/app/current_lib.dat","w",encoding="utf-8")
            wrfd.write("")
            wrfd.write(current_lib)
            wrfd.close()
            shut()
            
            
        #
        #  代码复用
        browsebt = tk.Button(libc, text = "SWITCH", fg='brown',bg="#dfdfdf" , font=(casfontdir, 25), width=15, height=1,command=change)
        browsebt.place(x=200,y=50,anchor="center")
        
        def newfold(*args):
            fn = tk.Tk()
            fn.geometry("%dx%d+%d+%d"%(350,130,(screenwidth-350)/2,(screenheight-130)/2))
            fn.title("Create New Library")
            fn.attributes("-topmost",True)
            fn.focus_force()
            fn.attributes("-toolwindow",3)
            instruct = tk.Label(fn,text="Input your New Library Name HERE:",fg="black",font=(casfontdir,11))
            instruct.place(x=10,y=10)
            entryBox = tk.Entry(fn,width=50)
            entryBox.place(x=10,y=40,anchor="nw")

            def done(*args):
                try:
                    result = entryBox.get().strip()
                    os.mkdir(path=mainprogram+f"/save/{result}")
                    listbox1.insert("end",result)
                    displaylist.append(result)
                    fn.destroy()
                except:
                    fn.attributes("-topmost",False)
                    tk.messagebox.showwarning("An ERROR has occured!",f'Possible Errors:\n<There is alerady a library named "{result}" in this folder!>\n<You might input forbidden-character codes!>')
                    fn.attributes("-topmost",True)
                    fn.focus_force()
            donebt = tk.Button(fn, text = "Finish", fg='brown',bg="#dfdfdf" , font=(casfontdir, 11), width=24, height=1,command=done)
            donebt.place(x=10,y=70,anchor="nw")
            def exitfn(*args):
                fn.destroy()
                return None
            fn.bind("<Escape>",exitfn)
            fn.bind("<Return>",done)

        libc.bind(f"{key_dic['home_switch']}",newfold)
        def keydel(*args): #删除内容=======已修改
            s_index = listbox1.curselection()[0]
            s_item = displaylist[s_index]
            listbox1.delete(s_index)
            displaylist.remove(s_item)
            path0 = mainprogram+f"/save/{s_item}"
            lst = os.listdir(path0)
            print(lst)
            for i in lst:
                os.remove(path0+f"/{i}")
            os.rmdir(path0)

            
        def configdel(*args):
            try:
                validity = tk.messagebox.askyesno("Configure",f"Are sure about removing library \"{listbox1.get(listbox1.curselection()[0])}\"?\nAll the saves in this folder will be lost!",default="no")
                if validity == True:
                    keydel()
            except:pass
        delbt = tk.Button(libc, text = "REMOVE", fg='grey',bg="#dfdfdf" , font=(casfontdir, 20), width=9, height=1,command=configdel)
        nwlbt = tk.Button(libc, text = "NEW", fg='brown',bg="#dfdfdf" , font=(casfontdir, 20), width=9, height=1,command=newfold)
        delbt.place(x=290,y=430,anchor="center")
        nwlbt.place(x=113,y=430,anchor="center")
        libc.bind("<BackSpace>",configdel)
        libc.bind("<Control-BackSpace>",keydel)
        libc.bind("<Return>",change)


    libc.bind(f"{key_dic['main_exit']}",shut)
    libc.bind("<Escape>",shut)
    
    libc.protocol('WM_DELETE_WINDOW', shut)
    display()

#==================================================================


def convert_to_title(path):
    count = len(path)
    result = []
    for letter in range(1024):
        if not path[count-1] == "/":
            result.append(path[count-1])
            count-=1
        else:
            result.reverse()
            res2 = [str(i) for i in result]
            res3 = "".join(res2)
            return(res3)
#print(convert_to_title("C:/Users/Bill Yi/Desktop/Recent files/CmBrowser"))


    

     #   ==========<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
def writepath(content):
    title = convert_to_title(content)
    print(title)

    lst = os.listdir(mainprogram+f"/save/{current_lib}")
    wrote = False
    for i in lst:
        if f"{title}.txt" == i:
            validity = tk.messagebox.askyesnocancel("Warning",f'Your library already contains a save named \n<{i[:-4]}>\n\nDo you want to overwrite the previousc save?\n<YES>: Overwrite\n<NO>: Keep both',default="no")
            if validity==True:
                w = open (mainprogram + f"/save/{current_lib}/{title}.txt","w",encoding="utf-8")
                w.write(content+"\n"+"0")
                w.close()
                wrote = True
            if validity==False:
                count = 1
                for i in lst:
                    if i == title+f"({str(count)}).txt":
                        count+=1
                    else:
                        w = open (mainprogram + f"/save/{current_lib}/{title}({str(count)}).txt","w",encoding="utf-8")
                        w.write(content+"\n"+"0")
                        w.close()
                        wrote = True
            else:
                print("cancelled")
    if wrote == False:
        w = open (mainprogram + f"/save/{current_lib}/{title}.txt","w",encoding="utf-8")
        w.write(content+"\n"+"0")
        w.close()

#标题界面
def home(): #  ===================================================================================================
    home = tk.Tk()
    screenwidth = home.winfo_screenwidth()
    screenheight = home.winfo_screenheight()
    home.focus_force()

    #按键功能
    def openlib(*args):
        home.destroy()
        cmlibrary()
    def openkeycfg(*args):
        home.destroy()
        keyconfig_start()

    def sbook(*args):
        try:
            path = filedialog.askdirectory(title = "Select the folder of your Book")
            writepath(path)
            #print(path)
        except:
            pass

    def sfolder(*args):
        try:
            path0 = filedialog.askdirectory(title = "Select a Directory of folders")
            files = os.listdir(path0)
            for i in files:
                if os.path.isdir(path0+"/"+i):
                    writepath(path0+"/"+i)
        except:pass


        

    if smode == "Vertical":
        home_w=600
        home_h=600
        home.geometry("%dx%d+%d+%d"%(600,600,(screenwidth-600)/2,(screenheight-600)/2-25))
    else:
        home_w=900
        home_h=600
        home.geometry("%dx%d+%d+%d"%(900,600,(screenwidth-900)/2,(screenheight-600)/2-25))

    #背景
    if pmode == "True":
        try:
            img = PhotoImage(file=mainprogram + "/app/bg0.png")
            img_label= tk.Label(home,image=img)  #▰▰
            if smode == "Vertical":
                img_label.place(x=0,y=0,anchor="nw")
            else:img_label.place(x=home_w/2, y=home_h/2,anchor="center")
        except:
            print("unable to load")
        
    #colorconfig = open(mainprogram+"/app/config.dat","r").readline().strip()

    home.configure(bg="black")
    home.title("CmBrowser")
    home.iconbitmap(mainprogram+"/app/book.ico")
    home.resizable(width = False,height = False)

    
    

    lib = tk.Button(home, text = "Library", fg='brown',bg="#dfdfdf" , font=(casfontdir, 14), width=11, height=1,command=openlib)
    lib.grid(row=0,column=0)
    #  按钮
    book = tk.Button(home, text='Select Book',fg="brown",bg="#dfdfdf", font=(casfontdir, 12), width=14, height=1, command=sbook)
    folder = tk.Button(home, text='Select Folder',fg="brown",bg="#dfdfdf", font=(casfontdir, 12), width=14, height=1, command=sfolder)

    def configstart(*argsv):
        home.destroy()
        config()
    def fontcfgstart(*args):
        home.destroy()
        fontcfg()
    configbt = tk.Button(home, text='Setting',fg="grey",bg="#dfdfdf", font=(casfontdir, 12), width=10, height=1, command=configstart)
    fontbt = tk.Button(home, text='Custom Font',fg="grey",bg="#dfdfdf", font=(casfontdir, 9), width=13, height=1, command=fontcfgstart)
    keybt = tk.Button(home, text='Key Config',fg="grey",bg="#dfdfdf", font=(casfontdir, 12), width=12, height=1, command=openkeycfg)

    book.grid(row=0,column=1)
    folder.grid(row=0,column=2)
    configbt.grid(row=0,column=3)
    fontbt.place(x=home_w,y=45,anchor="ne")
    home.bind(f"{key_dic['home_library']}",openlib)
    home.bind(f"{key_dic['home_book']}",sbook)
    home.bind(f"{key_dic['home_folder']}",sfolder)
    home.bind(f"{key_dic['home_config']}",configstart)
    home.bind("<Escape>",lambda *args:home.destroy())


    
    if smode == "Vertical":
        keybt.place(x=0,y=home_h-85)
    else:
        keybt.place(x=home_w,y=3,anchor="ne")
    
    def changeLib(*args):
        home.destroy()
        switch_library()
    home.bind(f"{key_dic['home_switch']}",changeLib)
    chlbt = tk.Button(home, text='Switch Library',fg="brown",bg="#dfdfdf", font=(casfontdir, 10), width=16, height=1, command=changeLib)
    chlbt.place(x=0,y=67,anchor="w")
    
    home.mainloop()
# =========================================================================================================================
if(__name__=="__main__"):
    home()





