import os, json, uuid, datetime
from flask import Flask, request, redirect, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER='static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DATA_FILE='wigs_data.json'
ORDERS_FILE='orders_data.json'
REVIEWS_FILE='reviews_data.json'

CATEGORIES=["Bone Straight","Curly Hair","Bob Wigs","Blonde Wigs","Braided Wigs","Pixie Cuts","Silky Straight","Wig Accessories","Sun Glasses","Wig Bundles"]
DELIVERY={"Dansoman - GHS 25":25,"Accra Central - GHS 30":30,"East Legon / Spintex - GHS 40":40,"Tema / Kasoa - GHS 50":50,"Kumasi / Takoradi - GHS 80":80,"Other Regions - GHS 100":100}
DISCOUNT_CODES={"CHRISTMAS15":{"percent":15,"cat":"All","desc":"Christmas 15% OFF"},"NEWYEAR30":{"percent":30,"cat":"All","desc":"New Year 30% OFF"},"PIXIE20":{"percent":20,"cat":"Pixie Cuts","desc":"Pixie 20% OFF"},"SILKY15":{"percent":15,"cat":"Silky Straight","desc":"Silky 15% OFF"},"ACCESS10":{"percent":10,"cat":"Wig Accessories","desc":"Access 10% OFF"},"SUNGLASS20":{"percent":20,"cat":"Sun Glasses","desc":"Sun Glass 20% OFF"},"BUNDLE30":{"percent":30,"cat":"Wig Bundles","desc":"Bundle 30% OFF"},"QUEEN10":{"percent":10,"cat":"All","desc":"Queen 10% OFF"}}

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
def load_reviews():
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE,'r') as f: return json.load(f)
        except: pass
    return {}
def save_reviews(r):
    with open(REVIEWS_FILE,'w') as f: json.dump(r,f)

