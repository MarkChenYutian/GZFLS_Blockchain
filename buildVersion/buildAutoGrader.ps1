Write-Output off
Write-Host "Converting AutoGrader to .pyc File ..."

Write-Host "Task 0 - Python 3.7 pyc File"
python -m compileall .\AutoGrader.py

Write-Host "Task 1 - Python 3.5 pyc File"
conda activate python35
python -m compileall .\AutoGrader.py
conda deactivate

Write-Host "Task 2 - Python 3.6 pyc File"
conda activate python36
python -m compileall .\AutoGrader.py
conda deactivate

Write-Host "Task 3 - Python 3.8 pyc File"
conda activate python38
python -m compileall .\AutoGrader.py
conda deactivate

Write-Host "Task 4 - Python 3.9 pyc File"
conda activate python39
python -m compileall .\AutoGrader.py
conda deactivate

Move-Item -Path .\__pycache__\AutoGrader.cpython-35.pyc -Destination .\AutoGrader.cpython-35.pyc
Move-Item -Path .\__pycache__\AutoGrader.cpython-36.pyc -Destination .\AutoGrader.cpython-36.pyc
Move-Item -Path .\__pycache__\AutoGrader.cpython-37.pyc -Destination .\AutoGrader.cpython-37.pyc
Move-Item -Path .\__pycache__\AutoGrader.cpython-38.pyc -Destination .\AutoGrader.cpython-38.pyc
Move-Item -Path .\__pycache__\AutoGrader.cpython-39.pyc -Destination .\AutoGrader.cpython-39.pyc