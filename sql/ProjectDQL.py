import random
import faker 
from datetime import datetime, timedelta

fake = faker.Faker("ko_KR")

def generate_phone_number():
    return "+82-" + "".join([str(random.randint(0, 9)) for _ in range(3)]) + "-" + "".join([str(random.randint(0, 9)) for _ in range(3)]) + "-" + "".join([str(random.randint(0, 9)) for _ in range(4)])

def generate_insert_statements():
    # 부서 데이터 각각의 data를 담는다
    department_data = [(1, '마케팅'),(2, '경영관리'),(3, '연구개발'),(4, '개발'),(5, '인사'),(6, '영업'),(7, '디자인')]  # department_id, department_name, department_number
    employee_data = []    # employee_id, department_id, employee_name, registration_number, education_level, skill_set, employee_email, employee_phone_number, employee_address
    customer_data = []    # customer_id, customer_name, customer_email, customer_phone_number, customer_address
    project_data = []     # project_id, customer_id, project_name, start_date, end_date
    participationProject_data = []  # employee_id, project_id, start_date, end_date, role
    contract_data = []    # contract_id, employee_id, annual_salary, contract_date
    salary_data = []      # salary_id, customer_id, contract_id, base_salary, monthly_salary
    peerEvaluation_data = []  # evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    peerEvaluationType_data = []  # evaluation_id, evaluation_type, evaluation_content
    PMEvaluation_data = []  # evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    PMEvaluationType_data = []  # evaluation_id, evaluation_type, evaluation_content
    customerEvaluation_data = []  # evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    customerEvaluationType_data = []  # evaluation_id, evaluation_type, evaluation_content
    incentive_data = []    # project_id, employee_id, incentive_amount
    seminar_data = []      # seminar_id, seminar_name, seminar_date, seminar_instructor
    seminarParticipation_data = []  # seminar_id, employee_id




    skill_sets = [ 
        # git, c, c++, java, python, sql, kafka, spring, spring boot, jpa, hibernate, mybatis, node.js, express.js, react.js, vue.js, angular.js, html, css, javascript, typescript, ruby, php, go, kotlin, swift, r, rust, scala, groovy, perl, shell, powershell, bash, awk, sed, rdbms, nosql, mongodb, redis, memcached, cassandra, elasticsearch, rabbitmq, kafka, activemq, artemis, jms
        # 아무거나 4개에서 6개 선택
        'git, c, c++, java, python',
        'sql, kafka, spring, spring boot, jpa',
        'hibernate, mybatis, node.js, express.js',
        'react.js, vue.js, angular.js, html',
        'css, javascript, typescript, ruby',
        'php, go, kotlin, swift, r',
        'rust, scala, groovy, perl, shell',
        'powershell, bash, awk, sed, rdbms',
        'nosql, mongodb, redis, memcached',
        'cassandra, elasticsearch, rabbitmq, kafka',
        'activemq, artemis, jms'
    ]
    # education_level = ['high school', 'associate degree', 'bachelor degree', 'master degree', 'doctoral degree'] # 고등학교, 전문대학, 학사, 석사, 박사
    education_level = ['고등학교', '전문대학', '학사', '석사', '박사']
    
    # member table
    for employee_id in range(1, 101): # 100명의 직원
        if employee_id <= 70: #개발자
            dept_id = 4  # 개발 부서
            registration_number = generate_registration_number()
            employee_data.append((employee_id, dept_id, fake.name(), registration_number, random.choice(education_level), random.choice(skill_sets), fake.email(), generate_phone_number(), fake.address()))
        else: #마케팅, 경영관리, 연구개발, 인사, 영업, 디자인
            dept_id = (employee_id % 7) + 1  # 나머지 부서 4:개발 부서또한 선택될 수 있음
            registration_number = generate_registration_number()
            employee_data.append((employee_id, dept_id, fake.name(), registration_number, random.choice(education_level), random.choice(skill_sets), fake.email(), generate_phone_number(), fake.address()))
            

    for customer_id in range(1, 101):# 100명의 고객
        customer_data.append((customer_id, fake.name(), fake.email(), generate_phone_number(), fake.address()))
    


    for project_id in range(1, 101): # 100개의 프로젝트 생성
        customer_id = random.randint(1, 100)
        start_date = fake.date_between(start_date='-10y', end_date='now')
        
        # 20개의 프로젝트는 진행중이므로 end_date가 null
        # null 은 그냥 null 인데 어떻게 해야 할까
        if project_id <= 20:
            end_date = 'null'
        else:
            #단 현재보다 크면 안됨
            end_date = fake.date_between(start_date=start_date, end_date='now')
        
        project_data.append((project_id, customer_id, fake.sentence(), start_date, end_date))
        

    # 프로젝트 참여 PM 먼저 설정
    for project_id in range(1, 101): # 100개의 프로젝트에 대해
        project = project_data[project_id - 1]
        #개발자 중에서 PM을 랜덤으로 선택
        projcet_PM = random.choice([employee for employee in employee_data if employee[1] == 4])
        participationProject_data.append((projcet_PM[0], project_id, project[3], project[4], 'PM'))
        
    for participationProject_id in range(1, 501):  # 500개의 프로젝트 참여 데이터 생성
        while True:  # 중복이 발생하지 않을 때까지 반복
            employee = random.choice(employee_data)
            project = random.choice(project_data)  # 아무거나 골라
            # start date 는 프로젝트 시작일부터 끝일 사이 끝이 없으면 시작일부터 현재까지
            if project[4] == 'null':
                start_date = fake.date_between(start_date=project[3], end_date='now') 
                end_date = None  # 'null' 대신 None 사용
            else:
                start_date = fake.date_between(start_date=project[3], end_date=project[4]) #프로젝트 시작일부터 끝일 사이
                end_date = fake.date_between(start_date=start_date, end_date=project[4]) # start_date부터 끝일 사이
    
            # 참여 데이터의 중복 체크
            participation_key = (employee[0], project[0])  # (employee_id, project_id) 조합
            if not any(p[:2] == participation_key for p in participationProject_data):
                # 중복이 아닐 경우 role 설정
                if employee[1] != 4:
                    role = 'other'
                else:
                    # 분석가, 설계자, 프로그래머, 테스터 중 하나 선택
                    role = random.choice(['PL', 'Analyst', 'Designer', 'Programmer', 'Tester'])
    
                # 데이터 추가
                participationProject_data.append((employee[0], project[0], start_date, end_date, role))
                break  # 중복이 없으므로 반복 종료

    # 개발자가 아닌 경우 role은 other
    if employee[1] != 4:
        role = 'other'
    else:
        # 분석가, 설계자, 프로그래머, 테스터 중 하나 선택
        role = random.choice(['PL', 'Analyst', 'Designer', 'Programmer', 'Tester'])
        
    
    # 인센티브 데이터 생성
    # 프로젝트에 end_date가 있는 경우 && 프로젝트 참여한 직원들만 인센티브 지급
    # contract_id, employee_id, annual_salary, contract_date
    # salary_id, customer_id, contract_id, base_salary, monthly_salary, salary_date, salary_date
    # project_id, employee_id, incentive_amount
    for project in project_data:
        for participation in participationProject_data:
            if project[0] == participation[1] and project[4] != 'null':
                # start_date 가 2년전 까지만 인센티브 지급
                if participation[2] >= (fake.date_between(start_date='-2y', end_date='now')):
                    incentive_amount = random.randint(1, 11) * 100000
                    incentive_data.append((project[0], participation[0], incentive_amount))
                    
        
    
    contract_id = 1
    for employee in employee_data:
        for _ in range(1, random.randint(1, 11)):  # 1에서 10 사이의 계약 수
            annual_salary = random.randint(3000, 10000) * 10000  # 연봉 생성
            year_offset = random.randint(0, 10)  # 0년에서 10년 사이의 오프셋
            contract_date = generate_december_contract_date(year_offset)  # 계약 날짜 생성
            # 계약 데이터 추가
            contract_data.append((contract_id, employee[0], annual_salary, contract_date))  # (contract_id, employee_id, contract_date, annual_salary)
            # 월급 데이터 생성 (12개월)
            base_salary = annual_salary / 12  # 월급 계산
            for month in range(1, 13):  # 1부터 12까지 월급 정보 생성
                salary_id = len(salary_data) + 1  # salary_id는 리스트의 길이를 기반으로 생성
                year = int(contract_date[:4])
                salary_date = f"{year + 1}-{month:02d}-10"  # 계약 날짜 생성
                # 만약 인센티브가 있는 경우 base_salary에 인센티브 amount 를 추가해서 monthly_salary로 설정
                monthly_salary = 0
                for incentive in incentive_data:
                    if incentive[0] == employee[0]:
                        monthly_salary = base_salary + incentive[2]
                salary_data.append((salary_id, employee[0], contract_id, base_salary, monthly_salary, salary_date))  # (salary_id, employee_id, contract_id, base_salary, monthly_salary)
            contract_id += 1  # 계약 ID 증가
    
    
    #seminar table
    for seminar_id in range(1, 101):  # 100개의 세미나 생성
        seminar_date = fake.date_between(start_date='-10y', end_date='now')
        seminar_data.append((seminar_id, fake.sentence(), seminar_date, fake.name()))
    
    #seminarParticipation table
    for seminarParticipation_id in range(1, 501):  # 500개의 세미나 참가 데이터 생성
        while True:  # 중복이 발생하지 않을 때까지 반복
            employee = random.choice(employee_data)
            seminar = random.choice(seminar_data)  # 아무거나 골라
            seminarParticipation_key = (seminar[0], employee[0])  # (seminar_id, employee_id) 조합
            if not any(p[:2] == seminarParticipation_key for p in seminarParticipation_data):
                seminarParticipation_data.append((seminar[0], employee[0]))
                break  # 중복이 없으므로 반복 종료
    

    # peerEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # peerEvaluationType : evaluation_id, evaluation_type, evaluation_content
    # PMEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # PMEbaluationType : evaluation_id, evaluation_type, evaluation_content
    # customerEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # customerEvaluationType : evaluation_id, evaluation_type, evaluation_content
    evaluation_types = ['업무 수행평가', '커뮤니케이션 수행평가']
    
    
    # end_date가 있는 프로젝트에 참여한 모든 직원들이 다른직원들에 대해 평가를 진행
    peerEvaluation_id = 1
    for project in project_data: # 모든 프로젝트를 검사
        if project[4] != 'null': # end_date가 있는 프로젝트에 대해서만
            for evaluator in participationProject_data: # 모든 프로젝트 참여 데이터를 검사
                if project[0] == evaluator[1]: # 프로젝트에 참여한 직원에 대해서만
                    for evaluated in participationProject_data: # 모든 프로젝트 참여 데이터를 검사
                        if project[0] == evaluated[1] and evaluator[0] != evaluated[0] and evaluator[0] != evaluated[0]: # 프로젝트에 참여한 직원에 대해서만 자신 빼고
                            score = random.randint(1, 10) # 1에서 10 사이의 점수
                            #fake 모듈을 사용하여 임의의 문자열을 넣는다
                            peerEvaluation_data.append((peerEvaluation_id, project[0], evaluator[0], evaluated[0], score))
                            peerEvaluationType_data.append((peerEvaluation_id, evaluation_types[0], fake.sentence()))
                            peerEvaluationType_data.append((peerEvaluation_id, evaluation_types[1], fake.sentence()))
                            peerEvaluation_id += 1
    
    # end_date 가 있는 프로젝트에 참여한 PM들이 다른 직원들에 대해 평가를 진행
    PMEvaluation_id = 1
    for project in project_data: # 모든 프로젝트를 검사
        if project[4] != 'null': # end_date가 있는 프로젝트에 대해서만
            for evaluator in participationProject_data: # 모든 프로젝트 참여 데이터를 검사
                if project[0] == evaluator[1] and evaluator[4] == 'PM': # PM인 경우
                    for evaluated in participationProject_data: # 모든 프로젝트 참여 데이터를 검사
                        if project[0] == evaluated[1] and evaluator[0] != evaluated[0] and evaluator[0] != evaluated[0]: # PM이면서 자신 빼고
                            score = random.randint(1, 10)
                            PMEvaluation_data.append((PMEvaluation_id, project[0], evaluator[0], evaluated[0], score))
                            PMEvaluationType_data.append((PMEvaluation_id, evaluation_types[0], fake.sentence()))
                            PMEvaluationType_data.append((PMEvaluation_id, evaluation_types[1], fake.sentence()))
                            PMEvaluation_id += 1
    
    # end_date 가 있는 프로젝트에 참여한 고객들이 다른 직원들에 대해 평가를 진행
    customerEvaluation_id = 1
    for project in project_data: # 모든 프로젝트를 검사
        if project[4] != 'null':
            for evaluator in customer_data:
                if project[1] == evaluator[0]:
                    for evaluated in participationProject_data:
                        if project[0] == evaluated[1] and evaluator[0] != evaluated[0] and evaluator[0] != evaluated[0]:
                            score = random.randint(1, 10)
                            customerEvaluation_data.append((customerEvaluation_id, project[0], evaluator[0], evaluated[0], score))
                            customerEvaluationType_data.append((customerEvaluation_id, evaluation_types[0], fake.sentence()))
                            customerEvaluationType_data.append((customerEvaluation_id, evaluation_types[1], fake.sentence()))
                            customerEvaluation_id += 1   
    
    
    
    #department table
    for dept in department_data:  # department_id, department_name, department_number
        print(f'INSERT INTO "Department" ("department_id", "department_name") VALUES ({dept[0]}, \'{dept[1]}\');')

    for employee in employee_data:  # employee_id, department_id, employee_name, registration_number, education_level, skill_set, employee_email, employee_phone_number, employee_address
        print(f'INSERT INTO "Employee" ("employee_id", "department_id", "employee_name", "registration_number", "education_level", "skill_set", "employee_email", "employee_phone_number", "employee_address") VALUES ({employee[0]}, {employee[1]}, \'{employee[2]}\', \'{employee[3]}\', \'{employee[4]}\', \'{employee[5]}\', \'{employee[6]}\', \'{employee[7]}\', \'{employee[8]}\');')

    for customer in customer_data:  # customer_id, customer_name, customer_email, customer_phone_number, customer_address
        print(f'INSERT INTO "Customer" ("customer_id", "customer_name", "customer_email", "customer_phone_number", "customer_address") VALUES ({customer[0]}, \'{customer[1]}\', \'{customer[2]}\', \'{customer[3]}\', \'{customer[4]}\');')

    for project in project_data:  # project_id, customer_id, project_name, start_date, end_date
        start_date = f"TO_DATE('{project[3]}', 'YYYY-MM-DD')"  # start_date를 TO_DATE로 변경
        end_date = f"TO_DATE('{project[4]}', 'YYYY-MM-DD')" if project[4] not in [None, 'null'] else 'NULL'  # end_date를 TO_DATE로 변경, None인 경우 NULL 처리
        print(f'INSERT INTO "Project" ("project_id", "customer_id", "project_name", "start_date", "end_date") VALUES ({project[0]}, {project[1]}, \'{project[2]}\', {start_date}, {end_date});')

    for participationProject in participationProject_data:  # employee_id, project_id, start_date, end_date, role
        start_date = f"TO_DATE('{participationProject[2]}', 'YYYY-MM-DD')"  # start_date를 TO_DATE로 변경
        end_date = f"TO_DATE('{participationProject[3]}', 'YYYY-MM-DD')" if participationProject[3] not in [None, 'null'] else 'NULL'  # end_date를 TO_DATE로 변경, None인 경우 NULL 처리
        print(f'INSERT INTO "ParticipationProject" ("employee_id", "project_id", "start_date", "end_date", "role") VALUES ({participationProject[0]}, {participationProject[1]}, {start_date}, {end_date}, \'{participationProject[4]}\');')


    for incentive in incentive_data:
        print(f'INSERT INTO "Incentive" ("project_id", "employee_id", "incentive_amount") VALUES ({incentive[0]}, {incentive[1]}, {incentive[2]});')
    
    for contract in contract_data:
        print(f'INSERT INTO "Contract" ("contract_id", "employee_id", "annual_salary", "contract_date") VALUES ({contract[0]}, {contract[1]}, {contract[2]}, TO_DATE(\'{contract[3]}\', \'YYYY-MM-DD\'));')
    for salary in salary_data:
        print(f'INSERT INTO "Salary" ("salary_id", "employee_id", "contract_id", "base_salary", "monthly_salary", "salary_date") VALUES ({salary[0]}, {salary[1]}, {salary[2]}, {salary[3]}, {salary[4]}, TO_DATE(\'{salary[5]}\', \'YYYY-MM-DD\'));')
        
        
    # peerEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # peerEvaluationType : evaluation_id, evaluation_type, evaluation_content
    # PMEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # PMEbaluationType : evaluation_id, evaluation_type, evaluation_content
    # customerEvaluation : evaluation_id, project_id, evaluator_id, evaluated_employee_id, score
    # customerEvaluationType : evaluation_id, evaluation_type, evaluation_content
    # print(peerEvaluation_data)
    for peerEvaluation in peerEvaluation_data:
        print(f'INSERT INTO "PeerEvaluation" ("evaluation_id", "project_id", "evaluator_id", "evaluated_employee_id", "score") VALUES ({peerEvaluation[0]}, {peerEvaluation[1]}, {peerEvaluation[2]}, {peerEvaluation[3]}, {peerEvaluation[4]});')
    # print(peerEvaluationType_data)
    for peerEvaluationType in peerEvaluationType_data:
        print(f'INSERT INTO "PeerEvaluationType" ("evaluation_id", "evaluation_type", "evaluation_content") VALUES ({peerEvaluationType[0]}, \'{peerEvaluationType[1]}\', \'{peerEvaluationType[2]}\');')
    # print(PMEvaluation_data)
    for PMEvaluation in PMEvaluation_data:
        print(f'INSERT INTO "PMEvaluation" ("evaluation_id", "project_id", "evaluator_id", "evaluated_employee_id", "score") VALUES ({PMEvaluation[0]}, {PMEvaluation[1]}, {PMEvaluation[2]}, {PMEvaluation[3]}, {PMEvaluation[4]});')
    # print(PMEvaluationType_data)
    for PMEvaluationType in PMEvaluationType_data:
        print(f'INSERT INTO "PMEvaluationType" ("evaluation_id", "evaluation_type", "evaluation_content") VALUES ({PMEvaluationType[0]}, \'{PMEvaluationType[1]}\', \'{PMEvaluationType[2]}\');')
    # print(customerEvaluation_data)
    for customerEvaluation in customerEvaluation_data:
        print(f'INSERT INTO "CustomerEvaluation" ("evaluation_id", "project_id", "evaluator_id", "evaluated_employee_id", "score") VALUES ({customerEvaluation[0]}, {customerEvaluation[1]}, {customerEvaluation[2]}, {customerEvaluation[3]}, {customerEvaluation[4]});')
    # print(customerEvaluationType_data)
    for customerEvaluationType in customerEvaluationType_data:
        print(f'INSERT INTO "CustomerEvaluationType" ("evaluation_id", "evaluation_type", "evaluation_content") VALUES ({customerEvaluationType[0]}, \'{customerEvaluationType[1]}\', \'{customerEvaluationType[2]}\');')    
    # print(incentive_data)
    for seminar in seminar_data:
        print(f'INSERT INTO "Seminar" ("seminar_id", "seminar_name", "seminar_date", "seminar_instructor") VALUES ({seminar[0]}, \'{seminar[1]}\', TO_DATE(\'{seminar[2]}\', \'YYYY-MM-DD\'), \'{seminar[3]}\');')
    # print(seminarParticipation_data)
    for seminarParticipation in seminarParticipation_data:
        print(f'INSERT INTO "SeminarParticipation" ("seminar_id", "employee_id") VALUES ({seminarParticipation[0]}, {seminarParticipation[1]});')
    print('COMMIT;')
    



def generate_registration_number():
    # 6자리 숫자와 7자리 숫자를 생성하여 주민등록번호 형식으로 반환
    first_part = f'{random.randint(0, 999999):06d}'  # 6자리 숫자
    second_part = f'{random.randint(0, 9999999):07d}'  # 7자리 숫자
    return f'{first_part}-{second_part}'


def generate_december_contract_date(year_offset):
    # 현재 연도에서 year_offset 만큼 이전 연도 선택
    year = 2023 - year_offset  # 현재 연도는 2023년으로 가정
    month = 12  # 12월
    day = random.randint(1, 31)  # 1일부터 31일까지의 날짜 중 랜덤 선택

    # 날짜 포맷팅
    return f"{year}-{month:02d}-{day:02d}"

#평가시 사용하는 date 처리 end_date + 2일로 정한다
def generate_evaluation_date(end_date):
    #date 모둘에 넣고
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    #2일 더한다
    end_date = end_date + timedelta(days=2)
    #다시 string으로 변환
    end_date = end_date.strftime('%Y-%m-%d')
    return end_date
    



if __name__ == "__main__":
    # 데이터 삽입 문 생성 및 출력
    generate_insert_statements()