## 웹사이트 이미지 자동 다운로드 프로그램
---
* 블로그에 포스팅하려는 원본 기사의 이미지를 자동으로 저장하는 프로그램
* CLI 기반 / 파이썬, urllib, BeautifulSoup, re 모듈 활용.
* 파일명의 경우, 이미지 순서대로 1, 2, ... 로 지정함.
* 슬라이드의 형태(좌우로 이미지를 넘길 수 있는 형태)로 삽입된 경우, 파일명을 1-1, 1-2, ... 로 지정함.
* 지원 사이트: WCCFTech (News Section), VideoCardz
* 작업 기간: 2024.03.25 ~ 2023.04.07 (13일)
---
### [프로그램 기능]
기사에 삽입된 이미지를 쉽게 다운로드하기 위해 고안한 프로그램입니다.<br><br>
따라서, 추가적인 기능은 없으며, WCCFTech 및 VideoCardz 의 뉴스 페이지가 아닌 곳에서는 테스트하지 않았습니다.
<br><br>
현재 다른 사이트에 대한 지원 계획은 없으며, 다른 곳의 Sources 를 활용하게 될 때, 해당 사이트에 대한 지원을 추가할 것입니다.
이미지는 프로그램이 위치한 곳과 같은 디렉토리에 저장됩니다. (저장경로 설정 불가)

### [이미지 파일명 명명규칙]
* 기본적으로, 기사에 이미지가 삽입되어 있는 순서대로 명명됩니다. (1, 2, ...)
* 단, 이미지가 슬라이드 형태로 삽입된 경우, <이미지 순서>-<슬라이드에서의 이미지 순서>.<확장자> 로 저장됩니다.
* 예를 들어, 슬라이드가 2번째로 등장하고, 슬라이드 내에서 세번재로 등장하는 이미지의 파일명은, 2-3 이 됩니다. 

### [사용된 라이브러리]
* BeautifulSoup (in bs4)
* parse (in urllib)
* urllib.request
* re
* time
* datetime
* os

---
Latest Edited on 24. 04. 07.<br>
Created on 24. 04. 07.
