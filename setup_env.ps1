# 가상환경이 존재하지 않는다면
if (-Not (Test-Path ".venv")) {
    # 가상환경 생성
    python -m venv .venv
    Write-Host "가상환경 생성 완료"
}

# 가상환경 구성
# 가상환경 이름: .venv
& .venv\Scripts\Activate.ps1
Write-Host "가상환경 구성 완료"

# Oracle Instant Client 환경변수 설정
$env:LD_LIBRARY_PATH = "$PWD\config\instantclient_23_6"
Write-Host "Oracle Instant Client 환경변수 설정 완료"
