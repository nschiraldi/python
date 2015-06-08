# Analyze the FAO Food Production Dataset
# World Country Code = 5000
# Maize item code = 56
# Production Element Code = 5510

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data in as a pandas dataframe
data = pd.read_csv('Downloads/Production_Crops_E_All_Data_(Norm).csv')
priceData = pd.read_csv('Downloads/maize_price_usdton.csv')
[countryCodes,idx] = np.unique(data['Country Code'],True) 
countryNames = data['Country'][idx[countryCodes < 5000]]
countryCodes = countryCodes[countryCodes < 5000]

# Find the Product (tons) for World Crops
index = np.nonzero(np.logical_and(np.logical_and(data['Country Code'] == 5000,data['Element Code'] == 5510),
        data['Item Code']==56))[0]
indexUS = np.nonzero(np.logical_and(np.logical_and(data['Country Code'] == 231,data['Element Code'] == 5510),
        data['Item Code']==56))[0]
        
# Percent Matrix
percentData = np.zeros((53,len(countryCodes)))
for country in xrange(0,len(countryCodes)):
    print country
    for year in xrange(1961,2014):
        indexCountry = np.logical_and(data['Country Code'] == countryCodes[country],data['Element Code'] == 5510)
        indexItem = np.logical_and(indexCountry,data['Item Code']==56)
        indexYear = np.nonzero(np.logical_and(indexItem,data['Year Code'] == year))[0]
        
        indexWorld = np.logical_and(data['Country Code'] == 5000,data['Element Code'] == 5510)
        indexItem = np.logical_and(indexWorld,data['Item Code']==56)
        indexYearWorld = np.nonzero(np.logical_and(indexItem,data['Year Code'] == year))[0]

        if indexYear:
            percentData[year-1961,country] = data['Value'][indexYear].values / data['Value'][indexYearWorld].values

t = np.argsort(percentData[52,:])

# Bar graphs of China and US % Procution of World 
countryLabs = countryNames[idx[t[-1:-6:-1]]].values
fig = plt.figure(figsize = (8.5,11))
plt.bar(np.arange(1961,2014),percentData[:,t[-1]],label = 'United States',color = '#1f78b4')
plt.bar(np.arange(1961,2014),percentData[:,t[-2]],label = 'China',color = '#b2df8a')
plt.legend(countryLabs,loc=1, borderaxespad=0.)
plt.ylim((0,.75))
plt.xlabel('Year')
plt.xlim((1960,2014))
plt.title('Top Two World Maize Producers')
plt.ylabel('Percent of World Production')
plt.grid(True)
plt.tight_layout()
plt.savefig('Desktop/corn_percent.jpg')
plt.close()

fig,ax1 = plt.subplots()
line1 = ax1.plot(np.arange(1961,2014),data['Value'][np.nonzero(np.logical_and(
        np.logical_and(data['Country'] == 'United States of America',
        data['Item Code'] == 56),data['Element'] == 'Yield'))[0]])

ax2 = ax1.twinx()
line2 = ax2.plot(np.arange(1991,2015),priceData['Value'].values,'r')
ax2.set_ylabel('$', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()