import os, json, uuid, datetime
from flask import Flask, request, redirect, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DATA_FILE = 'wigs_data.json'
ORDERS_FILE = 'orders_data.json'

CATEGORIES = ["Bone Straight", "Curly Hair", "Bob Wigs", "Blonde Wigs", "Braided Wigs", "Pixie Cuts", "Silky Straight", "Wig Accessories", "Sun Glasses", "Wig Bundles"]
DELIVERY = {"Dansoman - GHS 25":25,"Accra Central - GHS 30":30,"East Legon / Spintex - GHS 40":40,"Tema / Kasoa - GHS 50":50,"Kumasi / Takoradi - GHS 80":80,"Other Regions - GHS 100":100}
DISCOUNT_CODES = {"CHRISTMAS15":{"percent":15,"cat":"All","desc":"Christmas 15% OFF"},"NEWYEAR30":{"percent":30,"cat":"All","desc":"New Year 30% OFF"},"PIXIE20":{"percent":20,"cat":"Pixie Cuts","desc":"Pixie 20% OFF"},"SILKY15":{"percent":15,"cat":"Silky Straight","desc":"Silky 15% OFF"},"ACCESS10":{"percent":10,"cat":"Wig Accessories","desc":"Access 10% OFF"},"SUNGLASS20":{"percent":20,"cat":"Sun Glasses","desc":"Sun Glass 20% OFF"},"BUNDLE30":{"percent":30,"cat":"Wig Bundles","desc":"Bundle 30% OFF"},"QUEEN10":{"percent":10,"cat":"All","desc":"Queen 10% OFF"}}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,'r') as f: return json.load(f)
        except: pass
    return {"wigs":[],"logo":""}
def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f)
def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE,'r') as f: return json.load(f)
        except: pass
    return []
def save_orders(o):
    with open(ORDERS_FILE,'w') as f: json.dump(o,f)

