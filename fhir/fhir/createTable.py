import mysql.connector
from mysql.connector import errorcode

db = mysql.connector.connect(host='localhost',user='root',passwd='123456.abc')

cursor = db.cursor()


DB_NAME = 'fhir'
TABLES = {}

TABLES['Dispense'] = (
    "CREATE TABLE `Dispense` ("
    "  `dispenseID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `whenPrepared` date NOT NULL,"
    "  `PatientDisease` varchar(14) NOT NULL,"
     "  `medicationId` int(11) NOT NULL,"
   "  PRIMARY KEY (`dispenseID`)"
  #  "  CONSTRAINT `dispenseContains` FOREIGN KEY (`medicationId`) "
  #  "     REFERENCES `Medication` (`medicationId`) "
    ") ENGINE=InnoDB")

TABLES['Medication'] = (
    "CREATE TABLE `Medication` ("
    "  `medicationId` int(11) NOT NULL AUTO_INCREMENT,"
    "  `medicationCodingSystem` varchar(14) NOT NULL,"
    "  `medicationCodingID` varchar(14) NOT NULL,"
    "  `ingredientCodingSystem` varchar(14) NOT NULL,"
    "  `ingredientCodingID` varchar(14) NOT NULL,"
    "  PRIMARY KEY (`medicationId`)"
     #"  CONSTRAINT `dispenseContains` FOREIGN KEY (`ingredientCodingSystem`, `ingredientCodingID`) "
    # "     REFERENCES `Ingredient`(`codingSystem`, `codingID`) "
    ") ENGINE=InnoDB")


TABLES['Ingredient'] = (
    "CREATE TABLE `Ingredient` ("
    "  `DisplayName` varchar(14)  NOT NULL,"
    "  `codingSystem` varchar(14) NOT NULL,"
    "  `codingID` varchar(14) NOT NULL,"
    "  PRIMARY KEY (`codingSystem`, `codingID`)"
    ") ENGINE=InnoDB")

TABLES['Patient'] = (
    "CREATE TABLE `Patient` ("
    "  `patientID` int(14)  NOT NULL AUTO_INCREMENT,"
    "`allergyCodingSystem`varchar(14)  NOT NULL , "
    "`allergyCodingID`varchar(14)  NOT NULL , "
    " PRIMARY KEY (`patientID`)"
   # "  CONSTRAINT `dispenseContains` FOREIGN KEY (`allergyCodingSystem`, `allergyCodingID`) "
   #  "     REFERENCES `Ingredient`(`codingSystem`, `codingID`) "
    ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        db.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
db.close()