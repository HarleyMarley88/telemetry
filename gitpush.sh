#!/bin/bash

echo "Введите сообщение коммита:"
read COMMIT_MSG

git add .

git commit -m "$COMMIT_MSG"

git push origin main

echo "Готово!"
