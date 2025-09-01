@echo off
echo ========================================
echo    Sudalys QR Generator - Build All
echo ========================================
echo.

echo 1. Compilation de l'executable...
python build_scripts/build_exe.py
if %ERRORLEVEL% neq 0 (
    echo ERREUR: Echec de la compilation de l'executable
    pause
    exit /b 1
)

echo.
echo 2. Creation de l'installateur autonome...
python build_scripts/build_standalone_installer.py
if %ERRORLEVEL% neq 0 (
    echo ERREUR: Echec de la creation de l'installateur
    pause
    exit /b 1
)

echo.
echo ========================================
echo    BUILD TERMINE AVEC SUCCES!
echo ========================================
echo.
echo L'installateur autonome est pret dans installer_output/
echo Les utilisateurs n'ont qu'a lancer le .exe pour installer!
echo.
pause
