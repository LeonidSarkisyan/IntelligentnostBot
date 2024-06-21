@echo off
cd App
start cmd /c "go run cmd/main.go"
cd ..
cd bot
start cmd /c "python -m src.main"
