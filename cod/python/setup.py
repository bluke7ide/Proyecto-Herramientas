# Módulos
import pandas as pd
import time
import nltk # hay que revisar si esta se sigue usando 
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from textblob import TextBlob

from ProcesadorTexto import ProcesadorTexto, AnalizadorTexto

