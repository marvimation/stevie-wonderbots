#!/usr/bin/env python3
import psutil
import subprocess
import time
import os
import pyautogui
import re
from datetime import datetime

LOG_FILE = "/home/snap/Desktop/z_turtle_ai.log"
CHAT_PATTERNS = {
    'grok': ['grok', 'x.com', 'x\.com'],
    'openai': ['chat.openai.com', 'chatgpt'],
    'gemini': ['gemini.google.com']
}

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {msg}\n"
    print(f"[z_monitor] {msg}")
    with open(LOG_FILE, 'a') as f:
        f.write(line)

def is_relevant(cmd):
    if not cmd or len(cmd) < 2: return False
    cmd_str = ' '.join(cmd).lower()
    # Block list
    block = ['nano', 'sudo nano', 'cd ', 'clear', 'exit', 'vim', 'vi', 'mc', 'htop']
    if any(b in cmd_str for b in block): return False
    # Allow list
    allow = ['python', 'ls', 'cat', 'head', 'tail', 'tree', 'git', 'pytest', 'df', 'du', 'ps', 'wc', 'grep', 'find', 'echo']
    return any(a in cmd_str for a in allow)

def run_capture(cmd_list):
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=25)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

def summarize(text):
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) <= 20:
        return text.strip()
    return (
        f"OUTPUT SUMMARY ({len(lines)} lines):\n" +
        "\n".join(lines[:8]) + "\n" +
        f"... [{len(lines)-16} skipped] ...\n" +
        "\n".join(lines[-8:]) + "\n" +
        "END SUMMARY"
    )

def get_chat_window():
    try:
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            parts = line.split(None, 3)
            if len(parts) > 3:
                win_id = parts[0]
                title = parts[3].lower()
                for llm, patterns in CHAT_PATTERNS.items():
                    if any(p in title for p in patterns):
                        return llm, win_id
        return 'unknown', None
    except Exception as e:
        log(f"wmctrl error: {e}")
        return 'unknown', None

def inject(text, llm, win_id):
    if llm == 'unknown':
        log("No LLM window detected")
        return
    log(f"Injecting {len(text)} chars to {llm}")
    if win_id:
        subprocess.run(['wmctrl', '-i', '-a', win_id], timeout=5)
    time.sleep(1.5)
    pyautogui.write(text)
    pyautogui.press('enter')
    log(f"Injected to {llm}")

log("z_terminal_monitor STARTED - FINAL GOD MODE v2")

active = {}

while True:
    try:
        for term in psutil.process_iter(['pid', 'name']):
            if term.info['name'] not in ['bash', 'zsh']:
                continue
            try:
                children = term.children(recursive=True)
            except:
                continue

            for child in children:
                try:
                    cpid = child.pid
                    ccmd = child.cmdline()
                    if not ccmd or len(ccmd) < 2:
                        continue
                    if not is_relevant(ccmd):
                        continue

                    # Strip sudo
                    real_cmd = ccmd[1:] if ccmd[0].endswith('sudo') else ccmd
                    cmd_key = ' '.join(real_cmd)

                    if cpid not in active:
                        log(f"DETECTED: {cmd_key}")
                        active[cpid] = (real_cmd, cmd_key)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        # Check finished
        done = []
        for cpid, (real_cmd, cmd_key) in active.items():
            if not psutil.pid_exists(cpid):
                log(f"FINISHED: {cmd_key}")
                output = run_capture(real_cmd)
                if output.strip():
                    summary = summarize(output)
                    llm, win = get_chat_window()
                    inject(summary, llm, win)
                else:
                    log("No output")
                done.append(cpid)

        for pid in done:
            del active[pid]

        time.sleep(1.3)
    except Exception as e:
        log(f"ERROR: {e}")
        time.sleep(2)
