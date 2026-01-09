import os
import module_a_universe as mod_a
import module_b_scanner as mod_b
import module_c_news as mod_c
import module_d_writer as mod_d

def main():
    print("🚀 System Start: Turnaround Sniper")

    # [설정] True: 기존 스캔 데이터가 있으면 건너뜀 (뉴스/UI 테스트용)
    # 실전 매일 돌릴 때는 False로 변경 권장
    SKIP_IF_EXISTS = True 

    # 1. 유니버스 & 2. 기술적 스캔
    if SKIP_IF_EXISTS and os.path.exists("data/candidates_b.csv"):
        print("⏩ [Dev Mode] Skipping Scanner (Found existing data).")
    else:
        mod_a.build_universe()
        mod_b.run_scan()
    
    # 3. 뉴스 필터링
    mod_c.analyze_news()

    # 4. 대시보드 생성 & 한글 리포트 작성
    mod_d.export_to_json()

    print("🏁 Pipeline Completed Successfully.")

if __name__ == "__main__":
    main()
