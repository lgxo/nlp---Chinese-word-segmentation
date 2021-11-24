def readDic():
    dic = list()
    f_dic = open("../dic_cons/dic.txt", "r", encoding="ansi")
    # 设置最大长度
    dic.append(eval(f_dic.readline()))
    # 设置长度序列
    dic .append(list())
    for string in f_dic.readline().split(" "):
        dic[1].append(eval(string))
    # 读入词表
    i = 1
    while True:
        line = f_dic.readline()
        print(line)
        if line:
            if line == "\n" and i < len(dic[1])+1:
                dic.append(list())
                i += 1
                continue
            dic[i] += line.split(" ")[:-1]
        else:
            break
    f_dic.close()
    return dic


def fmm_impl(sent, dic):
    max_len = dic[0]
    len_lst = dic[1]
    seg = list()
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dictionary = readDic()
