class ProcesadorTexto():
  '''
  Clase para procesar y manipular datos de texto en un DataFrame.
      
  Atributos:
    __df (pd.DataFrame): DataFrame que contiene los mensajes a procesar.
      
  Metodos:
    __init__(df):
      Constructor de la clase ProcesadorTexto. 
      Inicializa la clase con un DataFrame.
      
    df:
      Método getter que obtiene el DataFrame actual.
    
    df(new_df):
      Método setter que cambia el DataFrame actual.
      
    leer(nombre):
      Lee un archivo CSV y carga sus datos en el DataFrame.
      
      guardar(nombre):
        Guarda el DataFrame actual en un archivo CSV.
      
      traducir():
        Traduce los mensajes del DataFrame de español a inglés 
        utilizando GoogleTranslator.
      
      analizar_sentimientos():
        Realiza análisis de sentimientos utilizando VADER y TextBlob
        y añade los resultados al DataFrame.
    '''
    
  def __init__(self, df):
    '''
    Constructor de la clase ProcesadorTexto. 
    Inicializa la clase con un DataFrame.
    
    Parámetros:
      df (pd.DataFrame): DataFrame con los datos iniciales
      
    Retorna:
      None
    '''
    
    self.__df = df
    
  @property
  def df(self):
    '''
    Método que obtiene el DataFrame actual.
    
    Parámetros:
      Ninguno
    
    Retorna:
      pd.DataFrame: El DataFrame actual.
    '''
    return self.__df
  
  @df.setter
  def df(self, new_df):
    '''
    Método que cambia el DataFrame actual.
    
    Parámetros:
      new_df (pd.DataFrame): Nuevo DataFrame para reemplazar el existente.
    
    Retorna:
      Nada
    '''
    self.__df = new_df
  
  def __str__(self):
    '''
    Método que retorna la información del DataFrame de la clase 
    ProcesadorTexto.
    
    Parámetros:
      Ninguno
    
    Retorna:
      str: Información sobre el DataFrame.
    '''
    return self.__df.info()
  
  def leer(self, nombre):
    '''
    Método que lee un archivo CSV y lo carga en el DataFrame.
    
    Parámetros:
      nombre (str): Nombre del archivo.
      
    Retorna:
      Nada
    '''
    self.__df = pd.read_csv("res/" + nombre + ".csv")
    self.__df["mensaje"] = self.__df['mensaje'].apply(lambda x:  str(x))
  
  def guardar(self, nombre):
    '''
    Método que guarda el DataFrame en un archivo CSV.
    
    Parámetros:
      nombre (str): Nombre del archivo.
    
    Returns:
      Nada
    '''
    self.__df.to_csv("res/" + nombre + ".csv", index=False)
      
  def traducir(self):
    '''
    Método que traduce los mensajes del DataFrame de español a inglés utilizando
    GoogleTranslator. Además, mide y muestra el tiempo que tarda en realizar la 
    traducción.
    
    Parámetros:
      Ninguno
    
    Retorna:
      Nada
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
    
    Parámetros:
      Ninguno
    
    Retorna:
      Nada
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
  Clase que hereda de ProcesadorTexto y añade métodos 
  para análisis estadístico y de texto.
    
  Métodos:
    __init__(df):
      Constructor de la clase AnalizadorTexto. 
      Hereda de ProcesadorTexto.
    
    editado():
      Retorna la cantidad de mensajes editados por cada autor.
    
    mensajes():
      Retorna la cantidad de mensajes enviados por cada autor.
    
    encontrar(frase):
      Retorna la cantidad de mensajes que contienen 
      una frase específica por cada autor.
    
    promedio_sentimientos():
      Retorna el promedio de sentimientos por autor.
  '''
    
  def __init__(self, df):
    '''
    Constructor de la clase AnalizadorTexto. 
    Hereda de ProcesadorTexto.
        
    Parámetros:
      df (pd.DataFrame): DataFrame con los datos iniciales.
      
    Retorna: 
      Nada
    '''
    ProcesadorTexto.__init__(self, df)
  
  def editado(self):
    '''
    Método que retorna la cantidad de mensajes editados por cada autor.
      
    Parámetros:
      Ninguno
      
    Returns:
      pd.Series: Serie con la cuenta de mensajes editados por autor.
    '''
    local = self.df[self.df["editado"]]
    return local["autor"].value_counts()

  def mensajes(self):
    '''
    Método que retorna la cantidad de mensajes enviados por cada autor.
      
    Parámetros:
      Ninguno
      
    Retorna:
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
      
    Parámetros:
      frase (str): Frase a buscar en los mensajes.
      
    Returns:
      pd.Series: Serie con la cuenta de mensajes que contienen la frase por autor.
    '''
    referencia = self.df["mensaje"].apply(lambda x: frase in x)
    local = self.df[referencia]
    return local["autor"].value_counts()

  def promedio_sentimientos(self):
    '''
    Método que retorna el promedio de sentimientos por autor.
      
    Parámetros:
      Ningunogen
      
    Retorna:
      pd.DataFrame: DataFrame con el promedio de sentimientos por autor.
    '''
    return self.df.groupby('autor')[['negativo', 'neutral', 'positivo', 'compuesto', 'polaridad', 'subjetividad']].mean()
    
  def racha(self):
    '''
    Método que calcula la racha más larga de días consecutivos con mensajes.
    
    Parámetros:
      df (pd.DataFrame): DataFrame con los datos.
    
    Returns:
      pd.DataFrame: DataFrame con la racha más larga de días consecutivos con mensajes.
    '''
    
    ref = pd.DataFrame({"dia": self.df['dia'].unique()})
    ref['consecutivos'] = ref['dia'].diff().dt.days.ne(1).cumsum()
    length_rachas = ref.groupby('consecutivos')['dia'].count()
    contador_racha_mas_larga = length_rachas.idxmax()
    longest_streak_df = ref[ref['consecutivos'] == contador_racha_mas_larga]
    
    primer_dia = longest_streak_df.iloc[0, 0]
    ultimo_dia = longest_streak_df.iloc[-1, 0]
    streak = length_rachas[contador_racha_mas_larga]
    
    return f"La mayor racha de días fue de {streak}, desde el {primer_dia} al {ultimo_dia}"

  def dia_mas_concurrido(self):
    '''
    Método que retorna el día con la mayor cantidad de mensajes enviados.
    
    Parámetros:
      df (pd.DataFrame): DataFrame con los datos.
    
    Retorna:
      pd.DataFrame: DataFrame con el día más concurrido y la cantidad de mensajes enviados.
    '''
    mensajes_contador = self.df['dia'].value_counts()
    dia = mensajes_contador.idxmax()
    contador = mensajes_contador.max()

    return f"El día más concurrido es el {dia}, con {contador} mensajes"
      
      
      
      
      
      
      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
