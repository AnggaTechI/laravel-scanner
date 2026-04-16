<h1 align="center">⚡ Laravel Scanner ⚡</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=00F7FF&center=true&vCenter=true&width=700&lines=Lightweight+Laravel+Audit+Tool;Fast+%7C+Concurrent+%7C+Clean+Workflow;Built+for+Authorized+Internal+Checks" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-1f6feb?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Laravel-ff2d20?style=for-the-badge&logo=laravel&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active-00c853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Purpose-Authorized%20Audit-6f42c1?style=for-the-badge" />
</p>

---

## ✨ About

A lightweight Python-based auditing utility for **authorized Laravel environment checks**.  
Designed for internal validation, deployment review, and controlled security assessment with a fast and simple workflow.

---

## 🚀 Highlights

- ⚡ Multi-target processing
- 🧵 Concurrent requests
- 🛡️ Request rate limiting
- 📝 Output logging
- 🔧 Easy configuration
- 🎯 Clean command-line workflow

---

## 📦 Requirements

- Python **3.10+**
- `requests`
- `PyMySQL`

---

## 🛠️ Installation

```bash
git clone https://github.com/AnggaTechI/laravel-scanner.git
cd laravel-scanner
pip install -r requirements.txt
```

---

## ▶️ Usage

1. Put your target list into `list.txt`
2. Run:

```bash
python laravel-scan.py
```

---

## ⚙️ Configuration

Edit the main script to adjust:

- `MAX_WORKERS`
- `MAX_REQUESTS_PER_SECOND`
- `REQUEST_TIMEOUT`
- `INPUT_FILE`

---

## 📁 Output

Results are saved into `.txt` log files for easier review and triage.

---

## ⚠️ Disclaimer

This project is intended **only for authorized testing and internal auditing**.  
Do not use it on systems you do not own or do not have explicit permission to assess.

---


