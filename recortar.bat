@echo off
REM Recorta los primeros 5 segundos del archivo prueba.mp4

set INPUT=prueba.mp4
set OUTPUT=prueba_5s.mp4

echo Recortando los primeros 5 segundos de %INPUT% ...
ffmpeg -i "%INPUT%" -t 5 -c copy "%OUTPUT%"

echo.
echo Listo! Se generó el archivo: %OUTPUT%
pause