SHOP_TEMPLATE="""
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>JustWearWigs JUMIA v9</title>
<style>
*{font-family:system-ui;box-sizing:border-box} body{margin:0;background:#f5f5f7;color:#111}
.top{position:sticky;top:0;z-index:50;background:#0a0a0f;color:white;padding:10px 12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.top a{color:white;text-decoration:none;font-weight:700}
.note{background:#fff3cd;border:1px solid #ffc107;color:#856404;padding:10px;text-align:center;font-weight:800;margin:8px;border-radius:12px}
.cats{display:flex;gap:8px;overflow-x:auto;padding:10px;background:white;margin:8px;border-radius:14px}.cat{padding:8px 16px;border-radius:20px;background:#eee;border:1px solid #ddd;white-space:nowrap;cursor:pointer}.cat.active{background:#ec4899;color:white;border-color:#ec4899}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px;padding-bottom:150px}
@media(min-width:700px){.grid{grid-template-columns:repeat(3,1fr)}} @media(min-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{background:white;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);cursor:pointer;position:relative}
.card img{width:100%;height:200px;object-fit:cover}
.badge{position:absolute;top:8px;left:8px;background:#feef00;color:#000;padding:3px 8px;border-radius:8px;font-weight:900;font-size:11px}
.heart{position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.9);width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:none;font-size:18px;cursor:pointer}
.card-body{padding:10px}.price{color:#ec4899;font-weight:900;font-size:15px}.old{color:#999;text-decoration:line-through;font-size:12px;margin-left:6px}
.express{background:#e6f7ff;color:#0077b6;padding:2px 6px;border-radius:6px;font-size:10px;font-weight:800}
.low{color:#ff0000;font-size:11px;font-weight:800}
.btn{width:100%;padding:11px;border-radius:10px;border:none;font-weight:800;margin-top:6px;cursor:pointer}.btn-pink{background:#ec4899;color:white}.btn-dark{background:#eee}
.panel{margin:10px;background:white;padding:16px;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06)}
input,select{padding:11px;border-radius:10px;border:1px solid #ddd;width:100%;margin:5px 0}
.dock{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);background:#0a0a0f;color:white;padding:10px 18px;border-radius:28px;display:flex;gap:12px;align-items:center;z-index:100}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:200;align-items:center;justify-content:center;padding:16px}.modal.show{display:flex}.modal-box{background:white;border-radius:20px;overflow:hidden;max-width:420px;width:100%;max-height:90vh;overflow-y:auto}.modal-box img{width:100%;height:340px;object-fit:cover}.modal-body{padding:14px}
.stars{color:#ffb400}
</style></head><body>
<div class=top>
{% if logo %}<img src="/{{logo}}" style=height:38px;width:38px;object-fit:cover;border-radius:10px;border:2px solid #ec4899>{% else %}👑{% endif %}
<b>JUSTWEARWIGS</b>
<input id=search placeholder="🔍 Search Jumia..." onkeyup=doSearch() style=max-width:160px;padding:8px;border-radius:20px;border:none>
<a href="/track" style=background:white;color:#111;padding:6px 12px;border-radius:20px;font-size:12px>📦 Track Order</a>
<span onclick="showWishlist()" style=cursor:pointer>❤️ <span id=wCount>0</span></span>
<a href="https://wa.me/233594204990" style=color:#25D366>💬 0594204990</a>
<a href="/admin" style=opacity:0.5;font-size:11px>Admin</a>
</div>
<div class=note>⚠️ NOTE: Delivery prices will depend on the motor rider 🏍️ — Rider will call!</div>
<div class=cats><button class="cat active" onclick=filterCat('All',this)>All</button>{% for c in cats %}<button class=cat onclick=filterCat('{{c}}',this)>{{c}}</button>{% endfor %}</div>
<div class=grid id=grid>{% for w in wigs %}
{% set disc = 15 %}
<div class=card data-name="{{w.name|lower}} {{w.category|lower}}" data-cat="{{w.category}}" onclick="openView('{{w.id}}','{{w.name}}','{{w.category}}',{{w.price}},{{w.stock}},'/{{w.image}}')">
<span class=badge>-{{disc}}%</span>
<button class=heart onclick="event.stopPropagation(); toggleWish('{{w.id}}','{{w.name}}',{{w.price}},'/{{w.image}}')" id=heart-{{w.id}}>🤍</button>
<img src="/{{w.image}}"><div class=card-body>
<div style=font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis>{{w.name}}</div>
<div style=font-size:11px;color:#666>{{w.category}} <span class=express>JUMIA EXPRESS</span></div>
{% if w.stock<=1 %}<div class=low>⚠️ Only {{w.stock}} left!</div>{% endif %}
<div><span class=price>GHS {{w.price}}</span><span class=old>GHS {{ (w.price*1.15)|int }}</span></div>
<div class=stars>★★★★★ <small style=color:#666>( {{ reviews.get(w.id,[])|length }} reviews )</small></div>
<button class=btn btn-pink onclick="event.stopPropagation(); addCart('{{w.id}}','{{w.name}}',{{w.price}})">🛒 Add to Cart</button>
</div></div>{% endfor %}</div>
{% if not wigs %}<div style=text-align:center;padding:40px>👑 No wigs yet — Go to <a href="/admin">/admin</a> upload logo + wigs!</div>{% endif %}

<div id=viewModal class=modal onclick="if(event.target==this)closeView()"><div class=modal-box><img id=mImg><div class=modal-body><h3 id=mName style=margin:0></h3><small id=mCat></small><div style=margin:8px 0><span id=mPrice style=color:#ec4899;font-weight:900;font-size:19px></span> <span style=color:#999;text-decoration:line-through;font-size:13px id=mOld></span> <span id=mStock></span></div><div class=stars>★★★★★ Jumia Express • View well before you buy</div><p style=font-size:12px;color:#555>⚠️ NOTE: Delivery prices will depend on motor rider — Premium quality wig</p><button class=btn btn-pink id=mAdd>🛒 Add to Cart</button><button class=btn btn-dark onclick="toggleWishFromModal()">❤️ Add to Wishlist</button><h4>⭐ Customer Reviews</h4><div id=revList></div><h4>Write Review</h4><select id=revStar><option value=5>⭐⭐⭐⭐⭐ 5</option><option value=4>⭐⭐⭐⭐ 4</option><option value=3>⭐⭐⭐ 3</option><option value=2>⭐⭐ 2</option><option value=1>⭐ 1</option></select><input id=revName placeholder="Your name"><input id=revText placeholder="Your review"><button class=btn btn-pink onclick=postReview()>Post Review</button><h4>Related Wigs</h4><div id=related style=display:grid;grid-template-columns:1fr 1fr;gap:8px></div><button class=btn btn-dark onclick=closeView()>Close</button></div></div></div>

<div class=panel id=cartPanel>
<h3>🛒 Cart — Edit / Cancel / Quantity (Jumia Style)</h3>
<div id=cartList>Empty</div>
<h4>👤 Your Details (For Order Confirmation & Tracking)</h4>
<input id=custName placeholder="Full Name *"><input id=custPhone placeholder="WhatsApp Number * 059..."><input id=custLoc placeholder="Location">
<h4>❤️ Wishlist</h4><div id=wishList>Empty</div>
<h4>🎁 Discount Code (All previous codes work)</h4>
<div style=display:flex;gap:6px><input id=code placeholder="CHRISTMAS15, NEWYEAR30, PIXIE20, BUNDLE30, QUEEN10"><button class=btn btn-pink style=width:100px;margin:0 onclick=applyCode()>Apply</button></div><div id=codeMsg style=color:#ec4899;font-weight:700></div>
<div style=margin:10px 0;padding:10px;background:#fff3cd;border-radius:10px;font-size:12px>⚠️ NOTE: Delivery prices will depend on motor rider — 4th place!</div>
<label>📍 Delivery Location</label><select id=deliverySel onchange=calcTotal()>{% for label,fee in delivery.items() %}<option value={{fee}}>{{label}}</option>{% endfor %}</select>
<div style=margin:10px 0;background:#f8f8f8;padding:12px;border-radius:10px;line-height:1.8>
Items: GHS <span id=iTotal>0</span><br>Discount: -GHS <span id=discAmt>0</span> <small id=discLabel></small><br>Delivery: GHS <span id=dFee>25</span><br><b style=color:#ec4899;font-size:17px>Total: GHS <span id=gTotal>0</span></b>
</div>
<button class=btn btn-pink onclick=checkoutWA()>✅ Confirm Order — Trackable Like Jumia!</button>
<button class=btn btn-dark onclick=clearCart()>❌ Cancel All</button>
<p style=font-size:11px;color:#888;text-align:center>MoMo 0594204990 • Instagram @just_wearwigs • NOTE: Delivery price depends on rider</p>
</div>
<div class=dock><div>🛒 <span id=fCount>0</span></div><div style=color:#ff6ec7;font-weight:800>GHS <span id=fTotal>0</span></div><button onclick="document.getElementById('cartPanel').scrollIntoView({behavior:'smooth'})" style=background:#ec4899;border:none;color:white;padding:8px 14px;border-radius:18px;font-weight:700">View Cart</button><a href="/track" style=color:white;font-size:12px>Track</a></div>
<script>
let cart=JSON.parse(localStorage.getItem('jww_cart_v9')||'[]');
let wishlist=JSON.parse(localStorage.getItem('jww_wish_v9')||'[]');
let disc=JSON.parse(localStorage.getItem('jww_disc_v9')||'null'); let discPct=disc?disc.percent:0;
let currentViewId=null;
let allWigs={{ wigs|tojson }};
let allReviews={{ reviews|tojson }};
function openView(id,name,cat,price,stock,img){
 currentViewId=id;
 document.getElementById('mImg').src=img; document.getElementById('mName').innerText=name; document.getElementById('mCat').innerText=cat+' • Stock '+stock;
 document.getElementById('mPrice').innerText='GHS '+price; document.getElementById('mOld').innerText='GHS '+Math.round(price*1.15); document.getElementById('mStock').innerText=stock<=1?' ⚠️ Only '+stock+' left!':'';
 document.getElementById('mAdd').onclick=()=>{addCart(id,name,price); closeView();};
 loadReviews(id); loadRelated(cat,id);
 document.getElementById('viewModal').classList.add('show');
}
function closeView(){document.getElementById('viewModal').classList.remove('show');}
function addCart(id,name,price){let ex=cart.find(c=>c.id==id); if(ex){ex.qty+=1}else{cart.push({id,name,price,qty:1});} saveCart();}
function saveCart(){localStorage.setItem('jww_cart_v9',JSON.stringify(cart)); renderCart();}
function renderCart(){let list=document.getElementById('cartList'); if(cart.length==0){list.innerHTML='Cart empty'; calcTotal(); return;} let html=''; cart.forEach((c,i)=>{html+=`<div style=display:flex;justify-content:space-between;align-items:center;padding:8px;background:#f8f8f8;border-radius:10px;margin:5px 0><div><b>${c.name}</b><br><small>GHS ${c.price} x ${c.qty} = GHS ${c.price*c.qty}</small> <button onclick="changeQty(${i},1)">+</button> <button onclick="changeQty(${i},-1)">-</button></div><button onclick="removeItem(${i})" style=background:#ff4444;border:none;color:white;padding:5px 9px;border-radius:8px">❌</button></div>`;}); list.innerHTML=html; calcTotal();}
function changeQty(i,d){cart[i].qty+=d; if(cart[i].qty<=0)cart.splice(i,1); saveCart();}
function removeItem(i){cart.splice(i,1); saveCart();}
function clearCart(){if(confirm('Cancel all?')){cart=[]; saveCart();}}
function toggleWish(id,name,price,img){let idx=wishlist.findIndex(w=>w.id==id); if(idx>=0){wishlist.splice(idx,1);}else{wishlist.push({id,name,price,img});} localStorage.setItem('jww_wish_v9',JSON.stringify(wishlist)); renderWish(); let h=document.getElementById('heart-'+id); if(h)h.innerText=wishlist.find(w=>w.id==id)?'❤️':'🤍';}
function toggleWishFromModal(){ if(currentViewId){ let w=allWigs.find(x=>x.id==currentViewId); if(w) toggleWish(w.id,w.name,w.price,'/'+w.image); } }
function renderWish(){let el=document.getElementById('wishList'); document.getElementById('wCount').innerText=wishlist.length; if(wishlist.length==0){el.innerHTML='Empty — Tap 🤍 on wigs'; return;} el.innerHTML=wishlist.map((w,i)=>`<div style=display:flex;gap:8px;align-items:center;padding:6px;background:#fff0f5;border-radius:10px;margin:4px 0><img src="${w.img}" style=width:40px;height:40px;object-fit:cover;border-radius:8px><div><b style=font-size:12px>${w.name}</b><br><small>GHS ${w.price}</small></div><button onclick="addCart('${w.id}','${w.name}',${w.price})" style=margin-left:auto;background:#ec4899;color:white;border:none;padding:6px 10px;border-radius:8px>Cart</button><button onclick="wishlist.splice(${i},1); localStorage.setItem('jww_wish_v9',JSON.stringify(wishlist)); renderWish()" style=background:#eee;border:none;padding:6px;border-radius:8px>❌</button></div>`).join('');}
function showWishlist(){document.getElementById('cartPanel').scrollIntoView({behavior:'smooth'});}
function calcTotal(){let dFee=parseInt(document.getElementById('deliverySel').value||25); document.getElementById('dFee').innerText=dFee; let items=cart.reduce((s,c)=>s+c.price*c.qty,0); let discAmt=Math.round(items*discPct/100); let grand=items-discAmt+dFee; if(grand<0)grand=dFee; document.getElementById('iTotal').innerText=items; document.getElementById('discAmt').innerText=discAmt; document.getElementById('discLabel').innerText=disc?`(${disc.desc})`:''; document.getElementById('gTotal').innerText=grand; document.getElementById('fCount').innerText=cart.reduce((s,c)=>s+c.qty,0); document.getElementById('fTotal').innerText=grand;}
function doSearch(){let q=document.getElementById('search').value.toLowerCase(); document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'':'none';});}
function filterCat(cat,el){document.querySelectorAll('.cat').forEach(b=>b.classList.remove('active')); if(el)el.classList.add('active'); document.querySelectorAll('.card').forEach(c=>{c.style.display=(cat=='All'||c.dataset.cat==cat)?'':'none';});}
function applyCode(){let code=document.getElementById('code').value.toUpperCase().trim(); fetch('/apply-discount?code='+code).then(r=>r.json()).then(d=>{if(d.valid){disc=d; discPct=d.percent; localStorage.setItem('jww_disc_v9',JSON.stringify(d)); document.getElementById('codeMsg').innerText='✅ '+d.desc+' '+d.percent+'% OFF'; calcTotal();} else {document.getElementById('codeMsg').innerText='❌ Invalid. Try CHRISTMAS15, NEWYEAR30, QUEEN10, BUNDLE30';}});}
function loadReviews(id){let list=allReviews[id]||[]; let el=document.getElementById('revList'); if(list.length==0){el.innerHTML='<small>No reviews yet — Be first!</small>'; return;} el.innerHTML=list.map(r=>`<div style=padding:6px;background:#f9f9f9;border-radius:8px;margin:4px 0><b>${r.name}</b> ${'⭐'.repeat(r.stars)}<br><small>${r.text}</small><br><small style=color:#999>${r.date}</small></div>`).join('');}
function loadRelated(cat,curId){let rel=allWigs.filter(w=>w.category==cat && w.id!=curId).slice(0,4); let el=document.getElementById('related'); el.innerHTML=rel.map(w=>`<div class=card onclick="openView('${w.id}','${w.name}','${w.category}',${w.price},${w.stock},'/${w.image}')" style=cursor:pointer><img src="/${w.image}" style=height:100px><div style=padding:6px><small>${w.name}</small><br><b style=color:#ec4899>GHS ${w.price}</b></div></div>`).join('');}
function postReview(){let s=document.getElementById('revStar').value; let n=document.getElementById('revName').value; let t=document.getElementById('revText').value; if(!n||!t){alert('Name + review needed'); return;} fetch('/add-review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({wig_id:currentViewId,name:n,stars:parseInt(s),text:t})}).then(r=>r.json()).then(()=>{alert('✅ Review posted!'); location.reload();});}
function checkoutWA(){
 if(cart.length==0){alert('Cart empty'); return;}
 let name=document.getElementById('custName').value.trim(); let phone=document.getElementById('custPhone').value.trim();
 if(!name||!phone){alert('Name + Phone required for Jumia tracking!'); return;}
 let dSel=document.getElementById('deliverySel'); let dLabel=dSel.options[dSel.selectedIndex].text;
 let payload={customer_name:name,customer_phone:phone,customer_loc:document.getElementById('custLoc').value,delivery_label:dLabel,delivery_fee:parseInt(dSel.value),items:cart,total:document.getElementById('gTotal').innerText,discount:disc?disc.desc:'None'};
 fetch('/create-order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
   let items=cart.map(c=>`${c.name} x${c.qty}`).join('%0A');
   let msg=`👑 NEW ORDER #${res.order_id} %0AName: ${name}%0APhone: ${phone}%0A${items}%0ATotal: GHS ${payload.total}%0ATrack at /track`;
   window.open('https://wa.me/233594204990?text='+msg,'_blank');
   alert('✅ Order #'+res.order_id+' Received! Track at /track with your phone number! We will WhatsApp you: Received → Packaging → On The Way → Delivered!');
   cart=[]; saveCart();
   window.location='/track?phone='+encodeURIComponent(phone);
 });
}
renderCart(); renderWish(); calcTotal();
</script></body></html>
"""

