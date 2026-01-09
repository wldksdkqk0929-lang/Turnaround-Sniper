import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
import os
import re

def clean_html(raw_html):
    # HTML 태그 제거 및 특수문자 정리
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_google_news(ticker):
    # 구글 뉴스 RSS 주소 (지난 7일간 뉴스 검색)
    url = f"https://news.google.com/rss/search?q={ticker}+stock+when:7d&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # 뉴스 아이템들 가져오기
            items = root.findall('./channel/item')
            
            if not items:
                return "No recent news found on Google"
            
            # 가장 최신 뉴스 3개의 제목을 합쳐서 반환
            titles = []
            for item in items[:2]: # 상위 2개만
                title = item.find('title').text
                # 언론사 이름 제거 (ex: - Yahoo Finance)
                if "-" in title:
                    title = title.split("-")[0].strip()
                titles.append(title)
            
            return " | ".join(titles)
            
    except Exception as e:
        return f"News Error: {str(e)}"
    
    return "No Data"

def analyze_news(input_path="data/candidates_b.csv", output_path="data/candidates_c.csv"):
    if not os.path.exists(input_path):
        print("❌ Module C: Input file not found.")
        return False
        
    df = pd.read_csv(input_path)
    if df.empty:
        print("⚠️ Module C: No candidates to analyze.")
        df.to_csv(output_path, index=False)
        return True

    results = []
    # 절대 안 되는 키워드 (파산 등)
    risk_words = ['bankruptcy', 'chapter 11', 'delisting', 'fraud', 'investigation']

    print(f"📰 Module C: Fetching Google News for {len(df)} Blue-Chips...")

    for i, row in df.iterrows():
        ticker = row['ticker']
        
        # 구글 뉴스 호출
        news_summary = get_google_news(ticker)
        
        # 리스크 필터링
        risk_found = False
        for risk in risk_words:
            if risk in news_summary.lower():
                risk_found = True
                print(f"   🔻 Risk Alert [{ticker}]: {risk} detected.")
                break
        
        if not risk_found:
            row['news_top'] = news_summary
            results.append(row)
            print(f"   ✅ [{ticker}] News: {news_summary[:50]}...")
        
        # 구글 차단 방지 딜레이
        time.sleep(0.5)

    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"✅ Module C: Analysis complete. {len(results)} stocks ready.")
    return True
