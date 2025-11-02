from flask import Flask, request, jsonify, render_template, g
import sqlite3, os, requests, time, threading
from datetime import datetime, timedelta

DB_PATH = "cuutoi.db"
app = Flask(__name__)

# ============================================================
# Database helpers
# ============================================================
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        note TEXT,
        phone TEXT,
        name TEXT,
        address TEXT,
        type TEXT DEFAULT 'help',
        last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    db = get_db()
    db.executescript(schema)
    db.commit()
    print("✅ Database ready.")

# ============================================================
# Cleanup background task
# ============================================================
def cleanup_expired_data():
    """Chạy nền: xóa donor_inactive >7 ngày, ngắt kết nối >3h"""
    while True:
        try:
            db = sqlite3.connect(DB_PATH)
            db.row_factory = sqlite3.Row

            # Nếu bảng chưa tạo thì bỏ qua vòng này
            try:
                db.execute("SELECT 1 FROM points LIMIT 1;")
            except sqlite3.OperationalError:
                print("⚠️ [Cleanup] Bảng chưa có, bỏ qua vòng này.")
                db.close()
                time.sleep(60)
                continue

            # Ngắt chia sẻ nếu offline >3h
            db.execute("""
                UPDATE points
                SET type='donor_inactive'
                WHERE type='donor' AND last_update < datetime('now', '-3 hours')
            """)

            # Xóa dữ liệu donor_inactive >7 ngày
            db.execute("""
                DELETE FROM points
                WHERE type='donor_inactive' AND last_update < datetime('now', '-7 days')
            """)

            db.commit()
            db.close()
            print(f"🧹 Cleanup done at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print("⚠️ [Cleanup error]", e)
        time.sleep(3600)  # chạy lại mỗi 1h

# ============================================================
# Routes
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/points", methods=["GET"])
def get_points():
    db = get_db()
    rows = db.execute("""
        SELECT id, lat, lon, note, phone, name, address, type, last_update
        FROM points
        WHERE type IN ('help','donor','donor_inactive')
        ORDER BY created_at DESC
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/points", methods=["POST"])
def add_point():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    note = data.get("note", "")
    phone = data.get("phone", "")
    name = data.get("name", "")
    address = data.get("address", "")
    type_ = data.get("type", "help")

    # Reverse geocode nếu chưa có địa chỉ
    if not address:
        try:
            res = requests.get(
                f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}",
                headers={"User-Agent": "CuuMapMini/1.0"},
                timeout=8,
            )
            address = res.json().get("display_name", "")
        except Exception:
            address = ""

    db = get_db()
    db.execute("""
        INSERT INTO points (lat, lon, note, phone, name, address, type, last_update)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (lat, lon, note, phone, name, address, type_))
    db.commit()
    return jsonify({"ok": True})

@app.route("/api/live_update", methods=["POST"])
def live_update():
    data = request.get_json()
    phone = data.get("phone")
    lat = data.get("lat")
    lon = data.get("lon")
    if not phone or not lat or not lon:
        return jsonify({"error": "missing phone or coordinates"}), 400
    db = get_db()
    db.execute("""
        UPDATE points
        SET lat=?, lon=?, last_update=datetime('now')
        WHERE phone=? AND type='donor'
    """, (lat, lon, phone))
    db.commit()
    return jsonify({"ok": True})

@app.route("/api/live_donors", methods=["GET"])
def live_donors():
    db = get_db()
    rows = db.execute("""
        SELECT name, phone, lat, lon, note, address, last_update
        FROM points
        WHERE type='donor' AND last_update >= datetime('now', '-3 hours')
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/stop_live", methods=["POST"])
def stop_live():
    data = request.get_json()
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "missing phone"}), 400
    db = get_db()
    db.execute("""
        UPDATE points
        SET type='donor_inactive', last_update=datetime('now')
        WHERE phone=? AND type='donor'
    """, (phone,))
    db.commit()
    return jsonify({"ok": True, "msg": "stopped_sharing"})

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    # 🔹 1. Tạo DB nếu chưa có
    if not os.path.exists(DB_PATH):
        with app.app_context():
            init_db()

    # 🔹 2. Chạy cleanup thread chỉ 1 lần thật
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=cleanup_expired_data, daemon=True).start()
        print("🧹 Cleanup thread started safely.")

    # 🔹 3. Run Flask
    app.run(host="0.0.0.0", port=8000, debug=True)
