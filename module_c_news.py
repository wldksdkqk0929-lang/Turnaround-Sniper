import yfinance as yf
import pandas as pd
import time
import os

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
    # 즉시 탈락시킬 키워드 (파산, 소송, 상장폐지 등)
    risk_words = ['bankruptcy', 'chapter 11', 'delisting', 'fraud', 'investigation', 'lawsuit']

    print(f"📰 Module C: Analyzing news for {len(df)} candidates...")

    for _, row in df.iterrows():
        try:
            ticker = row['ticker']
            stock = yf.Ticker(ticker)
            news_list = stock.news
            
            risk_found = False
            news_summary = "No recent news"

            if news_list:
                # 최근 뉴스 3개의 제목만 병합해서 검사
                titles = [n.get('title', '').lower() for n in news_list[:3]]
                full_text = " ".join(titles)
                news_summary = titles[0] # 대표 뉴스 하나 저장

                for risk in risk_words:
                    if risk in full_text:
                        risk_found = True
                        print(f"🔻 Filtered out {ticker}: Risk keyword '{risk}' detected.")
                        break
            
            if not risk_found:
                row['news_top'] = news_summary
                results.append(row)
            
            time.sleep(0.2) # 뉴스 검색은 부하가 크므로 딜레이 더 줌

        except Exception as e:
            # 에러나면 일단 통과시키되(안전), 로그 남김
            row['news_top'] = "Error fetching news"
            results.append(row)

    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"✅ Module C: {len(results)} survivors after news filter.")
    return True
