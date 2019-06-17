# Reading an excel file using Python 
import xlrd
import xlwt
import db
import db2

logFile = open("log.txt", "a")
  
def open_file(path):
  #Open and read an Excel file
  book = xlrd.open_workbook(path)

  #Pestana de dealer
  dealer_sheet = book.sheet_by_index(6)

  #num_rows=sheet.nrows
  #num_col = dealer_sheet.ncols

  for x in range(100):
    if(x != 0):
      cellVIN = dealer_sheet.cell(x,3)
      cell_pk_source_pa = dealer_sheet.cell(x,0)

      # procesa una unica linea usando el metodo fetchone().
      for id_venta, usuario_id, lead_id in db.queryBuscarVin(cellVIN):
        if(id_venta):
          ExisteVIN(id_venta, usuario_id, lead_id, cell_pk_source_pa)
        else:
          NoExisteVIN(cellVIN.value)


# Si el VIN de ABCNet coincide con el de CRM, la informacion de ABCNet reemplaza a la del lead
def ExisteVIN(id_venta, usuario_id, lead_id, cell_pk_source_pa):
  print("{0} - {1} - {2}".format(id_venta, usuario_id, lead_id))

  #Buscar datos de lead en las diferentes pestanas del excel
  customer_sheet = book.sheet_by_index(0)
  #phone_sheet = book.sheet_by_index(2)
  #email_sheet = book.sheet_by_index(3)

  for x in range(100):
    if(x != 0):
      costumer_cell_pk_source_pa = customer_sheet.cell(x,0)
      if(costumer_cell_pk_source_pa == cell_pk_source_pa):
        nombre = customer_sheet.cell(x,2)


  #logFile.write("Woops! I have deleted the content!\n")


def NoExisteVIN(vin):
  print vin + " no existe en CRM"
  #logFile.write(data + " -> no existe en CRM")

  
if __name__ == "__main__":
  path = "cfirst_052019.xlsx"
  open_file(path)
  db.db.close()
  logFile.close()