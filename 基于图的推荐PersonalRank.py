#-*-coding:utf-8-*-

def PersonalRank(G, alpha, root, max_step):
    rank = dict()  
    rank = {x:0 for x in G.keys()}
    rank[root] = 1  
    #��ʼ����  
    for k in range(max_step):  
        tmp = {x:0 for x in G.keys()}  
        #ȡ�ڵ�i�����ĳ���β�ڵ㼯��ri  
        for i, ri in G.items():  #i�Ƕ��㡣ri�����������Ķ��㼫��ߵ�Ȩ��
            #ȡ�ڵ�i�ĳ��ߵ�β�ڵ�j�Լ���E(i,j)��Ȩ��wij, �ߵ�Ȩ�ض�Ϊ1�����ⲻ��ʵ������  
            for j, wij in ri.items():   #j��i�����Ӷ��㣬wij��Ȩ��
                #i��j������һ����ߵ��׽ڵ㣬�����Ҫ����ͼ�ҵ�j����ߵ��׽ڵ㣬  
                #����������̾��Ǵ˴���2��forѭ����һ�α�������һ������  
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))  
        #����ÿ�����߶��Ǵ�root�ڵ���������root�ڵ��Ȩ����Ҫ����(1 - alpha)  
        #�ڡ��Ƽ�ϵͳʵ�����ϣ����߰���һ�����for j, wij in ri.items()���ѭ���£�����Ϊ�������⡣  
        tmp[root] += (1 - alpha)  
        rank = tmp  
  
        #���ÿ�ε���������ڵ��Ȩ��  
        print 'iter:  ' + str(k) + "\t",
        for key, value in rank.items():  
            print "%s:%.3f, \t"%(key, value),  
        print  
  
    return rank  
  

'''
��������G��ʾ����ͼ����A����ʾ�ڵ㣬��߶�Ӧ���ֵ��key�����ӵĶ��㣬value��ʾ�ߵ�Ȩ��
'''
if __name__ == '__main__':
    G = {'A' : {'a' : 1, 'c' : 1},  
         'B' : {'a' : 1, 'b' : 1, 'c':1, 'd':1},  
         'C' : {'c' : 1, 'd' : 1},  
         'a' : {'A' : 1, 'B' : 1},  
         'b' : {'B' : 1},  
         'c' : {'A' : 1, 'B' : 1, 'C':1},  
         'd' : {'B' : 1, 'C' : 1}}  
  
    PersonalRank(G, 0.85, 'A', 100)  