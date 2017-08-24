'''custom module for various functions

'''



def DiscountFunction(rates,period):

	'''Determines the Discount function, based on an input list of rates and compounting periods

	

	Syntax: DiscountFunction(rates[],periods) for cont compounting, use "e"

	'''

	import numpy as np

	if period == "e":

		t=range(1,len(rates)+1)

		df=list(map(lambda r,t: np.exp(-r*t),rates,t))

		return(df)

def BlackScholes(cp, spot,strike,mat,rf,vol,div):

	'''determines the price of an option by BMS equation

	cp [1 for call, -1 for put]

	spot=spot price of security

	strike = strike price of option

	mat = maturity

	rate = risk free rate

	vol = implied volatility

	div = dividends

	''' 

	import numpy as np

	import scipy as sp

	from scipy import stats

	

	d1 = (np.log(spot/strike)+(rf-div+.5*vol**2)*mat)/(vol*np.sqrt(mat))

	d2 = d1-vol*np.sqrt(mat)

	callprice=cp*spot*np.exp(-div*mat)*sp.stats.norm.cdf(cp*d1)-cp*strike*np.exp(-rf*mat)*sp.stats.norm.cdf(cp*d2)

	

	optprice=cp*spot*np.exp(-div*mat)*sp.stats.norm.cdf(cp*d1)-cp*strike*np.exp(-rf*mat)*sp.stats.norm.cdf(cp*d2)

	return(optprice)



def ImpliedVol(x, **kwargs):

	''' Returns implied volatility, based on BMS equation

	to be implimented later

	'''

	cp=None

	rf=None

	strike=None

	spot=None

	vol=None

	mat=None

	div=None

	#process arguments

	for key in kwargs:

		if key == "strike":

			strike = float(kwargs[key])

		if key == "spot":

			spot = float(kwargs[key])

		if key == "vol":

			vol = float(kwargs[key])

		if key == "mat":

			mat = float(kwargs[key])

		if key =="rf":

			rf = float(kwargs[key])

		if key =="div":

			div=float(kwargs[key])

		if key == "cp":

			if kwargs[key] == "c":

				cp=1

			else: cp=-1

			

def present_value(flows,df):

	'''Finds present value, given a list of cash flows and a continously discounted yield curve. 

	

	syntax: present_value(flows,rate) 

	'''

	import numpy as np

	pv=sum(map(lambda flows,df: flows*df,flows,df))

	return(pv)

def duration(flows,df,t, **kwargs):

	'''Returns the duration of a series of cash flows.

	

	duration(flows, df, t, flavor=[delta,dollar,macaulay])

	flows = a list of cash flows

	df = a list of the discount factors to be applied to each flow

	t = the time each flow occurs

	flavor ="" the type of duration desired, inputs must be "delta", "omega", or "macaulay"

	'''

	for key in kwargs:

		if key =="flavor":

			flavor=kwargs[key]

	if flavor=="delta":

		duration=sum(map(lambda flows, df, t:flows*df*t/100,flows,df, t))

	elif flavor=="macaulay":  

		npv=present_value(flows,df)

		duration=sum(map(lambda flows, df, t:flows*df*t/npv,flows,df, t))

	elif flavor=="omega":

		npv=present_value(flows,df)

		duration=sum(map(lambda flows, df, t:flows*df*t/100/npv,flows,df, t))

	else:

		print("this flavor has not been implimented")

	return(duration)

def YldCurve():

	import requests

	import bs4

	import pandas as pd

	import numpy as np

	import datetime



	r = requests.get('http://wsj.com/mdc/public/page/2_3020-tstrips.html?mod=mdc_bnd_pglnk')

	a=bs4.BeautifulSoup(r.content)

	table=a.body.findAll('table')[2]

	prices=[]

	for row in table.findAll('tr'):

		for col in row.findAll('td'):

			prices.append(col.text)

			

	#crop off the next portion after principal

	b=prices.index('Treasury Note, Stripped Principal')-1

	prices.pop(5)

	prices=np.array(prices)

	prices=prices[:b]

	prices=np.reshape(prices,((1+len(prices))/5,5))

	#separate column heads from data for use later

	names=prices[0]

	prices=prices[1:]

	#convert to dataframe, and change date strings to datetimes

	yields=pd.DataFrame(prices,columns=names)

	yields['Maturity']=yields['Maturity'].apply(lambda x: datetime.datetime.strptime(str(x),"%Y %b %d"))

	return(yields)
