import pymysql
import sys

try:

  ############### CONFIGURAR ESTO ###################
  # Abre conexion con la base de datos
  db2 = pymysql.connect(
    host="127.0.0.1",
    port=8889,
    user="root",
    password="root",
    db="ABCNet_example")
  ##################################################

  # prepare a cursor object using cursor() method
  cursor2 = db2.cursor()

except:
  print "Error al conectar a base de datos"
  sys.exit(0)


def vinAbcNet():
  cursor2.execute("SELECT pk_source_pa, vin from dealer limit 1000")

  return cursor2.fetchall()

def queryBuscarCustomer(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from customers where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchall()

def queryBuscarAddress(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from address where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchall()

def queryBuscarPhone(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from phone where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchall()

def queryBuscarEmail(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from email where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchall()

def queryBuscarVehicle(pk_source_vh):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from vehicle where pk_source_vh = %s", pk_source_vh)
  
  return cursor2.fetchall()

def queryBuscarVehicleFco(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from vehicle_fco where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchall()

def queryBuscarDealer(pk_source_pa):
  # ejecuta el SQL query usando el metodo execute().
  cursor2.execute("SELECT * from dealer where pk_source_pa = %s", pk_source_pa)

  return cursor2.fetchall()

def queryBuscarEmailCustomer(pk_source_pa):
  cursor2.execute("SELECT email from email where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchone()

def queryBuscarTelefonoCustomer(pk_source_pa):
  cursor2.execute("SELECT phone_number from phone where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchone()

def queryBuscarNombreCustomer(pk_source_pa):
  cursor2.execute("SELECT first_name, last_name from customers where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchone()

def queryBuscarRfcCustomer(pk_source_pa):
  cursor2.execute("SELECT nacional_identifier_1, nacional_identifier_2 from customers where pk_source_pa = %s", pk_source_pa)
  
  return cursor2.fetchone()
