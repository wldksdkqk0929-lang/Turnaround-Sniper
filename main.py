import os
import module_a_universe as mod_a
import module_b_scanner as mod_b
import module_c_news as mod_c

def main():
    print("🚀 System Start: Turnaround Sniper")
    
    # 각 단계별 성공 여부 체크 (하나라도 실패하면 중단)
    if not mod_a.build_universe():
        print("❌ System Halted at Module A.")
        return

    if not mod_b.run_scan():
        print("❌ System Halted at Module B.")
        return

    if not mod_c.analyze_news():
        print("❌ System Halted at Module C.")
        return

    print("🏁 Pipeline Completed Successfully.")

if __name__ == "__main__":
    main()
