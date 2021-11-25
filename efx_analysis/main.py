import statistics
import re


def updateRef(r, s):
    r_lst = list(r)
    nt = re.sub(r"][A-Za-z]+", "", s.group())
    r_lst[s.start():s.end()] = re.sub(r"/[A-Za-z]+\s*", "", nt[1:]) + "/ "
    return "".join(r_lst)


def factorCount(seg, ref):
    seg_lst = re.split(r"/ ", seg)[:-1]
    lgh = len("".join(seg_lst))
    # 参考分词结果处理（重点在于短语标记）
    nt = re.search(r"\[.*?][A-Za-z]+", ref)
    while nt is not None:
        ref = updateRef(ref, nt)
        nt = re.search(r"\[.*?][A-Za-z]+", ref)
    ref_lst = re.split(r"/[A-Za-z]*\s*", ref)[:-1]
    right = 0
    ref_len, seg_len = 0, 0
    ref_idx, seg_idx = 0, 0
    flag = True
    # 循环终止条件
    seg_len += len(seg_lst[seg_idx])
    ref_len += len(ref_lst[ref_idx])
    while ref_idx < len(ref_lst) and seg_idx < len(seg_lst):
        if seg_len == ref_len:
            if flag:
                right += 1
            if seg_len == lgh:
                break
            seg_idx += 1
            ref_idx += 1
            seg_len += len(seg_lst[seg_idx])
            # if ref_idx
            ref_len += len(ref_lst[ref_idx])
            flag = True
        elif seg_len < ref_len:
            seg_idx += 1
            seg_len += len(seg_lst[seg_idx])
            flag = False
        else:
            ref_idx += 1
            ref_len += len(ref_lst[ref_idx])
            flag = False
    return right, len(seg_lst), len(ref_lst)


def evaluate():
    right_f, right_b = 0, 0
    seg_f, seg_b = 0, 0
    ref_f, ref_b = 0, 0
    f_ref = open("../dic_cons/resources/199801_seg&pos.txt", "r", encoding="ansi")
    f_fmm = open("../fmm_bmm_impl/seg_FMM.txt", "r", encoding="ansi")
    f_bmm = open("../fmm_bmm_impl/seg_BMM.txt", "r", encoding="ansi")
    while True:
        line_ref = f_ref.readline()
        print(line_ref)
        if line_ref:
            if line_ref == "\n":
                f_fmm.readline()
                f_bmm.readline()
                continue
            right_f_incre, seg_f_incre, ref_f_incre = factorCount(f_fmm.readline(), line_ref)
            right_b_incre, seg_b_incre, ref_b_incre = factorCount(f_bmm.readline(), line_ref)
            right_f += right_f_incre
            right_b += right_b_incre
            seg_f += seg_f_incre
            seg_b += seg_b_incre
            ref_f += ref_f_incre
            ref_b += ref_b_incre
        else:
            break
    f_ref.close()
    f_fmm.close()
    f_bmm.close()
    p_f, r_f = right_f / seg_f, right_f / ref_f
    f_f = statistics.harmonic_mean([p_f, r_f])
    p_b, r_b = right_b / seg_b, right_b / ref_b
    f_b = statistics.harmonic_mean([p_b, r_b])
    return p_f, r_f, f_f, p_b, r_b, f_b


def genScore(sco):
    # sco: (p_val_f, r_val_f, f_val_f, p_val_b, r_val_f_b, f_val_b)
    f_sco = open("score.txt", "w", encoding="ansi")
    f_sco.write("\t\tFMM:\t\t\tBMM:\n\n")
    f_sco.write(f"precision:\t\t{sco[0]}\t{sco[3]}\n\n")
    f_sco.write(f"recall:\t\t{sco[1]}\t{sco[4]}\n\n")
    f_sco.write(f"F:\t\t{sco[2]}\t{sco[5]}")
    f_sco.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # r = "19980101-07-002-073/m  那/r  是/v  他们/r  如雷似火/l  、/w  震天动地/i"
    # s = "19980101-07-002-073/ 那/ 是/ 他们/ 如雷似火/ 、/ 震天动地/ "
    # a = factorCount(s, r)
    # print(a)
    score = evaluate()
    print("evaluate successfully")
    genScore(score)
