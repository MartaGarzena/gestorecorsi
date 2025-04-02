from database.DB_connect import DBConnect
from model.corso import Corso
from model.studente import Studente


class DAO():
    @staticmethod
    def getCodins():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT c.codins 
                        FROM corso c"""

            cursor.execute(query)

            for row in cursor:
                res.append(row["codins"])
            #processa res

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getAllCorsi():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT * FROM corso c"""

            cursor.execute(query)

            res = []
            for row in cursor:
                # res.append(Corso(codins=row["codins"],
                #                  crediti = row["crediti"],
                #                  nome = row["nome"],
                #                  pd = row["pd"]))
                res.append(Corso(**row))
            # processa res

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getCorsiPD(pd):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT *
                        FROM corso c
                        WHERE c.pd = %s"""

            cursor.execute(query, (pd,))

            res = []
            for row in cursor:
                res.append(Corso(**row))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getCorsiPDwithIscritti(pd):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT c.codins, c.crediti, c.nome, c.pd, count(*) as n
                        FROM corso c, iscrizione i
                        where c.codins = i.codins 
                        and c.pd = %s
                        group by c.codins, c.crediti, c.nome, c.pd"""

            cursor.execute(query, (pd,))

            res = []
            for row in cursor:
                res.append((Corso(row["codins"],
                                   row["crediti"],
                                   row["nome"],
                                   row["pd"]), row["n"]))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getStudentiCorso(codins):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT s.*
                        FROM studente s , iscrizione i 
                        WHERE s.matricola = i.matricola 
                        and i.codins = %s"""

            cursor.execute(query, (codins,))

            res = []
            for row in cursor:
                res.append(Studente(**row))
                # res.append(Studente(row["matricola"],
                #                     row["cognome"],
                #                     row["nome"],
                #                     row["CDS"]))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getCDSofCorso(codins):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT s.CDS, count(*) as n 
                        FROM studente s, iscrizione i 
                        WHERE s.matricola = i.matricola 
                        and i.codins = %s
                        and s.CDS != ""
                        group by s.CDS """

            cursor.execute(query, (codins,))

            res = []
            for row in cursor:
                res.append( (row["CDS"], row["n"]) )

            cursor.close()
            cnx.close()
            return res

if __name__ == "__main__":
    print(DAO.getCodins())
    for c in DAO.getCorsiPDwithIscritti(1):
        print(c)

