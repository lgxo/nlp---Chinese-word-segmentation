import re


# 更新读入的行（去掉短语标记）
def updateLine(li, m):
    l_s = list(li)
    del l_s[m.start():m.end() + 1]
    return "".join(l_s)


# 检查字典分支中是否有该词
def isListContains(dic_bran, word):
    return word in dic_bran


# 将单词加入
def addToDic(dic, token):
    loc = dic[1]
    length = len(token)
    # 如果之前没有length长度的词
    if length not in loc:
        loc.append(length)
        dic.append(list(token.split()))
        if dic[0] < length:
            dic[0] = length
    else:
        lst = dic[loc.index(length) + 2]
        if not isListContains(lst, token):
            lst.append(token)


# 提取词典
def extDic(dic):
    # 打开语料库文件
    f_raw = open("resources/199801_seg&pos.txt", "r", encoding="ansi")
    # 逐行处理
    while True:
        line = f_raw.readline()
        print(line)
        if line:
            # 处理短语标记
            all_found = re.findall(r"\[.*?][A-Za-z]+", line)
            for nt in all_found:
                phrase_marker = re.sub(r"][A-Za-z]+", "", nt)[1:]
                phrase = re.sub(r"/[A-Za-z]+\s*", "", phrase_marker)
                addToDic(dic, phrase)
                # print(phrase)
                # if re.search(r"/", phrase):
                #     print("***************************" + phrase)
                #     exit(0)
            # 处理分词
            itr = re.finditer(r"[^\[\s]\S*/[A-Za-z]+", line)
            for token in itr:
                # 取出词
                word = re.sub("/.*", "", token.group())
                addToDic(dic, word)
                # print(word)
                # if re.search(r"/", word):
                #     print("+++++++++++++++++++++++++++" + word)
                #     exit(0)
        else:
            break
    # 关闭语料库文件
    f_raw.close()


# 构建词典
def conDic(dic):
    # 打开要生成的词表文件
    f_pro = open("dic.txt", "w", encoding="ansi")
    # 写入词表中词的最大长度
    f_pro.write(str(dic[0]) + "\n")
    # f_pro.write("\n")
    # 写入此表中不同词长顺序排列
    f_pro.writelines(re.sub(",", "", str(dic[1])[1:-1]))
    # 统一格式统一处理
    f_pro.write("\n\n")
    for i in range(2, len(dic)):
        z = 0
        for j in range(len(dic[i])):
            z += 1
            f_pro.write(dic[i][j] + " ")
            if z == 100:
                z = 0
        f_pro.write("\n\n")
    # 关闭词表文件
    f_pro.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 第一个元素表示最大长度
    dictionary = [0, []]
    extDic(dictionary)
    conDic(dictionary)
    print("Dictionary constructs successfully")