SHOP_TEMPLATE = """
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>JustWearWigs v8.2 Orders</title>
<style>
*{font-family:system-ui;box-sizing:border-box} body{margin:0;background:#0a0a0f;color:white}
.top{position:sticky;top:0;z-index:50;background:rgba(15,15,25,0.92);backdrop-filter:blur(20px);padding:12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;border-bottom:1px solid rgba(255,255,255,0.1)}
.note{background:rgba(255,193,7,0.15);border:1px solid #ffc107;color:#ffeb3b;padding:12px;text-align:center;font-weight:800;margin:12px;border-radius:14px;font-size:14px}
.cats{display:flex;gap:8px;overflow-x:auto;padding:10px 12px}.cat{padding:10px 18px;border-radius:22px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);color:white;white-space:nowrap;cursor:pointer;font-weight:600}.cat.active{background:linear-gradient(90deg,#ec4899,#8b5cf6)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;padding-bottom:160px}.card{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:22px;overflow:hidden;cursor:pointer}.card img{width:100%;height:210px;object-fit:cover}.card-body{padding:12px}.price{color:#ff6ec7;font-weight:900}.low{color:#ff4444;font-weight:800;font-size:11px}.btn{width:100%;padding:12px;border-radius:14px;border:none;font-weight:800;margin-top:8px;cursor:pointer}.btn-pink{background:linear-gradient(90deg,#ec4899,#8b5cf6);color:white}.btn-dark{background:rgba(255,255,255,0.1);color:white;border:1px solid rgba(255,255,255,0.15)}
.panel{margin:12px;background:rgba(255,255,255,0.05);padding:18px;border-radius:22px;border:1px solid rgba(255,255,255,0.1)} input,select{padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.5);color:white;width:100%;margin:6px 0}
.dock{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:rgba(10,10,18,0.96);backdrop-filter:blur(20px);padding:12px 20px;border-radius:30px;display:flex;gap:14px;align-items:center;border:1px solid rgba(255,255,255,0.15);z-index:100}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:200;align-items:center;justify-content:center;padding:20px}.modal.show{display:flex}.modal-box{background:#161622;border:1px solid rgba(255,255,255,0.15);border-radius:26px;overflow:hidden;max-width:420px;width:100%}.modal-box img{width:100%;height:350px;object-fit:cover}.modal-body{padding:18px}.close{position:absolute;top:14px;right:14px;background:rgba(0,0,0,0.6);color:white;border:none;width:36px;height:36px;border-radius:50%;font-size:20px}
</style></head><body>
<div class=top>
{% if logo %}<img src="/{{logo}}" style=height:42px;width:42px;object-fit:cover;border-radius:12px;border:2px solid #ec4899>{% else %}<div style=font-size:26px>👑</div>{% endif %}
<div style=font-weight:900>JUSTWEARWIGS</div>
<input id=search placeholder="🔍 Search..." onkeyup=doSearch() style=max-width:180px>
<a href="https://wa.me/233594204990" style=color:#25D366;text-decoration:none;font-weight:800>💬 0594204990</a>
<a href="/admin" style=color:rgba(255,255,255,0.4);text-decoration:none;font-size:11px>Admin</a>
</div>
<div class=note>⚠️ NOTE: Delivery prices will depend on the motor rider 🏍️</div>
<div class=cats><button class="cat active" onclick=filterCat('All',this)>All</button>{% for c in cats %}<button class=cat onclick=filterCat('{{c}}',this)>{{c}}</button>{% endfor %}</div>
<div class=grid id=grid>{% for w in wigs %}
<div class=card data-name="{{w.name|lower}} {{w.category|lower}}" data-cat="{{w.category}}" onclick="openView('{{w.id}}','{{w.name}}','{{w.category}}',{{w.price}},{{w.stock}},'/{{w.image}}')">
<img src="/{{w.image}}"><div class=card-body><div style=font-size:13px;font-weight:700>{{w.name}}</div><div style=font-size:11px;opacity:0.7>{{w.category}} • Stock: {{w.stock}} {% if w.stock<=1 %}<span class=low>⚠️ Only {{w.stock}} left!</span>{% endif %}</div><div class=price>GHS {{w.price}}</div><button class=btn btn-pink onclick="event.stopPropagation(); addCart('{{w.id}}','{{w.name}}',{{w.price}})">🛒 Add to Order</button></div></div>{% endfor %}</div>

<div id=viewModal class=modal onclick="if(event.target==this)closeView()"><button class=close onclick=closeView()>×</button><div class=modal-box><img id=mImg><div class=modal-body><h3 id=mName style=margin:0></h3><small id=mCat style=opacity:0.6></small><div style=margin:10px 0><span id=mPrice style=color:#ff6ec7;font-weight:900;font-size:20px></span> <span id=mStock style=opacity:0.7></span></div><p style=font-size:13px;opacity:0.8>View well before you buy — Premium quality. NOTE: Delivery prices depend on motor rider.</p><button class=btn btn-pink id=mAdd>🛒 Add to Order</button><button class=btn btn-dark onclick=closeView()>Close</button></div></div></div>

<div class=panel id=cartPanel>
<h3>🛒 Your Order — Confirm & Checkout</h3>
<div id=cartList>Empty</div>
<h4>👤 Your Details (For Order Confirmation)</h4>
<input id=custName placeholder="Your Full Name *required">
<input id=custPhone placeholder="Your WhatsApp Number *required e.g., 0594204990">
<input id=custLoc placeholder="Your Location e.g., Dansoman">
<h4>🎁 Discount Code</h4>
<div style=display:flex;gap:8px><input id=code placeholder="CHRISTMAS15, NEWYEAR30, PIXIE20, QUEEN10"><button class=btn btn-pink style=width:110px;margin:0 onclick=applyCode()>Apply</button></div>
<div id=codeMsg style=margin:8px 0;font-weight:700;color:#ff6ec7></div>
<div style=margin:12px 0;padding:12px;background:rgba(255,193,7,0.12);border-radius:12px;border:1px solid rgba(255,193,7,0.3);font-size:13px>⚠️ NOTE: Delivery prices will depend on the motor rider</div>
<label>📍 Delivery Location</label>
<select id=deliverySel onchange=calcTotal()>{% for label,fee in delivery.items() %}<option value={{fee}}>{{label}}</option>{% endfor %}</select>
<div style=margin:14px 0;line-height:1.9;background:rgba(0,0,0,0.3);padding:14px;border-radius:14px>
Items: GHS <span id=iTotal>0</span><br>Discount: -GHS <span id=discAmt>0</span> <small id=discLabel></small><br>Delivery: GHS <span id=dFee>25</span><br><b style=color:#ff6ec7;font-size:18px>Total: GHS <span id=gTotal>0</span></b>
</div>
<button class=btn btn-pink onclick=checkoutWA()>✅ Confirm Order — We Will Notify You!</button>
<button class=btn btn-dark onclick=clearCart()>❌ Cancel All</button>
<p style=font-size:12px;opacity:0.6;text-align:center>MoMo: 0594204990 • NOTE: Delivery prices depend on motor rider</p>
</div>
<div class=dock><div>🛒 <span id=fCount>0</span> items</div><div style=color:#ff6ec7;font-weight:800>GHS <span id=fTotal>0</span></div><button onclick="document.getElementById('cartPanel').scrollIntoView({behavior:'smooth'})" style=background:linear-gradient(90deg,#ec4899,#8b5cf6);border:none;color:white;padding:9px 16px;border-radius:20px;font-weight:700">View Cart</button></div>
<script>
let cart=JSON.parse(localStorage.getItem('jww_cart_v82')||'[]');
let disc=JSON.parse(localStorage.getItem('jww_disc_v82')||'null'); let discPct=disc?disc.percent:0;
function openView(id,name,cat,price,stock,img){document.getElementById('mImg').src=img; document.getElementById('mName').innerText=name; document.getElementById('mCat').innerText=cat+' • Stock '+stock; document.getElementById('mPrice').innerText='GHS '+price; document.getElementById('mStock').innerText=stock<=1?'⚠️ Only '+stock+' left!':''; document.getElementById('mAdd').onclick=()=>{addCart(id,name,price); closeView();}; document.getElementById('viewModal').classList.add('show');}
function closeView(){document.getElementById('viewModal').classList.remove('show');}
function addCart(id,name,price){let ex=cart.find(c=>c.id==id); if(ex){ex.qty+=1}else{cart.push({id,name,price,qty:1});} saveCart();}
function saveCart(){localStorage.setItem('jww_cart_v82',JSON.stringify(cart)); renderCart();}
function renderCart(){let list=document.getElementById('cartList'); if(cart.length==0){list.innerHTML='Cart empty'; calcTotal(); return;} let html=''; cart.forEach((c,i)=>{html+=`<div style=display:flex;justify-content:space-between;align-items:center;padding:10px;background:rgba(255,255,255,0.06);border-radius:12px;margin:6px 0><div><b>${c.name}</b><br><small>GHS ${c.price} x ${c.qty} = GHS ${c.price*c.qty}</small> <button onclick="changeQty(${i},1)">+</button> <button onclick="changeQty(${i},-1)">-</button></div><button onclick="removeItem(${i})" style=background:#ff4444;border:none;color:white;padding:6px 10px;border-radius:8px">❌ Cancel</button></div>`;}); list.innerHTML=html; calcTotal();}
function changeQty(i,d){cart[i].qty+=d; if(cart[i].qty<=0)cart.splice(i,1); saveCart();}
function removeItem(i){cart.splice(i,1); saveCart();}
function clearCart(){if(confirm('Cancel all?')){cart=[]; saveCart();}}
function calcTotal(){let dFee=parseInt(document.getElementById('deliverySel').value||25); document.getElementById('dFee').innerText=dFee; let items=cart.reduce((s,c)=>s+c.price*c.qty,0); let discAmt=Math.round(items*discPct/100); let grand=items-discAmt+dFee; if(grand<0)grand=dFee; document.getElementById('iTotal').innerText=items; document.getElementById('discAmt').innerText=discAmt; document.getElementById('discLabel').innerText=disc?`(${disc.desc})`:''; document.getElementById('gTotal').innerText=grand; document.getElementById('fCount').innerText=cart.reduce((s,c)=>s+c.qty,0); document.getElementById('fTotal').innerText=grand;}
function doSearch(){let q=document.getElementById('search').value.toLowerCase(); document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'':'none';});}
function filterCat(cat,el){document.querySelectorAll('.cat').forEach(b=>b.classList.remove('active')); if(el)el.classList.add('active'); document.querySelectorAll('.card').forEach(c=>{c.style.display=(cat=='All'||c.dataset.cat==cat)?'':'none';});}
function applyCode(){let code=document.getElementById('code').value.toUpperCase().trim(); fetch('/apply-discount?code='+code).then(r=>r.json()).then(d=>{if(d.valid){disc=d; discPct=d.percent; localStorage.setItem('jww_disc_v82',JSON.stringify(d)); document.getElementById('codeMsg').innerText='✅ '+d.desc+' '+d.percent+'% OFF'; calcTotal();} else {document.getElementById('codeMsg').innerText='❌ Invalid. Try CHRISTMAS15, NEWYEAR30, QUEEN10';}});}
function checkoutWA(){
 if(cart.length==0){alert('Cart empty'); return;}
 let name=document.getElementById('custName').value.trim(); let phone=document.getElementById('custPhone').value.trim();
 if(!name||!phone){alert('Please enter your Name and WhatsApp Number — needed to confirm your order!'); return;}
 let dSel=document.getElementById('deliverySel'); let dLabel=dSel.options[dSel.selectedIndex].text;
 let payload={customer_name:name,customer_phone:phone,customer_loc:document.getElementById('custLoc').value,delivery_label:dLabel,delivery_fee:parseInt(dSel.value),items:cart,total:document.getElementById('gTotal').innerText,discount:disc?disc.desc:'None'};
 fetch('/create-order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
   let items=cart.map(c=>`${c.name} x${c.qty} = GHS ${c.price*c.qty}`).join('%0A');
   let msg=`👑 NEW ORDER #${res.order_id} %0AName: ${name}%0APhone: ${phone}%0ALoc: ${payload.customer_loc}%0A%0A${items}%0A%0ADelivery: ${dLabel}%0ATotal: GHS ${payload.total}%0A%0A✅ Order saved! Check /admin to confirm packaging!`;
   window.open('https://wa.me/233594204990?text='+msg,'_blank');
   alert('✅ Order #'+res.order_id+' Received! We will WhatsApp you for confirmation & packaging!');
   cart=[]; saveCart();
 });
}
renderCart(); calcTotal();
</script></body></html>
"""

