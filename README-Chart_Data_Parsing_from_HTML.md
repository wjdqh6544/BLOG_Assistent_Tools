## 웹사이트 이미지 자동 다운로드 프로그램
---
* WccfTech 기사에 첨부되어 있는 그래프의 정보를 파싱하여 .xlsx 로 저장하는 프로그램
* CLI 기반 / 지원 사이트: WccfTech
* WccfTech 사이트의 HTML 구조가 변경되면, 본 프로그램이 작동하지 않을 수 있습니다.
* 작업 기간: 2024.07.18 ~ 2024.07.18 (1일)
---
## [프로그램 사용 방법]
* WccfTech 기사의 URL 을 입력합니다.
* 그러면, URL로부터 HTML 코드를 가져와서, 파싱합니다.
* HTML 코드로부터 그래프 개수를 확인하고, 각 그래프에서 정보를 추출하여 리스트에 저장합니다.
* 리스트의 데이터가 .xlsx 파일에 저장됩니다. 이때, 각각의 그래프의 정보는 서로 다른 Sheet에 저장됩니다.<br>
즉, .xlsx 파일의 sheet 개수는, 기사에 첨부되어 있는 그래프의 개수와 같습니다.

### [사용된 라이브러리]
* BeautifulSoup (in bs4)
* Workbook, load_workbook (in openpyxl)
* urllib.request
* time
* os

---
Latest Edited on 24. 07. 18.<br>
Created on 24. 07. 18.