TRACK_TEMPLATE="""
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font-family:system-ui;padding:16px;background:#f5f5f7}.order{background:white;padding:14px;border-radius:14px;margin:10px 0;box-shadow:0 2px 8px rgba(0,0,0,0.06)} input{padding:12px;border-radius:10px;border:1px solid #ddd;width:100%;max-width:400px} button{padding:12px 18px;border-radius:10px;background:#ec4899;color:white;border:none;font-weight:800}</style></head><body>
<h2>📦 Track Your Order — Like Jumia</h2><a href="/">← Shop</a><br><br>
<form><input name=phone placeholder="Enter your WhatsApp number e.g., 059..." value="{{phone}}"><button>Track</button></form>
{% for o in orders %}
<div class=order>
<b>Order #{{o.id[:8]}} — {{o.date}}</b> — <b style=color:{% if o.status=='Received' %}#f59e0b{% elif o.status=='Packaging' %}#3b82f6{% elif o.status=='OnTheWay' %}#8b5cf6{% else %}#22c55e{% endif %}>{{o.status}}</b><br>
👤 {{o.customer_name}} — 📍 {{o.customer_loc}}<br>
Items: {% for it in o.items %}{{it.name}} x{{it.qty}} {% endfor %}<br>
Total: <b>GHS {{o.total}}</b> — {{o.delivery_label}}<br>
<p style=font-size:12px;color:#666>⚠️ NOTE: Delivery prices will depend on motor rider — Status updated by Admin. You will get WhatsApp: Received → Packaging → Out for Delivery → Delivered</p>
</div>
{% endfor %}
{% if phone and not orders %}<p>No orders for {{phone}} yet</p>{% endif %}
</body></html>
"""

