# Reading an excel file using Python
import xlrd
import xlwt
import db
import db2
import sys

logFile = open("log.txt", "a")
workbook = xlwt.Workbook(encoding='latin-1')

customer = workbook.add_sheet('Customer')
address_sheet = workbook.add_sheet('Address')
phone_sheet = workbook.add_sheet('Phone')
email_sheet = workbook.add_sheet('Email')
vehicle_sheet = workbook.add_sheet('Vehicle')
vehicle_fco_sheet = workbook.add_sheet('Vehicle_fco')
dealer_sheet = workbook.add_sheet('Dealer')
row = 0


def buscarVinAbcNet():
  global row

  for pk_source_pa, vinAbc in db2.vinAbcNet():
    # Si los vin coincides entra en el for si no, no entra
    if(db.queryBuscarVinCRM(vinAbc)):
      #print "esta"
      existeVin(row, pk_source_pa)
      row += 1
    else:
      #print "No esta"
      noExisteVIN(pk_source_pa)


def existeVin(row, pk_source_pa):
  for datos in db2.queryBuscarCustomer(pk_source_pa):
    col = 0    
    for dato in datos:
      try:
        customer.write(row, col, dato)
      except:
        print "No se pudo escribir datos en pestana customer -> {0}".format(pk_source_pa)
        break
      col += 1

  # Crear otras pestanas de excel, buscar y guardar datos

  # Pestana address
  for addresses in db2.queryBuscarAddress(pk_source_pa):
    col = 0    
    for address in addresses:
      try:
        address_sheet.write(row, col, address)
      except:
        print "No se pudo escribir datos en pestana address -> {0}".format(pk_source_pa)
        break      
      col += 1

  # Pestana phones
  for phones in db2.queryBuscarPhone(pk_source_pa):
    col = 0    
    for phone in phones:
      try:
        phone_sheet.write(row, col, phone)
      except:
        print "No se pudo escribir datos en pestana phones -> {0}".format(pk_source_pa)
        break   
      col += 1

  # Pestana email
  for emails in db2.queryBuscarEmail(pk_source_pa):
    col = 0    
    for email in emails:
      try:      
        email_sheet.write(row, col, email)
      except:
        print "No se pudo escribir datos en pestana email -> {0}".format(pk_source_pa)
        break
      col += 1

  # Pestana vehicle_fco
  for vehicles_fco in db2.queryBuscarVehicleFco(pk_source_pa):

    #Sacar datos de vehicle_fco para llenar pestana vehicle
    for vehicle in db2.queryBuscarVehicle(vehicles_fco[2]):
      col = 0
      for ve in vehicle:
        try:      
          vehicle_sheet.write(row, col, ve)
        except:
          print "No se pudo escribir datos en pestana vehicle -> {0}".format(pk_source_pa)
          break
        col += 1

    col = 0    
    for vehicle_fco in vehicles_fco:
      try:      
        vehicle_fco_sheet.write(row, col, vehicle_fco)
      except:
        print "No se pudo escribir datos en pestana vehicle_fco -> {0}".format(pk_source_pa)
        break
      col += 1

  # Pestana dealer
  for dealers in db2.queryBuscarDealer(pk_source_pa):
    col = 0    
    for dealer in dealers:
      try:      
        dealer_sheet.write(row, col, dealer)
      except:
        print "No se pudo escribir datos en pestana dealer -> {0}".format(pk_source_pa)
        break
      col += 1

  #Buscar nuevamente en VIN con pk_source_pa para cambiar b_existe = 1 en db CRM
  datosDealer = db2.queryBuscarDealer(pk_source_pa)
  if db.cambiarExisteVin(datosDealer[0][4]):
    print "Se cambio b_existe = 1 -> {0}".format(pk_source_pa)


def noExisteVIN(pk_source_pa):
  global row
  
  #logFile.write(data + " -> no existe en CRM")

  #buscar por email o rfc para pasar los datos
  if(buscarEmailRfcCustomerAbcNet(pk_source_pa)):
    print "Se guardo en excel"
  else:
    existeVin(row, pk_source_pa)
    row += 1
    print "VIN que no esta en CRM -> {0}".format(pk_source_pa)


