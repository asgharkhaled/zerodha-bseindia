from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
import unicodecsv
import redis
import pickle
import cherrypy
headers = {
        'accept': "*/*",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.8,ta;q=0.6,fr;q=0.4",
        'cache-control': "no-cache",
        }
#retrieving data from Bse India
bhavcopy_url = "http://www.bseindia.com/markets/equity/EQReports/Equitydebcopy.aspx"
main_response = requests.request("GET", bhavcopy_url, headers=headers).content
soup = BeautifulSoup(main_response, "html.parser")
bhavcopy_zip_url = soup.find(id="btnhylZip")['href']
print(bhavcopy_zip_url)
#Extracing the file
fileName = './test.zip'
req = requests.get(bhavcopy_zip_url)
file = open(fileName, 'wb')
for chunk in req.iter_content(100000):
    file.write(chunk)
file.close()
archive = ZipFile('./test.zip', 'r')
file_name = archive.namelist()[0]
fields_to_take = ['SC_CODE','SC_NAME','OPEN','LOW','HIGH','CLOSE']
with archive.open(file_name, 'rU') as f:
    reader = unicodecsv.DictReader(f)
    reader_rows = list(reader)
    reader_filtered_fields = [{field:dict_row[field] for field in fields_to_take}
                              for dict_row in reader_rows]
# print(reader_filtered_fields[0])
#Using Redis to Store data
r = redis.StrictRedis('localhost')
p_mydict = pickle.dumps(reader_filtered_fields)
r.set('bhav_data',p_mydict)
read_dict = r.get('bhav_data')
bhav_data = pickle.loads(read_dict)
# print(bhav_data)
newlist = sorted(bhav_data, key=lambda k: k['HIGH'], reverse=True)
print(newlist[0:9])

