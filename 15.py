
# step 1: ask user for calculation to be performed
# 第一步：选择需要执行的计算
operation = input("Would you like to add/subtract/multiply/divide? ").lower()
# 你要选择加法/减法/乘法/除法
# step 2: ask for numbers, alert order matters for subtracting and dividing
# 第二步：请求数字，对于减法和除法，警惕顺序很重要
if operation == "subtract" or operation == "divide":
    # 如果选择了除法或者减法
    print("You chose { }.".format(operation))
    print("Please keep in mind that the order of your numbers matter.")
# 请注意数字的顺序非常重要
num1 = input("What is the first number? ")
num2 = input("What is the second number? ")
# step 3: setup try/except for mathematical operation
# 第三步：为数学运算搭建Try/Except
try:
    # step 3a: immediately try to convert numbers input to floats
    # 3a步：立即将用户输入的数字转换为浮点型
    num1, num2 = float(num1), float(num2)
    # step 3b: perform operation and print result
    # 3b步：执行运算并打印结果
    if operation == "add":
        result = num1 + num2
        # print("{ } + { } = { }".format(num1, num2, result))
        print(result)
    elif operation == "subtract":
        result = num1 - num2
        print("{ } - { } = { }".format(num1, num2, result))
    elif operation == "multiply":
        
        result = num1 * num2
        print("{ } * { } = { }".format(num1, num2, result))
    elif operation == "divide":
        result = num1 / num2
        print("{ } / { } = { }".format(num1, num2, result))
    else:
        # else will be hit if they didn't chose an option correctly
        # 如果他们没有正确选择选项
        print("Sorry, but '{ }' is not an option.".format(operation))
except:
    # steb 3c: print error   #3c步：打印报错
    print("Error: Improper numbers used. Please try again.")

exit(0)
url = 'https://mfm.video.qq.com/danmu'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept-Encoding': 'gzip',
}
param = {
    'target_id': '2214904629',
    'timestamp': 0
}
page = requests.get(url=url, headers=headers, params=param).text
print(page)

# 导入所需要的库


class analyse:

    # 定义保存图片函数
    def save_image(self, image, addr, num):
        address = addr + str(num) + '.jpg'
        cv2.imwrite(address, image)
        print('生成成功')

    # 设置生成帧数
    def getImg(self, a, src):
        print('开始读取')
        # 读取视频文件
        video = cv2.VideoCapture(src)
        # 获取帧率和指定秒数帧
        index = a*video.get(cv2.CAP_PROP_FPS)
        # 读取指定秒数的帧
        video.set(cv2.CAP_PROP_POS_FRAMES, index)
        # 读帧
        if video.isOpened():
            success, frame = video.read()
            print('开始生成')
            self.save_image(self, frame, './image/', a)