def buscarEmailRfcCustomerAbcNet(pk_source_pa):
  global row

  # Buscar por email del customer en ABCNet
  email = db2.queryBuscarEmailCustomer(pk_source_pa)

  # Buscar telefono del customer en ABCNet
  telefono = db2.queryBuscarTelefonoCustomer(pk_source_pa)

  # Buscar telefono del customer en ABCNet
  nombre = db2.queryBuscarNombreCustomer(pk_source_pa)

  # Buscar telefono del customer en ABCNet
  rfc = db2.queryBuscarRfcCustomer(pk_source_pa)

  
  #buscar email en bd, si existe llamar afuncion existeVin
  emailExiste = db.buscarEmailCrm(email)
  if(emailExiste):
    existeVin(row, pk_source_pa)
    row += 1
  else:
    if(telefono):
      # Buscar telefono del customer en ABCNet
      telefonoExiste = db.buscarTelefonoCrm(telefono)
      if(telefonoExiste):
        existeVin(row, pk_source_pa)
        row += 1
      else:
        #Buscar nombre del customer en ABCNet
        nombreExiste = db.buscarNombreCrm(nombre)
        if(nombreExiste):
          existeVin(row, pk_source_pa)
          row += 1
        else:
          #Buscar rfc del customer en ABCNet
          if(rfc[0]):
            rfcExiste = db.buscarRfcCrmConsultor(rfc[0])
          else:
            rfcExiste = db.buscarRfcCrmConsultor(rfc[1])

          if(not rfcExiste):
            if(rfc[0]):
              rfcExiste = db.buscarRfcCrmDatosPiso(rfc[0])
            else:
              rfcExiste = db.buscarRfcCrmDatosPiso(rfc[1])

            if(not nombreExiste):
              return False

            existeVin(row, pk_source_pa)
            row += 1  
          else:
            existeVin(row, pk_source_pa)
            row += 1

  return True


def datosCustomerCrm(id_lead):
  global row
  
  datosLead = db.datosLead(id_lead)

  customer.write(row, 0, id_lead)
  customer.write(row, 1, "1")
  
  if(datosLead is not None):
    #Poner nombre en excel
    nombre = datosLead[1].split()
    if(len(nombre) > 2):
      apellidos = "{0} {1}".format(nombre[1], nombre[2])

      customer.write(row, 2, nombre[0])
      customer.write(row, 3, apellidos)
    else:
      if nombre:
        customer.write(row, 2, nombre[0])
        
        if(len(nombre) > 1):
          customer.write(row, 3, nombre[1])

    rfcPiso = db.RfcDatosPiso(id_lead)
    if(rfcPiso):
      customer.write(row, 5, rfcPiso)    
    else:
      rfcConsultor = db.RfcConsultor(id_lead)
      if(rfcConsultor):
        customer.write(row, 4, rfcConsultor)

    datosPhoneCrm(id_lead, datosLead[2])
    datosEmailCrm(id_lead, datosLead[3])
  else:
    print "lead -> {0}".format(id_lead)

  customer.write(row, 10, "SP")
  customer.write(row, 11, "AP")
  customer.write(row, 12, "EXF")


def datosPhoneCrm(id_lead, phone):
  phone_sheet.write(row, 1, id_lead)  
  phone_sheet.write(row, 2, phone)  
  phone_sheet.write(row, 3, "LND") 
  phone_sheet.write(row, 5, "AP")  


def datosEmailCrm(id_lead, email):
  email_sheet.write(row, 1, id_lead)  
  email_sheet.write(row, 2, email)
  email_sheet.write(row, 4, "AP")  

def leadsSoloCrm():
  global row

  for leadsVentas in db.leadsVentasCero():
    if(leadsVentas[3] is not None):
      #Buscar datos de customer en crm
      datosCustomerCrm(leadsVentas[3])
      db.cambiarExisteLead(leadsVentas[3])
      row += 1


if __name__ == "__main__":
  buscarVinAbcNet()
  leadsSoloCrm()

  workbook.save('output.xls')
  logFile.close()

  db.db.close()
  db2.db2.close()