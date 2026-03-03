# تطبيق Flask أساسي

ملفات مضافة/معدلة:

- `taqweed.py` — تطبيق Flask بسيط مع مسار الجذر.
- `templates/main.html` — قالب HTML بسيط.
- `requirements.txt` — يعتمد على `Flask`.

تشغيل محلي (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# خيار 1: تشغيل مباشرة
python taqweed.py
# خيار 2: باستخدام flask CLI
$env:FLASK_APP = "taqweed.py"
flask run --host=0.0.0.0
```

المشروع يستخدم مجلد `templates/` و`static/` الموجودين في جذر المشروع.
