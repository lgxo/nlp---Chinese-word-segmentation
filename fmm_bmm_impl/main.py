# 读入词典
def readDic():
    dic = list()
    f_dic = open("../dic_cons/dic.txt", "r", encoding="ansi")
    # 设置最大长度
    dic.append(eval(f_dic.readline()))
    # 设置长度序列
    dic.append(list())
    for string in f_dic.readline().split(" "):
        dic[1].append(eval(string))
    # 读入词表
    i = 1
    while True:
        line = f_dic.readline()
        # print(line)
        if line:
            if line == "\n" and i < len(dic[1]) + 1:
                dic.append(list())
                i += 1
                continue
            dic[i] += line.split(" ")[:-1]
        else:
            break
    f_dic.close()
    return dic


# ******************* 之后改为返回索引
# 判断该词是否是词表中的词
def isIn(wd, lst):
    return wd in lst


# 查询词典中对应长度词的位置
def findIndex(lgh, lst):
    while not isIn(lgh, lst):
        lgh -= 1
    return lgh, lst.index(lgh) + 2


def fmm_impl(sent, dic):
    max_len = dic[0]
    len_lst = dic[1]
    seg = list()
    while len(sent) > 0:
        length = min(max_len, len(sent))
        length, idx = findIndex(length, len_lst)
        word = sent[0:length]
        while not isIn(word, dic[idx]):
            if length == 1:
                break
            length, idx = findIndex(length - 1, len_lst)
            word = word[:length]
        seg.append(word)
        sent = sent[length:]
    return seg


def bmm_impl(sent, dic):
    max_len = dic[0]
    len_lst = dic[1]
    seg = list()
    while len(sent) > 0:
        length = min(max_len, len(sent))
        length, idx = findIndex(length, len_lst)
        word = sent[-length:]
        while not isIn(word, dic[idx]):
            if length == 1:
                break
            length, idx = findIndex(length - 1, len_lst)
            word = word[-length:]
        seg.insert(0, word)
        sent = sent[:-length]
    return seg


def genSegFile(dic):
    f_sent = open("resources/199801_sent.txt", "r", encoding="ansi")
    f_fmm = open("seg_FMM.txt", "w", encoding="ansi")
    f_bmm = open("seg_BMM.txt", "w", encoding="ansi")
    while True:
        line = f_sent.readline()
        print(line)
        if line:
            if line == "\n":
                print(line)
            f_fmm.writelines("/ ".join(fmm_impl(line, dic)))
            f_bmm.writelines("/ ".join(bmm_impl(line, dic)))
        else:
            break
    f_sent.close()
    f_fmm.close()
    f_bmm.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # txt = "我宣布中华人民共和国成立了！"
    dictionary = readDic()
    genSegFile(dictionary)
    print("gen seg successfully")
    # print(fmm_impl(txt, dictionary))
    # print(bmm_impl(txt, dictionary))