ADMIN_TEMPLATE = """
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font-family:system-ui;padding:15px;background:#0a0a0f;color:white} input,select{padding:12px;width:100%;max-width:420px;margin:6px 0;border-radius:12px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.5);color:white} button{padding:10px 14px;border-radius:12px;background:linear-gradient(90deg,#ec4899,#8b5cf6);color:white;border:none;font-weight:800;cursor:pointer;margin:3px}.card{background:rgba(255,255,255,0.06);padding:12px;border-radius:16px;margin:10px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap} img.th{width:70px;height:70px;object-fit:cover;border-radius:12px}.order{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);padding:16px;border-radius:18px;margin:12px 0}.status-Received{color:#fbbf24}.status-Packaging{color:#60a5fa}.status-OnTheWay{color:#a78bfa}.status-Delivered{color:#4ade80}</style></head><body>
<h1>👑 ADMIN v8.2 — ORDERS + LOGO + WIGS</h1>
<a href="/" style=color:#ff6ec7;text-decoration:none;font-weight:700>← View Shop</a>

<div style=background:rgba(236,72,153,0.15);padding:18px;border-radius:18px;border:1px solid rgba(236,72,153,0.3);margin:15px 0>
<h3>📸 1. LOGO — Where to paste logo</h3>
<form action="/upload-logo" method=post enctype=multipart/form-data>
<input type=file name=logo required accept=image/*><br><button>✅ Upload Logo</button>
</form>
{% if data.logo %}<img src="/{{data.logo}}" style=width:90px;height:90px;object-fit:cover;border-radius:16px;margin-top:8px>{% endif %}
</div>

<div style=background:rgba(34,197,94,0.12);padding:18px;border-radius:18px;border:1px solid rgba(34,197,94,0.3);margin:15px 0>
<h2>📦 2. ORDERS — Confirm as Admin & Notify Customer!</h2>
<p style=font-size:13px;opacity:0.8>When someone orders, it appears here. Click buttons to confirm & WhatsApp customer.</p>
{% for o in orders|reverse %}
<div class=order>
<b>Order #{{o.id[:8]}} — <span class="status-{{o.status}}">{{o.status}}</span></b> — {{o.date}}<br>
👤 {{o.customer_name}} — 📱 {{o.customer_phone}} — 📍 {{o.customer_loc}}<br>
📍 {{o.delivery_label}} — GHS {{o.delivery_fee}} — <b>Total: GHS {{o.total}}</b> — 🎁 {{o.discount}}<br>
<small>Items:</small><br>
{% for it in o.items %}<small>• {{it.name}} x{{it.qty}} = GHS {{it.price * it.qty}}</small><br>{% endfor %}
<div style=margin-top:10px;display:flex;gap:6px;flex-wrap:wrap>
<a href="/update-status/{{o.id}}/Packaging"><button>📦 Confirm Packaging</button></a>
<a href="/update-status/{{o.id}}/OnTheWay"><button>🚚 Out for Delivery</button></a>
<a href="/update-status/{{o.id}}/Delivered"><button style=background:linear-gradient(90deg,#22c55e,#16a34a)>✔️ Delivered</button></a>
<a href="https://wa.me/{{o.customer_phone|replace('+','')|replace(' ', '')}}?text=Hi {{o.customer_name}} 👑 Your order #{{o.id[:8]}} from JustWearWigs is {{o.status}}! 📦 Total GHS {{o.total}}. NOTE: Delivery price depends on rider 🏍️ Rider will call you. MoMo 0594204990" target=_blank><button style=background:#25D366>💬 WhatsApp Customer</button></a>
<a href="/delete-order/{{o.id}}" style=color:#ff4444;text-decoration:none>❌ Delete</a>
</div>
</div>
{% endfor %}
{% if not orders %}<p>No orders yet — Waiting for first customer!</p>{% endif %}
</div>

<h3>🛍️ 3. Upload Wig from Gallery</h3>
<form action="/add-wig" method=post enctype=multipart/form-data>
<input name=name placeholder="Name e.g., Pixie Blonde" required><br>
<input name=price type=number placeholder="Price GHS" required><br>
<input name=stock type=number value=5 placeholder="Stock" required><br>
<select name=category required>{% for c in cats %}<option>{{c}}</option>{% endfor %}</select><br>
<input type=file name=image required accept=image/*><br><button>🚀 Add to Shop</button>
</form>

<h3>✏️ 4. Edit Wigs</h3>
{% for w in data.wigs %}<div class=card><img class=th src="/{{w.image}}"><form action="/edit-wig/{{w.id}}" method=post style=display:flex;gap:6px;flex-wrap:wrap><input name=name value="{{w.name}}" style=width:150px><input name=price type=number value="{{w.price}}" style=width:70px><input name=stock type=number value="{{w.stock}}" style=width:55px><select name=category style=width:130px>{% for c in cats %}<option {% if c==w.category %}selected{% endif %}>{{c}}</option>{% endfor %}</select><button>Save</button></form><a href="/delete-wig/{{w.id}}" style=color:#ff4444>❌</a></div>{% endfor %}
</body></html>
"""

