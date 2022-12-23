"""
# GET order info: order/<int:order_id>
# GET order line info: orderline/<int:order_id>
# DELETE item info: catalog/delete/<item_id>
# POST item info: newitem/
PATCH item info: update/<item_id>
"""

from src.database_services.rdb_services import RDBService


class OrderInfoResource:
    @classmethod
    def add_order_new(cls, email, shipping_info, billing_info):
        res = RDBService.add_by_prefix(
            db_schema="f22_orders",
            table_name="order",
            column_names=["email", "shipping_info", "billing_info"],
            values=[email, shipping_info, billing_info]
        )
        return res

    @classmethod
    def add_orderline_item(cls, orderid, itemid, price, amount):
        new_lineid = RDBService.add_by_prefix_orderline(
            db_schema="f22_orders",
            table_name="orderline",
            column_names=["orderid", "itemid", "price", "amount"],
            # calculate subtotal by given price and amount
            values=[orderid, itemid, price, amount]
        )
        # total = ('total', price*amount)
        # total_info = [total]
        # _ = RDBService.update_by_value(db_schema="f22_orders",
        #                                           table_name="order",
        #                                           column_name="orderid",
        #                                           value=orderid,
        #                                           update_columns=total_info)
        return new_lineid

    @classmethod
    def get_order_by_id(cls, orderid, pg_dict):
        """
        :param pg_dict:
        :param orderid: order id
        :return: a dic of the order info
        """
        r1, _ = RDBService.get_by_value("f22_orders", "order", "orderid", [orderid], {"pg_flag": False})
        r2, num_of_rows = RDBService.get_by_value("f22_orders", "orderline", "orderid", [orderid], pg_dict)
        print('order:')
        print(r1)
        print('order_line:')
        print(r2)
        if r1:
            result = {'orderinfo': r1[0], 'orderline': r2}
        else:
            result = None
        return result, num_of_rows

    @classmethod
    def get_order_by_email(cls, email, pg_dict):
        """
        :param pg_dict: for pagination
        :param email: customer registration info email
        :return: a dic of the order
        """
        result, num_of_rows = RDBService.get_by_value("f22_orders", "order", "email", [email], pg_dict)
        return result, num_of_rows

    @classmethod
    def update_order_by_id(cls, orderid, new_data: dict):
        set_orderinfo_list = []
        for k, v in new_data.items():
            set_orderinfo_list.append((k, v))
        row_affected = 0
        if set_orderinfo_list:
            row_affected = RDBService.update_by_value(db_schema="f22_orders",
                                                      table_name="order",
                                                      column_name="orderid",
                                                      value=orderid,
                                                      update_columns=set_orderinfo_list)
        if row_affected == 0:
            return False
        else:
            return True

    @classmethod
    def update_orderline_by_id(cls, orderid, lineid, new_data: dict):
        set_orderline_list = []
        for k, v in new_data.items():
            set_orderline_list.append((k, v))
        row_affected = 0
        if set_orderline_list:
            row_affected = RDBService.update_by_value_2(db_schema="f22_orders",
                                                      table_name="orderline",
                                                      column_name1="lineid",
                                                      column_name2="orderid",
                                                      value1=lineid,
                                                      value2=orderid,
                                                      update_columns=set_orderline_list)
        if row_affected == 0:
            return False
        else:
            return True

    @classmethod
    def delete_order_by_id(cls, orderid):
        res = RDBService.delete_by_value("f22_orders", "orderline", "order", "orderid", "orderid", orderid)
        return res

    @classmethod
    def delete_orderline_by_id(cls, orderid, lineid):
        id_list = [orderid, lineid]
        res = RDBService.delete_by_value_single_table("f22_orders", "orderline", "orderid", "lineid", id_list)
        return res

    @classmethod
    def update_order_total(cls, orderid):
        row = RDBService.update_order_total(db_schema = 'f22_orders',
                                            table_name1 = 'orderline',
                                            table_name2 = 'order',
                                            orderid = orderid)
        if row == 0:
            return False
        else:
            return True

    #@classmethod
    # def update_total(cls, orderid, lineid):



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
