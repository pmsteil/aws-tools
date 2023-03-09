# python

import os



for i in range(5, 15):

    item = '''{ "cart_id": { "N": "%s" },
        "customer_name": { "S": "John Doe" },
        "customer_address": { "M": { "city": { "S": "Chico" },
                "address1": { "S": "333 Mulberry Lane" },
                "state": { "S": "TX"}}}}
        ''' % i

    print( f"adding ({i}) item: {item}" )

    # call aws cli to put item
    os.system("aws dynamodb put-item --table-name carts --item '{}'".format(item))
