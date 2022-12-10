import json
import requests

endpoint = "http://127.0.0.1:5011/items"


def get_stock(item_id):
    # return stock of an item
    stock_url = f"{endpoint}/{item_id}"
    rsp = requests.get(url=stock_url).json()
    stock = rsp["stock"]
    return stock


def minus_stock(item_id, amount):
    old_stock = get_stock(item_id)
    if old_stock < amount:
        return False
    new_stock = old_stock - amount
    stock_url = f"{endpoint}/{item_id}"
    update_json = {"stock": new_stock}
    rsp = requests.put(url=stock_url, json=update_json)
    return True


if __name__ == "__main__":
    # # json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)
    # data = json.dumps(r.json(), sort_keys=True, indent=4)
    num_of_item_available = get_stock(2)
    print(num_of_item_available)
    print(minus_stock(item_id=2, amount=7))

