import numpy as np
from matplotlib import pyplot as plt
import SMA

'''适应度函数'''
def fun(X):
    Results = np.sum(X ** 2)
    return Results


'''主函数 '''
# 设置参数
pop = 30  # 种群数量
MaxIter = 500  # 最大迭代次数
dim = 2  # 维度
lb = -10 * np.ones(dim)  # 下边界
ub = 10 * np.ones(dim)  # 上边界
# 调用SMA算法
GbestScore, GbestPositon, Curve = SMA.SMA(pop, dim, lb, ub, MaxIter, fun)
print('最优适应度值：', GbestScore)
print('最优解[x1,x2]：', GbestPositon)

# 绘制适应度曲线
plt.figure(1)
plt.plot(Curve, 'r-', linewidth=2)
plt.xlabel('Iteration', fontsize='medium')
plt.ylabel("Fitness", fontsize='medium')
plt.grid()
plt.title('SMA', fontsize='large')
plt.show()