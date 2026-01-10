import yfinance as yf
import pandas as pd
import os
import json

def run_scanner():
    print("📈 Module B: 주가 데이터 정밀 수집 중...")
    if not os.path.exists("data/survivors.json"): 
        print("❌ survivors.json이 없습니다.")
        return
    
    with open("data/survivors.json", "r", encoding="utf-8") as f:
        data = json.load(f).get('data', [])
        tickers = [item['ticker'] for item in data]

    results = []
    for t in tickers[:15]: # 안정성을 위해 15개만 집중 분석
        try:
            stock = yf.Ticker(t)
            # 데이터를 1개월치 가져와서 마지막 종가 확인
            hist = stock.history(period="1mo")
            if hist.empty:
                print(f"   ⚠️ {t}: 데이터를 찾을 수 없음")
                continue
            
            current_price = hist['Close'].iloc[-1]
            high_price = hist['High'].max()
            drop_rate = (high_price - current_price) / high_price if high_price > 0 else 0
            
            results.append({
                "ticker": t,
                "price": round(float(current_price), 2),
                "drop_rate": round(float(drop_rate), 4),
                "charts": {"daily_6m": hist['Close'].tail(30).tolist()}
            })
            print(f"   ✅ {t}: ${current_price:.2f} 확보")
        except Exception as e:
            print(f"   ❌ {t} 오류: {e}")
            continue

    os.makedirs("data", exist_ok=True)
    with open("data/survivors.json", "w", encoding="utf-8") as f:
        json.dump({"data": results}, f)
    print(f"🏁 Module B 완료: {len(results)}개 종목 가격 주입 성공.")

if __name__ == "__main__":
    run_scanner()
