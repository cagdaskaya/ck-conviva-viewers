# import base64
# import http.client
#
# conn = http.client.HTTPSConnection("api.conviva.com")
#
# encoded = base64.b64encode(b"cagdas.kaya@sky.uk:password").decode("ascii")
# headers = {
#     'Cache-Control': 'no-cache',
#     'Authorization': f'Basic {encoded}'
#     }
#
# api = "/insights/2.4/viewer/views.json"
# query = "?viewer_id=4f18f7b5e8e6bcc8fbed5448002ea0ee5c70dc0d"
# path = api + query
# conn.request("GET", path, headers=headers)
#
# res = conn.getresponse()
# data = res.read()
#
# print(encoded)
# print(data.decode("utf-8"))



