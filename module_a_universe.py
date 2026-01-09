import pandas as pd
import requests
import os
from io import StringIO

def build_universe(output_path="data/universe.csv"):
    # 데이터 폴더가 없으면 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("📡 Module A: Connecting to NASDAQ server...")
    try:
        response = requests.get(url, headers=headers, timeout=30) # 타임아웃 30초로 연장
        response.raise_for_status() # 404 등 에러 시 즉시 중단
        
        # 데이터 파싱
        data_str = response.text
        df = pd.read_csv(StringIO(data_str), sep="|")
        
        # 마지막 줄(메타데이터) 제거 및 티커 추출
        df = df.iloc[:-1] 
        tickers = [str(t) for t in df['Symbol'].tolist() if str(t).isalpha()] # 순수 알파벳 티커만 사용
        
        # 결과 저장
        pd.DataFrame({"ticker": tickers}).to_csv(output_path, index=False)
        print(f"✅ Module A: Success. {len(tickers)} tickers secured.")
        return True
        
    except Exception as e:
        print(f"❌ Module A Error: {e}")
        return False