ADMIN_TEMPLATE="""
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font-family:system-ui;padding:14px;background:#0a0a0f;color:white} input,select{padding:11px;width:100%;max-width:420px;margin:5px 0;border-radius:10px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.5);color:white} button{padding:10px 14px;border-radius:10px;background:linear-gradient(90deg,#ec4899,#8b5cf6);color:white;border:none;font-weight:800;margin:3px;cursor:pointer}.card{background:rgba(255,255,255,0.06);padding:10px;border-radius:14px;margin:8px 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap} img.th{width:60px;height:60px;object-fit:cover;border-radius:10px}.order{background:rgba(255,255,255,0.08);padding:14px;border-radius:16px;margin:10px 0}</style></head><body>
<h1>👑 ADMIN JUMIA v9 — ALL FEATURES</h1><a href="/" style=color:#ff6ec7>← Shop</a> | <a href="/track" style=color:#4ade80>Track Page</a>
<div style=background:rgba(236,72,153,0.15);padding:16px;border-radius:16px;margin:12px 0>
<h3>📸 1. LOGO — Where to paste logo</h3>
<form action="/upload-logo" method=post enctype=multipart/form-data><input type=file name=logo required accept=image/*><br><button>✅ Upload Logo</button></form>
{% if data.logo %}<img src="/{{data.logo}}" style=width:90px;height:90px;object-fit:cover;border-radius:14px;margin-top:6px><br><small style=color:#4ade80>✅ Logo Live</small>{% else %}<small style=color:#ff6ec7>⚠️ No logo yet</small>{% endif %}
</div>
<div style=background:rgba(34,197,94,0.12);padding:16px;border-radius:16px;margin:12px 0>
<h2>📦 2. ORDERS — Confirm & Notify (Jumia Style)</h2>
{% for o in orders|reverse %}
<div class=order><b>#{{o.id[:8]}} — {{o.status}} — {{o.date}}</b><br>👤 {{o.customer_name}} — 📱 {{o.customer_phone}} — 📍 {{o.customer_loc}}<br>{{o.delivery_label}} — GHS {{o.total}} — {{o.discount}}<br>{% for it in o.items %}<small>• {{it.name}} x{{it.qty}}</small><br>{% endfor %}
<div style=margin-top:8px><a href="/update-status/{{o.id}}/Packaging"><button>📦 Packaging</button></a><a href="/update-status/{{o.id}}/OnTheWay"><button>🚚 On The Way</button></a><a href="/update-status/{{o.id}}/Delivered"><button style=background:#22c55e>✔️ Delivered</button></a><a href="https://wa.me/{{o.customer_phone|replace('+','')|replace(' ', '')}}?text=Hi {{o.customer_name}} 👑 Order #{{o.id[:8]}} is {{o.status}}! Total GHS {{o.total}}. Track at {{request.host_url}}track?phone={{o.customer_phone}} NOTE: Delivery depends on rider 🏍️" target=_blank><button style=background:#25D366>💬 Notify Customer</button></a><a href="/delete-order/{{o.id}}"><button style=background:#ff4444>❌</button></a></div></div>
{% endfor %}
{% if not orders %}<p>No orders</p>{% endif %}
</div>
<h3>⭐ 3. REVIEWS — Manage</h3>{% for wig_id, revs in reviews.items() %}<div style=background:rgba(255,255,255,0.05);padding:10px;border-radius:12px;margin:6px 0><b>Wig {{wig_id[:6]}}</b> — {{revs|length}} reviews {% for r in revs %}<br><small>{{r.name}}: {{'⭐'*r.stars}} {{r.text}} — <a href="/delete-review/{{wig_id}}/{{loop.index0}}" style=color:#ff4444>Delete</a></small>{% endfor %}</div>{% endfor %}
<h3>🛍️ 4. Upload Wig from Gallery</h3>
<form action="/add-wig" method=post enctype=multipart/form-data><input name=name placeholder="Name" required><br><input name=price type=number placeholder="Price GHS" required><br><input name=stock type=number value=5 placeholder="Stock" required><br><select name=category required>{% for c in cats %}<option>{{c}}</option>{% endfor %}</select><br><input type=file name=image required accept=image/*><br><button>🚀 Add</button></form>
<h3>✏️ 5. Edit Wigs</h3>{% for w in data.wigs %}<div class=card><img class=th src="/{{w.image}}"><form action="/edit-wig/{{w.id}}" method=post style=display:flex;gap:5px;flex-wrap:wrap><input name=name value="{{w.name}}" style=width:130px><input name=price type=number value="{{w.price}}" style=width:65px><input name=stock type=number value="{{w.stock}}" style=width:50px><select name=category style=width:120px>{% for c in cats %}<option {% if c==w.category %}selected{% endif %}>{{c}}</option>{% endfor %}</select><button>Save</button></form><a href="/delete-wig/{{w.id}}" style=color:#ff4444>❌</a></div>{% endfor %}
</body></html>
"""

