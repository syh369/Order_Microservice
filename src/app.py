from flask import Flask, Response, request, jsonify, json

from application_services.catalog_item_info_resource import OrderInfoResource

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
        order = OrderInfoResource.get_order_by_id(new_order_id)
        rsp = jsonify(order)
        # rsp = Response(json.dumps({"message": "new item added"}), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "item creation failed"}), status=500, content_type="application/json")
    return rsp


@app.route("/order/<int:orderid>/orderline", methods=["POST"])
def add_orderline_item(orderid):
    data = json.loads(request.data)
    new_lineid = OrderInfoResource.add_orderline_item(
        orderid=orderid,
        itemid=data["itemid"],
        price=data["price"],
        amount=data["amount"]
    )
    if new_lineid:
        orderline = OrderInfoResource.get_order_by_id(orderid)["orderline"]
        for item in orderline:
            if item["lineid"] == new_lineid:
                return jsonify(item)
    else:
        return Response(json.dumps({"message": "can/t add item to orderline failed"}),
                        status=500, content_type="application/json")


@app.route("/order/<int:orderid>", methods=["GET"])
def get_order_by_id(orderid):
    result = OrderInfoResource.get_order_by_id(orderid)
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/order/<int:orderid>/orderline/<int:lineid>")
def get_orderline_by_id(orderid, lineid):
    orderline = OrderInfoResource.get_order_by_id(orderid)["orderline"]
    for item in orderline:
        if item["lineid"] == lineid:
            return jsonify(item)
    return Response("NOT FOUND", status=404, content_type="text/plain")


@app.route("/order/<string:email>", methods=["GET"])
def get_order_by_email(email):
    result = OrderInfoResource.get_order_by_email(email)
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/order/<int:orderid>", methods=["DELETE"])
def delete_order_by_id(orderid):
    OrderInfoResource.delete_order_by_id(orderid)

    rsp = Response("", status=200, content_type="application/json")
    return rsp


'''
@app.route("/order", methods="GET")
def get_post_items():
    if request.method == "GET":
        result = OrderInfoResource.get_items()
        if result:
            rsp = jsonify(result)
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp

@app.route("/orderinfo/<int:orderID>", methods=["GET"])
def get_orderinfo_by_id(orderID):
    result = OrderInfoResource.get_orderinfo_by_id(orderID)
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/catalog/<string:name>", methods=["GET"])
def get_item_by_name(name):
    result = CatalogItemInfoResource.get_item_by_name(name)
    if result:
        for item in result:
            item["stock"] = CatalogItemInfoResource.get_item_stock_by_id(item["id"])["stock"]
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/stock/<int:item_id>", methods=["GET"])
def get_item_stock_by_id(item_id):
    result = CatalogItemInfoResource.get_item_stock_by_id(item_id)
    if result:
        rsp = jsonify(result["stock"])
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/delete/<int:item_id>", methods=["DELETE"])
def delete_item_by_id(item_id):
    CatalogItemInfoResource.delete_item_by_id(item_id)
    # Don't know how the packet forms yet
    rsp = Response("", status=200, content_type="application/json")
    return rsp


@app.route("/catalog/update", methods=["PUT"])
def update_item_by_id():
    data = json.loads(request.data)
    # print(data)
    CatalogItemInfoResource.update_item_by_id(
        item_id=data["item_id"],
        update_column=data["update_column"],
        value_update=data["value_update"])
    rsp = Response("", status=200, content_type="application/json")
    return rsp
'''

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5011)
