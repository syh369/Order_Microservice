"""
# GET order info: order/<int:order_id>
# GET order line info: orderline/<int:order_id>
# DELETE item info: catalog/delete/<item_id>
# POST item info: newitem/
PATCH item info: update/<item_id>
"""

from database_services.rdb_services import RDBService


class OrderInfoResource:
    @classmethod
    def get_order_by_id(cls, orderID):
        """
        :param orderID: id of order
        :return: a dic of the order (order information includes all the line)
        """
        result = RDBService.find_by_template_join(
            db_schema="f22_orders",
            table_name1="order",
            table_name2="orderline",
            column_names1=["orderid", "email", "order_date", "total", "shipping_info", "billing_info"],
            column_names2=["orderid", "lineid", "itemid", "price", "amount", "subtotal"],
            template=None,
            join_column1="orderid",
            join_column2="orderid"
        )
        return result

    @classmethod
    def get_order_by_email(cls, email):
        """
        :param email: customer registration info email
        :return: a dic of the order
        """
        result = RDBService.get_by_value("f22_orders", "orderline", "email", email)
        return result

    @classmethod
    def delete_order_by_id(cls, orderid):
        RDBService.delete_by_value("f22_orders", "order", "orderid", orderid)
        RDBService.delete_by_value("f22_orders", "orderline", "orderid", orderid)

'''
    @classmethod
    def delete_line_by_id(cls, orderid, lineid):
        conn = cls._get_db_connection()
        cur = conn.cursor()
        db_schema = "f22_orders"
        table_name = "orderline"

        sql = "delete from " + db_schema + "." + table_name + " where " + \
              "orderid = " + str(orderid) + " and where lineid = " + str(lineid)
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        print(res)
        res = cur.fetchall()
        conn.commit()

    @classmethod
    def create_order_new(cls, email, shipping_info, billing_info):
        RDBService.add_by_prefix(
            db_schema="f22_orders",
            table_name="order",
            column_names=["email", "shipping_info", "billing_info"],
            values=[email, shipping_info, billing_info]
        )

    @classmethod
    def add_line_new(cls, line_id, order_id, item_id, price, amount):
        RDBService.add_by_prefix(
            db_schema="f22_orders",
            table_name="orderline",
            column_names=["line_id", "order_id", "item_id", "price", "amount"],
            values=[line_id, order_id, item_id, price, amount]
        )

    @classmethod
    def update_item_by_id(cls, item_id, update_column, value_update):
        """
        update an attribute of a item by id
        :param item_id:
        :param update_column:
        :param value_update:
        :return:
        """
        if update_column != "stock":
            RDBService.update_by_template("catalog_db",
                                          "item_info",
                                          "id",
                                          item_id,
                                          update_column,
                                          value_update)
        else:
            RDBService.update_by_template("catalog_db",
                                          "item_stocking",
                                          "item_id",
                                          item_id,
                                          update_column,
                                          value_update)
'''