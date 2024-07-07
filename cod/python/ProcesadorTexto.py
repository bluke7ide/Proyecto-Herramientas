class ProcesadorTexto():
  '''
  Clase para procesar y manipular datos de texto en un DataFrame.
      
  Attributes:
    __df (pd.DataFrame): DataFrame que contiene los mensajes a procesar.
      
  Methods:
    __init__(df):
      Constructor de la clase ProcesadorTexto. Inicializa la clase con un DataFrame.
      
    df:
      Método getter que obtiene el DataFrame actual.
    
    df(new_df):
      Método setter que cambia el DataFrame actual.
      
    leer(nombre):
      Lee un archivo CSV y carga sus datos en el DataFrame.
      
      guardar(nombre):
        Guarda el DataFrame actual en un archivo CSV.
      
      traducir():
        Traduce los mensajes del DataFrame de español a inglés utilizando GoogleTranslator.
      
      analizar_sentimientos():
        Realiza análisis de sentimientos utilizando VADER y TextBlob y añade los resultados al DataFrame.
    '''
    
  def __init__(self, df):
    '''
    Constructor de la clase ProcesadorTexto. Inicializa la clase con un DataFrame.
    
    Parameters:
      df (pd.DataFrame): DataFrame con los datos iniciales
      
    Returns:
      None
    '''
    
    self.__df = df
    self.__df["hora"] = self.__df["hora"].apply(
      lambda x: str(timedelta(seconds = x))
      )
    
    self.__df["dia"] = pd.to_datetime(self.__df['dia'], format='%Y%m%d').dt.date
    
  @property
  def df(self):
    '''
    Método que obtiene el DataFrame actual.
    
    Parameters:
      None
    
    Returns:
      pd.DataFrame: El DataFrame actual.
    '''
    return self.__df
  
  @df.setter
  def df(self, new_df):
    '''
    Método que cambia el DataFrame actual.
    
    Parameters:
      new_df (pd.DataFrame): Nuevo DataFrame para reemplazar el existente.
    
    Returns:
      None
    '''
    self.__df = new_df
  
  def __str__(self):
    '''
    Método que retorna la información del DataFrame de la clase 
    ProcesadorTexto.
    
    Parameters:
      None
    
    Returns:
      str: Información sobre el DataFrame.
    '''
    return self.__df.info()
  
  def leer(self, nombre):
    '''
    Método que lee un archivo CSV y lo carga en el DataFrame.
    
    Parameters:
      nombre (str): Nombre del archivo.
      
    Returns:
      None
    '''
    self.__df = pd.read_csv("res/" + nombre + ".csv")
    self.__df["mensaje"] = self.__df['mensaje'].apply(lambda x:  str(x))
  
  def guardar(self, nombre):
    '''
    Método que guarda el DataFrame en un archivo CSV.
    
    Parameters:
      nombre (str): Nombre del archivo.
    
    Returns:
      None
    '''
    self.__df.to_csv("res/" + nombre + ".csv", index=False)
      
  def traducir(self):
    '''
    Método que traduce los mensajes del DataFrame de español a inglés utilizando
    GoogleTranslator. Además, mide y muestra el tiempo que tarda en realizar la 
    traducción.
    
    Parameters:
      None
    
    Returns:
      None
    '''
    t_inicial = time.time()
    traductor = GoogleTranslator(source = 'es', target = 'en')
    traducido = pd.DataFrame(traductor.translate_batch(list(self.__df["mensaje"])))
    traducido = traducido.transform(lambda x: x.fillna(self.__df["mensaje"]))
    self.__df["mensaje"] = traducido
    t_final = time.time()
    print('Tiempo de ejecución: ' + (t_final - t_inicial))
    
  def analizar_sentimientos(self):
    '''
    Método que realiza el análisis de sentimientos utilizando VADER y TextBlob.
    Añade los resultados del análisis al DataFrame.
    
    Parameters:
    None
    
    Returns:
    None
    '''
    sid = SentimentIntensityAnalyzer()
    sentimientos1 = self.__df['mensaje'].apply(lambda x:  sid.polarity_scores(x))
    sentimientos1 = sentimientos1.apply(lambda x: pd.Series(x))
    
    sentimientos2 = self.__df['mensaje'].apply(lambda x:  TextBlob(x).sentiment)
    sentimientos2 = sentimientos2.apply(lambda x: pd.Series(x))
    sentimientos = pd.concat([sentimientos1, sentimientos2], axis = 1)
    sentimientos.columns = ["negativo",
                            "neutral",
                            "positivo",
                            "compuesto",
                            "polaridad",
                            "subjetividad"]
    self.__df = pd.concat([self.__df, sentimientos], axis = 1)
    
