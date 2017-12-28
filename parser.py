from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
import unicodecsv
import redis
import pickle
import cherrypy

def get_context_data(name=None):
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
  #Using Redis to Store data
  r = redis.StrictRedis('localhost')
  p_mydict = pickle.dumps(reader_filtered_fields)
  r.set('bhav_data',p_mydict)
  read_dict = r.get('bhav_data')
  bhav_data = pickle.loads(read_dict)
  #getting top 10 stock based on high value
  newlist = sorted(bhav_data, key=lambda k: k['HIGH'], reverse=True)
  templist_data = None
  if name is not None:
    try:
      temp_dict = build_dict(newlist, key="SC_NAME")
      templist_data = temp_dict[name]
    except Exception as e:
      print(e)
  templist = []
  if templist_data:
    templist.append(templist_data)
    newlist = templist
  print(newlist)
  return newlist[:10]


def build_dict(seq, key):
  return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


##writing cherry py HTML - CSS
class Index(object):

    @cherrypy.expose()
    def index(self, name=None):
      newlist = get_context_data(name)
      test = ''''''
      tbody = '''
        <tr  bgcolor="#ccccb3">
          <td>{i}</td>
          <td>{SC_CODE}</td>
          <td>{SC_NAME}</td>
          <td>{OPEN}</td>
          <td>{HIGH}</td>
          <td>{LOW}</td>
          <td>{CLOSE}</td>
        </tr>'''
      for i, item in enumerate(newlist):
        i = i + 1
        test += tbody.format(i=i, **item)
      return '''<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
</head>
<body>
    
<div class="container">
  <h2>Top 10 Stock entries from Bse India</h2>
  </br></br>


 <form class="form-inline" action="." method="GET">
    <div class="form-group">
      <label for="search">Name Search:</label>
      <input type="text" id="search" class="form-control" name="name" class="show">      
    </div>
    <button type="submit" class="btn btn-sm btn-primary" id="submit">search</button> 
  </form>
</br>
  <div class="table-responsive">          
  <table class="table table-striped">
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
'''+test+'''
  </table>
  </div>
</div>
</br>
<div align="center">Done by,</br>
<b> M Asghar Khaled</b></br>
+919597817276</div>
</body>
</html>'''

cherrypy.quickstart(Index())
