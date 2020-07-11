from django.db import models
# Create your models here.
import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from django.contrib.postgres.fields import ArrayField
import requests
from statsmodels.tsa.arima_model import ARIMA

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def Arima(symbol):
	infy = yf.Ticker("%s.NS" % symbol)
	dataset = infy.history(period="5y")
	dataset.index = range(len(dataset))
	model = ARIMA(dataset['Close'], order=(15,1,3))
	model_fit = model.fit()
	x=model_fit.forecast(3)
	y=list(x[0])
	mlprediction = [round(num, 2) for num in y]
	return mlprediction


def Report(symbol):
	r=requests.get('https://www.nseindia.com/api/annual-reports?index=equities&symbol=%s' % symbol, headers=headers)
	listreport=[]
	for i in range(2):
		listreport.append(r.json().get('data')[i].get('fileName'))
		listreport.append(r.json().get('data')[i].get('toYr'))
	return listreport

class StockData(models.Model):
	symbol = models.CharField(max_length=12,default=None,primary_key=True)
	mlprediction = ArrayField(models.DecimalField(blank=True,null=True,max_digits=7, decimal_places=2),blank=True,null=True)
	listreport=ArrayField(models.TextField(blank=True,null=True),blank=True,null=True)

	def __str__(self):
		return self.symbol

	def __unicode__(self):
		return self.symbol

	def save(self, *args, **kwargs) -> None:
		self.mlprediction=Arima(self.symbol)
		self.listreport=Report(self.symbol)
		super().save(*args, **kwargs)
