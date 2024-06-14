#' Función que realiza el scrap a partir de un archivo json 
#' de un chat de Telegram, mientras pueda ser exportable
#' mediante la aplicación de desktop de Telegram.
#' 
#' @param name - string: nombre del archivo, puesto en la carpeta data.
#' 
#' @returns data.frame: los datos después del proceso de lectura.
scrapT <- function(name){
  # Importa
  ruta <- paste("data/", name, ".json", sep = '')
  telegram <- fromJSON(ruta)
  
  # En dataframe
  telegram <- as.data.frame(telegram$messages)
  
  # Cambios de forma
  telegram <- telegram[telegram$type == "message",]
  telegram$text[!is.na(telegram$photo)] <- 'photo'
  telegram$text[!is.na(telegram$file)] <- 'file'
  telegram$text[!is.na(telegram$media_type)] <- telegram$media_type[!is.na(telegram$media_type)]
  telegram$edited[!is.na(telegram$edited)] <- TRUE
  
  # Seleccionar las que aportan
  # ATENCIÓN: Se removió el reply column puesto que whatsapp no lo tiene
  telegram <- telegram %>% select(date, from, text, edited)
  
  # Formatos
  telegram <- telegram %>% separate(date, c('dia','hora'), sep = 'T')
  telegram$dia <- ymd(telegram$dia)
  telegram$hora <- hms(telegram$hora)
  colnames(telegram) <- c("dia", "hora", "autor", "mensaje", "editado")
  telegram$editado[is.na(telegram$editado)] = FALSE
  
  return(telegram)
}