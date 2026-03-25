import json, unittest, datetime

with open("./data-1.json","r", encoding="utf-8") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r", encoding="utf-8") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    parts = jsonObject["location"].split("/")

    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": parts[0],
            "city": parts[1],
            "area": parts[2],
            "factory": parts[3],
            "section": parts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }


def convertFromFormat2(jsonObject):
    dt = datetime.datetime.strptime(jsonObject['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = round((dt - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }


def main(jsonObject):
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult)


if __name__ == '__main__':
    unittest.main()