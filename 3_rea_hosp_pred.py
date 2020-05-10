import requests
import pandas
import numpy
import datetime
from sklearn import linear_model,neighbors,svm,preprocessing,tree,ensemble
import os

class analysis:
    def __init__(self,path_folder,url_csv,col_id,col_drop,nb_day_analyze):
        self.nb_day_analyze = nb_day_analyze
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
        temp_rea = pandas.DataFrame()
        temp_rea['dep'] = [x['dep'].iloc[0]]
        temp_rad = pandas.DataFrame()
        temp_rad['dep'] = [x['dep'].iloc[0]]
        temp_dc = pandas.DataFrame()
        temp_dc['dep'] = [x['dep'].iloc[0]]
        for i in range(len(x)):
            jour = x['jour'].iloc[i]
            temp_hosp[jour] = [x['hosp'].iloc[i]]
            temp_rea[jour] = [x['rea'].iloc[i]]
            temp_rad[jour] = [x['rad'].iloc[i]]
            temp_dc[jour] = [x['dc'].iloc[i]]
        self.mat_hosp = self.mat_hosp.append(temp_hosp)
        self.mat_rea = self.mat_rea.append(temp_rea)
        self.mat_rad = self.mat_rad.append(temp_rad)
        self.mat_dc = self.mat_dc.append(temp_dc)

    def hot_encoder(self):
        enc = preprocessing.OneHotEncoder()
        enc.fit(self.mat[['id']])
        self.mat_hot_encoder = pandas.DataFrame(numpy.array(enc.transform(self.mat[['id']]).toarray()))
        self.mat_hot_encoder.columns = self.mat['id'].unique()

    def to_analyze(self,mat,nb_day_pred):
        n = mat.shape[1] - 1
        analyze = numpy.array(mat)[:,(n - nb_day_pred - self.nb_day_analyze + 1):(n - nb_day_pred + 1)]
        target = numpy.array(mat)[:,n]
        target_1 = numpy.array(mat)[:,(n - nb_day_pred + 1)]
        analyze = numpy.c_[analyze,target]
        analyze = numpy.c_[analyze,target_1]
        for i in range(1,mat.shape[1]):
            if n - nb_day_pred - self.nb_day_analyze + 1 - i >= 0:
                analyze_i = numpy.array(mat)[:,(n - nb_day_pred - self.nb_day_analyze + 1 - i):(n - nb_day_pred - i + 1)]
                target_i = numpy.array(mat)[:,(n - i)]
                target_i1 = numpy.array(mat)[:,(n - nb_day_pred - i + 1)]
                analyze_i = numpy.c_[analyze_i,target_i]
                analyze_i = numpy.c_[analyze_i,target_i1]
                analyze = numpy.r_[analyze,analyze_i]
        return analyze

    def create_mat_prod(self):
        sex = [0]
        dep = self.mat['dep'].unique()
        for s in sex:
            for d in dep:
                if str(d) != 'nan':
                    print(str(s) + ' - ' + str(d))
                    sel = numpy.array(self.mat['sexe'] == s) * numpy.array(self.mat['dep'] == d)
                    self.in_1_line(self.mat[sel])
        
        col_dc = self.mat_dc.columns
        np_dc = numpy.array(self.mat_dc)
        dep = np_dc[:,0]
        np_dc = numpy.delete(np_dc,0,1)
        for i in range(1,np_dc.shape[1]):
            sel_err = np_dc[:,i] < np_dc[:,(i-1)]
            if sum(sel_err) > 0:
                np_dc[sel_err,i] = np_dc[sel_err,(i-1)]
        np_dc = numpy.c_[dep,np_dc]
        self.mat_dc = pandas.DataFrame(np_dc)
        self.mat_dc.columns = col_dc

        self.mat_hosp.to_csv('C:\\covid-fr\\datas\\hosp_prod.csv',index = False,sep = ';')
        self.mat_rea.to_csv('C:\\covid-fr\\datas\\rea_prod.csv',index = False,sep = ';')
        self.mat_rad.to_csv('C:\\covid-fr\\datas\\rad_prod.csv',index = False,sep = ';')
        self.mat_dc.to_csv('C:\\covid-fr\\datas\\dc_prod.csv',index = False,sep = ';')
        
    def create_mat_analyze(self,nb_day_pred):

        self.mat_hosp = pandas.read_csv('C:\\covid-fr\\datas\\hosp_prod.csv',engine = 'python',sep = ';')
        self.mat_rea = pandas.read_csv('C:\\covid-fr\\datas\\rea_prod.csv',engine = 'python',sep = ';')
        self.mat_rad = pandas.read_csv('C:\\covid-fr\\datas\\rad_prod.csv',engine = 'python',sep = ';')
        self.mat_dc = pandas.read_csv('C:\\covid-fr\\datas\\dc_prod.csv',engine = 'python',sep = ';')

        self.mat_hosp = self.mat_hosp.drop(['dep'],axis = 1)
        self.mat_rea = self.mat_rea.drop(['dep'],axis = 1)
        self.mat_rad = self.mat_rad.drop(['dep'],axis = 1)
        self.mat_dc = self.mat_dc.drop(['dep'],axis = 1)
       
        n_hosp = self.to_analyze(self.mat_hosp,nb_day_pred)
        n_rea = self.to_analyze(self.mat_rea,nb_day_pred)
        n_dc = self.to_analyze(self.mat_dc,nb_day_pred)
        n_rad = self.to_analyze(self.mat_rad,nb_day_pred)

        self.mat_hosp = pandas.DataFrame(n_hosp)
        self.mat_rea = pandas.DataFrame(n_rea)
        self.mat_rad = pandas.DataFrame(n_rad)
        self.mat_dc = pandas.DataFrame(n_dc)

        self.mat_hosp.to_csv('C:\\covid-fr\\datas\\hosp_' + str(k) + '.csv',index = False,sep = ';')
        self.mat_rea.to_csv('C:\\covid-fr\\datas\\rea_' + str(k) + '.csv',index = False,sep = ';')
        self.mat_rad.to_csv('C:\\covid-fr\\datas\\rad_' + str(k) + '.csv',index = False,sep = ';')
        self.mat_dc.to_csv('C:\\covid-fr\\datas\\dc_' + str(k) + '.csv',index = False,sep = ';')

