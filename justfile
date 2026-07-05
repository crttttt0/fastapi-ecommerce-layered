set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    just --list

run:
    uv run uvicorn app.main:app --reload
