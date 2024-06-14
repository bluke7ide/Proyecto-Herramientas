#' Función que realiza el scrap a partir de un archivo txt 
#' de un chat de Whatsapp, mientras pueda ser exportable
#' mediante la aplicación de celular de iPhone de Whatsapp. Tiene que coincidir
#' con este formato, al menos arreglamos el problema de 24 y 12 horas 
#' pero las aplicaciones Android usan separadores extraños indiferenciables del 
#' texto.
#' 
#' @param name - string: nombre del archivo, puesto en la carpeta data.
#' 
#' @returns data.frame: los datos después del proceso de lectura.
scrapW <- function(name){

  # buscar el archivo
  ruta <- paste("data/", name, ".txt", sep = '')
  texto <- read_file(ruta)
  
  # remover, si es posible, los \r, y trabajar en \n
  texto <- str_replace_all(texto, "\r", "")
  texto <- strsplit(texto, '\n')[[1]]
  
  # separar horas y mensaje
  temp <- str_split_fixed(texto, "\\] ", 2)  
  
  # realizar el dataframe con los datos iniciales
  datos <- data.frame(hora = numeric(length(texto)))
  datos$hora <- temp[,1]
  datos$autor <- numeric(length(texto))
  datos$mensaje <- temp[,2]
  
  # Dividir entre autor y mensaje
  temp <- str_split_fixed(datos$mensaje, ": ", 2)
  datos$autor <- temp[,1]
  datos$mensaje <- temp[,2]
  
  # Sacar los índices de los enters en línea
  indices <- as.numeric(rownames(datos[!grepl("\\[", datos$hora),]))
  
  # Operar estas líneas
  for (i in indices){
    datos$mensaje[i] <- datos$hora[i]
    datos[i,1:2] <- datos[i-1,1:2]
  }
  datos$mensaje <- as.character(datos$mensaje)
  
  # Eliminar el corchete extra
  datos$hora <- gsub("\\[", "", datos$hora)
  
  # Dividir en días y horas
  datos <- datos %>% separate(hora, into = c("dia", "hora"), sep = ", ")
  
  # Formato lubridate
  datos$dia <- as_date(dmy(datos$dia))
  
  # En caso de PM, o p. m. AM lo ignora
  datos<- datos %>% mutate(pm = grepl("[pP]", datos$hora))
  datos$hora <- str_replace_all(datos$hora, "p\\.\\s*m\\.", "")
  datos$hora <- str_replace_all(datos$hora, "a\\.\\s*m\\.", "")  
  
  # Moverse a hms de 24 horas
  datos$hora <- hms(datos$hora)
  datos$hora <- datos$hora + hours(datos$pm*12)
  
  # Quitar la columna extra
  datos <- datos %>% select(-pm)
  
  # Añadir la columna de editado
  datos <- datos %>% mutate(editado = grepl("<Se editó este mensaje.>", datos$mensaje))
  datos$mensaje <- gsub("<Se editó este mensaje.>", "", datos$mensaje)
  
  return(datos)
}