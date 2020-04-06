import requests
import pandas
import datetime
import numpy

date = datetime.datetime.now()
date = date.strftime('%d.%m.%Y')
r = requests.get('https://www.data.gouv.fr/en/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7')
fichier = open('C:\\covid-fr\\datas\\' + 'region_covid_' + date + '.csv','wb')
fichier.write(r.content)
fichier.close()

region = pandas.read_csv('C:\\covid-fr\\datas\\' + 'region_covid_' + date + '.csv', sep = ';', engine = 'python')
region['jour'] = region['jour'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
region['total_hosp'] = region['hosp'] + region['rad']
pct_col = ['rea','rad','dc']
for p in pct_col:
    region['pct_' + p] = region[p] / region['total_hosp']
    variance = numpy.array(region['pct_' + p]) * (1 - numpy.array(region['pct_' + p]))
    ic = numpy.power(variance / numpy.array(region['total_hosp']),0.5)
    region['pct_' + p + '_up'] = region['pct_' + p] + 1.96 * ic
    region['pct_' + p + '_dn'] = region['pct_' + p] - 1.96 * ic
    region['pct_' + p] = region['pct_' + p].apply(lambda x: str(x).lower().replace('nan','0'))
    region['pct_' + p + '_up'] = region['pct_' + p + '_up'].apply(lambda x: str(x).lower().replace('nan','0'))
    region['pct_' + p + '_dn'] = region['pct_' + p + '_dn'].apply(lambda x: str(x).lower().replace('nan','0'))
    region['pct_' + p] = region['pct_' + p].apply(lambda x: str(x).lower().replace('inf','0'))
    region['pct_' + p + '_up'] = region['pct_' + p + '_up'].apply(lambda x: str(x).lower().replace('inf','0'))
    region['pct_' + p + '_dn'] = region['pct_' + p + '_dn'].apply(lambda x: str(x).lower().replace('inf','0'))
    region['pct_' + p + '_up'] = region['pct_' + p + '_up'].apply(lambda x: min(float(x),1))
    region['pct_' + p + '_dn'] = region['pct_' + p + '_dn'].apply(lambda x: max(float(x),0))
    region['pct_' + p] = region['pct_' + p].apply(lambda x: int(float(x) * 10000) / 10000)
    region['pct_' + p + '_up'] = region['pct_' + p + '_up'].apply(lambda x: int(float(x) * 10000) / 10000)
    region['pct_' + p + '_dn'] = region['pct_' + p + '_dn'].apply(lambda x: int(float(x) * 10000) / 10000)
region = region.sort_values(by = ['dep','jour'])
region.to_csv('C:\\covid-fr\\datas\\' + 'region_covid_' + date + '.csv',sep = ';',index = False)

dep = numpy.array(region['dep'].unique())
dep = pandas.DataFrame(dep)
dep.columns = ['dep']
dep.to_csv('C:\\covid-fr\\datas\\dep.csv',index = False,sep = ';')
