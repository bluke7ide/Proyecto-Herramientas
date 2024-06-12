'''
Función que analiza sentimientos usando la librería 'nltk'.
Dado que el método utilizado está entrenado en inglés, primero se traducen los
mensajes usando la librería 'translate' (está limitada a una cantidad de traducciones)
'''
import pandas as pd
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from translate import Translator

# nltk.download('vader_lexicon') # correr solo la primera vez

def sentimientos_nltk(df):
  
  df_pandas = pd.DataFrame(df)
  
  sid = SentimentIntensityAnalyzer()

  df_pandas['sentimiento_nltk'] = df_pandas['mensaje'].apply(lambda j: sid.polarity_scores(j)['compound'])

  return(df_pandas)




from textblob import TextBlob

def analizar_sentimiento(txt):
  '''
  Función que analiza sentimientos de un texto usando la librería 'TextBlob'.
  '''
  blob = TextBlob(txt)
  sentimiento = blob.sentiment

  return(sentimiento[0])


def sentimientos_textblob(df):
  '''
  Función que analiza sentimientos de una columna de mensajes en un dataframe.
  Este método también está entrenado en inglés, por lo que se utilizan las 
  traducciones previas.
  '''
  
  df_pandas = pd.DataFrame(df)
  df_pandas['sentimiento_textblob'] = df_pandas['mensaje'].apply(lambda j: analizar_sentimiento(j))
  
  return(df_pandas)
  


from transformers import pipeline

def sentimientos_transformers(df):
  '''
  Función que analiza sentimientos usando la librería 'transformers'.
  Este método está entrenado para analizar sentimientos de mensajes en español.
  '''
  
  df_pandas = pd.DataFrame(df)
  sentiment_analysis = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
  df_pandas['sentimiento_transformers'] = df_pandas['mensaje'].apply(lambda j: sentiment_analysis(j)[0]['score'])
  
  return(df_pandas)
