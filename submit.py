from requests import post

def makeDict(counter):
    res = {}
    res['name'] = 'Product No.%s' % counter
    res['price'] = '%s' % (0.67*(counter-0.43)**3)
    res['category'] = 'Category No.%s' % (counter % 5)
    return res

<<<<<<< HEAD
if __name__=="__main__":
    target = "http://localhost:5000/product-create"
=======

if __name__=="__main__":
    target = "http://localhost:5000/product-admin-submit"
>>>>>>> wtforms_image
    for i in range(30):
        post(target, makeDict(i))
