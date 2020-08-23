[中文](#关于) | [English](#About)
# KindlePartner 
## About
KindlePartner is a tool to decompose My Clippings.txt file into serval txt files. Each file is a full copy of a particular book note in My Clippings.txt.

## Usage
1. Clone this repository
```
git clone https://github.com/RingWong/KindlePartner.git
```
2. Install the requirement
```
pip install -r requirement.txt
```
3. Run KindlePartner

There is two choices to run KindlePartner: **CMD mode** or **GUI mode**.

- **CMD Mode**

You can learn more about the arguments using the helping message:
```
python start.py --help
```
or just use the simplest command to run KindlePartner:
```
python start.py /path/to/My Clippings.txt /path/to/store/the/splitting/result 
```

- **GUI Mode**
```
python start.py
```
This command will start a GUI window, then you can run KindlePartner just click some buttons.

# KindlePartner

## 关于
使用Kindle进行阅读，阅读期间对书本的标注信息都存放在My Clipping.txt文件中。本项目将My Clipping.txt文件进行分割，按书名生成若干个子文件，每个文件对应My Clipping.txt文件中某一本书的全部标注信息。

## 使用方法
1. 克隆本项目
```
git clone https://github.com/RingWong/KindlePartner.git
```
2. 安装依赖
```
pip install -r requirement.txt
```
3. 运行

有两种运行方式: **CMD**模式 和 **GUI**模式.

- **CMD**模式

使用帮助来了解更多的参数信息:
```
python start.py --help
```
或者只使用最简单的运行方式:
```
python start.py /path/to/My Clippings.txt /path/to/store/the/splitting/result 
```

- **GUI**模式
```
python start.py
```
此命令将打开一个GUI窗口，点击鼠标即可运行。

