import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>👑 JustWearWigs is LIVE!</h1><p>Going to /admin soon... <a href='/admin'>Admin</a></p><p>WhatsApp: 0594204990 | IG: @just_wearwigs</p>"

@app.route('/admin')
def admin():
    return "<h1>ADMIN LIVE ✅</h1><p>Shop is working! Now we can add MEGA code.</p><a href='/'>← Shop</a>"

if __name__ == '__main__':
    app.run()
