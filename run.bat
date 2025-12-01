@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ===============================================================================
echo    NETWORK INTRUSION DETECTION - SPARK BIG DATA
echo ===============================================================================
echo.

REM Kiểm tra Python 3.11 virtual environment
if not exist "venv311\Scripts\python.exe" (
    echo [ERROR] Virtual environment Python 3.11 chưa được cài đặt!
    echo Vui lòng chạy setup_python311.bat trước
    pause
    exit /b 1
)

echo [INFO] Sử dụng Python 3.11: venv311\Scripts\python.exe
echo [INFO] Kiểm tra thư viện...

REM Kiểm tra và cài đặt PySpark
venv311\Scripts\python.exe -c "import pyspark" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Đang cài đặt PySpark và PyArrow...
    venv311\Scripts\pip.exe install pyspark "pyarrow>=11.0.0" -q
) else (
    REM Kiểm tra PyArrow version
    venv311\Scripts\python.exe -c "import pyarrow; assert int(pyarrow.__version__.split('.')[0]) >= 11" >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Nâng cấp PyArrow lên phiên bản 11+...
        venv311\Scripts\pip.exe install "pyarrow>=11.0.0" --upgrade -q
    )
)

REM Kiểm tra và cài đặt XGBoost
venv311\Scripts\python.exe -c "import xgboost" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Đang cài đặt XGBoost...
    venv311\Scripts\pip.exe install xgboost -q
)

REM Kiểm tra file dữ liệu
if not exist "KDDTrain+.txt" (
    echo [ERROR] Không tìm thấy file KDDTrain+.txt
    pause
    exit /b 1
)

if not exist "KDDTest+.txt" (
    echo [ERROR] Không tìm thấy file KDDTest+.txt
    pause
    exit /b 1
)

echo.
echo [INFO] Bắt đầu train models...
echo ===============================================================================
echo.

echo [MODE] Train và lưu models
venv311\Scripts\python.exe spark_intrusion_detection.py --save-models

REM Tự động tạo dashboard sau khi train xong
if not errorlevel 1 (
    echo.
    echo [INFO] Đang tạo dashboard...
    venv311\Scripts\python.exe generate_dashboard_data.py >nul 2>&1
    if not errorlevel 1 (
        echo ✓ Dashboard đã sẵn sàng
        timeout /t 2 /nobreak >nul
        start dashboard.html >nul 2>&1
        echo ✓ Đã mở dashboard
    )
)

:end
echo.
echo ===============================================================================
echo [INFO] Hoàn tất!
echo ===============================================================================
pause