@app.route('/')
def home():
    data=load_data()
    return render_template_string(SHOP_TEMPLATE, wigs=data['wigs'], cats=CATEGORIES, delivery=DELIVERY, logo=data.get('logo',''), reviews=load_reviews())

@app.route('/track')
def track():
    phone=request.args.get('phone','').strip()
    orders=load_orders()
    if phone:
        orders=[o for o in orders if phone in o.get('customer_phone','')]
    else:
        orders=[]
    return render_template_string(TRACK_TEMPLATE, orders=orders, phone=phone)

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

@app.route('/add-review', methods=['POST'])
def add_review():
    j=request.json
    revs=load_reviews()
    wid=j.get('wig_id')
    if wid not in revs: revs[wid]=[]
    revs[wid].append({"name":j.get('name'),"stars":j.get('stars',5),"text":j.get('text'),"date":datetime.datetime.now().strftime("%Y-%m-%d")})
    save_reviews(revs)
    return jsonify({"ok":True})

@app.route('/delete-review/<wid>/<int:idx>')
def delete_review(wid,idx):
    revs=load_reviews()
    if wid in revs and 0<=idx<len(revs[wid]):
        revs[wid].pop(idx)
        save_reviews(revs)
    return redirect('/admin')

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_TEMPLATE, data=load_data(), cats=CATEGORIES, orders=load_orders(), reviews=load_reviews())

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

