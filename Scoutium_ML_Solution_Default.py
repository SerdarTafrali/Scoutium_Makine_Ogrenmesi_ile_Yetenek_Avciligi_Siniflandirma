################################################################
# Scoutium Makine Öğrenmesi ile Yetenek Avcılığı Sınıflandırma
################################################################

"""
- İş Problemi:

Scoutlar tarafından izlenen futbolcuların özelliklerine verilen puanlara göre,
oyuncuların hangi sınıf (average, highlighted) oyuncu olduğunu tahminleme.

- Veriseti Hikayesi:

Veri seti Scoutium’dan maçlarda gözlemlenen futbolcuların özelliklerine göre,
scoutların değerlendirdikleri futbolcuların, maç içerisinde puanlanan
özellikleri ve puanlarını içeren bilgilerden oluşmaktadır.

attributes: Oyuncuları değerlendiren kullanıcıların bir maçta izleyip değerlendirdikleri her oyuncunun
özelliklerine verdikleri puanları içeriyor. (bağımsız değişkenler)

potential_labels: Oyuncuları değerlendiren kullanıcıların her bir maçta
 oyuncularla ilgili nihai görüşlerini içeren potansiyel etiketlerini içeriyor. (hedef değişken)

- Veriseti Hakkında:

9 Değişken, 10730 Gözlem, 0.65 mb

Değişkenler:

task_response_id: Bir scoutun bir maçta bir takımın kadrosundaki tüm oyunculara dair değerlendirmelerinin kümesi.

match_id: İlgili maçın id'si.

evaluator_id: Değerlendiricinin(scout'un) id'si.

player_id: İlgili oyuncunun id'si.

position_id: İlgili oyuncunun o maçta oynadığı pozisyonun id'si.
1- Kaleci
2- Stoper
3- Sağ bek
4- Sol bek
5- Defansif orta saha
6- Merkez orta saha
7- Sağ kanat
8- Sol kanat
9- Ofansif orta saha
10- Forvet

analysis_id: Bir scoutun bir maçta bir oyuncuya dair özellik değerlendirmelerini içeren küme.
attribute_id: Oyuncuların değerlendirildiği her bir özelliğin id'si.
attribute_value: Bir scoutun bir oyuncunun bir özelliğine verilen değer(puan).
potential_label: Bir scoutun bir maçta bir oyuncuyla ilgili nihai kararını belirten etiket. (hedef değişken)

"""

## Importing Dataset, Required Library and Functions:

import pandas as pd
import numpy as np
from sklearn.model_selection import *
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import cross_val_predict
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


## Data Preparation

### Görev 1: scoutium_attributes.csv ve scoutium_potential_labels.csv dosyalarını okutunuz.

df = pd.read_csv("DSMLBC12/Ödev Çözümleri/ML3/Scoutium Makine Öğrenmesi ile Yetenek Avcılığı Sınıflandırma/scoutium_attributes.csv", sep=";")
df.head()
df.shape
df2 = pd.read_csv("DSMLBC12/Ödev Çözümleri/ML3/Scoutium Makine Öğrenmesi ile Yetenek Avcılığı Sınıflandırma/scoutium_potential_labels.csv", sep=";")
df2.head()
df2.shape

# Görev 2: Okutmuş olduğumuz csv dosyalarını merge fonksiyonunu kullanarak birleştirelim.
# ("task_response_id", 'match_id', 'evaluator_id' "player_id" olmak üzere
#  4 adet değişken üzerinden birleştirme işlemini gerçekleştiriniz.)

dff = pd.merge(df, df2, how='left', on=["task_response_id", 'match_id', 'evaluator_id', "player_id"])

# Görev 3: position_id içerisindeki Kaleci (1) sınıfını verisetinden kaldırınız.

dff = dff[dff["position_id"] != 1]

# Görev 4: potential_label içerisindeki below_average sınıfını verisetinden kaldırınız.
# ( below_average sınıfı  tüm verisetinin %1'ini oluşturur)

dff = dff[dff["potential_label"] != "below_average"]

# Görev 5: Oluşturduğunuz veri setinden “pivot_table” fonksiyonunu kullanarak bir tablo oluşturunuz.
# Bu pivot table'da her satırda bir oyuncu olacak şekilde manipülasyon yapınız.

