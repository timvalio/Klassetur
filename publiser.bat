@echo off
chcp 65001 >nul
REM publiser.bat - bygger kartsida pa nytt og sender den til GitHub Pages.
REM Dobbeltklikk denne i stedet for a apne GitHub Desktop.
cd /d "%~dp0"
echo.
echo ===  Publiserer Klassetur 2027  ===
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo Finner ikke git. Bruk GitHub Desktop denne gangen.
  goto slutt
)

where python >nul 2>nul
if errorlevel 1 (
  echo Finner ikke python. Publiserer filene slik de ligger.
  goto publiser
)

echo Bygger kartsida fra turarkene...
cd underlag
python lag_kart.py
set BYGG=%errorlevel%
cd ..
if not "%BYGG%"=="0" (
  echo.
  echo Ombyggingen feilet. Ingenting er publisert - se meldingen over.
  goto slutt
)

:publiser
echo.
git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo Ingenting har endret seg - nettsida er allerede oppdatert.
  goto slutt
)

git commit -m "Oppdatert %DATE% %TIME:~0,5%"
git push origin
if errorlevel 1 (
  echo.
  echo Push feilet. Apne GitHub Desktop og trykk Push origin derfra.
  goto slutt
)
echo.
echo Ferdig. Nettsida er oppdatert om under ett minutt.

:slutt
echo.
pause