class prediction_covid:
    def __init__(self,cv,nb_day,nb_day_analyze,filename):
        self.covid = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_' + str(nb_day_analyze) + '.csv',sep = ';',engine = 'python')
        self.covid_train = pandas.DataFrame()
        self.covid_test = pandas.DataFrame()
        self.mes = pandas.DataFrame()
        for i in range(nb_day):
            self.mes['lm_' + str(i + 1)] = [0,0]
        self.mes_extrapolation = pandas.DataFrame()
        for i in range(nb_day):
            self.mes_extrapolation['lm_' + str(i + 1)] = [0,0]
        # self.mes['tree'] = [0]
        # self.mes['rf'] = [0]
        # self.mes['knn'] = [0]
        self.cv = cv
        self.nb_day = nb_day
        self.file = filename
        self.nb_day_analyze = nb_day_analyze

    def create_train_test(self):
        sel_train = numpy.random.choice(range(len(self.covid)),size = int(0.9 * len(self.covid)),replace = False)
        self.covid_train = self.covid.iloc[sel_train]
        self.covid_train.index = numpy.array(range(len(self.covid_train)))
        self.covid_test = self.covid.drop(sel_train,axis = 0)
        self.covid_test.index = numpy.array(range(len(self.covid_test)))

    def trans(self,x):
        # m = x.shape[1] - 1
        # x = numpy.c_[x,numpy.c_[x[:,1:(m+1)]] / numpy.c_[x[:,0:m]]]
        # sel = x.astype(str) == 'inf'
        # x[sel] = 0
        # sel = sel.astype(int)
        # x = numpy.c_[x,sel]
        # sel = x.astype(str) == 'nan'
        # x[sel] = 0
        # sel = sel.astype(int)
        # x = numpy.c_[x,sel]
        x = pandas.DataFrame(x)
        return x

    def mesure_prediction(self):
        for cvi in range(self.cv):
            self.create_train_test()

            for i in range(self.nb_day):

                y_train = self.covid_train[[str(self.nb_day)]]
                y_train_extrapolation = self.covid_train[[str(self.nb_day + 1)]]
                y_test = self.covid_test[[str(self.nb_day)]]
                x_train = self.covid_train.drop([str(self.nb_day),str(self.nb_day + 1)],axis = 1)
                x_test = self.covid_test.drop([str(self.nb_day),str(self.nb_day + 1)],axis = 1)
                y_test = numpy.array(y_test)[:,0]
                m = len(x_train.columns)

                model = linear_model.LinearRegression()
                x_an_train = numpy.array(x_train[x_train.columns[(m - i - 1):m]])
                x_an_test = numpy.array(x_test[x_test.columns[(m - i - 1):m]])
                x_an_train = self.trans(x_an_train)
                x_an_test = self.trans(x_an_test)

                model.fit(x_an_train,y_train)
                pred = model.predict(x_an_test)[:,0]
                self.mes['lm_' + str(i + 1)].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv
                self.mes['lm_' + str(i + 1)].iloc[1] += numpy.mean(abs(y_test - pred)) / self.cv

                model.fit(x_an_train,y_train_extrapolation)

                for predi in range(self.nb_day_analyze):
                    pred = model.predict(x_an_test)[:,0]
                    col_p1 = x_test.columns[1:len(x_test.columns)]
                    col_p0 = x_test.columns[0:(len(x_test.columns) - 1)]
                    x_test[col_p0] =  x_test[col_p1]
                    x_test[x_test.columns[len(x_test.columns) - 1]] = pred
                    x_an_test = numpy.array(x_test[x_test.columns[(m - i - 1):m]])
                    x_an_test = self.trans(x_an_test)

                self.mes_extrapolation['lm_' + str(i + 1)].iloc[0] += numpy.mean(numpy.power(y_test - pred,2.0)) / self.cv
                self.mes_extrapolation['lm_' + str(i + 1)].iloc[1] += numpy.mean(abs(y_test - pred)) / self.cv

        self.mes.to_csv('C:\\covid-fr\\datas\\' + self.file + '_' + str(self.nb_day_analyze) + '_mes.csv',sep = ';',index = False)
        self.mes_extrapolation.to_csv('C:\\covid-fr\\datas\\' + self.file + '_' + str(self.nb_day_analyze) + '_mes_extrapolation.csv',sep = ';',index = False)

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

