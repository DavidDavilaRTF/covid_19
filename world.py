import requests
import pandas
import numpy
from sklearn import linear_model,neighbors,svm,preprocessing,tree,ensemble

class download_file:
    def __init__(self,url_csv,path_folder):
        self.url_csv = url_csv
        self.path_folder = path_folder

    def download(self):
        r = requests.get(self.url_csv)
        filename = self.url_csv.split('/')
        filename = filename[len(filename) - 1]
        fichier = open(self.path_folder + filename,'wb')
        fichier.write(r.content)
        fichier.close()

class analysis:
    def __init__(self,path_folder,url_csv,col_id,col_drop,nb_day):
        self.nb_day = nb_day
        self.path_folder = path_folder
        self.filename = url_csv.split('/')
        self.filename = self.filename[len(self.filename) - 1]
        self.col_id = col_id
        self.mat = pandas.read_csv(self.path_folder + self.filename,sep = ',',engine = 'python')
        self.mat['id'] = ''
        for ci in self.col_id:
            self.mat[ci] = self.mat[ci].apply(lambda x: str(x).lower().replace('nan',''))
            sel = self.mat[ci] != ''
            if sum(sel) > 0:
                self.mat['id'][sel] += self.mat[ci][sel] + '_'
        self.mat['id'] = self.mat['id'].apply(lambda x: x[0:(len(x) - 1)])
        self.mat = self.mat.drop(col_drop, axis = 1)
        self.mat_hot_encoder = pandas.DataFrame()

    def hot_encoder(self):
        enc = preprocessing.OneHotEncoder()
        enc.fit(self.mat[['id']])
        self.mat_hot_encoder = pandas.DataFrame(numpy.array(enc.transform(self.mat[['id']]).toarray()))
        self.mat_hot_encoder.columns = self.mat['id'].unique()

    def diff_date(self):
        self.hot_encoder()
        n_mat = self.mat.drop('id',axis = 1)
        n_mat = numpy.array(n_mat)
        new_case = n_mat[:,1:n_mat.shape[1]] - n_mat[:,0:(n_mat.shape[1] - 1)]
        new_case = numpy.append(n_mat[:,0:1],new_case,axis = 1)
        analyze = new_case[:,0:self.nb_day]
        analyze = numpy.append(analyze,numpy.array(self.mat_hot_encoder),axis = 1)
        for i in range(self.nb_day + 1,new_case.shape[1]+1):
            analyze_i = numpy.append(new_case[:,(i-self.nb_day):i],numpy.array(self.mat_hot_encoder),axis = 1)
            # analyze_i = new_case[:,(i-self.nb_day):i]
            analyze = numpy.append(analyze,analyze_i,axis = 0)
        analyze = pandas.DataFrame(analyze)
        colnames = []
        k = 0
        for i in range(len(analyze.columns)):
            if i < self.nb_day:
                colnames.append(i)
            else:
                colnames.append(self.mat_hot_encoder.columns[k])
                k += 1
        analyze.columns = colnames
        analyze.to_csv('C:\\covid-fr\\datas\\legend.csv',index = False,sep = ';')

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

csv = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']
path_folder = 'C:\\covid-fr\\datas\\'
col_id = [['Province/State','Country/Region']]
col_drop = [['Province/State','Country/Region','Lat','Long']]

for url_csv in csv:
    df = download_file(url_csv,path_folder)
    df.download()

an = analysis(path_folder,csv[0],col_id[0],col_drop[0],11)
an.diff_date()

pc = prediction_covid(10,10)
pc.mesure()
pc.analyze()

while True:
    pass