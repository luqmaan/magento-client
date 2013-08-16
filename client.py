from suds.client import Client


def enable_logging():
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(
        logging.DEBUG)  # MUST BE THIS?
    # logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
    # logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
    # logging.getLogger('suds.resolver').setLevel(logging.DEBUG)
    # logging.getLogger('suds.xsd.query').setLevel(logging.DEBUG)
    # logging.getLogger('suds.xsd.basic').setLevel(logging.DEBUG)
    # logging.getLogger('suds.binding.marshaller').setLevel(logging.DEBUG)


def products_to_skus(products):
    return dict([(int(prod.product_id), prod) for prod in products])


def get_magento_products(client, session):
    """ Gets products from Magento's API """
    products = client.service.catalogProductList(session)
    skus = [product['sku'] for product in products]
    inventory = client.service.catalogInventoryStockItemList(session, skus)
    transformed = products_to_skus(inventory)
    ordoro_products = []
    for product in products:
        ordoro_products.append({
            "sku": product.sku,
            "cart_specific_id": product.product_id,
            "quantity": transformed[int(product.product_id)].qty
        })
    return ordoro_products


def get_api_products():
    """ Simulates querying products from Ordoro's API """
    return [{'sku': 'n2610', 'quantity': 996.0000, 'cart_specific_id': 16},
            {'sku': 'bb8100', 'quantity': 797.0000, 'cart_specific_id': 17}]


def main():
    username = 'username'
    password = 'abc123'
    url = 'http://magento.localhost/api/v2_soap/?wsdl'
    client = Client(url)
    session = client.service.login(username, password)
    products = get_magento_products(client, session)
    print products


if __name__ == "__main__":
    main()
