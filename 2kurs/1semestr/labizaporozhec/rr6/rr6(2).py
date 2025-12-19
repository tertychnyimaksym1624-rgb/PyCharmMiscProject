from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype=str)
spec = iris[:, 4]
quan_charact = iris[:, :4].astype(float)
fig,ax=plt.subplots(2,2,figsize=(40,20))
#plot00(pie)
iris_types,quantity=np.unique(spec,return_counts=True)
ax[0][0].set_title("percentage of every iris type")
ax[0][0].pie(quantity,labels=iris_types)


#plot01(pie)

sepal_charact=quan_charact[np.argsort(quan_charact[:,0])]
sepal_length_points,sepal_width_points=sepal_charact[:,0],sepal_charact[:,1]

ax[0][1].set_title("relation of sepal length to its width")
ax[0][1].plot(sepal_length_points,sepal_width_points,color="black")
ax[0][1].scatter(sepal_length_points,sepal_width_points,marker="*",color="violet",joinstyle='round')
ax[0][1].set_xlabel("sepal length")
ax[0][1].set_ylabel("sepal width")
ax[0][1].grid()

# plot10(relation of sepal length to sepal witdth)

iris_setosa=quan_charact[np.argsort(quan_charact[:np.where(spec==iris_types[0])[0][-1]][:,2])]#отримуємо масив з усима характеристиками iris_setosa
setosa_petal_lenght,setosa_petal_width=iris_setosa[:,2],iris_setosa[:,3]
ax[1][0].plot(setosa_petal_lenght,setosa_petal_width,label="setosa")
iris_versicolor=quan_charact[np.argsort(quan_charact[np.where(spec==iris_types[1])[0][0]:np.where(spec==iris_types[1])[0][-1]][:,2])+np.where(spec==iris_types[1])[0][0]]#отримуємо масив з усима характеристиками iris_versicolor
versicolor_petal_lenght,versicolor_petal_width=iris_versicolor[:,2],iris_versicolor[:,3]
ax[1][0].plot(versicolor_petal_lenght,versicolor_petal_width,label="versicolor")
iris_virginica=quan_charact[np.argsort(quan_charact[np.where(spec==iris_types[2])[0][0]:np.where(spec==iris_types[2])[0][-1]][:,2])+np.where(spec==iris_types[2])[0][0]]#отримуємо масив з усима характеристиками iris_versicolor
virginica_petal_lenght,virginica_petal_width=iris_virginica[:,2],iris_virginica[:,3]
ax[1][0].plot(virginica_petal_lenght,virginica_petal_width,label="virginica")
ax[1][0].grid()
ax[1][0].set_title("relation of petal length and width of every iris type")
ax[1][0].set_xlabel("petal length")
ax[1][0].set_ylabel("petal width")
ax[1][0].legend()

#plot11(boxes)
data_to_plot = []
for s in iris_types:
    sepal_width_for_species = quan_charact[spec == s, 1]
    data_to_plot.append(sepal_width_for_species)

bplot = ax[1, 1].boxplot(data_to_plot, tick_labels=iris_types, patch_artist=True)
manual_colors = ['cornflowerblue', 'orange', 'mediumseagreen']


for patch, color in zip(bplot['boxes'], manual_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax[1, 1].set_title('sepal width distribution')
ax[1, 1].set_ylabel('width')
ax[1, 1].grid(True, axis='y')


plt.show()