import yfinance as yf
import pandas as pd
import time
import os

def run_scan(input_path="data/universe.csv", output_path="data/candidates_b.csv"):
    if not os.path.exists(input_path):
        print("❌ Module B: Input file not found.")
        return False

    df_unv = pd.read_csv(input_path)
    tickers = df_unv['ticker'].tolist()
    results = []
    
    # [설정] 시가총액 기준: 20억 달러 (약 2.8조 원) 이상만 통과
    MIN_MARKET_CAP = 2_000_000_000 
    
    print(f"🔬 Module B: Scanning {len(tickers)} tickers for Blue-Chips...")
    print(f"   (Filter: Drop > 30%, Recovery 5~20%, Market Cap > $2B)")

    # [테스트 모드] 실전 배치 시 tickers[:500]을 tickers 로 변경 권장 (이미 하셨다면 그대로 두세요)
    # 전체를 다 돌리려면 시간이 꽤 걸리므로(30분+), GitHub Actions 시간 제한(6시간) 내에는 충분합니다.
    scan_list = tickers 
    
    for i, ticker in enumerate(scan_list):
        try:
            # 로그: 100개마다 진행상황 표시
            if i % 100 == 0: print(f"...Scanning {i}/{len(scan_list)}...")

            stock = yf.Ticker(ticker)
            
            # 1. 기술적 분석 (속도 빠름 - 먼저 체크)
            hist = stock.history(period="1y", auto_adjust=True)
            if len(hist) < 200: continue 

            high_1y = hist['High'].max()
            curr = hist['Close'].iloc[-1]
            low_20d = hist['Low'].iloc[-20:].min()
            
            if high_1y == 0: continue

            dd = (curr / high_1y) - 1       # 고점 대비 낙폭
            rec = (curr / low_20d) - 1      # 저점 대비 반등폭

            # 1차 관문: 가격 조건 (-30% 하락, 5~20% 반등)
            if dd <= -0.30 and 0.05 <= rec <= 0.20:
                
                # 2차 관문: 덩치(시가총액) 확인 (속도 느림 - 합격자만 조회)
                try:
                    cap = stock.info.get('marketCap', 0)
                    if cap is None: cap = 0
                except:
                    cap = 0
                
                # 시가총액 20억 달러 미만이면 탈락 (잡주 제거)
                if cap < MIN_MARKET_CAP:
                    # print(f"   -> Drop {ticker}: Too small (${cap/1000000:.1f}M)") # 로그 너무 많으면 주석 처리
                    continue
                
                # 최종 합격
                print(f"   ★ Found: {ticker} (Drop: {dd*100:.1f}%, Cap: ${cap/1000000000:.2f}B)")
                results.append({
                    "ticker": ticker, 
                    "price": round(curr, 2), 
                    "drop_rate": round(dd * 100, 2), 
                    "recovery_rate": round(rec * 100, 2),
                    "market_cap": cap # 나중에 대시보드에 표시 가능
                })
            
            # API 보호용 딜레이
            time.sleep(0.1)

        except Exception:
            continue

    # 결과 저장
    if results:
        pd.DataFrame(results).to_csv(output_path, index=False)
        print(f"✅ Module B: Found {len(results)} Blue-Chip candidates.")
    else:
        print("⚠️ Module B: No candidates found.")
        pd.DataFrame(columns=["ticker", "price", "drop_rate", "recovery_rate", "market_cap"]).to_csv(output_path, index=False)
    
    return True