class prod:
    def __init__(self,filename,nb_day_pred):
        try:
            opt_file = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_' + str(nb_day_pred) + '_mes.csv',sep = ';',engine = 'python')
            self.opt = 1
            minima = opt_file['lm_1'].iloc[0]
            for i in range(2,len(opt_file.columns)):
                if minima >  opt_file['lm_' + str(i)].iloc[0]:
                    self.opt = i
                    minima = opt_file['lm_' + str(i)].iloc[0]
            self.train = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_' + str(nb_day_pred) + '.csv',sep = ';',engine = 'python')
        except:
            pass

        # opt_file = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_' + str(nb_day_pred) + '_mes_extrapolation.csv',sep = ';',engine = 'python')
        self.opt_extrapolation = 10
        # minima = opt_file['lm_1'].iloc[0]
        # for i in range(2,len(opt_file.columns)):
        #     if minima >  opt_file['lm_' + str(i)].iloc[0]:
        #         self.opt_extrapolation = i
        #         minima = opt_file['lm_' + str(i)].iloc[0]
        
        self.prod_file = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_prod.csv',sep = ';',engine = 'python')
        self.dep = self.prod_file[['dep']]
        self.train_extrapolation = pandas.read_csv('C:\\covid-fr\\datas\\' + filename + '_' + str(1) + '.csv',sep = ';',engine = 'python')
        self.file_name = filename
        self.nb_day_pred = nb_day_pred

    def trans(self,x):
        # m = x.shape[1] - 1
        # x = numpy.c_[x,numpy.c_[x[:,1:(m+1)]] / numpy.c_[x[:,0:m]]]
        # sel = x.astype(str) == 'inf'
        # x[sel] = 0
        # sel = sel.astype(int)
        # x = numpy.c_[x,sel]
        # sel = x.astype(str) == 'nan'
        # x[sel] = 0
        # sel = sel.astype(int)
        # x = numpy.c_[x,sel]
        x = pandas.DataFrame(x)
        return x

    def prod_pred(self):

        y_train = self.train[[str(len(self.train.columns) - 2)]]
        x_train = self.train.drop([str(len(self.train.columns) - 2),str(len(self.train.columns) - 1)],axis = 1)
        colu = x_train.columns
        colu = colu[(len(colu) - self.opt):len(colu)]
        x_train = numpy.array(x_train[colu])
        colu = self.prod_file.columns
        colu = colu[(len(colu) - self.opt):len(colu)]
        x_pred = numpy.array(self.prod_file[colu])
        x_train = self.trans(x_train)
        x_pred = self.trans(x_pred)

        model = linear_model.LinearRegression()
        model.fit(x_train,y_train)
        pred = model.predict(x_pred)[:,0]
        date = datetime.datetime.now() + datetime.timedelta(days=self.nb_day_pred)
        date = date.strftime('%d.%m.%Y')
        self.dep[self.file_name + '_' + date] = pred
        self.dep.to_csv('C:\\covid-fr\\datas\\' + self.file_name + '_' + str(self.nb_day_pred) + '_pred.csv',index = False,sep = ';')

    def prod_pred_extrapolation(self):

        y_train = self.train_extrapolation[[str(len(self.train_extrapolation.columns) - 1)]]
        x_train = self.train_extrapolation.drop([str(len(self.train.columns) - 2),str(len(self.train.columns) - 1)],axis = 1)
        colu = x_train.columns
        colu = colu[(len(colu) - self.opt_extrapolation):len(colu)]
        x_train = numpy.array(x_train[colu])
        colu = self.prod_file.columns
        colu = colu[(len(colu) - self.opt_extrapolation):len(colu)]
        x_pred = numpy.array(self.prod_file[colu])
        x_train = self.trans(x_train)
        x_pred = self.trans(x_pred)
        model = linear_model.LinearRegression()
        model.fit(x_train,y_train)

        for predi in range(self.nb_day_pred):
            pred = model.predict(x_pred)[:,0]
            col_p1 = self.prod_file.columns[1:len(self.prod_file.columns)]
            col_p0 = self.prod_file.columns[0:(len(self.prod_file.columns) - 1)]
            self.prod_file[col_p0] =  self.prod_file[col_p1]
            self.prod_file[self.prod_file.columns[len(self.prod_file.columns) - 1]] = pred
            x_pred = numpy.array(self.prod_file[colu])
            x_pred = self.trans(x_pred)

        date = datetime.datetime.now() + datetime.timedelta(days=self.nb_day_pred)
        date = date.strftime('%d.%m.%Y')
        self.dep[self.file_name + '_' + date] = pred
        self.dep.to_csv('C:\\covid-fr\\datas\\' + self.file_name + '_' + str(self.nb_day_pred) + '_pred_extrapolation.csv',index = False,sep = ';')

