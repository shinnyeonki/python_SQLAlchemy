/*
    1. 부서
    2. 직원
    3. 고객
    4. 프로젝트
    5. 프로젝트 참여
    6. 계약
    7. 급여
    8. 동료 평가, 동료 평가 타입
    9. PM 평가, PM 평가 타입
    10. 고객 평가, 고객 평가 타입
    11. 인센티브
    12. 세미나
    13. 세미나 참여

    동료 평가 타입등을 속성에서 table 로 분리하였음
    개발자는 프로젝트 참여시 적절한 직무로 다른 부서사람은 프로젝트 참여시 "기타"로

*/

CREATE TABLE "Department" (
    "department_id" INTEGER NOT NULL,
    "department_name" VARCHAR2(50) NOT NULL,
    CONSTRAINT "PK_DEPARTMENT" PRIMARY KEY ("department_id"),
    CONSTRAINT "CK_Department_department_name" CHECK ("department_name" IN ('마케팅', '경영관리', '연구개발', '개발', '인사', '영업', '디자인'))
);

CREATE TABLE "Employee" (
    "employee_id" INTEGER NOT NULL,
    "department_id" INTEGER NOT NULL,
    "employee_name" VARCHAR2(30) NOT NULL,
    "registration_number" VARCHAR2(14) NOT NULL, --정말 varchar2로 할 것인가
    "education_level" VARCHAR2(50) NOT NULL,
    "skill_set" VARCHAR2(200) NULL, -- 스킬셋은 string 으로 저장
    "employee_email" VARCHAR2(50) NULL,
    "employee_phone_number" VARCHAR2(20) NULL,
    "employee_address" VARCHAR2(100) NULL,
    CONSTRAINT "PK_EMPLOYEE" PRIMARY KEY ("employee_id"),
    CONSTRAINT "FK_Department_TO_Employee_1" FOREIGN KEY ("department_id") REFERENCES "Department" ("department_id")
);

CREATE TABLE "Customer" (
    "customer_id" INTEGER NOT NULL,
    "customer_name" VARCHAR2(30) NOT NULL,
    "customer_email" VARCHAR2(50) NULL,
    "customer_phone_number" VARCHAR2(20) NULL,
    "customer_address" VARCHAR2(100) NULL,
    CONSTRAINT "PK_CUSTOMER" PRIMARY KEY ("customer_id")
);

CREATE TABLE "Project" (
    "project_id" INTEGER NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "project_name" VARCHAR2(100) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NULL, -- check 을 사용하여 프로젝트(start_date) 시작일 보다 커야 한다
    CONSTRAINT "PK_PROJECT" PRIMARY KEY ("project_id"),
    CONSTRAINT "FK_Customer_TO_Project_1" FOREIGN KEY ("customer_id") REFERENCES "Customer" ("customer_id"),
    CONSTRAINT "CK_Project_EndDate" CHECK ("end_date" >= "start_date") -- end_date는 start_date보다 커야 함
);

CREATE TABLE "ParticipationProject" (
    "employee_id" INTEGER NOT NULL,
    "project_id" INTEGER NOT NULL,
    "start_date" DATE NOT NULL, --트리거를 사용하여 프로젝트 시작일 보다 커야 한다??
    "end_date" DATE NULL, 
    "role" VARCHAR2(30) NOT NULL,
    CONSTRAINT "PK_PARTICIPATION_PROJECT" PRIMARY KEY ("employee_id", "project_id"),
    CONSTRAINT "FK_Employee_TO_ParticipationProject_1" FOREIGN KEY ("employee_id") REFERENCES "Employee" ("employee_id"),
    CONSTRAINT "FK_Project_TO_ParticipationProject_1" FOREIGN KEY ("project_id") REFERENCES "Project" ("project_id"),
    CONSTRAINT "CK_ParticipationProject_EndDates" CHECK ("end_date" >= "start_date"), -- start_date는 참조하는 프로젝트의 start_date보다 커야 하고, end_date는 해당 프로젝트의 end_date보다 작아야 함
    CONSTRAINT "CK_ParticipationProject_role" CHECK ("role" IN ('PM', 'PL', 'Analyst', 'Designer', 'Programmer', 'Tester', 'other')) -- role의 값 제한 PM: Project Manager, PL: Project Leader, 분석가, 설계자, 프로그래머, 테스터
);

