import numpy as np
import matplotlib.pyplot as plt

y_axis = [8725,16750,26349,29074,32926,34863,39131,44981,52530,59313,67582,69230]
#x_axis = range(len(y_axis))
x_axis = ['rrc00','rrc01','rrc03','rrc04','rrc05','rrc06','rrc07','rrc10','rrc11','rrc13','rrc14','rrc16']
width_n = 0.8
bar_color = 'blue'

plt.bar(x_axis, y_axis, width=width_n, color=bar_color, align='center')
#plt.show()
plt.savefig('test1.png')

plt.clf()
plt.cla()
plt.close()

y_axis = [25,750,349,74,926,63,131,981,530,313,582,230]
#x_axis = range(len(y_axis))
x_axis = ['rrc00','rrc01','rrc03','rrc04','rrc05','rrc06','rrc07','rrc10','rrc11','rrc13','rrc14','rrc16']
width_n = 0.8
bar_color = 'red'

plt.bar(x_axis, y_axis, width=width_n, color=bar_color, align='center')
#plt.show()
plt.savefig('test2.png')
