# Wrapper: run curl-based API tests defined in API_TEST.md
Set-Location $PSScriptRoot
python .\run_api_tests.py
exit $LASTEXITCODE