CREATE TABLE "Contract" (
    "contract_id" INTEGER NOT NULL,
    "employee_id" INTEGER NOT NULL,
    "annual_salary" INTEGER NOT NULL,
    "contract_date" DATE NOT NULL,
    CONSTRAINT "PK_CONTRACT" PRIMARY KEY ("contract_id"),
    CONSTRAINT "FK_Employee_TO_Contract_1" FOREIGN KEY ("employee_id") REFERENCES "Employee" ("employee_id")
);

CREATE TABLE "Salary" (
    "salary_id" INTEGER NOT NULL,
    "employee_id" INTEGER NOT NULL,
    "contract_id" INTEGER NOT NULL,
    "base_salary" INTEGER NOT NULL,
    "monthly_salary" INTEGER NOT NULL,
    "salary_date" DATE NOT NULL,
    CONSTRAINT "PK_SALARY" PRIMARY KEY ("salary_id"),
    CONSTRAINT "FK_Employee_TO_Salary_1" FOREIGN KEY ("employee_id") REFERENCES "Employee" ("employee_id"),
    CONSTRAINT "FK_Contract_TO_Salary_1" FOREIGN KEY ("contract_id") REFERENCES "Contract" ("contract_id")
);

--동료 평가, PM 평가, 고객 평가
CREATE TABLE "PeerEvaluation" (
    "evaluation_id" INTEGER NOT NULL,
    "project_id" INTEGER NOT NULL,
    "evaluator_id" INTEGER NOT NULL,
    "evaluated_employee_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    CONSTRAINT "PK_PEEREVALUATION" PRIMARY KEY ("evaluation_id"),
    CONSTRAINT "FK_Project_TO_PeerEvaluation_1" FOREIGN KEY ("project_id") REFERENCES "Project" ("project_id"),
    CONSTRAINT "FK_Employee_TO_PeerEvaluation_1" FOREIGN KEY ("evaluator_id") REFERENCES "Employee" ("employee_id"),
    CONSTRAINT "FK_Employee_TO_PeerEvaluation_2" FOREIGN KEY ("evaluated_employee_id") REFERENCES "Employee" ("employee_id"),
    CONSTRAINT "CK_PeerEvaluation_Score" CHECK ("score" BETWEEN 0 AND 10)
);

CREATE TABLE "PeerEvaluationType" (
    "evaluation_id" INTEGER NOT NULL,
    "evaluation_type" VARCHAR2(50) NOT NULL,
    "evaluation_content" VARCHAR2(500) NULL,
    CONSTRAINT "PK_PEEREVALUATIONTYPE" PRIMARY KEY ("evaluation_id", "evaluation_type"),
    CONSTRAINT "FK_PeerEvaluation_TO_PeerEvaluationType_1" FOREIGN KEY ("evaluation_id") REFERENCES "PeerEvaluation" ("evaluation_id")
);

CREATE TABLE "PMEvaluation" (
    "evaluation_id" INTEGER NOT NULL,
    "project_id" INTEGER NOT NULL,
    "evaluator_id" INTEGER NOT NULL,
    "evaluated_employee_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    CONSTRAINT "PK_PMEVALUATION" PRIMARY KEY ("evaluation_id"),
    CONSTRAINT "FK_Project_TO_PMEvaluation_1" FOREIGN KEY ("project_id") REFERENCES "Project" ("project_id"),
    CONSTRAINT "FK_Employee_TO_PMEvaluation_1" FOREIGN KEY ("evaluator_id") REFERENCES "Employee" ("employee_id"),
    CONSTRAINT "FK_Employee_TO_PMEvaluation_2" FOREIGN KEY ("evaluated_employee_id") REFERENCES "Employee" ("employee_id")
);

