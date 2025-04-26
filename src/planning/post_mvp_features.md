# MVP 이후 추가 기능 계획

## 1. 일정 관리 시스템
### 1.1 기능 개요
- 모든 회원이 공유하는 공통 달력 기능
- 일정 추가, 수정, 삭제 기능
- 일정 카테고리 분류 및 색상 코딩
- 일정 알림 기능 (이메일, 푸시 알림)

### 1.2 기술 요구사항
- **프론트엔드**: 
  - 달력 라이브러리 (FullCalendar.js)
  - 드래그 앤 드롭 기능
  - 반응형 디자인
- **백엔드**:
  - 실시간 업데이트 (WebSocket)
  - 알림 시스템 (이메일, 푸시)
- **데이터베이스**:
  - 일정 테이블 추가
  - 알림 설정 테이블 추가

### 1.3 데이터베이스 설계
- **일정 테이블 (events)**
  - event_id: 일정 고유 ID (PK)
  - title: 일정 제목
  - description: 일정 설명
  - start_date: 시작 일시
  - end_date: 종료 일시
  - category: 일정 카테고리
  - color: 일정 색상
  - created_by: 생성자 ID
  - created_at: 생성 일시
  - updated_at: 수정 일시

- **알림 설정 테이블 (event_notifications)**
  - notification_id: 알림 고유 ID (PK)
  - event_id: 일정 ID (FK)
  - user_id: 사용자 ID
  - notification_type: 알림 유형 (이메일, 푸시)
  - notification_time: 알림 시간
  - created_at: 생성 일시

## 2. 온라인 엑셀 동시 편집 시스템
### 2.1 기능 개요
- 엑셀 파일 온라인 업로드 및 편집
- 다중 사용자 동시 편집 지원
- 셀 잠금 기능 (다른 사용자가 편집 중인 셀 보호)
- 변경 사항 실시간 동기화
- 편집 이력 관리 및 되돌리기 기능

### 2.2 기술 요구사항
- **프론트엔드**:
  - 스프레드시트 라이브러리 (Handsontable, AG Grid)
  - 실시간 협업 기능
  - 셀 잠금 및 권한 관리 UI
- **백엔드**:
  - 실시간 데이터 동기화 (WebSocket)
  - 파일 변환 및 저장 시스템
  - 충돌 해결 알고리즘
- **데이터베이스**:
  - 스프레드시트 테이블 추가
  - 편집 세션 테이블 추가
  - 셀 잠금 테이블 추가

### 2.3 데이터베이스 설계
- **스프레드시트 테이블 (spreadsheets)**
  - spreadsheet_id: 스프레드시트 고유 ID (PK)
  - title: 스프레드시트 제목
  - file_path: 파일 경로
  - created_by: 생성자 ID
  - created_at: 생성 일시
  - updated_at: 수정 일시
  - version: 버전 번호

- **편집 세션 테이블 (edit_sessions)**
  - session_id: 세션 고유 ID (PK)
  - spreadsheet_id: 스프레드시트 ID (FK)
  - user_id: 사용자 ID
  - start_time: 시작 시간
  - end_time: 종료 시간
  - status: 세션 상태 (활성, 종료)

- **셀 잠금 테이블 (cell_locks)**
  - lock_id: 잠금 고유 ID (PK)
  - spreadsheet_id: 스프레드시트 ID (FK)
  - user_id: 사용자 ID
  - cell_reference: 셀 참조 (예: A1, B2)
  - locked_at: 잠금 시간
  - expires_at: 만료 시간

## 3. 구현 우선순위
1. **1단계: 일정 관리 시스템 기본 기능**
   - 달력 UI 구현
   - 일정 CRUD 기능
   - 기본 알림 기능

2. **2단계: 온라인 엑셀 기본 기능**
   - 스프레드시트 UI 구현
   - 파일 업로드/다운로드
   - 기본 편집 기능

3. **3단계: 실시간 협업 기능**
   - WebSocket 연동
   - 동시 편집 기능
   - 셀 잠금 기능

4. **4단계: 고급 기능**
   - 고급 알림 시스템
   - 편집 이력 관리
   - 충돌 해결 알고리즘 개선

## 4. 기대효과
- **일정 관리 시스템**
  - 팀 일정 관리 효율성 향상
  - 일정 충돌 감소
  - 회의 및 이벤트 참여율 증가

- **온라인 엑셀 동시 편집**
  - 문서 협업 효율성 향상
  - 버전 관리 문제 해결
  - 원격 작업 지원 강화 