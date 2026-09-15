@echo off
setlocal
cd /d "%~dp0"
echo.
echo  Sletter turark som er tatt ut av lista (Paris, Dubai, Kobenhavn, Hamburg) og den gamle rydd-opp.bat:
for %%f in (underlag\Klassetur-Paris.html underlag\Klassetur-Dubai.html underlag\Klassetur-Kobenhavn.html underlag\Klassetur-Hamburg.html rydd-opp.bat) do (
  if exist "%%f" ( del "%%f" && echo     slettet   %%f ) else ( echo     fantes ikke   %%f )
)
echo.
echo  Ferdig. Commit og push i GitHub Desktop etterpaa. Denne fila sletter seg selv naa.
pause
(goto) 2>nul & del "%~f0"
