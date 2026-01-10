import yfinance as yf
import pandas as pd
import os
import json

def run_scanner():
    print("📈 Module B: 실시간 주가 데이터 수집 중...")
    if not os.path.exists("data/survivors.json"): return
    
    with open("data/survivors.json", "r", encoding="utf-8") as f:
        tickers = [item['ticker'] for item in json.load(f)['data']]

    results = []
    for t in tickers[:20]: # 상위 20개 우선 분석
        try:
            stock = yf.Ticker(t)
            # [수정] 데이터가 없을 경우를 대비해 여러 방식으로 가격 추출 시도
            hist = stock.history(period="1mo")
            if hist.empty: continue
            
            current_price = hist['Close'].iloc[-1]
            high_price = hist['High'].max()
            drop_rate = (high_price - current_price) / high_price if high_price > 0 else 0
            
            results.append({
                "ticker": t,
                "price": round(float(current_price), 2),
                "drop_rate": round(float(drop_rate), 4),
                "charts": {"daily_6m": hist['Close'].tail(30).tolist()}
            })
            print(f"   {t}: ${current_price:.2f} 확보 완료")
        except: continue

    with open("data/survivors.json", "w", encoding="utf-8") as f:
        json.dump({"data": results}, f)
    print(f"✅ Module B 완료: {len(results)}개 종목 가격 업데이트.")

if __name__ == "__main__":
    run_scanner()
