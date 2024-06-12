spammer <- function(df){
  num <- df%>% count(autor) %>% arrange(desc(n))
  return(num)
}

dia_concurrido <- function(df){
  num <- df%>% count(dia) %>% arrange(desc(n))
  return(num)
}

hora_concurrida <- function(df){
  df$hora <- hour(df$hora)
  num <- df %>% count(hora) %>% arrange(desc(n))
  return(num[1,1])
}

streak_dias <- function(df){
  num <- unique(df$dia)
  dif <- num[1:length(num)-1] - num[2:length(num)]
  df <- data.frame(dif = dif)
  tabla <- df %>%
    mutate(is_target = dif == -1,               
           group = cumsum(!is_target)) %>%         
    group_by(group) 
  agrupados <- tabla %>%
    summarise(length = sum(is_target)) %>%         
    filter(length > 0) %>%arrange(desc(length))
  maximo <- agrupados[1,] 
  primerdia <- 0
  for(i in 1:length(tabla$group)){
    if (tabla$group[i]!= maximo$group | tabla$is_target[i] == FALSE){
      next
    } else {
      if (primerdia == 0){
        primerdia <- i
      }
      ultimodia <-i
    }
  }
  
  maximo <- maximo$length
  primerdia <- num[primerdia]
  ultimodia <- num[ultimodia+1]
  return(list(maximo, primerdia, ultimodia))
}

el_graciosito <- function(df){
  df <- df %>% mutate(sticker = grepl("sticker omitido", df$mensaje))
  df <- df[df$sticker,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_grafico <- function(df){
  df <- df %>% mutate(imagen = grepl("imagen omitida", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_waze <- function(df){
  df <- df %>% mutate(ubicacion = grepl("Ubicación:", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_inseguro <- function(df){
  df <- df %>% mutate(seguridad = grepl("Cambió tu código de seguridad con", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_camarografo <- function(df){
  df <- df %>% mutate(video = grepl("Video omitido", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_wikipedia <- function(df){
  df <- df %>% mutate(docs = grepl("documento omitido", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_corrector <- function(df){
  df <- df %>% mutate(edit = grepl("<Se editó este mensaje.>", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_link <- function(df){ # verificar doble
  df <- df %>% mutate(link = grepl("https://", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}

el_jefe <- function(df){ # verificar doble
  df <- df %>% mutate(ping = grepl("@", df$mensaje))
  df <- df[df$imagen,]
  num <- df %>% count(autor) %>% arrange(desc(n))
  return(num)
}