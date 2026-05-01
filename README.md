##  요약
### 📌 아키텍처

Spring Boot 스타일 계층 구조
SQL Map (-- key:) 기반 쿼리 관리
서비스별 SQL 분리

### 📌 DB & Oracle

ORM 미사용
python‑oracledb
PL/SQL 익명 블록 호출
OUT / IN OUT / RETURN
REF CURSOR / OBJECT / COLLECTION
OBJECT → dataclass 자동 매핑
ARRAY / ASSOCIATIVE ARRAY 지원
NUMBER → Decimal / int 정책 처리

### 📌 공통 기능

.env 기반 환경 설정
트랜잭션 공통 처리 (with transactional())
OFFSET/FETCH 페이징
동적 WHERE
SQL 세미콜론 자동 제거

### 📌 인증

로그인 API
bcrypt 비밀번호 검증
JWT 발급 ✅

### 폴더 구조
app/
├─ main.py
├─ config/
│  ├─ app_config.py          # ✅ .env 로드
│  └─ database.py            # ✅ Oracle pool
├─ controller/
│  ├─ auth_controller.py     # ✅ 로그인
│  └─ user_controller.py
├─ service/
│  ├─ auth_service.py
│  └─ user_service.py
├─ repository/
│  ├─ auth_repository.py
│  └─ user_repository.py
├─ query/
│  ├─ auth/
│  │  └─ auth.sql            # ✅ 로그인 SQL
│  └─ user/
│     └─ user.sql
├─ util/
│  ├─ query_loader.py
│  ├─ sql_template.py
│  ├─ tx.py
│  ├─ oracle_types.py
│  ├─ number_policy.py
│  ├─ object_mapper.py
│  ├─ db_executor.py
│  └─ security.py            # ✅ JWT / password
└─ common/
   └─ exception.py
