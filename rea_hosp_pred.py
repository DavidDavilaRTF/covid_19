import requests
import pandas
import numpy
import datetime
from sklearn import linear_model,neighbors,svm,preprocessing,tree,ensemble

class analysis:
    def __init__(self,path_folder,url_csv,col_id,col_drop,nb_day):
        self.nb_day = nb_day
        self.path_folder = path_folder
        self.filename = url_csv.split('/')
        self.filename = self.filename[len(self.filename) - 1]
        self.col_id = col_id
        self.mat = pandas.read_csv(self.path_folder + self.filename,sep = ';',engine = 'python')
        self.mat = self.mat[['dep','sexe','jour','hosp','rea','rad','dc']]
        self.mat_hot_encoder = pandas.DataFrame()
        self.mat_hosp = pandas.DataFrame()
        self.mat_rea = pandas.DataFrame()
        self.mat_rad = pandas.DataFrame()
        self.mat_dc = pandas.DataFrame()

    def in_1_line(self,x):
        temp_hosp = pandas.DataFrame()
        temp_hosp['dep'] = [x['dep'].iloc[0]]
        temp_hosp['sexe'] = [x['sexe'].iloc[0]]
        temp_rea = pandas.DataFrame()
        temp_rea['dep'] = [x['dep'].iloc[0]]
        temp_rea['sexe'] = [x['sexe'].iloc[0]]
        temp_rad = pandas.DataFrame()
        temp_rad['dep'] = [x['dep'].iloc[0]]
        temp_rad['sexe'] = [x['sexe'].iloc[0]]
        temp_dc = pandas.DataFrame()
        temp_dc['dep'] = [x['dep'].iloc[0]]
        temp_dc['sexe'] = [x['sexe'].iloc[0]]
        for i in range(len(x)):
            jour = x['jour'].iloc[i]
            temp_hosp[jour] = x['hosp'].iloc[i]
            temp_rea[jour] = x['rea'].iloc[i]
            temp_rad[jour] = x['rad'].iloc[i]
            temp_dc[jour] = x['dc'].iloc[i]
        self.mat_hosp = self.mat_hosp.append(temp_hosp)
        self.mat_rea = self.mat_rea.append(temp_rea)
        self.mat_rad = self.mat_rad.append(temp_rad)
        self.mat_dc = self.mat_dc.append(temp_dc)


    def hot_encoder(self):
        enc = preprocessing.OneHotEncoder()
        enc.fit(self.mat[['id']])
        self.mat_hot_encoder = pandas.DataFrame(numpy.array(enc.transform(self.mat[['id']]).toarray()))
        self.mat_hot_encoder.columns = self.mat['id'].unique()

    def diff_date(self):
        sex = self.mat['sexe'].unique()
        dep = self.mat['dep'].unique()
        for s in sex:
            for d in dep:
                if str(d) != 'nan':
                    print(str(s) + ' - ' + str(d))
                    sel = numpy.array(self.mat['sexe'] == s) * numpy.array(self.mat['dep'] == d)
                    self.in_1_line(self.mat[sel])
        self.mat_hosp.to_csv('C:\\covid-fr\\datas\\hosp.csv',index = False,sep = ';')
        self.mat_rea.to_csv('C:\\covid-fr\\datas\\rea.csv',index = False,sep = ';')
        self.mat_rad.to_csv('C:\\covid-fr\\datas\\rad.csv',index = False,sep = ';')
        self.mat_dc.to_csv('C:\\covid-fr\\datas\\dc.csv',index = False,sep = ';')

class prediction_covid:
    def __init__(self,cv,nb_day):
        self.covid = pandas.read_csv('C:\\covid-fr\\datas\\legend.csv',sep = ';',engine = 'python')
        self.covid_train = pandas.DataFrame()
        self.covid_test = pandas.DataFrame()
        self.mes = pandas.DataFrame()
        self.mes['lm'] = [0]
        self.mes['tree'] = [0]
        self.mes['rf'] = [0]
        self.mes['knn'] = [0]
        self.cv = cv
        self.nb_day = nb_day

    def create_train_test(self):
        sel_train = numpy.random.choice(range(len(self.covid)),size = int(0.9 * len(self.covid)),replace = False)
        self.covid_train = self.covid.iloc[sel_train]
        self.covid_train.index = numpy.array(range(len(self.covid_train)))
        self.covid_test = self.covid.drop(sel_train,axis = 0)
        self.covid_test.index = numpy.array(range(len(self.covid_test)))

    def mesure(self):
        for i in range(self.cv):
            self.create_train_test()
            y_train = self.covid_train[[str(self.nb_day)]]
            y_test = self.covid_test[[str(self.nb_day)]]
            x_train = self.covid_train.drop([str(self.nb_day)],axis = 1)
            x_test = self.covid_test.drop([str(self.nb_day)],axis = 1)
            y_test = numpy.array(y_test)[:,0]

            model = linear_model.LinearRegression()
            model.fit(x_train,y_train)
            pred = model.predict(x_test)[:,0]
            self.mes['lm'].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv

            model = tree.DecisionTreeClassifier()
            model.fit(x_train,y_train)
            pred = model.predict(x_test)
            self.mes['tree'].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv

            model = ensemble.RandomForestClassifier()
            model.fit(x_train,y_train)
            pred = model.predict(x_test)
            self.mes['rf'].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv

            model = neighbors.KNeighborsClassifier()
            model.fit(x_train,y_train)
            pred = model.predict(x_test)
            self.mes['knn'].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv

            print(i)
            print(self.mes)

    def analyze(self):
        y = self.covid[[str(self.nb_day)]]
        x = self.covid.drop([str(self.nb_day)],axis = 1)
        model = linear_model.LinearRegression()
        model.fit(x,y)
        R2 = model.score(x,y)
        coeff = model.coef_
        cnst = model.intercept_
        mat_coef = pandas.DataFrame()
        mat_coef['col'] = list(x.columns) + ['cnst']
        mat_coef['coeff'] = numpy.append(coeff,cnst)
        mat_coef['R2'] = R2
        mat_coef.to_csv('C:\\covid-fr\\datas\\coeff.csv',index = False,sep = ';')

path_folder = 'C:\\covid-fr\\datas\\'
col_id = [['Province/State','Country/Region']]
col_drop = [['Province/State','Country/Region','Lat','Long']]
date = datetime.datetime.now()
date = date.strftime('%d.%m.%Y')
csv = ['region_covid_' + date + '.csv']

an = analysis(path_folder,csv[0],col_id[0],col_drop[0],11)
an.diff_date()

# pc = prediction_covid(10,10)
# pc.mesure()
# pc.analyze()

# while True:
#     pass