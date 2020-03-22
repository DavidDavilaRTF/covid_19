import requests
import pandas
import datetime
import numpy

date = datetime.datetime.utcnow()
date = date.strftime('%d.%m.%Y')
r = requests.get('https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4')
fichier = open('C:\\covid-fr\\datas\\' + 'covid_' + date + '.csv','wb')
fichier.write(r.content)
fichier.close()

col_ratio = ['deces','reanimation','hospitalises','gueris']
covid_pandas = pandas.read_csv('C:\\covid-fr\\datas\\' + 'covid_' + date + '.csv', sep = ',', engine = 'python')
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: str(y).lower()))
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: y.replace('nan','0')))
for c in col_ratio:
    covid_pandas['ratio_' + c] =  numpy.array(covid_pandas[c]).astype(float) / numpy.array(covid_pandas['cas_confirmes']).astype(float)
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: str(y).lower()))
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: y.replace('nan','0')))

for c in col_ratio:
    covid_pandas['ratio_' + c + '_ic_inf'] =  numpy.array(covid_pandas['ratio_' + c]).astype(float) - \
                                        1.96 * numpy.power(numpy.array(covid_pandas['ratio_' + c]).astype(float) \
                                        * (1 - numpy.array(covid_pandas['ratio_' + c]).astype(float)) \
                                        / numpy.array(covid_pandas['cas_confirmes']).astype(float),0.5)
    covid_pandas['ratio_' + c + '_ic_sup'] =  numpy.array(covid_pandas['ratio_' + c]).astype(float) + \
                                        1.96 * numpy.power(numpy.array(covid_pandas['ratio_' + c]).astype(float) \
                                        * (1 - numpy.array(covid_pandas['ratio_' + c]).astype(float)) \
                                        / numpy.array(covid_pandas['cas_confirmes']).astype(float),0.5)

covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: str(y).lower()))
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: y.replace('nan','0')))
covid_pandas = covid_pandas.apply(lambda x: x.apply(lambda y: y.replace('inf','0')))
covid_pandas['date'] = covid_pandas['date'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
covid_pandas = covid_pandas.sort_values(by = ['maille_nom','date'])

for c in col_ratio:
    covid_pandas['ratio_' + c + '_ic_inf'] = covid_pandas['ratio_' + c + '_ic_inf'].apply(lambda x: max(0,float(x)))
    covid_pandas['ratio_' + c + '_ic_sup'] = covid_pandas['ratio_' + c + '_ic_sup'].apply(lambda x: int(float(x) * 10000)/10000)
    covid_pandas['ratio_' + c + '_ic_inf'] = covid_pandas['ratio_' + c + '_ic_inf'].apply(lambda x: int(float(x) * 10000)/10000)
    covid_pandas['ratio_' + c] = covid_pandas['ratio_' + c].apply(lambda x: int(float(x) * 10000)/10000)

covid_pandas.to_csv('C:\\covid-fr\\datas\\' + 'covid_' + date + '.csv',sep = ';',index = False)
covid_pandas.to_csv('C:\\Site_Web\\' + 'covid_' + date + '.csv',sep = ';',index = False)
covid_pandas = pandas.DataFrame(numpy.array(covid_pandas['maille_nom'].unique()))
covid_pandas.columns = ['state']
covid_pandas.to_csv('C:\\covid-fr\\datas\\' + 'state_' + date + '.csv',sep = ';',index = False)
covid_pandas.to_csv('C:\\Site_Web\\' + 'state_' + date + '.csv',sep = ';',index = False)
