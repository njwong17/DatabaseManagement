import psycopg2
from tabulate import tabulate

def deleteDatabase():
    #Delete Databases
    cur.execute("""DROP TABLE IF EXISTS Stock;""")
    cur.execute("""DROP TABLE IF EXISTS Product;""")
    cur.execute("""DROP TABLE IF EXISTS Depot;""")
    


def setupDatabase():
    #Product Database
    cur.execute("""CREATE TABLE Product(prod varchar(255),pname varchar(255),price int);""")
    cur.execute("""INSERT INTO Product(prod, pname, price) VALUES ('p1', 'tape', 2.5), ('p2', 'tv', 250), ('p3', 'ver', 80);""")
    cur.execute("""ALTER TABLE product ADD CONSTRAINT primary_product PRIMARY KEY (prod);""")
    #Depot Database
    cur.execute("""CREATE TABLE Depot(dep varchar(255), addr varchar(255), volume int);""")
    cur.execute("""INSERT INTO Depot(dep, addr, volume) VALUES ('d1', 'New York', 9000), ('d2', 'Syracuse', 6000), ('d4', 'New York', 2000);""")
    cur.execute("""ALTER TABLE depot ADD CONSTRAINT primary_depot PRIMARY KEY (dep);""")
    #Stock Database
    cur.execute("""CREATE TABLE Stock(prod varchar(255),dep varchar(255),quantity int);""")
    cur.execute("""INSERT INTO Stock(prod, dep, quantity) VALUES('p1', 'd1', 1000),
    ('p1', 'd2', -100),('p1', 'd4', 1200),('p3', 'd1', 3000),('p3', 'd4', 2000),
    ('p2', 'd4', 1500),('p2', 'd1', -400),('p2', 'd2', 2000);""")


con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="lychee")

#For isolation: SERIALIZABLE
con.set_isolation_level(3)
#For atomicity
con.autocommit = False

try:
    cur = con.cursor()
    #Set Database to original state for testing
    deleteDatabase()
    setupDatabase()
    
    cur.execute("""ALTER TABLE stock
    ADD CONSTRAINT FK_PROD_STO
    FOREIGN KEY (prod) REFERENCES product(prod) ON DELETE CASCADE;""")

    cur.execute("""DELETE FROM product WHERE prod='p1';""")

    cur.execute("""SELECT * FROM product;""")

    print(cur.fetchall())

    cur.execute("""SELECT * FROM stock;""")

    print(cur.fetchall())

except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback()
finally:
    if con:
        con.commit()
        cur.close
        con.close
        print("PostgreSQL connection is now closed")