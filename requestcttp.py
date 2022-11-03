import requests

url = 'http://localhost:8081'
headers = {'Request-Taint': '1'} # if you put it 0 your turn off the CTTP support 
body = {'Name':'?', 'non-private' : '?' , 'surname':'?'}

proxy_servers = {
   'http': 'http://localhost:8080',
}

taintspec=open('test.txt','w') 
taintspec.write("application/x-taint-bin \\x3B\\x03")
taintspec.close()
files = {'Content-Type': open('test.txt', 'rb')}

r=requests.post(url, headers=headers, data=body ,proxies=proxy_servers , files=files)
print(r)
