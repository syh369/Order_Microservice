from flask import Flask, Response, request, jsonify, json, url_for

from application_services.catalog_item_info_resource import OrderInfoResource
from utils import wrap_pagination, wrap_link, wrap_pg_dict

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {
        "get_order_by_id": "/order/<int:orderid>",
        "get_order_by_email": "/order/<str:email>",
        "delete_order_by_id": "/order/<int:order_id>",
    }
    return jsonify(context)


@app.route("/order", methods=["POST"])
def add_order_new():
    data = json.loads(request.data)
    new_order_id = OrderInfoResource.add_order_new(
        email=data["email"],
        shipping_info=data["shipping_info"],
        billing_info=data["billing_info"]
    )
    if new_order_id:
        _, _, pg_dict = wrap_pg_dict(enable=False)
        order, _ = OrderInfoResource.get_order_by_id(new_order_id, pg_dict)
        rsp = jsonify(order)
        # rsp = Response(json.dumps({"message": "new item added"}), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "item creation failed"}), status=500, content_type="application/json")
    return rsp


@app.route("/order/<int:orderid>/orderline", methods=["POST"])
def add_orderline_item(orderid):
    data = json.loads(request.data)
    _, _, pg_dict = wrap_pg_dict(enable=False)
    exist, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if not exist:
        return Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    new_lineid = OrderInfoResource.add_orderline_item(
        orderid=orderid,
        itemid=data["itemid"],
        price=data["price"],
        amount=data["amount"]
    )
    if new_lineid:
        OrderInfoResource.update_order_total(orderid)
        _, _, pg_dict = wrap_pg_dict(enable=False)
        orderinfo, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
        orderline = orderinfo["orderline"]
        for item in orderline:
            if item["lineid"] == new_lineid:
                return jsonify(item)
    else:
        return Response(json.dumps({"message": "can/t add item to orderline failed"}),
                        status=500, content_type="application/json")


@app.route("/order/<int:orderid>", methods=["GET"])
def get_order_by_id(orderid):
    page, pagesize = request.args.get("page", type=int), request.args.get("pagesize", type=int)
    page, pagesize, pg_dict = wrap_pg_dict(page=page, pagesize=pagesize, enable=True)
    result, num_of_rows = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if result:
        print("result")
        print(result)
        # add links
        for item in result["orderline"]:
            item["links"] = list()
            item["links"].append(wrap_link(url_for("get_order_by_id", orderid=item["orderid"]), "order"))
            item["links"].append(wrap_link(url_for("get_orderline_by_id",
                                                   orderid=item["orderid"], lineid=item["lineid"]), "self"))
        result["orderline"] = wrap_pagination(result["orderline"], pagesize, page, num_of_rows)

        rsp = jsonify(result)
    else:
        rsp = Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    return rsp


# TODO: fix this, check the return of get_order_by_id
@app.route("/order/<int:orderid>/orderline/<int:lineid>")
def get_orderline_by_id(orderid, lineid):
    _, _, pg_dict = wrap_pg_dict(enable=False)
    orderinfo, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if orderinfo:
        orderline = orderinfo["orderline"]
    else:
        return Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    for line in orderline:
        if line["lineid"] == lineid:
            line["links"] = list()
            line["links"].append(wrap_link(url_for("get_order_by_id", orderid=line["orderid"]), "order"))
            line["links"].append(wrap_link(url_for("get_orderline_by_id", orderid=line["orderid"], lineid=line["lineid"]), "self"))
            return jsonify(line)
    return Response(json.dumps({"message": "order line not found"}), status=404, content_type="application/json")


@app.route("/order/<string:email>", methods=["GET"])
def get_order_by_email(email):
    page, pagesize = request.args.get("page", type=int), request.args.get("pagesize", type=int)
    page, pagesize, pg_dict = wrap_pg_dict(page=page, pagesize=pagesize, enable=True)
    results, num_of_rows = OrderInfoResource.get_order_by_email(email, pg_dict)
    if num_of_rows:
        for res in results:
            res["links"] = list()
            res["links"].append(wrap_link(url_for("get_order_by_id", orderid=res["orderid"]), "order"))
            res["links"].append(wrap_link(url_for("get_order_by_email", email=res["email"]), "self"))
        rsp = jsonify(wrap_pagination(results, pagesize, page, num_of_rows))
    else:
        rsp = Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    return rsp


@app.route("/order/<int:orderid>", methods=["PUT"])
def update_order_by_id(orderid):
    new_data = json.loads(request.data)
    _, _, pg_dict = wrap_pg_dict(enable=False)
    exist, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if not exist:
        return Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    success = OrderInfoResource.update_order_by_id(orderid, new_data)
    if success:
        _, _, pg_dict = wrap_pg_dict(enable=False)
        res, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
        res = res['orderinfo']
    else:
        res = Response(json.dumps({"message": "same order update"}), status=400, content_type="application/json")
    return res


@app.route("/order/<int:orderid>/orderline/<int:lineid>", methods=["PUT"])
def update_orderline_by_id(orderid, lineid):
    new_data = json.loads(request.data)
    _, _, pg_dict = wrap_pg_dict(enable=False)
    exist, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if not exist:
        return Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    orderline = exist["orderline"]
    print(orderline)
    lineid_list = []
    for line in orderline:
        lineid_list.append(line["lineid"])
    if lineid not in lineid_list:
        return Response(json.dumps({"message": "orderline not found"}), status=404, content_type="application/json")
    success = OrderInfoResource.update_orderline_by_id(orderid, lineid, new_data)
    if success:
        OrderInfoResource.update_order_total(orderid)
        _, _, pg_dict = wrap_pg_dict(enable=False)
        res, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
        for line in res['orderline']:
            if line['lineid'] == lineid:
                res = line
    else:
        res = Response(json.dumps({"message": "same orderline update"}), status=400, content_type="application/json")
    return res


@app.route("/order/<int:orderid>", methods=["DELETE"])
def delete_order_by_id(orderid):
    _, _, pg_dict = wrap_pg_dict(enable=False)
    exist, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    if not exist:
        return Response(json.dumps({"message": "order not found"}), status=404, content_type="application/json")
    success = OrderInfoResource.delete_order_by_id(orderid)
    if success:
        rsp = Response(json.dumps({"message": "order deletion successful"}), status=200,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "order deletion failed"}), status=500, content_type="application/json")
    return rsp


@app.route("/order/<int:orderid>/orderline/<int:lineid>", methods=["DELETE"])
def delete_orderline_by_id(orderid, lineid):
    _, _, pg_dict = wrap_pg_dict(enable=False)
    orderinfo, _ = OrderInfoResource.get_order_by_id(orderid, pg_dict)
    ret_line = orderinfo["orderline"]
    lineid_list = []
    for line in ret_line:
        lineid_list.append(line["lineid"])
    if lineid not in lineid_list:
        return Response(json.dumps({"message": "orderline not found"}), status=404, content_type="application/json")
    success = OrderInfoResource.delete_orderline_by_id(orderid, lineid)
    if success:
        OrderInfoResource.update_order_total(orderid)
        rsp = Response(json.dumps({"message": "orderline deletion successful"}), status=200,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "orderline deletion failed"}), status=500,
                       content_type="application/json")
    return rsp


'''
'''

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5013)
