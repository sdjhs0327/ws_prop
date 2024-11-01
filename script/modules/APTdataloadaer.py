import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import requests
import xmltodict
import math

sigungu_cd = {
            '종로구': '11110', '중구': '11140', '용산구': '11170', '성동구': '11200', '광진구': '11215',
            '동대문구': '11230', '중랑구': '11260', '성북구': '11290', '강북구': '11305', '도봉구': '11320',
            '노원구': '11350', '은평구': '11380', '서대문구': '11410', '마포구': '11440', '양천구': '11470',
            '강서구': '11500', '구로구': '11530', '금천구': '11545', '영등포구': '11560', '동작구': '11590',
            '관악구': '11620', '서초구': '11650', '강남구': '11680', '송파구': '11710', '강동구': '11740'
            }

authKey = 'G7GuVfz99A0umUDOAuZlRXMYlZmKxBd3hHsj8EiZ89SSD7r5qrn08q70LM96fyblxiM3eGxWsgkIjhF%2BAWTVBg%3D%3D'

class AptTradingDataloader(object):
    def __init__(self, authKey):
        self.authKey = authKey
        self.raw_cols = {"aptDong": "단지동명", "aptNm": "단지명", "aptSeq": "단지일련번호", "bonbun": "법정동본번", "bubun": "법정동부번",
                     "buildYear": "건축년도", "buyerGbn": "매수자유형명", "cdealDay": "해제사유발생일자", "cdealType": "해제여부",
                     "dealAmount": "거래금액", "dealDay": "거래일자", "dealMonth": "거래월", "dealYear": "거래년도", "dealingGbn": "거래구분명",
                     "estateAgentSggNm": "중개사소재시군구명", "excluUseAr": "전용면적제곱미터", "floor": "층수", "jibun": "법정동지번내용",
                     "landCd": "대지구분코드", "landLeaseholdGbn": "토지임대여부", "rgstDate": "등기일자", "roadNm": "도로명",
                     "roadNmBonbun": "도로명본번", "roadNmBubun": "도로명부번", "roadNmCd": "도로명코드", "roadNmSeq": "도로명일련번호",
                     "roadNmSggCd": "도로명시군구코드", "roadNmbCd": "도로명지상지하코드", "sggCd": "법정동시군구코드", "slerGbn": "매도자유형명",
                     "umdCd": "법정동읍면동코드", "umdNm": "법정동읍면동명"}
        self.data_cols = ['거래년도', '거래월', '거래일자', '등기일자', ## 언제
                          '법정동시군구코드', '법정동읍면동코드', '법정동읍면동명', '대지구분코드', '법정동본번', '법정동부번', '법정동지번내용', ## 어디서
                          '도로명시군구코드', '도로명코드', '도로명일련번호', '도로명본번', '도로명부번', '도로명지상지하코드', '도로명', ## 어디서
                          '단지일련번호', '단지명', '단지동명', '건축년도', '전용면적제곱미터', '층수', '토지임대여부', ## 무엇을
                          '거래구분명', '거래금액', '매수자유형명', '매도자유형명', ## 어떻게
                          '해제여부', '해제사유발생일자', '중개사소재시군구명'] ## 기타
        self.cols = ['거래년도', '거래월', '거래일자', ## 언제
                     '법정동시군구코드', '법정동읍면동코드', ## 어디서
                     '단지일련번호', '단지명', '전용면적제곱미터', '층수', '건축년도', ## 무엇을
                     '거래구분명', '거래금액', ## 어떻게
                     '해제여부'] ## 기타


    ## APT 매매이력 API
    def get_apt_trading_raw(self, sigungu_cd, base_month):
        authKey = self.authKey
        try:
            num_of_rows = 100
            url = f"http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?serviceKey={authKey}&LAWD_CD={sigungu_cd}&DEAL_YMD={base_month}&pageNo=1&numOfRows={num_of_rows}"
            response = requests.get(url, timeout=5)
            raw = xmltodict.parse(response.text)
            total_cnt = int(raw['response']['body']['totalCount'])
            max_page = int(math.ceil(total_cnt//num_of_rows))
            raw = raw['response']['body']['items']['item']
            dataset = pd.DataFrame(raw)
            if max_page > 1:
                for page_no in range(2, max_page+1):
                    url = f"http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?serviceKey={authKey}&LAWD_CD={sigungu_cd}&DEAL_YMD={base_month}&pageNo={page_no}&numOfRows={num_of_rows}"
                    response = requests.get(url, timeout=5)
                    raw = xmltodict.parse(response.text)
                    raw = raw['response']['body']['items']['item']
                    dataset = pd.concat([dataset, pd.DataFrame(raw)])
            return dataset
        except Exception as e:
            return print(f'{e} {base_month}, {sigungu_cd} 결과를 가져오는데 실패했습니다.')
        
    def preproc_apt_trading(self, apt_trading_raw):
        raw_cols = self.raw_cols
        data_cols = self.data_cols
        cols = self.cols
        dataset = apt_trading_raw.rename(columns=raw_cols)
        dataset = dataset[data_cols]
        df = dataset[cols]
        return dataset, df


class AptRentDataloader(object):
    def __init__(self, authKey):
        self.authKey = authKey
        self.raw_cols = {"aptNm":'단지명', 'buildYear':'건축년도', 'contractTerm':'계약기간', 'contractType':'거래구분명', 'dealDay':'거래일자',
                        'dealMonth':'거래월', 'dealYear':'거래년도', 'deposit':'보증금액', 'excluUseAr':'전용면적제곱미터', 'floor':'층수',
                        'jibun':'법정동지번내용', 'monthlyRent':'월세금액', 'preDeposit':'종전계약보증금', 'preMonthlyRent':'종전계약월세',
                        'sggCd':'법정동시군구코드', 'umdNm':'법정동읍면동명', 'useRRRight':'갱신요구권사용여부'}

        self.data_cols = ['거래년도', '거래월', '거래일자', ## 언제
                        '법정동시군구코드', '법정동읍면동명', '법정동지번내용', ## 어디서
                        '단지명', '전용면적제곱미터', '층수', '건축년도', ## 무엇을
                        '거래구분명', '보증금액', '월세금액', '종전계약보증금', '종전계약월세', '갱신요구권사용여부'] ## 어떻게
            
    def get_apt_rent_raw(self, sigungu_cd, base_month):
        authKey = self.authKey
        try:
            num_of_rows = 100
            url = f"http://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent?serviceKey={authKey}&LAWD_CD={sigungu_cd}&DEAL_YMD={base_month}"
            response = requests.get(url)
            raw = xmltodict.parse(response.text)
            total_cnt = int(raw['response']['body']['totalCount'])
            max_page = int(math.ceil(total_cnt//num_of_rows))
            raw = raw['response']['body']['items']['item']
            dataset = pd.DataFrame(raw)
            if max_page > 1:
                for page_no in range(2, max_page+1):
                    url = f"http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?serviceKey={authKey}&LAWD_CD={sigungu_cd}&DEAL_YMD={base_month}&pageNo={page_no}&numOfRows={num_of_rows}"
                    response = requests.get(url)
                    raw = xmltodict.parse(response.text)
                    raw = raw['response']['body']['items']['item']
                    dataset = pd.concat([dataset, pd.DataFrame(raw)])
            return dataset
        except Exception as e:
                return print(f'{e} {base_month}, {sigungu_cd} 결과를 가져오는데 실패했습니다.')
            
    def preproc_apt_trading(self, apt_rant_raw):
        raw_cols = self.raw_cols
        data_cols = self.data_cols
        dataset = apt_rant_raw.rename(columns=raw_cols)
        dataset = dataset[data_cols]
        return dataset