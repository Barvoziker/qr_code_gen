@echo off
echo === Compilation de l'application QR Code ===
echo.

REM Nettoyer les répertoires build et dist
if exist build\ (
    echo Suppression du dossier build...
    rmdir /s /q build
)

if exist dist\ (
    echo Suppression du dossier dist...
    rmdir /s /q dist
)

echo.
echo Création de l'icône à partir du logo...
python create_icon.py

echo.
echo Lancement de la compilation...
echo.

REM Exécuter le script Python de compilation
python build_exe.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Compilation terminée avec succès ===
    echo L'exécutable se trouve dans le dossier dist\
) else (
    echo.
    echo === ERREUR: La compilation a échoué ===
)

echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause > nul
