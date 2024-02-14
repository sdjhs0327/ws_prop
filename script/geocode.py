## 지도, 좌표 관련 함수를 정의한 파일
import urllib
import json
from pyproj import Proj, transform


def search_map(search_text):
    client_id = 'r1o7ovyug8' #클라이언트 ID값
    client_secret = 'Dvj6g1fVXA5IhqdhNfxOZkYG2F1I2RLGGa1mYezy' #클라이언트 Secret값
    encText = urllib.parse.quote(search_text) 
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='+encText
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

def transform_tm_latlon(x, y):
    tm_inProj = Proj(init='epsg:2097')
    wgs84_outProj = Proj(init='epsg:4326')
    return transform(tm_inProj, wgs84_outProj, x, y)