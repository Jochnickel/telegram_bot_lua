cd "$(dirname "$0")"
printf "git: " && git pull
python3 main.py
