#!/bin/bash
cd App
nohup go run cmd/main.go > go_server.log 2>&1 &
cd ../bot
nohup python -m src.main > python_bot.log 2>&1 &
