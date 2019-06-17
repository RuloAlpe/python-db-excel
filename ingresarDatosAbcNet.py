import db
import xlrd
import xlwt

def open_file(path):
  #Open and read an Excel file
  book = xlrd.open_workbook(path)

  # print number of sheets
  #print book.nsheets

  # print sheet names
  #print book.sheet_names()

  # get the first worksheet
  #first_sheet = book.sheet_by_index(0)

  # read a row
  #print first_sheet.row_values(0)

  # read a cell
  #cell = first_sheet.cell(0,0)
  #print cell
  #print cell.value

  # read a row slice
  #print first_sheet.row_slice(rowx=0, start_colx=0, end_colx=2)

  for x in range(1):
    #Pestana de dealer
    sheet = book.sheet_by_index(x)
    num_rows = sheet.nrows
    num_cols = sheet.ncols
    # print "{0} - {1}".format(num_rows, num_cols)
    listDatos = []

    for i in range(num_rows):
      for j in range(num_cols):
        if(x == 0 and i != 0):
          query = "insert into customer values (%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
          listDatos.append(sheet.cell(i,j).value)
          db.cursor.execute(query, tuple(listDatos))

          # Guardar cambios.
          db.db.commit()


  print tuple(listDatos)


if __name__ == "__main__":
  path = "cfirst_052019.xlsx"
  open_file(path)
  db.db.close()