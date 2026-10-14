# 바이블트리 2026 11–12월 베트남어판 인쇄 검수

저학년 Nhi đồng · 고학년 Thiếu nhi (A4), 청소년 Thanh thiếu niên · 청년 Thanh niên (A5) 네 권의 표지·128면 펼침 열람과 용어 검수표입니다. 화면 말은 한국어판 검수 사이트와 같게 한국어입니다.

- 페이지: https://fastkorea12-png.github.io/bibletree-print-review-1112-vi/
- 한국어판: https://fastkorea12-png.github.io/bibletree-print-review-1112/

## 한국어판과 다른 점
- 책 코드 `vlow` `vhigh` `vteen` `vyoung`(한국어판 기록과 섞이지 않음). 용어 의견은 `vterm`(spread = terms.json 안 순번).
- 펼침 제목은 베트남어, 아래 작은 글씨로 한국어 원고 제목(`### 제목:`).
- **한국어판 나란히**: 열람에서 누르면 같은 책·같은 펼침 번호의 한국어판 그림을 한국어판 사이트(`…/bibletree-print-review-1112/img/<low|high|teen|young>/sNN.jpg`)에서 바로 불러와 아래에 보여 줌(그림은 복사하지 않음).
- **용어 검수표** 탭(`#terms`): `terms.json`을 읽음. 형식은 `[{id, group, ko, vi, alts:[{vi, count, ages}], status, note, example_vi, example_ref}]`. ‘✓ 좋아요’는 `st:'ok'`, 다른 표현을 고르거나 적으면 `st:'fix'`이고 글은 `선택: <vi> — <의견>`.
  - **지금 `terms.json`이 없음**(`바이블트리 집필/2026-11-12_베트남어/용어검수표.json`이 아직 만들어지지 않음). 없으면 탭에 ‘아직 올라오지 않았어요’가 뜸. 준비되면 저장소 맨 위에 `terms.json`으로 복사해 commit · push.

## 검수 기록(백엔드)
한국어판과 같은 Apps Script 웹 앱·같은 시트를 씀. **`apps-script/Code.gs`(vlow…vyoung, vterm 허용 · vterm spread 0–999)를 Apps Script 편집기에 붙여 넣고 ‘배포 관리 > 수정 > 새 버전’으로 다시 배포해야** 베트남어판 기록이 남음(새 배포를 만들면 주소가 바뀜). 그 전에는 남기기를 누르면 ‘남기지 못했어요’가 뜸.

## 다시 만들기
1. 그림: `python3 -I tools/make_site.py . <임시폴더>` → `img/<코드>/`(s00–s64, thumbs, cover)와 `data.json`. 본문은 `조판/pdf/BibleTree_2026_11-12_<이름>_VI_<판형>.pdf`(재단 크기), 표지는 `조판/pdf/표지/…_VI_Spread_…_bleed2mm.pdf`(도련 2mm 잘라 냄). 날짜·요일·제목·본문주소는 베트남어 원고, 주별 주제는 조판과 같은 규칙(그 주에서 가장 많이 쓴 표현), 한국어 제목은 한국어 원고에서 읽음.
2. 페이지: `python3 -I tools/build_index.py .` → `tools/template.html` + `data.json` + 시트 주소로 `index.html`.
3. commit · push → GitHub Pages가 1분 안에 갱신.
