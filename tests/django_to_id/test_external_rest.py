import OsmApi

#curl -X GET http://127.0.0.1:8000/api/0.6/node/1 -u admin:password > out.html

class IntegrationTest(object):
    def __init__(self):
        pass

    def run(self):
        #first create a changeset

        osm_api = OsmApi.OsmApi(api="127.0.0.1", port=8000, username="admin", password="password")
        test = osm_api.NodeGet(1)
        print(test)


if __name__ == "__main__":
    it = IntegrationTest()
    it.run()



