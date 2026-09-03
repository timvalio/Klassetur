@echo off
setlocal
cd /d "%~dp0"
set "HER=%~dp0"
set "HER=%HER:~0,-1%"
for %%d in ("%HER%") do set "NAVN=%%~nxd"
echo.
echo  Rydder opp i: %HER%
echo.
if not exist "underlag\Klassetur-kandidater-2027.html" (
  echo  Finner ikke mappa underlag her. Ingenting er slettet.
  pause
  exit /b 1
)
echo  Sletter gamle kopier i rota - de ligger fortsatt i underlag:
for %%f in (
  Klassetur-kandidater-2027.html Klassetur-A-Gdansk.html Klassetur-B-Kreta.html Klassetur-C-Split.html
  Klassetur-Albania.html Klassetur-Algarve.html Klassetur-Bulgaria.html Klassetur-CostaBlanca.html
  Klassetur-CostaBrava.html Klassetur-CostaDelSol.html Klassetur-Mallorca.html Klassetur-Malta.html
  Klassetur-Montenegro.html Klassetur-Rhodos.html Klassetur-Riga.html Klassetur-Tyrkia.html
  Klassetur-Vilnius.html flypriser.py ruter.csv lag_kart.py
) do (
  if exist "%%f" (
    if exist "underlag\%%f" (
      del "%%f" && echo     slettet   %%f
    ) else (
      echo     beholdt   %%f  - finnes ikke i underlag
    )
  )
)
echo.
if /i "%NAVN%"=="Klassetur 2027" (
  echo  Mappa heter allerede Klassetur 2027. Ferdig - denne fila sletter seg selv.
  pause
  (goto) 2>nul & del "%~f0"
)
if exist "%~dp0..\Klassetur 2027\" (
  echo  Det finnes allerede en mappe Klassetur 2027 ved siden av - bytter ikke navn.
  echo  Ferdig. Denne fila kan slettes.
  pause
  exit /b 0
)
echo  Ferdig med opprydding.
echo  Trykk en tast for a gi mappa nytt navn (Klassetur 2027). Denne bat-fila sletter seg selv samtidig.
pause >nul
(goto) 2>nul & del "%~f0" & cd /d "%~d0\" & ren "%HER%" "Klassetur 2027"