# Adım 1: İndekste “player_id”,“position_id” ve “potential_label”,  sütunlarda “attribute_id” ve
# değerlerde scout’ların oyunculara verdiği puan “attribute_value” olacak şekilde pivot table’ı oluşturunuz.

pt = pd.pivot_table(dff, values="attribute_value", columns="attribute_id", index=["player_id","position_id","potential_label"])

# Adım 2: “reset_index” fonksiyonunu kullanarak index hatasından kurtulunuz ve
# “attribute_id” sütunlarının isimlerini stringe çeviriniz.

pt = pt.reset_index(drop=False)
pt.columns = pt.columns.map(str)

################################################################
# Görev 6:  Label Encoder fonksiyonunu kullanarak “potential_label” kategorilerini
# (average, highlighted) sayısal olarak ifade ediniz.
################################################################

le = LabelEncoder()
pt["potential_label"] = le.fit_transform(pt["potential_label"])


################################################################
# Görev 7: Sayısal değişken kolonlarını “num_cols” adıyla bir listeye atayınız.
################################################################

num_cols = pt.columns[3:]


################################################################
# Görev 8: Kaydettiğiniz bütün “num_cols” değişkenlerindeki veriyi ölçeklendirmek için standardScaler uygulayınız.
################################################################

scaler = StandardScaler()
pt[num_cols] = scaler.fit_transform(pt[num_cols])


################################################################
# Görev 9: Elimizdeki veri seti üzerinden minimum hata ile futbolcuların potansiyel etiketlerini tahmin eden bir
# makine öğrenmesi modeli geliştiriniz.
################################################################

y = pt["potential_label"]
X = pt.drop(["potential_label", "player_id"], axis=1)

models = [('LR', LogisticRegression()),
                   ('KNN', KNeighborsClassifier()),
                   #("SVC", SVC()),
                   #("CART", DecisionTreeClassifier()),
                   ("RF", RandomForestClassifier()),
                   #('Adaboost', AdaBoostClassifier()),
                   ('GBM', GradientBoostingClassifier()),
                   ('XGBoost', XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
                   #('CatBoost', CatBoostClassifier(verbose=False)),
              ("LightGBM", LGBMClassifier())]


import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=ConvergenceWarning)
warnings.simplefilter(action="ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")



for name, model in models:
    print(name)
    for score in ["roc_auc", "f1", "precision", "recall", "accuracy"]:
        cvs = cross_val_score(model, X, y, scoring=score, cv=10).mean()
        print(score+" score:"+str(cvs))

# Hiperparametre Optimizasyonu:

lgbm_model = LGBMClassifier(random_state=46)
lgbm_params = {"learning_rate": [0.01, 0.1],
               "n_estimators": [500, 1500],
               "colsample_bytree": [0.5, 0.7, 1]
             }

lgbm_gs_best = GridSearchCV(lgbm_model,
                            lgbm_params,
                            cv=3,
                            n_jobs=-1,
                            verbose=True).fit(X, y)

final_model = lgbm_model.set_params(**lgbm_gs_best.best_params_).fit(X, y)
rmse = np.mean(np.sqrt(-cross_val_score(final_model, X, y, cv=5, scoring="neg_mean_squared_error")))

print("LightGBM")
for score in ["roc_auc", "f1", "precision", "recall", "accuracy"]:
    cvs = cross_val_score(final_model, X, y, scoring=score, cv=10).mean()
    print(score + " score:" + str(cvs))

# Bu durumda base modelin skoru daha iyi demektir. Base parametreler ile ilerlemeyi tercih ederiz.

################################################################
# Görev 10: Değişkenlerin önem düzeyini belirten feature_importance fonksiyonunu kullanarak özelliklerin sıralamasını çizdiriniz.
################################################################

# feature importance
def plot_importance(model, features, num=len(X), save=False):

    feature_imp = pd.DataFrame({"Value": model.feature_importances_, "Feature": features.columns})
    plt.figure(figsize=(10, 10))
    sns.set(font_scale=1)
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value", ascending=False)[0:num])
    plt.title("Features")
    plt.tight_layout()
    plt.show()
    if save:
        plt.savefig("importances.png")

model = LGBMClassifier()
model.fit(X, y)

plot_importance(model, X)