class AnalizadorTexto(ProcesadorTexto):
  '''
  Clase que hereda de ProcesadorTexto y añade métodos para análisis estadístico y de texto.
    
  Methods:
    __init__(df):
      Constructor de la clase AnalizadorMensajes. Hereda de ProcesadorTexto.
    
    editado():
      Retorna la cantidad de mensajes editados por cada autor.
    
    mensajes():
      Retorna la cantidad de mensajes enviados por cada autor.
    
    encontrar(frase):
      Retorna la cantidad de mensajes que contienen una frase específica por cada autor.
    
    promedio_sentimientos():
      Retorna el promedio de sentimientos por autor.
  '''
    
  def __init__(self, df):
    '''
    Constructor de la clase AnalizadorTexto. Hereda de ProcesadorTexto.
        
    Parameters:
      df (pd.DataFrame): DataFrame con los datos iniciales.
      
    Returns: 
      None
    '''
    ProcesadorTexto.__init__(self, df)
  
  def editado(self):
    '''
    Método que retorna la cantidad de mensajes editados por cada autor.
      
    Parameters:
      None
      
    Returns:
      pd.Series: Serie con la cuenta de mensajes editados por autor.
    '''
    local = self.df[self.df["editado"]]
    return local["autor"].value_counts()

  def mensajes(self):
    '''
    Método que retorna la cantidad de mensajes enviados por cada autor.
      
    Parameters:
      None
      
    Returns:
      pd.Series: Serie con la cuenta de mensajes por autor.
    '''
    return self.df["autor"].value_counts()

  def encontrar(self, frase):
    '''
    Método que retorna la cantidad de mensajes que contienen una frase específica por cada autor.
    
    Se sugieren las siguientes frases:
      "Change your security code with"
      "document omitted"
      "https://"
      "image omitted"
      "sticker omitted"
      "@"
      "This message has been deleted"
      "Video omitted"
      "Location:"
      "omitted audio"
      
    Parameters:
      frase (str): Frase a buscar en los mensajes.
      
    Returns:
      pd.Series: Serie con la cuenta de mensajes que contienen la frase por autor.
    '''
    audio = self.df["mensaje"].apply(lambda x: frase in x)
    local = self.df[audio]
    return local["autor"].value_counts()

  def promedio_sentimientos(self):
    '''
    Método que retorna el promedio de sentimientos por autor.
      
    Parameters:
      None
      
    Returns:
      pd.DataFrame: DataFrame con el promedio de sentimientos por autor.
    '''
    return self.df.groupby('autor')[['negativo', 'neutral', 'positivo', 'compuesto', 'polaridad', 'subjetividad']].mean()
    
  def racha(self, df):
    '''
    Método que calcula la racha más larga de días consecutivos con mensajes.
    
    Parameters:
      df (pd.DataFrame): DataFrame con los datos.
    
    Returns:
      pd.DataFrame: DataFrame con la racha más larga de días consecutivos con mensajes.
    '''
    df['dia'] = pd.to_datetime(df['dia'])  # se puede borrar si 'dia' ya es datetime
    df = df.sort_values(by='dia')
    df['consecutivos'] = df['dia'].diff().dt.days.ne(1).cumsum()
    length_rachas = df.groupby('consecutivos')['dia'].count()
    contador_racha_mas_larga = length_rachas.idxmax()
    longest_streak_df = df[df['consecutivos'] == contador_racha_mas_larga]
    return longest_streak_df.iloc[:, [0]]

  def dia_mas_concurrido(self, df):
    '''
    Método que retorna el día con la mayor cantidad de mensajes enviados.
    
    Parameters:
      df (pd.DataFrame): DataFrame con los datos.
    
    Returns:
      pd.DataFrame: DataFrame con el día más concurrido y la cantidad de mensajes enviados.
    '''
    mensajes_contador = df['dia'].value_counts()
    dia = mensajes_contador.idxmax()
    contador = mensajes_contador.max()
    result_df = pd.DataFrame({'dia': [dia], 'Cantidad': [contador]})
    return result_df
      
      
      
      
      
      
      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
