import pymysql
import sys

try:

  ############### CONFIGURAR ESTO ###################
  # Abre conexion con la base de datos
  db = pymysql.connect(
    host="127.0.0.1",
    port=8889,
    user="root",
    password="root",
    db="mkt911_crm_peugeot_test2")
  ##################################################

  # prepare a cursor object using cursor() method
  cursor = db.cursor()

except:
  print "Error al conectar a base de datos"
  sys.exit(0)

# ejecuta el SQL query usando el metodo execute().
#cursor.execute("SELECT VIN from leads_venta where id_venta = 1406")

# procesa una unica linea usando el metodo fetchone().
#data = cursor.fetchone()
#print format(data)

# desconecta del servidor
#db.close()

def queryBuscarVinCRM(vin):
  # ejecuta el SQL query usando el metodo execute().
  cursor.execute("SELECT usuario_id from leads_venta where VIN = %s", vin)

  return cursor.fetchone()


def buscarEmailCrm(email):
  cursor.execute("SELECT lead_id from leads where correo = %s", email)

  return cursor.fetchone()

def buscarTelefonoCrm(phone):
  cursor.execute("SELECT lead_id from leads where telefono like %s", phone[0])

  return cursor.fetchone()

def buscarNombreCrm(nombre):
  cursor.execute("SELECT lead_id from leads where nombre like %s limit 1", ("%" + nombre[0] + " " + nombre[1] + "%",))

  return cursor.fetchone()

def buscarRfcCrmConsultor(rfc):
  cursor.execute("SELECT lead_id from consultor_empresarial where rfc like %s limit 1", ("%" + rfc + "%",))

  return cursor.fetchone()

def buscarRfcCrmDatosPiso(rfc):
  cursor.execute("SELECT lead_id from leads_datos_piso where rfc_comercial like %s limit 1", ("%" + rfc + "%",))

  return cursor.fetchone()

def cambiarExisteVin(vin):
  cursor.execute("UPDATE leads_venta SET b_existe = 1 WHERE vin = %s", vin)

  return db.commit()

def cambiarExisteLead(id):
  cursor.execute("UPDATE leads_venta SET b_existe = 1 WHERE lead_id = %s", id)

  return db.commit()

def leadsVentasCero():
  cursor.execute("SELECT * from leads_venta where b_existe = 0 limit 1000")

  return cursor.fetchall()

def datosLead(id_lead):
  cursor.execute("SELECT * from leads where lead_id = %d", id_lead)

  return cursor.fetchone()

def RfcDatosPiso(id_lead):
  cursor.execute("SELECT rfc_comercial from leads_datos_piso where lead_id = %s", id_lead)

  return cursor.fetchone()

def RfcConsultor(id_lead):
  cursor.execute("SELECT rfc from consultor_empresarial where lead_id = %s", id_lead)

  return cursor.fetchone()
