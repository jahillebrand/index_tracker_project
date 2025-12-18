from apiObj import apiObj
from symbolObj import symbolObj

apiKey = apiObj()

vgtObj = symbolObj("vgt",apiKey)

print(vgtObj.lastUpdatedAdjPrice)
print(vgtObj.tenYearReturn)