@app.route('/')
def home():
    data=load_data()
    return render_template_string(SHOP_TEMPLATE, wigs=data['wigs'], cats=CATEGORIES, delivery=DELIVERY, logo=data.get('logo',''))

@app.route('/apply-discount')
def apply_discount():
    code=request.args.get('code','').upper().strip()
    if code in DISCOUNT_CODES:
        return jsonify({"valid":True, **DISCOUNT_CODES[code]})
    return jsonify({"valid":False})

@app.route('/create-order', methods=['POST'])
def create_order():
    j=request.json
    orders=load_orders()
    oid=str(uuid.uuid4())
    order={"id":oid,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"customer_name":j.get('customer_name'),"customer_phone":j.get('customer_phone'),"customer_loc":j.get('customer_loc',''),"delivery_label":j.get('delivery_label'),"delivery_fee":j.get('delivery_fee'),"items":j.get('items'),"total":j.get('total'),"discount":j.get('discount','None'),"status":"Received"}
    orders.append(order)
    save_orders(orders)
    return jsonify({"ok":True,"order_id":oid[:8]})

@app.route('/update-status/<oid>/<status>')
def update_status(oid,status):
    orders=load_orders()
    for o in orders:
        if o['id']==oid:
            o['status']=status
    save_orders(orders)
    return redirect('/admin')

