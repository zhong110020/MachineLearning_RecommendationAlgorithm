from __future__ import division
import os
import operator
import read as read

# 获得用户偏好
def get_up(item_cate, input_file):
    """
    1)得到每个用户评分4.0以上电影的信息。
    2)获得这些电影的种类。
    3)判定用户对这些种类的喜好程度，进行打分，并累加。
    分值=用户评分 * 时间权重 * 种类占比。
    比如用户给a电影打了4分，时间权重为0.1，该电影动作类占比0.5，则对动作类的喜好程度上升0.2。
    4)得到用户最喜欢的前两个种类。
    """
    linenum = 0
    if not os.path.exists(input_file):
        return {}
    record = {}
    up = {}
    score_thr = 4.0
    topk = 2
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if(len(item) < 4):
            continue
        userid,itemid,rating,time = item[0],item[1],float(item[2]),int(item[3])
        if rating < score_thr:
            continue
        if itemid not in item_cate:
            continue
        time_score = get_time_score(time)
        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0
            record[userid][fix_cate] += rating * time_score * item_cate[itemid][fix_cate]
    fp.close()
    for userid in record:
        if userid not in up:
            up[userid]=[]
        total = 0
        for combo in sorted(record[userid].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
            up[userid].append((combo[0],combo[1]))
            total += combo[1]
        for index in range(len(up[userid])):
            up[userid][index] = (up[userid][index][0],round(up[userid][index][1]/total,3))
    return up

def get_time_score(time):
    """
    返回时间的得分
    """
    fix_time_stamp = 1476086345
    total_sec = 24*60*60
    delta = (fix_time_stamp-time)/total_sec/100
    return round(1/(1+delta),3)

def recom(cate_item_sort,up,userid,topk=10):
    """
    获得用户id后，我们只需查询用户偏好的种类，按照此种类查找cate_item_sort字典获得排名靠前的电影即可。
    """
    if userid not in up:
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for zuhe in up[userid]:
        cate = zuhe[0]
        ratio = zuhe[1]
        num = int(topk*ratio) + 1
        if cate not in cate_item_sort:
            continue
        recom_list = cate_item_sort[cate][:num]
        recom_result[userid] += recom_list
    return  recom_result


def run_main():
    avg_score = read.get_avg("data/ratings.txt")
    item_cate, cate_item_sort = read.get_item_cate("data/movies.txt",avg_score)
    up = get_up(item_cate,"data/ratings.txt")
    print(len(up))
    print(up["1"])
    print(recom(cate_item_sort,up,"1"))


if __name__ == "__main__":
    run_main()