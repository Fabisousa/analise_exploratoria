# -*- coding: utf-8 -*-
"""Cópia de MachineLearninCardio_official.2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I7wGYpM8gDlNqI3DVYc0MDU1R50Sheki

##carregando bibliotecas
"""

import pandas as pd
import numpy as np
import seaborn as sns
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as scs

#importando/lendo o arquivo a ser trabalhado com o pandas
mlcardio = pd.read_csv('/content/cardio_train.csv',sep=';')
mlcardio

#excluindo a coluna id
mlcardio = mlcardio.drop(['id'],axis = 1)
#verificando algumas informações
mlcardio.describe()

#alterando as idades de dias para anos aproximadamente
idade = mlcardio['age']
anos = (idade/365).round()
anos = anos.astype('int64')
mlcardio['age'] = anos
mlcardio.head()

#calculando o IMC e adicionando ele a base
IMC = (mlcardio['weight']/(mlcardio['height']/100)**2)
IMC = pd.DataFrame(IMC)
mlcardio['IMC'] = IMC.round()
mlcardio.head()

#colocando como 'valor faltante' nos outliers, pois há algumas inconsistencias nos extremos 
#criando uma função que irá fazer isso:
def exclui_outliers(mlcardio, col_name):
  intervalo = 2*mlcardio[col_name].std()
  media = mlcardio[col_name].mean()
  mlcardio.loc[mlcardio[col_name] < (media - intervalo), col_name] = np.nan
  mlcardio.loc[mlcardio[col_name] > (media + intervalo), col_name] = np.nan

#executando a função nas colunas onde havia erros perceptiveis nos outiliers
numerical_cols = ['height','weight','ap_hi','ap_lo','IMC']
for col in numerical_cols:
  exclui_outliers(mlcardio, col)

#como é possível notar valores negativos foram retirados e valores extremamente altos também
mlcardio.describe()

#porém como a função substitui esses utilier por valores faltantes é possível ver que agora eles aparecem na nossa base

mlcardio.isna().sum()

mlcardio.shape

# e para trabalhar com os algoritmos de machine learning temos que retira-los
mlcardio.dropna(axis = 0, inplace = True)

mlcardio.info()

#há variáveis qe são categóricas e estão aparecendo como inteiras,logo mudaremos os tipos delas para string
mlcardio[['gender','cholesterol',	'gluc',	'smoke',	'alco',	'active'	]] = mlcardio[['gender','cholesterol',	'gluc',	'smoke',	'alco',	'active'	]].astype(str)
mlcardio.info()

#vizualização iniciall de quem tem problema cardiaco(1) e quem não tem no nosso conjunto de dados(0)
sns.countplot('cardio',data=mlcardio)

#pandas.get_dummies () é usado para manipulação de dados. Ele converte dados categóricos em variáveis ​​fictícias ou indicadoras
mlcardio=pd.get_dummies(mlcardio)

mlcardio

mlcardio = mlcardio.drop(['cholesterol_3','gluc_3','smoke_0','alco_0','active_0'],axis = 1)

X = mlcardio.drop(['cardio'], axis=1)
y = mlcardio.cardio

X.head()

y.head()

#normalizar os dados - colocar na mesma escala ou limitar os dados
X = (X - X.min())/(X.max()-X.min())
X.head(10)

from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=5)

"""##Regressão logística"""

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train,y_train)

y_pred = lr.predict(X_test)

lr.predict_proba(X_test)

y_pred

print(accuracy_score(y_test,y_pred)*100,'%')

dic = {1:'positivo',0:'negativo'}

ax = sns.heatmap(confusion_matrix(y_test,y_pred)/1000, annot=True, cmap="RdPu")
plt.ylabel('Previsto')
plt.xlabel('Valor Real')
plt.title('Matriz de confusão na ordem de 10³ \n')

confusao = confusion_matrix(y_test,y_pred)
confusao

#calculando o odds ration
odds = np.exp(lr.coef_)

for i in range(0, len(X.columns)):
    print(X.columns[i],":",odds[0][i])

"""##Random Forest"""

#Random Forest
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

y_predic=clf.predict(X_test)

print(accuracy_score(y_test,y_predic)*100)

sns.barplot(x=X.columns, y=clf.feature_importances_,palette='cool')
plt.xticks(rotation=50)

ax = sns.heatmap(confusion_matrix(y_test,y_predic)/1000, annot=True, cmap="YlGnBu")
plt.ylabel('Previsto')
plt.xlabel('Valor Real')

"""##SMV"""

#SVM
from sklearn.svm import SVC
clf = SVC()
clf.fit(X_train,y_train)

y_predicao=clf.predict(X_test)

print(accuracy_score(y_test,y_predicao)*100)

ax = sns.heatmap(confusion_matrix(y_test,y_predicao)/1000, annot=True, cmap="RdBu")
plt.ylabel('Previsto')
plt.xlabel('Valor Real')
plt.title('Matriz de confusão na ordem de 10³ \n')