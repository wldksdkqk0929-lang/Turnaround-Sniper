import pandas as pd
import json
import os
from datetime import datetime

def export_to_json(input_path="data/candidates_c.csv", output_path="data/data.json"):
    print("📝 Module D: Generating Operation Report...")
    
    # --- [1. 전장 상황판 (단계별 로그 수집)] ---
    logs = []
    stats = {"universe": 0, "s1_filtered": 0, "s2_checked": 0, "final_ready": 0}

    # Step A: Universe 확인
    if os.path.exists("data/universe.csv"):
        try:
            uni_df = pd.read_csv("data/universe.csv")
            stats['universe'] = len(uni_df)
            logs.append(f"✅ [Step 1] Universe Secured: {len(uni_df):,} tickers found.")
        except:
            logs.append("⚠️ [Step 1] Universe file exists but is unreadable.")
    else:
        logs.append("❌ [Step 1] Universe file NOT found. (Pipeline broken?)")

    # Step B: Technical Scan 확인
    if os.path.exists("data/candidates_b.csv"):
        try:
            b_df = pd.read_csv("data/candidates_b.csv")
            stats['s1_filtered'] = len(b_df)
            if len(b_df) > 0:
                logs.append(f"✅ [Step 2] Technical Scan: {len(b_df)} candidates survived the drop.")
            else:
                logs.append("⚠️ [Step 2] No candidates met the technical criteria.")
        except:
            logs.append("⚠️ [Step 2] Scanner file error.")
    else:
        logs.append("⏭️ [Step 2] Scanner output missing (Skipped or Failed).")

    # Step C: News Analysis 확인
    candidates = []
    if os.path.exists(input_path):
        try:
            df = pd.read_csv(input_path)
            stats['s2_checked'] = len(df)
            
            if not df.empty:
                logs.append(f"✅ [Step 3] News Filter: {len(df)} candidates passed risk check.")
                
                # 데이터 매핑 시작
                for _, row in df.iterrows():
                    rec_rate = row.get('recovery_rate', 0) / 100.0
                    tag = "READY" if rec_rate >= 0.10 else "WATCH"
                    if tag == "READY": stats['final_ready'] += 1
                    
                    # [수정] nan(빈값) 처리 로직 추가
                    news_text = row.get('news_top', '')
                    if pd.isna(news_text) or str(news_text).lower() == 'nan' or str(news_text).strip() == "":
                        context_msg = "No significant news found"
                    else:
                        context_msg = str(news_text)

                    candidate = {
                        "ticker": str(row['ticker']),
                        "price": float(row['price']),
                        "metrics": {
                            "drop_rate": row.get('drop_rate', 0),
                            "rec_rate": rec_rate
                        },
                        "evidence": {
                            "s4_tag": tag
                        },
                        "context": context_msg
                    }
                    candidates.append(candidate)
            else:
                logs.append("⚠️ [Step 3] Candidates list is empty after news filter.")
        except Exception as e:
            logs.append(f"❌ [Step 3] Error processing final CSV: {str(e)}")
    else:
        logs.append("❌ [Step 3] Final candidate file not found.")

    logs.append("🏁 [System] Report generation complete.")

    # --- [2. 최종 JSON 패키징] ---
    data = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S KST"),
            "pipeline_stats": stats,
            "system_logs": logs
        },
        "candidates": candidates
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Module D: JSON generated successfully at {output_path}")
        return True
    except Exception as e:
        print(f"❌ Module D: Failed to save JSON - {e}")
        return False
