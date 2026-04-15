from web3 import Web3
import json
import base64

webs = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
one = {"from": "0x9d7377B5c56832c19EC53bFf307563726eBa93A3"}

with open("blocks/build/contracts/Store.json") as d:
    contract = webs.eth.contract(
        address="0x1123EA783b42b77D9b486CB4Bd04293BfcD7448C", abi=json.load(d)["abi"]
    ).functions


def addData(data:dict)->str:
    try:
        encoded=base64.b64encode(json.dumps(data).encode()).decode()
        contract.addString(encoded).transact(one)
        return "Success"
    except Exception as e:
        return str(e)

def retriveData()->list:
    ff=[]
    try:
        view=contract.getAll().call(one)
        for i in view:
            dd=json.loads(base64.b64decode(i[1]).decode())
            dd['realId']=i[0]
            ff.append(dd)
        return ff
    except Exception as _:
        return ff
    
def updateViewPoint(id:int,dd:dict)->str:
    try:
        for i in retriveData():
            if i['realId'] == id:
                try:
                    del dd['realId']
                except Exception as _:
                    ""
                contract.updateStore(id,base64.b64encode(json.dumps(dd).encode()).decode()).transact(one)
                return "Success"
        return "Failed to Updated"
    except Exception as e:
        return "Not Updated"