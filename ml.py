import sklearn
import numpy
import xgboost
import pandas
from sklearn import linear_model,neighbors,svm,preprocessing,tree,ensemble

class pprocessing:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def one_hot_encoder(self):
        col_str = []
        for col in self.x:
            sel_str = self.x[col].apply(lambda x: isinstance(x,str))
            if sum(sel_str) > 0:
                col_str.append(col)
        enc = preprocessing.OneHotEncoder()
        enc.fit(self.x[col_str])
        enc_pd = pandas.DataFrame(numpy.array(enc.transform(self.x[col_str]).toarray()))
        self.x = self.x.drop(col_str,axis = 1)
        self.x = pandas.concat([self.x,enc_pd],axis = 1)

    def standardization(self):
        scaler = preprocessing.StandardScaler()
        scaler.fit(self.x)
        self.x = scaler.transform(self.x)
        self.x = pandas.DataFrame(self.x)
    
    def normalization(self):
        scaler = preprocessing.Normalizer()
        scaler.fit(self.x)
        self.x = scaler.transform(self.x)
        self.x = pandas.DataFrame(self.x)

class ml:
    def __init__(self,x,y,pct_test,kernel_svm = '',xgboost_reg = ''):
        sel_train = numpy.random.choice(range(len(x)),size = int((1 - pct_test) * len(x)),replace = False)
        self.x_train = x.iloc[sel_train]
        self.x_train.index = numpy.array(range(len(self.x_train)))
        self.x_test = x.drop(sel_train,axis = 0)
        self.x_test.index = numpy.array(range(len(self.x_test)))
        self.y_train = y.iloc[sel_train]
        self.y_test = y.drop(sel_train,axis = 0)
        self.kernel_svm = kernel_svm
        self.xgboost_reg = xgboost_reg
    
    def lm_predict(self):
        model = linear_model.LinearRegression()
        model.fit(self.x_train,self.y_train)
        return model.predict(x_test)

    def lasso_predict(self):
        model = linear_model.Lasso()
        model.fit(self.x_train,self.y_train)
        return model.predict(self.x_test)

    def svm_predict(self):
        model = svm.SVC(kernel=self.kernel_svm)
        sel = numpy.array(self.y_train[self.y_train.columns[0]] == 0)
        self.y_train[self.y_train.columns[0]][sel] = -1
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

    def logistic_predict(self):
        model = linear_model.LogisticRegression()
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

    def tree_predict(self):
        model = tree.DecisionTreeClassifier()
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

    def rf_predict(self):
        model = ensemble.RandomForestClassifier()
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

    def knn_predict(self):
        model = neighbors.KNeighborsClassifier()
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

    def xgboost_predict(self):
        model = xgboost.XGBRegressor(objective=self.xgboost_reg, random_state=42)
        model.fit(self.x_train,self.y_train)
        return model.predict_proba(self.x_test)

x = pandas.DataFrame()
x['a'] = ['a','b','c','d','e','a','b','c','d','e']
x['b'] = [1,2,3,4,5,6,7,8,9,10]
x['c'] = ['a','b','c','d','e','a','b','c','d','e']
y = pandas.DataFrame()
y['res'] = [1,1,1,1,1,0,0,0,0,0]
pp = pprocessing(x = x,y = y)
pp.one_hot_encoder()
pp.normalization()
an = ml(x=pp.x,y=pp.y,pct_test = 0.2)
print(an.tree_predict())
