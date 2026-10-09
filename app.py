import os, json, uuid
from flask import Flask, request, redirect, session, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'justwearwigs-mega-v8-final-2026'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DATA_FILE = 'wigs_data.json'

CATEGORIES = ["Bone Straight", "Curly Hair", "Bob Wigs", "Blonde Wigs", "Braided Wigs", "Pixie Cuts", "Silky Straight", "Wig Accessories", "Sun Glasses", "Wig Bundles"]
DELIVERY = {
    "Dansoman - GHS 25": 25,
    "Accra Central - GHS 30": 30,
    "East Legon / Spintex - GHS 40": 40,
    "Tema / Kasoa - GHS 50": 50,
    "Kumasi / Takoradi - GHS 80": 80,
    "Other Regions - GHS 100": 100
}
DISCOUNT_CODES = {
    "CHRISTMAS15": {"percent": 15, "cat": "All", "desc": "Christmas 15% OFF"},
    "NEWYEAR30": {"percent": 30, "cat": "All", "desc": "New Year 30% OFF"},
    "PIXIE20": {"percent": 20, "cat": "Pixie Cuts", "desc": "Pixie 20% OFF"},
    "SILKY15": {"percent": 15, "cat": "Silky Straight", "desc": "Silky 15% OFF"},
    "ACCESS10": {"percent": 10, "cat": "Wig Accessories", "desc": "Accessories 10% OFF"},
    "SUNGLASS20": {"percent": 20, "cat": "Sun Glasses", "desc": "Sun Glasses 20% OFF"},
    "BUNDLE30": {"percent": 30, "cat": "Wig Bundles", "desc": "Bundles 30% OFF"},
    "QUEEN10": {"percent": 10, "cat": "All", "desc": "Queen 10% OFF"}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,'r') as f: return json.load(f)
        except: pass
    return {"wigs": [], "logo": ""}
def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f)

