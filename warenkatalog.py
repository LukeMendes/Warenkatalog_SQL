import mysql
import mysql.connector
from time import sleep
def datenbank_erstellen():
    connection = verbindung_herstellen(False)
    c = connection.cursor()
    try:
        c.execute("""CREATE DATABASE if not exists warenkatalog;""")
        print("Datenbank erfolgreich erstellt.")
    except mysql.connector.Error:
        print(f"Fehler beim Erstellen der Datenbank: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def verbindung_herstellen(vorhandene_Datenbank=True):
    try:
        if vorhandene_Datenbank:
            conn = mysql.connector.connect(host='localhost', user='root', password='12345', db='warenkatalog')
            return conn
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='12345')
            return conn
    except mysql.connector.errors.ProgrammingError:
        print("Es ist ein Fehler bei der Verbindung mit der Datenbank aufgetreten!")
        sleep(5)
        return Exception
def tabelle_erstellen():
    connection = verbindung_herstellen()
    c = connection.cursor()
    try:
        sql = """CREATE TABLE IF NOT EXISTS warenkatalog (ID INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                                    produktname VARCHAR(50) NOT NULL,
                                                    artikelnummer VARCHAR(50) NOT NULL,
                                                    nettopreis DECIMAL(10, 2) NOT NULL);"""
        c.execute(sql)
        connection.commit()
        print("Tabelle erfolgreich erstellt.")
    except mysql.connector.Error():
        print(f"Fehler beim Erstellen der Tabelle: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def tabelle_zeigen():
    connection = verbindung_herstellen()
    c = connection.cursor()
    leer = True
    try:
        c.execute("""SELECT * FROM warenkatalog;""")
        tabelle = c.fetchall()
        if len(tabelle) != 0:
            leer = False
    except mysql.connector.Error:
        print(f"Fehler beim Anzeigen der Tabelle: {mysql.connector}")
        sleep(5)
    finally:
        connection.close()
        if leer == False:
            return tabelle
        else:
            return "Die Tabelle enthält noch keine Einträge."
def artikel_hinzufügen():
    connection = verbindung_herstellen()
    c = connection.cursor()
    try:
        name = input("Bitte geben Sie den Namen des Artikels ein: ")
        nummer = input("Bitte geben Sie die Nummer des Artikels ein: ")
        preis = float(input("Bitte geben Sie den Nettopreis des Artikels ein: "))
        params = (name, nummer, preis)
        sql = """INSERT INTO warenkatalog (produktname, artikelnummer, nettopreis) VALUES (%s, %s, %s);"""
        c.execute(sql, params)
        connection.commit()
        print("Eintrag erfolgreich hinzugefügt.")
    except mysql.connector.Error():
        print(f"Fehler beim hinzufügen des Eintrags: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def spalte_hinzufügen():
    connection = verbindung_herstellen()
    c = connection.cursor()
    try:
        name = input("Bitte geben Sie den Namen der neuen Spalte ein: ")
        datentyp = input("""Bitte geben Sie den Datentyp der neuen Spalte ein. 
        INT(Länge), VARCHAR(Länge), BOOL, DATE, DECIMAL(Länge, Kommastellen)
        -->""")
        sql = f"""ALTER TABLE warenkatalog ADD {name} {datentyp};"""
        c.execute(sql)
        connection.commit()
        print("Spalte erfolgreich hinzugefügt.")
    except mysql.connector.Error():
        print(f"Fehler beim hinzufügen der Spalte: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def tabelle_aktualisieren(inhalt, count):
    connection = verbindung_herstellen()
    c = connection.cursor()
    while True:
        try:
            id = int(input("Bitte geben Sie die ID des Eintrags ein, der geändert werden soll: "))
            sleep(3)
            if id < 1 or id > count:
                raise Exception
            aktualisieren = input("Bitte geben Sie die Spalte ein, die geändert werden soll: ")
            sleep(3)
            wert = input("Bitte geben Sie den neuen Wert an: ")
            sleep(3)
            break
        except Exception:
            print("Ungültige Eingabe!\n\nInhalt:\n")
            sleep(5)
            for i in inhalt:
                print(i)
            sleep(5)
    try:
        params = (wert, id)
        sql = f"""UPDATE warenkatalog SET {aktualisieren} = %s WHERE ID = %s;"""
        c.execute(sql, params)
        connection.commit()
        print("Eintrag erfolgreich aktualisiert.")
    except mysql.connector.Error():
        print(f"Fehler beim aktualisieren des Eintrags: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def artikel_löschen(inhalt, count):
    connection = verbindung_herstellen()
    c = connection.cursor()
    while True:
        try:
            id = int(input("Bitte geben Sie die ID des Eintrags ein, der gelöscht werden soll: "))
            sleep(3)
            if id < 1 or id > count:
                raise Exception
            break
        except Exception:
            print("Ungültige Eingabe!\n\nInhalt:\n")
            sleep(5)
            for i in inhalt:
                print(i)
            sleep(5)
    try:
        params = (id,)
        sql = f"""DELETE FROM warenkatalog WHERE ID = %s;"""
        c.execute(sql, params)
        connection.commit()
        print("Eintrag erfolgreich gelöscht.")
    except mysql.connector.Error():
        print(f"Fehler beim löschen des Eintrags: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def datenbank_löschen():
    connection = verbindung_herstellen(False)
    c = connection.cursor()
    try:
        c.execute("""DROP TABLE IF EXISTS warenkatalog;""")
        connection.commit()
    except mysql.connector.Error:
        print(f"Fehler beim Löschen der Datenbank: {mysql.connector.Error}")
        sleep(5)
    finally:
        connection.close()
def programm_beenden():
    inhalt = tabelle_zeigen()
    sleep(3)
    print("\nLetzter Stand der Tabelle:\n")
    sleep(5)
    for i in inhalt:
        print(i)
    sleep(5)
    print("Programm beendet.")
    exit(0)
def main():
    try:
        connection = verbindung_herstellen(False)
        c = connection.cursor()
        c.execute("""SHOW DATABASES""")
        datenbanken = c.fetchall()
        connection.close()
        if ("warenkatalog",) in datenbanken:
            print("Die Datenbank \"warenkatalog\" existiert bereits.")
            sleep(1)
            while True:
                sleep(2)
                löschen = input("Soll die Datenbank gelöscht werden? y/n: ").lower()
                sleep(2)
                if löschen == "y":
                    datenbank_löschen()
                    sleep(3)
                    datenbank_erstellen()
                    sleep(3)
                    break
                elif löschen == "n":
                    break
                else:
                    print("Ungültige Eingabe!")
        else:
            print("Die Datenbank \"warenkatalog\" existiert noch nicht.")
            sleep(3)
            datenbank_erstellen()
        connection = verbindung_herstellen()
        c = connection.cursor()
        c.execute("""SHOW TABLES;""")
        tabellen = c.fetchall()
        connection.close()
        if ("warenkatalog",) in tabellen:
                print("Die Tabelle \"warenkatalog\" existiert bereits.")
        else:
            print("Die Tabelle \"warenkatalog\" existiert noch nicht.")
            sleep(3)
            datenbank_erstellen()
        menü = ["1 -> Artikel hinzufügen", "2 -> Spalte hinzufügen", "3 -> Tabelle aktualisieren",
                "4 -> Artikel löschen", "5 -> Programm beenden"]
        while True:
            count = 0
            inhalt = tabelle_zeigen()
            sleep(2)
            if type(inhalt) == str:
                print(f"\n{inhalt}")
            else:
                print("\nInhalt:")
                for i in inhalt:
                    print(i)
                    count += 1
            try:
                sleep(5)
                print("Menü")
                for i in menü:
                    print(i)
                sleep(5)
                auswahl = int(input("Was wollen Sie machen: "))
                sleep(3)
                if auswahl < 1 or auswahl > len(menü):
                    raise Exception
                match auswahl:
                    case 1:
                        artikel_hinzufügen()
                    case 2:
                        spalte_hinzufügen()
                    case 3:
                        if type(inhalt) == str:
                            print(f"\n{inhalt} Die Tabelle kann nicht aktualisiert werden.")
                        else:
                            tabelle_aktualisieren(inhalt, count)
                    case 4:
                        if type(inhalt) == str:
                            print(f"\n{inhalt} Die Tabelle kann keine Einträge löschen.")
                        else:
                            artikel_löschen(inhalt, count)
                    case 5:
                        raise KeyboardInterrupt
            except KeyboardInterrupt:
                print("Programm wird beendet...")
                return programm_beenden()
            except Exception:
                print("Ungültige Eingabe!")
    except KeyboardInterrupt:
        print("Programm wird beendet...")
        return programm_beenden()
    except:
        sleep(1)
        print("Ein Fehler ist aufgetreten!")
        return exit(-1)
if __name__ == "__main__":
    main()