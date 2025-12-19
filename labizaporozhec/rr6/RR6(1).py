import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype='str')
spec = iris[:, 4]
quan_charact = iris[:, :4].astype(float)
fig, ax=plt.subplots(2,1, figsize=(40,20))
# first plot(sepal leght distribution)
sepal_length,sepal_quantity= np.unique(quan_charact[:,0],return_counts=True)
ax[0].bar(sepal_length,sepal_quantity,width=0.1,color="blue",edgecolor="black",linewidth=1)
ax[0].set_xlabel("sepall length")
ax[0].set_ylabel("quantity")
ax[0].set_xticks(sepal_length)
#second plot(petal length distribution)
sepal_widht,quantity=np.unique(quan_charact[:,2], return_counts=True)
ax[1].bar(sepal_widht,quantity,width=0.1,color="green",edgecolor="black",linewidth=1)
ax[1].set_xlabel("sepal width")
ax[1].set_ylabel("quantity")
ax[1].set_xticks(sepal_widht)
plt.show()