CREATE TABLE "PMEvaluationType" (
    "evaluation_id" INTEGER NOT NULL,
    "evaluation_type" VARCHAR2(50) NOT NULL,
    "evaluation_content" VARCHAR2(500) NULL,
    CONSTRAINT "PK_PMEVALUATIONTYPE" PRIMARY KEY ("evaluation_id", "evaluation_type"),
    CONSTRAINT "FK_PMEvaluation_TO_PMEvaluationType_1" FOREIGN KEY ("evaluation_id") REFERENCES "PMEvaluation" ("evaluation_id")
);

CREATE TABLE "CustomerEvaluation" (
    "evaluation_id" INTEGER NOT NULL,
    "project_id" INTEGER NOT NULL,
    "evaluator_id" INTEGER NOT NULL,
    "evaluated_employee_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    CONSTRAINT "PK_CUSTOMEREVALUATION" PRIMARY KEY ("evaluation_id"),
    CONSTRAINT "FK_Project_TO_CustomerEvaluation_1" FOREIGN KEY ("project_id") REFERENCES "Project" ("project_id"),
    CONSTRAINT "FK_Customer_TO_CustomerEvaluation_1" FOREIGN KEY ("evaluator_id") REFERENCES "Customer" ("customer_id"),
    CONSTRAINT "FK_Employee_TO_CustomerEvaluation_1" FOREIGN KEY ("evaluated_employee_id") REFERENCES "Employee" ("employee_id")
);

CREATE TABLE "CustomerEvaluationType" (
    "evaluation_id" INTEGER NOT NULL,
    "evaluation_type" VARCHAR2(50) NOT NULL,
    "evaluation_content" VARCHAR2(500) NULL,
    CONSTRAINT "PK_CUSTOMEREVALUATIONTYPE" PRIMARY KEY ("evaluation_id", "evaluation_type"),
    CONSTRAINT "FK_CustomerEvaluation_TO_CustomerEvaluationType_1" FOREIGN KEY ("evaluation_id") REFERENCES "CustomerEvaluation" ("evaluation_id")
);

--인센티브
CREATE TABLE "Incentive" (
    "project_id" INTEGER NOT NULL,
    "employee_id" INTEGER NOT NULL,
    "incentive_amount" INTEGER NOT NULL,
    CONSTRAINT "PK_INCENTIVE" PRIMARY KEY ("project_id", "employee_id"),
    CONSTRAINT "FK_Project_TO_Incentive_1" FOREIGN KEY ("project_id") REFERENCES "Project" ("project_id"),
    CONSTRAINT "FK_Employee_TO_Incentive_1" FOREIGN KEY ("employee_id") REFERENCES "Employee" ("employee_id")
);

--세미나, 세미나 참여
CREATE TABLE "Seminar" (
    "seminar_id" INTEGER NOT NULL,
    "seminar_name" VARCHAR2(100) NOT NULL,
    "seminar_date" DATE NOT NULL, 
    "seminar_instructor" VARCHAR2(100) NOT NULL,
    CONSTRAINT "PK_SEMINAR" PRIMARY KEY ("seminar_id") -- seminar_id 를 pk 로 설정
);

CREATE TABLE "SeminarParticipation" (
    "seminar_id" INTEGER NOT NULL,
    "employee_id" INTEGER NOT NULL,
    CONSTRAINT "PK_SEMINARPARTICIPATION" PRIMARY KEY ("seminar_id", "employee_id"), -- seminar_id, employee_id 를 pk 로 설정
    CONSTRAINT "FK_Seminar_TO_SeminarParticipation_1" FOREIGN KEY ("seminar_id") REFERENCES "Seminar" ("seminar_id"),
    CONSTRAINT "FK_Employee_TO_SeminarParticipation_1" FOREIGN KEY ("employee_id") REFERENCES "Employee" ("employee_id")
);



COMMENT ON TABLE "ParticipationProject" IS '프로젝트 참여 테이블';
COMMENT ON COLUMN "ParticipationProject"."start_date" IS 'check 를 사용하여 프로젝트 시작일 보다 커야 하고 종료일 보다 작아야 한다';

