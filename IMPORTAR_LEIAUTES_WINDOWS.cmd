@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (where python >nul 2>&1 && set "PY=python")
if not defined PY (
 echo Instale Python 3 em https://www.python.org/downloads/windows/ e marque Add Python to PATH.
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 %PY% -m venv .venv
 if errorlevel 1 goto erro
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erro
set "DOC=all"
set /p "DOC=Documento [all, dce, mdfe, nf3e, cte, cteos, gtve, abi, nfgas, nfag, nfcom, bpe, bpetm, bpeta] (Enter = all): "
set "HTML="
set /p "HTML=Pasta dos manuais HTML salvos (Enter = baixar direto do portal): "
if defined HTML (
 ".venv\Scripts\python.exe" scripts\import_documents.py --document "%DOC%" --html-dir "%HTML%"
) else (
 ".venv\Scripts\python.exe" scripts\import_documents.py --document "%DOC%"
)
set "RC=%errorlevel%"
echo.
echo Confira public\data\importacao_documentos.json. Os catalogos anteriores foram protegidos.
if not "%RC%"=="0" echo Houve falha em pelo menos uma fonte. Nao considere os catalogos completos.
echo Abra public\EXPLORADOR_OFFLINE_COMPLETO.html para testar os catalogos disponiveis.
echo Para publicar, envie a pasta public na RAIZ do repositorio, nao dentro de outra pasta public.
pause
exit /b %RC%
:erro
echo Falha ao preparar o Python. Confira a conexao e a instalacao.
pause
exit /b 1
