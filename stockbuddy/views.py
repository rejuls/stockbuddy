from django.http import HttpResponse
import requests
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
import feedparser
from .models import StockData
from django.forms.models import model_to_dict
from flair.models import TextClassifier
from flair.data import Sentence

# TODO: requirements file
# TODO: remove all comments you made
# TODO: remove junk files
# TODO: login logic

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def stock_view(request):
	import yfinance as yf
	dictstock={}
	dictnews={}
	query=StockData.objects.all()

	for obj in query:
		stockdata = yf.Ticker("%s.NS" % obj.symbol)
		name=stockdata.info['longName']
		hist = stockdata.history(period="1d")
		ltp=hist.iloc[-1].Close
		dictstock[obj.symbol]=(name,ltp)

	rss_url='https://news.google.com/rss/search?q=Indian%20Stock%20Market&hl=en-IN&gl=IN&ceid=IN:en&hl=en-IN'
	news_feed = feedparser.parse(rss_url)
	for i in range(4):
		dictnews[news_feed.entries[i].title]=news_feed.entries[i].link

	return render(request,"home.html",{"dictstock":dictstock,"dictnews":dictnews})

def newsprediction(title):
	classifier = TextClassifier.load('bestmodel.pt')
	sentence = Sentence(title)
	classifier.predict(sentence)
	n= str(sentence.labels[0]).split()[0]
	if n=="0":
		return 0
	else:
		return 1

def analysis(score,percentchange):
	if score==0:
		newsmark=5
	elif score==1:
		newsmark=3
	else:
		newsmark=0

	if percentchange>=3:
		mlmark=5
	elif percentchange<=-3:
		mlmark=0
	else:
		mlmark=3
	return newsmark+mlmark

def stockdetail_view(request,symbol):
	import yfinance as yf
	stockdata = yf.Ticker("%s.NS" % symbol)
	name=stockdata.info['longName']
	hist = stockdata.history(period="1mo")
	ltp=hist.iloc[-1].Close
	Graph=hist.iloc[-7:].Close.to_json().replace("\"", "")
	Obj=StockData.objects.get(symbol=symbol)
	reports=Obj.listreport
	score=0
	rss_url='https://news.google.com/rss/search?q=%s&hl=en-IN&gl=IN&ceid=IN:en&hl=en-IN' % name.replace(" ","%20")
	dictnews={}
	news_feed = feedparser.parse(rss_url)
	for i in range(2):
		newsscore=int(newsprediction(news_feed.entries[i].title.rsplit("-",1)[0]))
		dictnews[news_feed.entries[i].title]=(news_feed.entries[i].link,newsscore)
		score+=newsscore

	y=Obj.mlprediction
	mlquery=[float(i) for i in y]
	percentchange=((mlquery[2]-ltp)/ltp)*100
	analysisscore=analysis(score,percentchange)

	return render(request,"stockview.html",{"symbol":symbol,"name":name,"ltp":ltp,"Graph":Graph,"dictnews":dictnews,"mlquery":mlquery,"reports":reports,"analysisscore":analysisscore})
