from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select distinct(year(`Date`)) as year
                    from go_daily_sales"""

        cursor.execute(query, )

        for row in cursor:
            res.append(row["year"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllNations():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select distinct(Country) 
                    from go_retailers gr """

        cursor.execute(query, )

        for row in cursor:
            res.append(row["Country"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodes(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select *
                    from go_retailers
                    where Country = %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            res.append(Retailer(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def verificaNodi(nodo1: Retailer, nodo2: Retailer, year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select count(distinct(gds.Product_number)) as N
                    from go_daily_sales gds, go_daily_sales gds2 
                    where gds.Retailer_code = %s and gds2.Retailer_code = %s
                    and year(gds2.`Date`) = year(gds.`Date`) and year(gds2.`Date`) = %s and gds2.Product_number = gds.Product_number
                    group by gds.Retailer_code, gds2.Retailer_code  """

        cursor.execute(query, (nodo1.Retailer_code, nodo2.Retailer_code, year))

        for row in cursor:
            res.append(row)

        cursor.close()
        conn.close()
        if len(res) == 0:
            return
        if res[0] == 0:
            return
        return res
