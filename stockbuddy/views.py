from django.http import HttpResponse
import requests
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here

#new
'''def result_view(request):
	queryset3 = OffstageResult.objects.all()
	queryset2=Point.objects.all()
	queryset = OnstageResult.objects.all()
	dict = {"onresult" : queryset, "offresult" : queryset3,"point":queryset2}
	#print(type(dict['result'].event_name))
	return render(request,"results.html",dict)'''

def stock_view(request):
	stockapi1=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=NSE:TCS&apikey=D7Y416RS0V7N4CS4')
	stockapi2=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=NSE:YESBANK&apikey=7SKLUNALXS2N5PBZ')
	stockapi3=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=NSE:ICICIBANK&apikey=V9KB0QZSBY2AC71R')
	stockapi4=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=NSE:INFY&apikey=198YPQ4FJUYRMU9D')
	stockjson1=stockapi1.json()
	stockjson2=stockapi2.json()
	stockjson3=stockapi3.json()
	stockjson4=stockapi4.json()
	return render(request,"results.html",{
	'symbol1':stockjson1['Meta Data']['2. Symbol'],'point1':stockjson1['Time Series (Daily)']['2020-03-16']['5. adjusted close'],
	'symbol2':stockjson2['Meta Data']['2. Symbol'],'point2':stockjson2['Time Series (Daily)']['2020-03-16']['5. adjusted close'],
	'symbol3':stockjson3['Meta Data']['2. Symbol'],'point3':stockjson3['Time Series (Daily)']['2020-03-16']['5. adjusted close'],
	'symbol4':stockjson4['Meta Data']['2. Symbol'],'point4':stockjson4['Time Series (Daily)']['2020-03-16']['5. adjusted close']
	})


def stockdetail_view(request):
	return render(request,"infosys.html")
