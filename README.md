<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->






<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Yd Cabin Auto Card Test Demo</h3>

  <p align="center">
    无风波浪狂，入夜分明见
    <br />
    
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">目录</h2></summary>
  <ol>
    <li><a href="#参考项目">参考项目</a></li>
    <li>
      <a href="#项目介绍">项目介绍</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#使用说明">使用说明</a>
      <ul>
        <li><a href="#准备工作">准备工作</a></li>
        <li><a href="#配置">配置</a></li>
        <li><a href="#运行">运行</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    
  </ol>
</details>

<!-- ACKNOWLEDGEMENTS -->
## 参考项目

* [CphrAutoCard](https://github.com/cyanot/CphrAutoCard)
* [DingDingAutoPlayCard](https://github.com/1414044032/DingDingAutoPlayCard)
* [TopSup](https://github.com/Skyexu/TopSup)
* [awesome-adb](https://github.com/mzlogin/awesome-adb)


<!-- ABOUT THE PROJECT -->
## 项目介绍


    本项目仅用于交流学习



### Built With

* [Python](https://www.python.org/)
* [pyinstaller](http://www.pyinstaller.org/)



<!-- GETTING STARTED -->
## 使用说明

本项目依赖于android adb工具,推荐逍遥模拟器

### 准备工作

1. 安装 adb  
请到 [官网](https://developer.android.google.cn/studio/command-line/adb) 下载，并配置环境变量    
配置完成后输入以下命令检查：  
![adb](./images/adb.png)  
   
```angular2html
# 获取当前运行包名
adb shell dumpsys window | findstr mCurrentFocus
```

2. 安装 python3
[官网](https://www.python.org/)

  
    
      

### 配置
1. 下载代码
   ```sh
   git clone https://github.com/odison/YdCabinAutoCard.git
   ```
2. 安装依赖
   ```sh
   # 在程序根目录
   pip install -r requirements.txt
   ```
3. 配置  
配置文件是config目录下的 configure.conf  
3.1 百度OCR  
在[百度OCR平台](https://cloud.baidu.com/product/ocr)上创建应用申请 API Key 和 Secret Key  
    ```sh
    # 在配置文件中配置，ocr 普通识别文字接口 每天有 50000 次调用，
    # 但是只有2 rps，所以只能各用各的
    [baidu_api]
    APP_ID = 
    API_KEY = 
    SECRET_KEY = 
    ```
    如果是使用虚拟机，需要设置高精度识别，不然识别出来的班次信息会有所不对，在以下代码修改：
    ```bash
    # 代码目录：common/ocr.py 
    # line 302 可以自行选用 高精度识别还是普通识别
    # 高精度识别 日免费调用 500 次 额度
    response = client.basicAccurate(image_data)
    # 普通识别 日免费调用 50000 次 额度
    # response = client.basicGeneral(image_data)
    ```  

    3.2 邮箱SMTP设置
    ```sh
    [mail]
    # 发件人邮箱地址
    sender = 
    # 收件邮箱地址，自己使用这两个可以用同一个
    receiver = 
    # smtp 服务器地址，需要前往邮箱web版开通smtp发信功能
    host = 
    # smtp 端口
    port = 
    # 邮箱smtp登录用户名
    username = 
    # 注意此处的密码不是邮箱密码，而是开启smtp时候的授权码
    password = 
    ```  
      

### 运行

```sh
python play.py
```





<!-- LICENSE -->
## License

Distributed under the [BSD License](http://www.linfo.org/bsdlicense.html). See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

不要联系我，自己看代码吧……





