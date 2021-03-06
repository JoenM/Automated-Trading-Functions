import urllib
import urllib2
import json
import time
import hmac,hashlib
 
def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))
 

APIKey = '' #Insert API Key
Secret = '' #Insert API Secret
 
def post_process( before):
    after = before
 
    if('return' in after):
        if(isinstance(after['return'], list)):
            for x in xrange(0, len(after['return'])):
                if(isinstance(after['return'][x], dict)):
                    if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                        after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                           
    return after
 
def api_query( command, req={}):
 
    if(command == "returnTicker" or command == "return24Volume"):
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
        return json.loads(ret.read())
    elif(command == "returnOrderBook"):
        ret = urllib2.urlopen(urllib2.Request('http://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
        return json.loads(ret.read())
    elif(command == "returnMarketTradeHistory"):
        ret = urllib2.urlopen(urllib2.Request('http://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair'])))
        return json.loads(ret.read())
    else:
        req['command'] = command
        req['nonce'] = int(time.time()*1000)
        post_data = urllib.urlencode(req)
 
        sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
        headers = {
            'Sign': sign,
            'Key': APIKey
        }
 
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
        jsonRet = json.loads(ret.read())
        return post_process(jsonRet)
 

    return api_query('returnTradeHistory',{"currencyPair":currencyPair})
 

def buy(currencyPair,rate,amount):
    return api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

a=buy('USDT_BTC',450,0.001)
print(a)

    