class merge_covid:
    def __init__(self,filename,nb_day_pred):
        self.nb_day_pred = nb_day_pred
        self.filename = filename
        self.pred = pandas.DataFrame()
        self.pred_extrapolation = pandas.DataFrame()
        self.pred_mes_extrapolation = pandas.DataFrame()
        self.pred_mes = pandas.DataFrame()

    def merge_file(self):
        self.pred = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_1_pred.csv',engine = 'python',sep = ';')
        os.remove('C:\\covid-fr\\datas\\' + self.filename + '_1_pred.csv')
        for i in range(2,self.nb_day_pred + 1):
            temp = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_pred.csv',engine = 'python',sep = ';')
            self.pred = self.pred.merge(temp,on = ['dep'],how = 'inner')
            os.remove('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_pred.csv')
        self.pred.to_csv('C:\\covid-fr\\datas\\' + self.filename + '_pred.csv',index = False,sep = ';')

    def merge_file_mes(self):
        self.pred_mes = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_1_mes.csv',engine = 'python',sep = ';')
        os.remove('C:\\covid-fr\\datas\\' + self.filename + '_1_mes.csv')
        for i in range(2,self.nb_day_pred + 1):
            temp = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_mes.csv',engine = 'python',sep = ';')
            self.pred_mes = self.pred_mes.append(temp)
            os.remove('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_mes.csv')
        self.pred_mes.to_csv('C:\\covid-fr\\datas\\' + self.filename + '_mes.csv',index = False,sep = ';')

    def merge_file_extrapolation(self):
        self.pred_extrapolation = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_1_pred_extrapolation.csv',engine = 'python',sep = ';')
        os.remove('C:\\covid-fr\\datas\\' + self.filename + '_1_pred_extrapolation.csv')
        for i in range(2,self.nb_day_pred + 1):
            temp = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_pred_extrapolation.csv',engine = 'python',sep = ';')
            self.pred_extrapolation = self.pred_extrapolation.merge(temp,on = ['dep'],how = 'inner')
            os.remove('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_pred_extrapolation.csv')
        self.pred_extrapolation.to_csv('C:\\covid-fr\\datas\\' + self.filename + '_pred_extrapolation.csv',index = False,sep = ';')

    def merge_file_mes_extrapolation(self):
        self.pred_mes_extrapolation = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_1_mes_extrapolation.csv',engine = 'python',sep = ';')
        os.remove('C:\\covid-fr\\datas\\' + self.filename + '_1_mes_extrapolation.csv')
        for i in range(2,self.nb_day_pred + 1):
            temp = pandas.read_csv('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_mes_extrapolation.csv',engine = 'python',sep = ';')
            self.pred_mes_extrapolation = self.pred_mes_extrapolation.append(temp)
            os.remove('C:\\covid-fr\\datas\\' + self.filename + '_' + str(i) + '_mes_extrapolation.csv')
        self.pred_mes_extrapolation.to_csv('C:\\covid-fr\\datas\\' + self.filename + '_mes_extrapolation.csv',index = False,sep = ';')

path_folder = 'C:\\covid-fr\\datas\\'
col_id = [['Province/State','Country/Region']]
col_drop = [['Province/State','Country/Region','Lat','Long']]
date = datetime.datetime.now()
date = date.strftime('%d.%m.%Y')
csv = ['region_covid_' + date + '.csv']
nb_day_pred = 6 + 1
cv = 100
filename = ['rea','hosp','dc','rad']

an = analysis(path_folder,csv[0],col_id[0],col_drop[0],10)
an.create_mat_prod()
for k in range(1,nb_day_pred):
    an.create_mat_analyze(k)

for k in range(1,nb_day_pred):
    for f in filename:
        pc = prediction_covid(cv,10,k,f)
        pc.mesure_prediction()

for k in range(1,nb_day_pred):
    for f in filename:
        pr = prod(f,k)
        pr.prod_pred()
        pr.prod_pred_extrapolation()

for f in filename:
    mp = merge_covid(f,nb_day_pred - 1)
    mp.merge_file()
    mp.merge_file_extrapolation()
    mp.merge_file_mes()
    mp.merge_file_mes_extrapolation()
