<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sniper Pro | 지휘 통제실</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800&display=swap');
        body { font-family: 'Pretendard', sans-serif; background-color: #0b0e11; color: #e6edf3; }
        
        /* 카드 및 레이아웃 스타일 */
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .header-gradient { background: linear-gradient(90deg, #161b22 0%, #0d1117 100%); }
        
        /* 상태 태그 */
        .tag-ready { background-color: rgba(46, 160, 67, 0.15); color: #3fb950; border: 1px solid rgba(46, 160, 67, 0.4); }
        .tag-watch { background-color: rgba(56, 139, 253, 0.15); color: #58a6ff; border: 1px solid rgba(56, 139, 253, 0.4); }
        
        /* 아코디언 애니메이션 */
        .hidden-row { display: none; }
        .expanded-row { background-color: #1c2128; border-top: 1px dashed #30363d; animation: slideDown 0.3s ease-out; }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

        /* 프로그레스 바 스타일 (지휘관님이 좋아하신 스타일) */
        .bar-bg { background-color: #30363d; height: 6px; border-radius: 3px; overflow: hidden; }
        .bar-fill-red { background-color: #fa7970; height: 100%; }
        .bar-fill-green { background-color: #3fb950; height: 100%; }
    </style>
</head>
<body class="p-4 md:p-8 max-w-7xl mx-auto">

    <header class="flex justify-between items-end mb-8 pb-4 border-b border-gray-800">
        <div>
            <h1 class="text-3xl font-extrabold tracking-tight flex items-center">
                <i class="fa-solid fa-crosshairs text-red-500 mr-3"></i>
                Turnaround Sniper
                <span class="ml-3 text-xs font-normal text-gray-500 border border-gray-700 px-2 py-0.5 rounded">Pro v2.3</span>
            </h1>
            <p class="text-gray-400 text-sm mt-2 ml-1">AI 기반 미국 주식 역발상 투자 시스템</p>
        </div>
        <div class="text-right hidden md:block">
            <div id="last-update" class="text-xs font-mono text-gray-500">데이터 수신 대기중...</div>
            <div class="text-xs text-green-500 mt-1 font-bold"><i class="fa-solid fa-satellite-dish mr-1"></i>Server Online</div>
        </div>
    </header>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div class="card p-5 border-l-4 border-green-500 relative overflow-hidden">
            <div class="absolute right-[-20px] top-[-20px] text-green-900/20 text-9xl font-bold"><i class="fa-brands fa-searchengin"></i></div>
            <h3 class="text-gray-400 text-xs font-bold uppercase mb-2">🔥 오늘의 원픽 (Top Pick)</h3>
            <div id="top-pick-ticker" class="text-3xl font-bold text-white z-10 relative">-</div>
            <div id="top-pick-desc" class="text-sm text-gray-400 mt-2 z-10 relative leading-relaxed">분석 중입니다...</div>
        </div>

        <div class="card p-5 border-l-4 border-blue-500">
            <h3 class="text-gray-400 text-xs font-bold uppercase mb-2">📊 시장 포지션</h3>
            <div class="flex items-center justify-between mb-2">
                <span class="text-xs text-red-400">공포 (Over-sold)</span>
                <span class="text-xs text-green-400">탐욕 (Over-bought)</span>
            </div>
            <div class="bar-bg mb-2">
                <div class="bg-blue-500 h-full rounded-full" style="width: 20%"></div> </div>
            <p class="text-xs text-gray-400">현재 포착된 종목들은 대다수 <span class="text-white font-bold">과매도 구간</span>에 위치해 있습니다.</p>
        </div>

        <div class="card p-5 border-l-4 border-purple-500">
            <h3 class="text-gray-400 text-xs font-bold uppercase mb-2">📡 스캔 현황</h3>
            <div class="flex justify-between items-center mt-4">
                <div class="text-center">
                    <span class="block text-2xl font-bold text-white" id="stat-total">-</span>
                    <span class="text-[10px] text-gray-500">검색된 종목</span>
                </div>
                <div class="text-gray-600"><i class="fa-solid fa-arrow-right"></i></div>
                <div class="text-center">
                    <span class="block text-2xl font-bold text-green-400" id="stat-ready">-</span>
                    <span class="text-[10px] text-gray-500">최종 타겟</span>
                </div>
            </div>
        </div>
    </section>

    <main>
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
                <i class="fa-solid fa-list-ul text-green-500"></i>
                <h3 class="text-lg font-bold text-white">작전 후보군 (Candidates)</h3>
            </div>
            <span class="text-xs text-gray-500"><i class="fa-solid fa-computer-mouse mr-1"></i>항목을 클릭하여 상세 분석 확인</span>
        </div>

        <div class="flex flex-col space-y-3" id="candidate-list">
            <div class="p-10 text-center text-gray-600">데이터 로딩 중...</div>
        </div>
    </main>

    <script>
        async function loadDashboard() {
            try {
                const response = await fetch('data/data.json?t=' + Date.now());
                const data = await response.json();

                // 1. 상단 브리핑 업데이트
                document.getElementById('last-update').innerText = `최근 업데이트: ${data.metadata.generated_at}`;
                document.getElementById('stat-total').innerText = (data.metadata.pipeline_stats.universe || 5200).toLocaleString();
                const readyList = data.candidates.filter(c => c.evidence.s4_tag === 'READY');
                document.getElementById('stat-ready').innerText = readyList.length;

                // Top Pick 로직 (Ready 중 반등폭 큰 순서)
                readyList.sort((a, b) => b.metrics.rec_rate - a.metrics.rec_rate);
                const topPick = readyList[0] || data.candidates[0];

                if (topPick) {
                    document.getElementById('top-pick-ticker').innerText = `${topPick.ticker} $${topPick.price}`;
                    document.getElementById('top-pick-desc').innerText = 
                        `${topPick.ticker}은(는) 고점 대비 -${topPick.metrics.drop_rate.toFixed(1)}% 하락했으나, 최근 바닥에서 +${(topPick.metrics.rec_rate*100).toFixed(1)}% 반등하며 추세 전환을 시도 중입니다.`;
                }

                // 2. 리스트 생성
                const listContainer = document.getElementById('candidate-list');
                listContainer.innerHTML = '';

                data.candidates.forEach((stock, index) => {
                    const isReady = stock.evidence.s4_tag === 'READY';
                    const tagClass = isReady ? 'tag-ready' : 'tag-watch';
                    const drop = Math.abs(stock.metrics.drop_rate).toFixed(1);
                    const rec = (stock.metrics.rec_rate * 100).toFixed(1);
                    
                    // 뉴스 제목 (없으면 기본값)
                    let newsTitle = stock.context;
                    if (newsTitle.length > 80) newsTitle = newsTitle.substring(0, 80) + "...";

                    // 리스트 아이템 (카드 형태)
                    const itemHTML = `
                        <div class="card overflow-hidden transition hover:border-gray-500">
                            <div class="p-4 flex flex-col md:flex-row items-center justify-between cursor-pointer" onclick="toggleRow(${index})">
                                <div class="flex items-center w-full md:w-1/4 mb-4 md:mb-0">
                                    <div class="w-12 h-12 rounded-lg bg-gray-800 flex items-center justify-center mr-4 font-bold text-xl text-white border border-gray-700">
                                        ${stock.ticker[0]}
                                    </div>
                                    <div>
                                        <div class="text-xl font-bold text-white">${stock.ticker}</div>
                                        <div class="text-sm font-mono text-gray-400">$${stock.price}</div>
                                    </div>
                                </div>

                                <div class="w-full md:w-1/3 px-4 mb-4 md:mb-0">
                                    <div class="flex justify-between text-xs mb-1">
                                        <span class="text-gray-400">낙폭 (Drop)</span>
                                        <span class="text-red-400 font-bold">-${drop}%</span>
                                    </div>
                                    <div class="bar-bg mb-3">
                                        <div class="bar-fill-red" style="width: ${Math.min(drop, 100)}%"></div>
                                    </div>
                                    
                                    <div class="flex justify-between text-xs mb-1">
                                        <span class="text-gray-400">반등 (Recovery)</span>
                                        <span class="text-green-400 font-bold">+${rec}%</span>
                                    </div>
                                    <div class="bar-bg">
                                        <div class="bar-fill-green" style="width: ${Math.min(rec*3, 100)}%"></div>
                                    </div>
                                </div>

                                <div class="w-full md:w-1/3 text-right pl-4">
                                    <div class="text-xs text-gray-500 mb-2 truncate text-left md:text-right">${newsTitle}</div>
                                    <span class="px-3 py-1 rounded text-xs font-bold ${tagClass}">${stock.evidence.s4_tag}</span>
                                    <i id="icon-${index}" class="fa-solid fa-chevron-down text-gray-600 ml-3 text-xs transition-transform"></i>
                                </div>
                            </div>

                            <div id="detail-${index}" class="hidden-row px-6 py-6 bg-[#11141a] border-t border-gray-800">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div>
                                        <h4 class="text-xs font-bold text-blue-400 uppercase mb-3"><i class="fa-solid fa-robot mr-2"></i>AI 전략 분석 보고서</h4>
                                        <div class="text-sm text-gray-300 leading-7 whitespace-pre-line bg-gray-900/50 p-4 rounded border border-gray-800">
                                            ${stock.evidence.analysis_kr}
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <h4 class="text-xs font-bold text-gray-500 uppercase mb-3"><i class="fa-regular fa-newspaper mr-2"></i>관련 뉴스 (News Context)</h4>
                                        <div class="text-sm text-gray-400 p-3 mb-3 border-l-2 border-gray-700">
                                            "${stock.context}"
                                        </div>
                                        <a href="https://www.google.com/search?q=${stock.ticker}+stock+news" target="_blank" 
                                           class="inline-flex items-center text-xs text-blue-400 hover:text-blue-300 hover:underline">
                                            구글 뉴스 원문 전체보기 <i class="fa-solid fa-external-link-alt ml-1"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    listContainer.insertAdjacentHTML('beforeend', itemHTML);
                });

            } catch (err) {
                console.error(err);
                document.getElementById('candidate-list').innerHTML = `<div class="p-10 text-center text-red-500">데이터 로딩 실패.<br>${err}</div>`;
            }
        }

        function toggleRow(index) {
            const row = document.getElementById(`detail-${index}`);
            const icon = document.getElementById(`icon-${index}`);
            
            if (row.classList.contains('hidden-row')) {
                row.classList.remove('hidden-row');
                row.classList.add('expanded-row');
                icon.style.transform = 'rotate(180deg)';
            } else {
                row.classList.add('hidden-row');
                row.classList.remove('expanded-row');
                icon.style.transform = 'rotate(0deg)';
            }
        }

        loadDashboard();
    </script>
</body>
</html>