SHOP_TEMPLATE = """
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>JustWearWigs - Futuristic MEGA v8</title>
<style>
*{font-family:system-ui;box-sizing:border-box} body{margin:0;background:#0a0a0f;color:white;min-height:100vh}
.top{position:sticky;top:0;z-index:50;background:rgba(15,15,25,0.92);backdrop-filter:blur(20px);padding:12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;border-bottom:1px solid rgba(255,255,255,0.1)}
.note{background:rgba(255,193,7,0.15);border:1px solid #ffc107;color:#ffeb3b;padding:12px;text-align:center;font-weight:800;margin:12px;border-radius:14px;font-size:14px}
.cats{display:flex;gap:8px;overflow-x:auto;padding:10px 12px}.cat{padding:10px 18px;border-radius:22px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);color:white;white-space:nowrap;cursor:pointer;font-weight:600}
.cat.active{background:linear-gradient(90deg,#ec4899,#8b5cf6);border-color:transparent;box-shadow:0 4px 15px rgba(236,72,153,0.4)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;padding-bottom:160px}
@media(min-width:700px){.grid{grid-template-columns:repeat(3,1fr)}} @media(min-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:22px;overflow:hidden;transition:0.3s;cursor:pointer}
.card:hover{transform:translateY(-4px);box-shadow:0 10px 30px rgba(236,72,153,0.25);border-color:rgba(236,72,153,0.4)}
.card img{width:100%;height:210px;object-fit:cover}.card-body{padding:12px}
.price{color:#ff6ec7;font-weight:900;font-size:16px}.stock{font-size:11px;opacity:0.7}.low{color:#ff4444;font-weight:800}
.btn{width:100%;padding:12px;border-radius:14px;border:none;font-weight:800;margin-top:8px;cursor:pointer}.btn-pink{background:linear-gradient(90deg,#ec4899,#8b5cf6);color:white;box-shadow:0 4px 15px rgba(236,72,153,0.3)}
.btn-dark{background:rgba(255,255,255,0.1);color:white;border:1px solid rgba(255,255,255,0.15)}
.panel{margin:12px;background:rgba(255,255,255,0.05);padding:18px;border-radius:22px;border:1px solid rgba(255,255,255,0.1)}
input,select{padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.5);color:white;width:100%;margin:6px 0}
.dock{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:rgba(10,10,18,0.96);backdrop-filter:blur(20px);padding:12px 20px;border-radius:30px;display:flex;gap:14px;align-items:center;border:1px solid rgba(255,255,255,0.15);box-shadow:0 10px 40px rgba(0,0,0,0.5);z-index:100}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:200;align-items:center;justify-content:center;padding:20px}
.modal.show{display:flex}.modal-box{background:#161622;border:1px solid rgba(255,255,255,0.15);border-radius:26px;overflow:hidden;max-width:420px;width:100%}
.modal-box img{width:100%;height:350px;object-fit:cover}.modal-body{padding:18px}
.close{position:absolute;top:14px;right:14px;background:rgba(0,0,0,0.6);color:white;border:none;width:36px;height:36px;border-radius:50%;font-size:20px}
</style></head><body>
<div class=top>
<div style=font-weight:900;letter-spacing:1px>👑 JUSTWEARWIGS</div>
<input id=search placeholder="🔍 Search wigs, pixie, glasses..." onkeyup=doSearch() style=max-width:220px>
<a href="https://wa.me/233594204990" style=color:#25D366;text-decoration:none;font-weight:800>💬 0594204990</a>
<a href="https://instagram.com/just_wearwigs" style=color:#ff6ec7;text-decoration:none;font-weight:700>📸 @just_wearwigs</a>
<a href="https://tiktok.com/@justwearwigs" style=color:white;text-decoration:none>🎵 TikTok</a>
<a href="/admin" style=color:rgba(255,255,255,0.5);text-decoration:none;font-size:12px>Admin</a>
</div>

<div class=note>⚠️ NOTE: Delivery prices will depend on the motor rider 🏍️ — Rider will call you to confirm final price!</div>

<div class=cats>
<button class="cat active" onclick=filterCat('All',this)>All Wigs</button>
{% for c in cats %}<button class=cat onclick=filterCat('{{c}}',this)>{{c}}</button>{% endfor %}
</div>

<div class=grid id=grid>
{% for w in wigs %}
<div class=card data-name="{{w.name|lower}} {{w.category|lower}}" data-cat="{{w.category}}" onclick="openView('{{w.id}}','{{w.name}}','{{w.category}}',{{w.price}},{{w.stock}},'/{{w.image}}')">
<img src="/{{w.image}}" loading=lazy>
<div class=card-body>
<div style=font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis>{{w.name}}</div>
<div class=stock>{{w.category}} • Stock: {{w.stock}} {% if w.stock<=1 %}<span class=low>⚠️ Only {{w.stock}} left!</span>{% endif %}</div>
<div class=price>GHS {{w.price}}</div>
<button class=btn btn-pink onclick="event.stopPropagation(); addCart('{{w.id}}','{{w.name}}',{{w.price}})">🛒 Add to Order</button>
</div></div>
{% endfor %}
</div>
{% if not wigs %}<div style=text-align:center;padding:60px 20px;opacity:0.7><h2>👑 Welcome to MEGA Shop!</h2><p>10 Categories ready:<br>Pixie Cuts, Silky Straight, Wig Accessories, Sun Glasses, Wig Bundles + 5<br><br>Go to <a href="/admin" style=color:#ec4899>/admin</a> to upload from gallery!</p></div>{% endif %}

<div id=viewModal class=modal onclick="if(event.target==this)closeView()"><button class=close onclick=closeView()>×</button><div class=modal-box><img id=mImg><div class=modal-body><h3 id=mName style=margin:0></h3><small id=mCat style=opacity:0.6></small><div style=margin:10px 0><span id=mPrice style=color:#ff6ec7;font-weight:900;font-size:20px></span> <span id=mStock style=opacity:0.7></span></div><p style=font-size:13px;opacity:0.8>✨ View well before you buy — High quality, 100% human hair / premium accessories. Delivery: NOTE: Delivery prices will depend on the motor rider.</p><button class=btn btn-pink id=mAdd>🛒 Add to Order</button><button class=btn btn-dark onclick=closeView()>Close</button></div></div></div>

<div class=panel id=cartPanel>
<h3>🛒 Your Cart — Change Wig / Cancel / Quantity</h3>
<div id=cartList style=margin:10px 0>Empty — Add wigs to order</div>
<h4>🎁 Discount Code (15-30% OFF)</h4>
<div style=display:flex;gap:8px><input id=code placeholder="Try CHRISTMAS15, NEWYEAR30, PIXIE20, BUNDLE30, QUEEN10"><button class=btn btn-pink style=width:110px;margin:0 onclick=applyCode()>Apply</button></div>
<div id=codeMsg style=margin:8px 0;font-weight:700;color:#ff6ec7></div>
<div style=margin:12px 0;padding:12px;background:rgba(255,193,7,0.12);border-radius:12px;border:1px solid rgba(255,193,7,0.3);font-size:13px>⚠️ <b>NOTE: Delivery prices will depend on the motor rider</b> — Prices below are estimates. Rider will confirm!</div>
<label>📍 Delivery Location</label>
<select id=deliverySel onchange=calcTotal()>{% for label,fee in delivery.items() %}<option value={{fee}}>{{label}}</option>{% endfor %}</select>
<div style=margin:14px 0;line-height:1.9;background:rgba(0,0,0,0.3);padding:14px;border-radius:14px>
Items: GHS <span id=iTotal>0</span><br>
Discount: -GHS <span id=discAmt>0</span> <small id=discLabel></small><br>
Delivery: GHS <span id=dFee>25</span> <small style=opacity:0.6>(NOTE: depends on rider)</small><br>
<b style=font-size:18px;color:#ff6ec7>Total: GHS <span id=gTotal>0</span></b>
</div>
<button class=btn btn-pink onclick=checkoutWA()>✅ Checkout via WhatsApp 0594204990</button>
<button class=btn btn-dark onclick=clearCart()>❌ Cancel All Orders</button>
<p style=font-size:12px;opacity:0.6;text-align:center;margin-top:10px>MoMo Pay: 0594204990 • Capital Hills, Tue-Sat • NOTE: Delivery prices will depend on the motor rider — 4th place notice!</p>
</div>

<div class=dock><div>🛒 <span id=fCount>0</span> items</div><div style=color:#ff6ec7;font-weight:800>GHS <span id=fTotal>0</span></div><button onclick="document.getElementById('cartPanel').scrollIntoView({behavior:'smooth'})" style=background:linear-gradient(90deg,#ec4899,#8b5cf6);border:none;color:white;padding:9px 16px;border-radius:20px;font-weight:700">View Cart</button></div>

<script>
let wigsData = { {% for w in wigs %}"{{w.id}}": {"name":"{{w.name}}","cat":"{{w.category}}","price":{{w.price}},"stock":{{w.stock}},"img":"/{{w.image}}"}, {% endfor %} };
let cart=JSON.parse(localStorage.getItem('jww_cart_v8')||'[]');
let disc=JSON.parse(localStorage.getItem('jww_disc_v8')||'null'); let discPct=disc?disc.percent:0;
let currentView=null;
function openView(id,name,cat,price,stock,img){currentView={id,name,price}; document.getElementById('mImg').src=img; document.getElementById('mName').innerText=name; document.getElementById('mCat').innerText=cat+' • Stock '+stock; document.getElementById('mPrice').innerText='GHS '+price; document.getElementById('mStock').innerText=stock<=1?'⚠️ Only '+stock+' left!':''; document.getElementById('mAdd').onclick=()=>{addCart(id,name,price); closeView();}; document.getElementById('viewModal').classList.add('show');}
function closeView(){document.getElementById('viewModal').classList.remove('show');}
function addCart(id,name,price){let ex=cart.find(c=>c.id==id); if(ex){ex.qty+=1}else{cart.push({id,name,price,qty:1});} saveCart();}
function saveCart(){localStorage.setItem('jww_cart_v8',JSON.stringify(cart)); renderCart();}
function renderCart(){let list=document.getElementById('cartList'); if(cart.length==0){list.innerHTML='Cart empty — Add wigs from above!'; calcTotal(); return;} let html=''; cart.forEach((c,i)=>{html+=`<div style=display:flex;justify-content:space-between;align-items:center;padding:10px;background:rgba(255,255,255,0.06);border-radius:12px;margin:6px 0><div><b>${c.name}</b><br><small>GHS ${c.price} x ${c.qty} = GHS ${c.price*c.qty}</small> <button onclick="changeQty(${i},1)" style=margin-left:8px>+</button> <button onclick="changeQty(${i},-1)">-</button> <button onclick="changeWig(${i})" style=font-size:11px>🔄 Change Wig</button></div><button onclick="removeItem(${i})" style=background:#ff4444;border:none;color:white;padding:6px 10px;border-radius:8px">❌ Cancel</button></div>`;}); list.innerHTML=html; calcTotal();}
function changeQty(i,d){cart[i].qty+=d; if(cart[i].qty<=0)cart.splice(i,1); saveCart();}
function changeWig(i){let newId=prompt('Enter new wig name to change? Or cancel to pick from shop:'); if(!newId){document.getElementById('grid').scrollIntoView({behavior:'smooth'}); alert('Select new wig from shop to replace'); cart.splice(i,1); saveCart(); return;}}
function removeItem(i){cart.splice(i,1); saveCart();}
function clearCart(){if(confirm('Cancel all orders?')){cart=[]; saveCart();}}
function calcTotal(){let dFee=parseInt(document.getElementById('deliverySel').value||25); document.getElementById('dFee').innerText=dFee; let items=cart.reduce((s,c)=>s+c.price*c.qty,0); let discAmt=Math.round(items*discPct/100); let grand=items-discAmt+dFee; if(grand<0)grand=dFee; document.getElementById('iTotal').innerText=items; document.getElementById('discAmt').innerText=discAmt; document.getElementById('discLabel').innerText=disc?`(${disc.desc})`:''; document.getElementById('gTotal').innerText=grand; document.getElementById('fCount').innerText=cart.reduce((s,c)=>s+c.qty,0); document.getElementById('fTotal').innerText=grand;}
function doSearch(){let q=document.getElementById('search').value.toLowerCase(); document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'':'none';});}
function filterCat(cat,el){document.querySelectorAll('.cat').forEach(b=>b.classList.remove('active')); if(el)el.classList.add('active'); document.querySelectorAll('.card').forEach(c=>{c.style.display=(cat=='All'||c.dataset.cat==cat)?'':'none';});}
function applyCode(){let code=document.getElementById('code').value.toUpperCase().trim(); if(!code){return;} fetch('/apply-discount?code='+code).then(r=>r.json()).then(d=>{if(d.valid){disc=d; discPct=d.percent; localStorage.setItem('jww_disc_v8',JSON.stringify(d)); document.getElementById('codeMsg').innerText='✅ '+d.desc+' — '+d.percent+'% OFF Applied!'; calcTotal();} else {document.getElementById('codeMsg').innerText='❌ Invalid code. Try CHRISTMAS15, NEWYEAR30, QUEEN10, PIXIE20, BUNDLE30';}});}
function checkoutWA(){if(cart.length==0){alert('Cart empty! Add wigs first'); return;} let dSel=document.getElementById('deliverySel'); let dLabel=dSel.options[dSel.selectedIndex].text; let items=cart.map(c=>`${c.name} x${c.qty} = GHS ${c.price*c.qty}`).join('%0A'); let tot=document.getElementById('gTotal').innerText; let discInfo=disc?`Discount: ${disc.desc} -GHS ${document.getElementById('discAmt').innerText}%0A`:''; let msg=`👑 JustWearWigs MEGA ORDER%0A%0A${items}%0A%0A${discInfo}Delivery: ${dLabel}%0ANOTE: Delivery prices will depend on the motor rider%0A%0ATotal: GHS ${tot}%0A%0APay MoMo: 0594204990%0AFrom: Website`; window.open('https://wa.me/233594204990?text='+msg,'_blank');}
renderCart(); calcTotal();
</script>
</body></html>
"""

ADMIN_TEMPLATE = """
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font-family:system-ui;padding:15px;background:#0a0a0f;color:white} input,select{padding:12px;width:100%;max-width:420px;margin:6px 0;border-radius:12px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.5);color:white} button{padding:12px 18px;border-radius:12px;background:linear-gradient(90deg,#ec4899,#8b5cf6);color:white;border:none;font-weight:800;cursor:pointer}.card{background:rgba(255,255,255,0.06);padding
