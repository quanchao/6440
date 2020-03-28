from datetime import date, datetime, timedelta
import mysql.connector
db = mysql.connector.connect(host='localhost',user='root',passwd='123456.abc')

cursor = db.cursor()

def medicitionForSameDisease(medicationID):
    query =("SELECT h1.medicationID FROM Medication as h1 "
             "left outer join  MedicationDispense as h2 on h1.medicationID = h2.medicationID "
             "join Dispense as h3 on h2.dispenseID = h3.dispenseID "
             "WHERE PatientDisease in"
             "(SELECT PatientDisease FROM Medication as h1 "
             "left outer join  MedicationDispense as h2 on h1.medicationID = h2.medicationID "
             "join Dispense as h3 on h2.dispenseID = h3.dispenseID "
             "WHERE h1.medicationID is %s)")
    cursor.execute(query, medicationID)
    res = []
    for id in cursor:
        res.append(id)
    return res

def medicationForSameIngredient(medicationID):
    query = ("SELECT h1.medicationID FROM Medication as h1 "
             "left outer join  MedicationIngredient as h2 on h1.medicationID = h2.medicationID "
             "join Ingredient as h3 on h2.codingSystem = h3.codingSystem and h2.codingID = h3.codingID  "
             "WHERE h2.Ingredient in"
             " (SELECT h2.Ingredient FROM Medication as h1 "
             "left outer join  MedicationIngredient as h2 on h1.medicationID = h2.medicationID "
             "join Ingredient as h3 on h2.codingSystem = h3.codingSystem and h2.codingID = h3.codingID "
             "WHERE h1.medicationID is %s)")
    cursor.execute(query,medicationID)
    res = []
    for id in cursor:
        res.append(id)
    return res

def countUsage(medicationID):
    query = ("SELECT count(*) FROM Medication as h1 "
             "left outer join  MedicationDispense as h2 on h1.medicationID = h2.medicationID "
             "join Dispense as h3 on h2.dispenseID = h3.dispenseID "
             "WHERE h1.medicationID is %s")
    cursor.execute(query, medicationID)
    res = []
    for id in cursor:
        res.append(id)
    return res[0]




def countUsageByMonth(medicationID):
    query = ("SELECT count(*) FROM Medication as h1 "
             "left outer join  MedicationDispense as h2 on h1.medicationID = h2.medicationID "
             "join Dispense as h3 on h2.dispenseID = h3.dispenseID "
             "WHERE h1.medicationID is %s "
             "GROUP BY YEAR(whenPrepared), Month(whenPrepared) "
             "ORDER BY YEAR(whenPrepared), Month(whenPrepared) DESC"
             )
    cursor.execute(query, medicationID)
    res = []
    for num in cursor:
        res.append(num)
    return res


def countAllergyOccurrence(medicationID):
    query = ("SELECT count(*) FROM Medication as h1 "
             "left outer join  MedicationIngredient as h2 on h1.medicationID = h2.medicationID "
             "join Ingredient as h3 on h2.codingSystem = h3.codingSystem and h2.codingID = h3.codingID  "
             "join Allergy as h4 on h2.codingSystem = h3.codingSystem and h2.codingID = h3.codingID "
             "WHERE h1.medicationID is %s ")
    cursor.execute(query, medicationID)
    res = []
    for num in cursor:
        res.append(num)
    return res[0]


cursor.close()
db.close()