@app.route('/delete-order/<oid>')
def delete_order(oid):
    orders=load_orders()
    orders=[o for o in orders if o['id']!=oid]
    save_orders(orders)
    return redirect('/admin')

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_TEMPLATE, data=load_data(), cats=CATEGORIES, orders=load_orders())

@app.route('/upload-logo', methods=['POST'])
def upload_logo():
    data=load_data()
    f=request.files.get('logo')
    if f and f.filename:
        fname='logo_'+secure_filename(f.filename)
        path=os.path.join(UPLOAD_FOLDER,fname)
        f.save(path)
        data['logo']=path
        save_data(data)
    return redirect('/admin')

@app.route('/add-wig', methods=['POST'])
def add_wig():
    data=load_data()
    f=request.files.get('image')
    if f and f.filename:
        fname=str(uuid.uuid4())[:8]+'_'+secure_filename(f.filename)
        path=os.path.join(UPLOAD_FOLDER,fname)
        f.save(path)
        data['wigs'].append({"id":str(uuid.uuid4()),"name":request.form.get('name'),"price":int(request.form.get('price',0)),"stock":int(request.form.get('stock',5)),"category":request.form.get('category'),"image":path})
        save_data(data)
    return redirect('/admin')

@app.route('/edit-wig/<wid>', methods=['POST'])
def edit_wig(wid):
    data=load_data()
    for w in data['wigs']:
        if w['id']==wid:
            w['name']=request.form.get('name')
            w['price']=int(request.form.get('price',0))
            w['stock']=int(request.form.get('stock',0))
            w['category']=request.form.get('category')
    save_data(data)
    return redirect('/admin')

@app.route('/delete-wig/<wid>')
def del_wig(wid):
    data=load_data()
    data['wigs']=[w for w in data['wigs'] if w['id']!=wid]
    save_data(data)
    return redirect('/admin')

if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
