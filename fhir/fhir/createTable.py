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
   "  PRIMARY KEY (`dispenseID`)"
    ") ENGINE=InnoDB")

TABLES['Medication'] = (
    "CREATE TABLE `Medication` ("
    "  `medicationId` int(11) NOT NULL AUTO_INCREMENT,"
    "  `CodingSystem` varchar(14) NOT NULL,"
    "  `CodingID` varchar(14) NOT NULL,"
    "  PRIMARY KEY (`medicationId`)"
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
    " PRIMARY KEY (`patientID`)"
    ") ENGINE=InnoDB")

TABLES['MedicationDispense'] = (
    "CREATE TABLE `MedicationDispense` ("
    "  `dispenseID` int(11) NOT NULL AUTO_INCREMENT,"
     "  `medicationId` int(11) NOT NULL,"
   "  PRIMARY KEY (`dispenseID`,  `medicationId`),"
    "  CONSTRAINT `dispense1` FOREIGN KEY (`dispenseID`) "
    "     REFERENCES `Dispense` (`dispenseID`), "
    "  CONSTRAINT `medication1` FOREIGN KEY (`medicationId`) "
    "     REFERENCES `Medication` (`medicationId`) "
    ") ENGINE=InnoDB")

TABLES['MedicationIngredient'] = (
    "CREATE TABLE `MedicationIngredient` ("
     "  `medicationId` int(11) NOT NULL,"
     "  `codingSystem` varchar(14) NOT NULL,"
    "  `codingID` varchar(14) NOT NULL,"
   "  PRIMARY KEY ( `medicationId`, `codingSystem` ,  `codingID`),"
    "  CONSTRAINT `medication2` FOREIGN KEY (`medicationId`) "
    "     REFERENCES `Medication` (`medicationId`), "
    "  CONSTRAINT `ingredient1` FOREIGN KEY (`codingSystem` ,  `codingID`) "
    "     REFERENCES `Ingredient` (`codingSystem` ,  `codingID`) "
    ") ENGINE=InnoDB")

TABLES['Allergy'] = (
    "CREATE TABLE `Allergy` ("
     "  `patientID` int(11) NOT NULL,"
     "  `codingSystem` varchar(14) NOT NULL,"
    "  `codingID` varchar(14) NOT NULL,"
   "  PRIMARY KEY ( `patientID`, `codingSystem` ,  `codingID`),"
    "  CONSTRAINT `patient1` FOREIGN KEY (`patientID`) "
    "     REFERENCES `Patient` (`patientID`), "
    "  CONSTRAINT `ingredient2` FOREIGN KEY (`codingSystem` ,  `codingID`) "
    "     REFERENCES `Ingredient` (`codingSystem` ,  `codingID`) "
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