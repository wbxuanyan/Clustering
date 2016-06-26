#encoding:utf-8
num0 = raw_input("请输入一组时间序列：")
num1 = num0.replace(' ','')  #去空格
num2 = list(num1)  # 用列表表示，项是字符
num3 = [int(i) for i in num2]   #将每一项转换成整型类型
num4 = raw_input("请再输入一组时间序列：")
num5 = num4.replace(' ','')    #同上
num6 = list(num5)
num7 = [int(i) for i in num6]
print num3    #打印出列表
print num7
print len(num3)-1
print len(num7)-1
dic = {}


def dis(n,m):
    return abs(num3[n]-num7[m])   #计算对应点的欧氏距离


def dtw(n,m,lj_dis = 0):
    if n ==m==0:
        return abs(num3[0]-num7[0])  #左下角点
    elif m == 0 and n>0:      # 计算第一行的累计距离
        for i in range(0,n+1,1):
            lj_dis += abs(num3[i]-num7[0])
    elif n == 0 and m>0:    #计算第一列的累计距离
        for i in range(0,m+1,1):
            lj_dis += abs(num3[0]-num7[i])
    if n>0 and m>0:
            return dic[(n,m)]  #返回之前保存在字典中的值
    return lj_dis


def main():
    for n in range(1,24,1):
        m = 1
        while True:
            dic[(n,m)]= min(dtw(n-1,m),dtw(n,m-1),dtw(n-1,m-1)+ dis(n,m)) + dis(n,m)  #关键递推式
            m = m+1
            if m==24:
                break
        if n ==23 and m ==24:
            lj_dis = dic[(n,m-1)]
            return lj_dis
if __name__ =="__main__":
    main()
    print "两组时间序列相似度为：{}".format(main())
