@echo off
:: Step 1: Display a message
echo =====================================
echo Starting the compilation process with cx_Freeze...
echo =====================================

:: Step 2: Run cx_Freeze to compile the script
echo Compiling the Python script into an executable...

:: Clean up previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Execute cx_Freeze setup script
python setup.py build

if %errorlevel% neq 0 (
    echo =====================================
    echo ERROR: Failed to compile the script.
    echo Ensure cx_Freeze is installed and working.
    echo =====================================
    pause
    exit /b 1
)

:: Step 3: Move the executable to the dist folder
move build\exe.* dist

:: Step 4: Display success message
echo =====================================
echo Compilation completed successfully!
echo The executable is located in the "dist" folder.
echo =====================================
pause
