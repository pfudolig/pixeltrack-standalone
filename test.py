import matplotlib.pyplot as plt

x = [0,1,2,3,4]
y = [5,6,7,8,9]

plt.plot(x,y,'o',linestyle='solid')
plt.show()
plt.savefig('test.png')
plt.close()