#Displaying top 10 S
##writing cherry py 
class Index(object):

    @cherrypy.expose()
    def index(self):
        return '''<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
  <h2>Top 10 Stock entries from Bse India</h2>
  </br></br>
  <div class="table-responsive">          
  <table class="table">
    <thead>
      <tr>
        <th>#</th>
        <th>Code</th>
        <th>Name</th>
        <th>Open</th>
        <th>High</th>
        <th>Low</th>
        <th>Close</th>
      </tr>
    </thead>
    <tbody>
      <tr  bgcolor="#ccccb3">
        <td>1</td>
        <td>'''+newlist[0]['SC_CODE']+'''</td>
        <td>'''+newlist[0]['SC_NAME']+'''</td>
        <td>'''+newlist[0]['OPEN']+'''</td>
        <td>'''+newlist[0]['HIGH']+'''</td>
        <td>'''+newlist[0]['LOW']+'''</td>
        <td>'''+newlist[0]['CLOSE']+'''</td>
      </tr>

      <tr>
        <td>2</td>
        <td>'''+newlist[1]['SC_CODE']+'''</td>
        <td>'''+newlist[1]['SC_NAME']+'''</td>
        <td>'''+newlist[1]['OPEN']+'''</td>
        <td>'''+newlist[1]['HIGH']+'''</td>
        <td>'''+newlist[1]['LOW']+'''</td>
        <td>'''+newlist[1]['CLOSE']+'''</td>
      </tr>

      <tr  bgcolor="#ccccb3">
        <td>3</td>
        <td>'''+newlist[2]['SC_CODE']+'''</td>
        <td>'''+newlist[2]['SC_NAME']+'''</td>
        <td>'''+newlist[2]['OPEN']+'''</td>
        <td>'''+newlist[2]['HIGH']+'''</td>
        <td>'''+newlist[2]['LOW']+'''</td>
        <td>'''+newlist[2]['CLOSE']+'''</td>
      </tr>

      <tr>
        <td>4</td>
        <td>'''+newlist[3]['SC_CODE']+'''</td>
        <td>'''+newlist[3]['SC_NAME']+'''</td>
        <td>'''+newlist[3]['OPEN']+'''</td>
        <td>'''+newlist[3]['HIGH']+'''</td>
        <td>'''+newlist[3]['LOW']+'''</td>
        <td>'''+newlist[3]['CLOSE']+'''</td>
      </tr>

      <tr  bgcolor="#ccccb3">
        <td>5</td>
        <td>'''+newlist[4]['SC_CODE']+'''</td>
        <td>'''+newlist[4]['SC_NAME']+'''</td>
        <td>'''+newlist[4]['OPEN']+'''</td>
        <td>'''+newlist[4]['HIGH']+'''</td>
        <td>'''+newlist[4]['LOW']+'''</td>
        <td>'''+newlist[4]['CLOSE']+'''</td>
      </tr>

      <tr>
        <td>6</td>
        <td>'''+newlist[5]['SC_CODE']+'''</td>
        <td>'''+newlist[5]['SC_NAME']+'''</td>
        <td>'''+newlist[5]['OPEN']+'''</td>
        <td>'''+newlist[5]['HIGH']+'''</td>
        <td>'''+newlist[5]['LOW']+'''</td>
        <td>'''+newlist[5]['CLOSE']+'''</td>
      </tr>

      <tr  bgcolor="#ccccb3">
        <td>7</td>
        <td>'''+newlist[6]['SC_CODE']+'''</td>
        <td>'''+newlist[6]['SC_NAME']+'''</td>
        <td>'''+newlist[6]['OPEN']+'''</td>
        <td>'''+newlist[6]['HIGH']+'''</td>
        <td>'''+newlist[6]['LOW']+'''</td>
        <td>'''+newlist[6]['CLOSE']+'''</td>
      </tr>

      <tr>
        <td>8</td>
        <td>'''+newlist[7]['SC_CODE']+'''</td>
        <td>'''+newlist[7]['SC_NAME']+'''</td>
        <td>'''+newlist[7]['OPEN']+'''</td>
        <td>'''+newlist[7]['HIGH']+'''</td>
        <td>'''+newlist[7]['LOW']+'''</td>
        <td>'''+newlist[7]['CLOSE']+'''</td>
      </tr>

      <tr  bgcolor="#ccccb3">
        <td>9</td>
        <td>'''+newlist[8]['SC_CODE']+'''</td>
        <td>'''+newlist[8]['SC_NAME']+'''</td>
        <td>'''+newlist[8]['OPEN']+'''</td>
        <td>'''+newlist[8]['HIGH']+'''</td>
        <td>'''+newlist[8]['LOW']+'''</td>
        <td>'''+newlist[8]['CLOSE']+'''</td>
      </tr>

      <tr>
        <td>10</td>
        <td>'''+newlist[9]['SC_CODE']+'''</td>
        <td>'''+newlist[9]['SC_NAME']+'''</td>
        <td>'''+newlist[9]['OPEN']+'''</td>
        <td>'''+newlist[9]['HIGH']+'''</td>
        <td>'''+newlist[9]['LOW']+'''</td>
        <td>'''+newlist[9]['CLOSE']+'''</td>
      </tr>
     
    </tbody>
  </table>
  </div>
</div>
</br></br>
<div align="center">Done by,</br>
<b> M Asghar Khaled</b></br>
+919597817276</div>
</body>
</html>'''

cherrypy.quickstart(Index())
# print(bhav_data[0])
# print(type(bhav_data))
# temp_dict = {}
# temp_dict['code'] = []
# temp_dict['high'] = []
# # {"code":[1,2],"high":[10,12]}
# for items in bhav_data:
#     temp_dict['code'].append(items['SC_CODE'])
#     temp_dict['high'].append(items['HIGH'])
# print(temp_dict)
# def build_dict(seq, key):
#     return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
# info_by_name = build_dict(reader_filtered_fields, key="SC_NAME")
# tom_info = info_by_name["ABB LTD.    "] 
# print(tom_info)