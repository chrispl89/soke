# Skrypt uruchomieniowy dla SOKE
Set-Location $PSScriptRoot
& .\.venv\Scripts\Activate.ps1
streamlit run src/soke/app.py

