# coding:utf-8
"""测试不同方法目标IoU性能
"""
import matplotlib as mpl
import pylab as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
font = FontProperties(fname=r"/home/kilox/Downloads/SimHei.ttf", size=12)
x_major_locator = MultipleLocator(1)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)

y1 = [0.96, 0.92, 0.97, 0.92, 0.95,
      0.96, 0.95, 0.89, 0.9, 0.92,
      0.97, 0.91, 0.95, 0.95, 0.95,
      0.71, 0.95, 0.97, 0.95, 0.88]
x1 = range(0, 20)

x2 = range(0, 20)
y2 = [0.96, 0.91, 0.97, 0.92, 0.95,
      0.96, 0.93, 0.89, 0.91, 0.95,
      0.93, 0.94, 0.94, 0.95, 0.96,
      0.71, 0.95, 0.96, 0.95, 0.88]

x4 = range(0, 20)
y4 = [0.96, 0.92, 0.97, 0.92, 0.95,
      0.96, 0.95, 0.89, 0.9, 0.92,
      0.97, 0.91, 0.95, 0.95, 0.95,
      0.71, 0.95, 0.97, 0.95, 0.88]

x3 = range(0, 20)
y3 = [0.96, 0.92, 0.97, 0.92, 0.95,
      0.96, 0.95, 0.89, 0.9, 0.92,
      0.97, 0.91, 0.95, 0.95, 0.95,
      0.71, 0.95, 0.97, 0.95, 0.88]

plt.plot(x1, y1, label='Tfeat', linewidth=1, color='r', marker='o',
         markerfacecolor='blue', markersize=3)
plt.plot(x2, y2, label='ContexDes', linewidth=1, color='g', marker='v',
         markerfacecolor='blue', markersize=3)
plt.plot(x3, y3, label='ORB', linewidth=1, color='b', marker='*',
         markerfacecolor='blue', markersize=3)
plt.plot(x4, y4, label='Hardnet', linewidth=1, color='y', marker='s',
         markerfacecolor='blue', markersize=3)
plt.xlabel(u'图像组号', fontproperties=font)
plt.ylabel(u'配准后IOU', fontproperties=font)
plt.title(u'配准方法对比', fontproperties=font)
plt.legend()
plt.show()

