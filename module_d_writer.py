import pandas as pd
import json
import os
import datetime
import numpy as np

def export_to_json(input_path="data/candidates_final.csv", output_path="data/data.json"):
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        return

    try:
        df = pd.read_csv(input_path)
        
        # [핵심 수술] NaN(빈 값)을 None(JSON의 null)으로 변환
        # 이것을 안 하면 브라우저가 멈춥니다.
        df = df.replace({np.nan: None})

        candidates = []
        for _, row in df.iterrows():
            # 차트 데이터(history)가 문자열로 되어있으면 리스트로 복구
            history_raw = row.get('history', '[]')
            if isinstance(history_raw, str):
                try:
                    # 안전하게 파싱 (작은따옴표 문제 해결)
                    history_data = json.loads(history_raw.replace("'", '"'))
                except:
                    history_data = []
            else:
                history_data = []

            candidate = {
                "ticker": row['ticker'],
                "price": row['price'],
                "drop_rate": row['drop_rate'],
                "recovery_rate": row['recovery_rate'],
                "rsi": row.get('rsi', 0),
                "high_52w": row.get('high_52w', 0),
                "low_52w": row.get('low_52w', 0),
                "history": str(history_data), # 나중에 JS에서 파싱하도록 다시 문자열로
                "context": row.get('context', 'No news available'),
                "evidence": {
                    "s4_tag": row.get('s4_tag', 'WATCH'),
                    "analysis_kr": row.get('analysis_kr', '분석 대기 중...')
                }
            }
            candidates.append(candidate)

        final_data = {
            "metadata": {
                "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S KST"),
                "total_count": len(candidates)
            },
            "candidates": candidates
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ JSON Export Successful! ({len(candidates)} items)")

    except Exception as e:
        print(f"❌ JSON Export Failed: {e}")

if __name__ == "__main__":
    export_to_json()
