
from bs4 import BeautifulSoup
import requests
import mysql.connector


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "###",
    database = "testdb"
)
mycursor = mydb.cursor()
#url connection

url = "https://datatables.net/examples/basic_init/zero_configuration.html"

data = requests.get(url)

#Then we create a BeautifulSoup object
soup = BeautifulSoup(data.text, 'html.parser')


def getTheTable():
    table = soup.find_all("td")    #we found all td tags and contents
    return table

def writeDataToSql(table):  #there was 342 contents in one array when i gathered all data from website. it had to be divided 57 pieces because logically every 6 pieces must inserted to one by one to the rows. and that is protects sql structure and every column gets it is own true values
    for row in range(57):
        try:
            columnindex = row*6
            sqlFormula = "INSERT INTO dataprac2 (Name, POSITION, OFFICE,AGE,STARTDATE,SALARY) VALUES(%s,%s,%s,%s,%s,%s)"     #those "s" are placeholders with this idea we can insert values in another string variable
            
            name = table[columnindex].text
            position = table[columnindex+1].text
            office = table[columnindex+2].text
            age = int(table[columnindex+3].text)
            startdate = table[columnindex+4].text
            salary = table[columnindex+5].text

            vals = [(name,position,office,age,startdate,salary)]                                            #that is better way than writing too many sqlFormula
            mycursor.executemany(sqlFormula,vals) 
        except Exception:
            print(Exception.add_note)
   
table = getTheTable()
writeDataToSql(table)
mydb.commit()

