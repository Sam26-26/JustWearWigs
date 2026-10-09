import os, json, uuid, datetime
from flask import Flask, request, redirect, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
ADMIN_KEY = 'JustWearWigs2024' # YOUR SECRET ADMIN KEY - Only you know this
MOMO_NUMBER = '0598952333'
WHATSAPP_NUM = '233594204990'

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
def is_admin():
    k = request.args.get('key') or request.form.get('key') or request.args.get('password')
    return k == ADMIN_KEY

SHOP_TEMPLATE="""
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>JustWearWiG's Official</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{font-family:system-ui;box-sizing:border-box} body{margin:0;background:#fff0f5;color:#111}
.pink-header{background:linear-gradient(90deg,#f472b6,#ec4899);color:white;padding:14px 16px;display:flex;align-items:center;gap:12px}
.contact-bar{display:flex;gap:8px;padding:10px;background:#fff0f5;overflow-x:auto}
.contact-chip{background:white;border:1px solid #ffd6e7;padding:8px 12px;border-radius:22px;display:flex;align-items:center;gap:8px;white-space:nowrap;font-size:12px;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,0.06);text-decoration:none;color:#111}
.icon-box{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;color:white;flex-shrink:0}
.wa-bg{background:#25D366}.ig-bg{background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5)}.tt-bg{background:#000000}.momo-bg{background:#0047AB}
.note{background:#fff3cd;border:1px solid #ffc107;color:#856404;padding:10px;text-align:center;font-weight:800;margin:8px;border-radius:12px;font-size:13px}
.shop-head{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;font-weight:900;color:#ec4899;font-size:18px;background:white;margin:8px;border-radius:12px}
.cats{display:flex;gap:8px;overflow-x:auto;padding:10px;background:white;margin:8px;border-radius:14px}.cat{padding:8px 16px;border-radius:20px;background:#ffe6f2;border:1px solid #ffd6e7;white-space:nowrap;cursor:pointer;font-weight:600}.cat.active{background:#ec4899;color:white}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:10px;padding-bottom:160px}
@media(min-width:700px){.grid{grid-template-columns:repeat(3,1fr)}} @media(min-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{background:white;border-radius:18px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,0.06);position:relative;border:1px solid #ffe6f2}
.card img{width:100%;height:210px;object-fit:cover}
.card-body{padding:10px}.price{color:#c2185b;font-weight:900}
.qty{display:flex;align-items:center;gap:6px;margin:6px 0}.qty button{width:26px;height:26px;border-radius:8px;border:1px solid #ffd6e7;background:#fff0f5;font-weight:800}
.btn{width:100%;padding:11px;border-radius:12px;border:none;font-weight:800;margin-top:6px;cursor:pointer}.btn-pink{background:#f472b6;color:white}.btn-outline{background:white;color:#ec4899;border:1px solid #ec4899}
.badge{position:absolute;top:8px;left:8px;background:#feef00;color:#000;padding:3px 8px;border-radius:8px;font-weight:900;font-size:11px}
.heart{position:absolute;top:8px;right:8px;background:white;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:none;font-size:18px;cursor:pointer}
.panel{margin:10px;background:white;padding:16px;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06)}
input,select{padding:11px;border-radius:10px;border:1px solid #ddd;width:100%;margin:5px 0}
.dock{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);background:#111;color:white;padding:10px 18px;border-radius:28px;display:flex;gap:12px;align-items:center;z-index:100}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:200;align-items:center;justify-content:center;padding:16px}.modal.show{display:flex}.modal-box{background:white;border-radius:20px;overflow:hidden;max-width:420px;width:100%;max-height:90vh;overflow-y:auto}.modal-box img{width:100%;height:340px;object-fit:cover}.modal-body{padding:14px}
</style></head><body>
<div class=pink-header>
<div style=font-size:32px>👑</div>
<div>{% if logo %}<img src="/{{logo}}" style=height:38px;width:38px;object-fit:cover;border-radius:10px;border:2px solid white;margin-right:6px;vertical-align:middle>{% endif %}<b>JustWearWiG's</b><small>📍 Capital Hills | Tuesday to Saturday</small></div>
</div>
<div class=contact-bar>
<a class=contact-chip href="https://wa.me/233594204990" target=_blank><span class="icon-box wa-bg"><i class="fab fa-whatsapp"></i></span><span><b>WhatsApp</b></span></a>
<a class=contact-chip href="https://instagram.com/just_wearwigs" target=_blank><span class="icon-box ig-bg"><i class="fab fa-instagram"></i></span><small>Instagram<br><b>@just_wearwigs</b></small></a>
<a class=contact-chip href="https://tiktok.com/@justwearwigs" target=_blank><span class="icon-box tt-bg"><i class="fab fa-tiktok"></i></span><small>TikTok<br><b>@justwearwigs</b></small></a>
<div class=contact-chip><span class="icon-box momo-bg"><i class="fas fa-mobile-screen"></i></span><small>MoMo Pay:<br><b>0598952333</b></small></div>
<div class=contact-chip style=padding:6px 10px><i class="fas fa-search" style=color:#ec4899></i><input id=search placeholder="Search..." onkeyup=doSearch() style=border:none;width:110px;padding:2px;font-size:12px></div>
</div>
<div class=note>⚠️ NOTE: Delivery prices will depend on the motor rider 🏍️</div>
<div class=shop-head><span>Shop Wigs</span><span style=font-size:14px>🛒 Cart (<span id=headCart>0</span>) <a href="/track" style=text-decoration:none;color:#ec4899;font-size:12px>📦 Track</a> ❤️ <span id=wCount>0</span></span></div>
<div class=cats><button class="cat active" onclick=filterCat('All',this)>All</button>{% for c in cats %}<button class=cat onclick=filterCat('{{c}}',this)>{{c}}</button>{% endfor %}</div>
<div class=grid id=grid>{% for w in wigs %}
<div class=card data-name="{{w.name|lower}} {{w.category|lower}}" data-cat="{{w.category}}">
<span class=badge>-15%</span>
<button class=heart onclick="toggleWish('{{w.id}}','{{w.name}}',{{w.price}},'/{{w.image}}')" id=heart-{{w.id}}>🤍</button>
<img src="/{{w.image}}" onclick="openView('{{w.id}}','{{w.name}}','{{w.category}}',{{w.price}},{{w.stock}},'/{{w.image}}')">
<div class=card-body>
<div style=font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis>{{w.name}}</div>
<div style=display:flex;align-items:center;gap:8px;margin:6px 0><span style=color:#c2185b;font-weight:700;font-size:12px>GHS {{w.price}}</span><span class=qty><button onclick="changeCardQty('{{w.id}}',-1)">-</button><span id=qty-{{w.id}}>1</span><button onclick="changeCardQty('{{w.id}}',1)">+</button></span></div>
{% if w.stock<=1 %}<small style=color:red;font-weight:800>⚠️ Only {{w.stock}} left!</small>{% endif %}
<button class=btn btn-pink onclick="addCartWithQty('{{w.id}}','{{w.name}}',{{w.price}})">Add to Cart</button>
<button class=btn btn-outline onclick="preorder('{{w.name}}')">Preorder</button>
</div></div>{% endfor %}</div>
{% if not wigs %}<div style=text-align:center;padding:30px>👑 No wigs yet — Owner upload in admin with key!</div>{% endif %}
<div id=viewModal class=modal onclick="if(event.target==this)closeView()"><div class=modal-box><img id=mImg><div class=modal-body><h3 id=mName style=margin:0></h3><small id=mCat></small><div><span id=mPrice style=color:#c2185b;font-weight:900;font-size:18px></span> <span id=mOld style=color:#999;text-decoration:line-through></span> <span id=mStock></span></div><button class=btn btn-pink id=mAdd>🛒 Add to Cart</button><button class=btn btn-outline onclick="toggleWishFromModal()">❤️ Wishlist</button><h4>⭐ Reviews</h4><div id=revList></div><input id=revName placeholder="Name"><select id=revStar><option value=5>5 stars</option><option value=4>4</option><option value=3>3</option><option value=2>2</option><option value=1>1</option></select><input id=revText placeholder="Your review"><button class=btn btn-pink onclick=postReview()>Post Review</button><div id=related style=display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px></div><button class=btn style=background:#eee;margin-top:10px onclick=closeView()>Close</button></div></div></div>
<div class=panel id=cartPanel>
<h3>🛒 Your Cart — JustWearWiG's</h3>
<div id=cartList>Empty</div>
<h4>👤 Details for Confirmation & Tracking</h4><input id=custName placeholder="Full Name *"><input id=custPhone placeholder="WhatsApp * 059..."><input id=custLoc placeholder="Location">
<h4>❤️ Wishlist</h4><div id=wishList>Empty</div>
<h4>🎁 Discount Code</h4>
<div style=display:flex;gap:6px><input id=code placeholder="CHRISTMAS15, NEWYEAR30, QUEEN10"><button class=btn btn-pink style=width:100px;margin:0 onclick=applyCode()>Apply</button></div><div id=codeMsg style=color:#ec4899;font-weight:700></div>
<label>📍 Delivery Location</label><select id=deliverySel onchange=calcTotal()>{% for label,fee in delivery.items() %}<option value={{fee}}>{{label}}</option>{% endfor %}</select>
<div style=margin:10px 0;background:#f8f8f8;padding:12px;border-radius:10px;line-height:1.8>Items: GHS <span id=iTotal>0</span><br>Discount: -GHS <span id=discAmt>0</span> <small id=discLabel></small><br>Delivery: GHS <span id=dFee>25</span><br><b style=color:#ec4899;font-size:17px>Total: GHS <span id=gTotal>0</span></b></div>
<button class=btn btn-pink onclick=checkoutWA()>✅ Confirm Order — Works on All Devices!</button>
<button class=btn style=background:#eee onclick=clearCart()>❌ Cancel All</button>
<p style=font-size:11px;color:#888;text-align:center>MoMo: 0598952333 • IG: @just_wearwigs • TikTok: @justwearwigs</p>
</div>
<div class=dock><div>🛒 <span id=fCount>0</span></div><div style=color:#ff6ec7;font-weight:800>GHS <span id=fTotal>0</span></div><button onclick="document.getElementById('cartPanel').scrollIntoView({behavior:'smooth'})" style=background:#ec4899;border:none;color:white;padding:8px 14px;border-radius:18px;font-weight:700">View Cart</button></div>
<script>
let cart=JSON.parse(localStorage.getItem('jww_cart_v95')||'[]');
let wishlist=JSON.parse(localStorage.getItem('jww_wish_v95')||'[]');
let cardQty={};
let disc=JSON.parse(localStorage.getItem('jww_disc_v95')||'null'); let discPct=disc?disc.percent:0;
let currentViewId=null; let allWigs={{ wigs|tojson }}; let allReviews={{ reviews|tojson }};
function changeCardQty(id,d){ if(!cardQty[id]) cardQty[id]=1; cardQty[id]+=d; if(cardQty[id]<1) cardQty[id]=1; document.getElementById('qty-'+id).innerText=cardQty[id]; }
function addCartWithQty(id,name,price){ let q=cardQty[id]||1; let ex=cart.find(c=>c.id==id); if(ex){ex.qty+=q}else{cart.push({id,name,price,qty:q});} saveCart(); }
function openView(id,name,cat,price,stock,img){ currentViewId=id; document.getElementById('mImg').src=img; document.getElementById('mName').innerText=name; document.getElementById('mCat').innerText=cat+' • Stock '+stock; document.getElementById('mPrice').innerText='GHS '+price; document.getElementById('mOld').innerText='GHS '+Math.round(price*1.15); document.getElementById('mStock').innerText=stock<=1?' ⚠️ Only '+stock+' left!':''; document.getElementById('mAdd').onclick=()=>{addCartWithQty(id,name,price); closeView();}; loadReviews(id); loadRelated(cat,id); document.getElementById('viewModal').classList.add('show');}
function closeView(){document.getElementById('viewModal').classList.remove('show');}
function saveCart(){localStorage.setItem('jww_cart_v95',JSON.stringify(cart)); renderCart();}
function renderCart(){let list=document.getElementById('cartList'); if(cart.length==0){list.innerHTML='Cart empty'; calcTotal(); return;} let html=''; cart.forEach((c,i)=>{html+=`<div style=display:flex;justify-content:space-between;align-items:center;padding:8px;background:#fff0f5;border-radius:10px;margin:5px 0><div><b>${c.name}</b><br><small>GHS ${c.price} x ${c.qty} = GHS ${c.price*c.qty}</small> <button onclick="changeQty(${i},1)">+</button> <button onclick="changeQty(${i},-1)">-</button></div><button onclick="removeItem(${i})" style=background:#ff4444;border:none;color:white;padding:5px 9px;border-radius:8px">❌</button></div>`;}); list.innerHTML=html; calcTotal();}
function changeQty(i,d){cart[i].qty+=d; if(cart[i].qty<=0)cart.splice(i,1); saveCart();}
function removeItem(i){cart.splice(i,1); saveCart();}
function clearCart(){if(confirm('Cancel all?')){cart=[]; saveCart();}}
function toggleWish(id,name,price,img){let idx=wishlist.findIndex(w=>w.id==id); if(idx>=0){wishlist.splice(idx,1);}else{wishlist.push({id,name,price,img});} localStorage.setItem('jww_wish_v95',JSON.stringify(wishlist)); renderWish(); let h=document.getElementById('heart-'+id); if(h)h.innerText=wishlist.find(w=>w.id==id)?'❤️':'🤍';}
function toggleWishFromModal(){ if(currentViewId){ let w=allWigs.find(x=>x.id==currentViewId); if(w) toggleWish(w.id,w.name,w.price,'/'+w.image); } }
function renderWish(){let el=document.getElementById('wishList'); document.getElementById('wCount').innerText=wishlist.length; if(wishlist.length==0){el.innerHTML='Empty'; return;} el.innerHTML=wishlist.map((w,i)=>`<div style=display:flex;gap:8px;align-items:center;padding:6px;background:#fff0f5;border-radius:10px;margin:4px 0><img src="${w.img}" style=width:40px;height:40px;object-fit:cover;border-radius:8px><div><b style=font-size:12px>${w.name}</b><br><small>GHS ${w.price}</small></div><button onclick="addCartWithQty('${w.id}','${w.name}',${w.price})" style=margin-left:auto;background:#ec4899;color:white;border:none;padding:6px 10px;border-radius:8px>Cart</button><button onclick="wishlist.splice(${i},1); localStorage.setItem('jww_wish_v95',JSON.stringify(wishlist)); renderWish()" style=background:#eee;border:none;padding:6px;border-radius:8px>❌</button></div>`).join('');}
function calcTotal(){let dFee=parseInt(document.getElementById('deliverySel').value||25); document.getElementById('dFee').innerText=dFee; let items=cart.reduce((s,c)=>s+c.price*c.qty,0); let discAmt=Math.round(items*discPct/100); let grand=items-discAmt+dFee; if(grand<0)grand=dFee; document.getElementById('iTotal').innerText=items; document.getElementById('discAmt').innerText=discAmt; document.getElementById('discLabel').innerText=disc?`(${disc.desc})`:''; document.getElementById('gTotal').innerText=grand; document.getElementById('fCount').innerText=cart.reduce((s,c)=>s+c.qty,0); document.getElementById('fTotal').innerText=grand; document.getElementById('headCart').innerText=cart.reduce((s,c)=>s+c.qty,0);}
function doSearch(){let q=document.getElementById('search').value.toLowerCase(); document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'':'none';});}
function filterCat(cat,el){document.querySelectorAll('.cat').forEach(b=>b.classList.remove('active')); if(el)el.classList.add('active'); document.querySelectorAll('.card').forEach(c=>{c.style.display=(cat=='All'||c.dataset.cat==cat)?'':'none';});}
function applyCode(){let code=document.getElementById('code').value.toUpperCase().trim(); fetch('/apply-discount?code='+code).then(r=>r.json()).then(d=>{if(d.valid){disc=d; discPct=d.percent; localStorage.setItem('jww_disc_v95',JSON.stringify(d)); document.getElementById('codeMsg').innerText='✅ '+d.desc+' '+d.percent+'% OFF'; calcTotal();} else {document.getElementById('codeMsg').innerText='❌ Invalid';}});}
function loadReviews(id){let list=allReviews[id]||[]; let el=document.getElementById('revList'); if(list.length==0){el.innerHTML='<small>No reviews yet</small>'; return;} el.innerHTML=list.map(r=>`<div style=padding:6px;background:#fff0f5;border-radius:8px;margin:4px 0><b>${r.name}</b> ${'⭐'.repeat(r.stars)}<br><small>${r.text}</small></div>`).join('');}
function loadRelated(cat,curId){let rel=allWigs.filter(w=>w.category==cat && w.id!=curId).slice(0,4); let el=document.getElementById('related'); el.innerHTML=rel.map(w=>`<div style=background:white;border-radius:12px;overflow:hidden;border:1px solid #ffe6e7;cursor:pointer" onclick="openView('${w.id}','${w.name}','${w.category}',${w.price},${w.stock},'/${w.image}')"><img src="/${w.image}" style=width:100%;height:90px;object-fit:cover><div style=padding:6px><small>${w.name}</small><br><b style=color:#c2185b>GHS ${w.price}</b></div></div>`).join('');}
function postReview(){let s=document.getElementById('revStar').value; let n=document.getElementById('revName').value; let t=document.getElementById('revText').value; if(!n||!t){alert('Name + review'); return;} fetch('/add-review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({wig_id:currentViewId,name:n,stars:parseInt(s),text:t})}).then(r=>r.json()).then(()=>{alert('Review posted!'); location.reload();});}
function preorder(name){let msg=`Hi JustWearWiG's 👑 I want to preorder ${name}`; let url=`https://wa.me/233594204990?text=${encodeURIComponent(msg)}`; window.location.href=url; }
function checkoutWA(){
 if(cart.length==0){alert('Cart empty'); return;}
 let name=document.getElementById('custName').value.trim(); let phone=document.getElementById('custPhone').value.trim();
 if(!name||!phone){alert('Name + WhatsApp required'); return;}
 let dSel=document.getElementById('deliverySel'); let dLabel=dSel.options[dSel.selectedIndex].text;
 let payload={customer_name:name,customer_phone:phone,customer_loc:document.getElementById('custLoc').value,delivery_label:dLabel,delivery_fee:parseInt(dSel.value),items:cart,total:document.getElementById('gTotal').innerText,discount:disc?disc.desc:'None'};
 fetch('/create-order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
   let itemsText=cart.map(c=>`- ${c.name} x${c.qty} = GHS ${c.price*c.qty}`).join('\\n');
   let fullMsg=`👑 NEW ORDER #${res.order_id}\\n\\nName: ${name}\\nPhone: ${phone}\\nLocation: ${payload.customer_loc}\\n\\nItems:\\n${itemsText}\\n\\n${dLabel}\\nDiscount: ${payload.discount}\\nTotal: GHS ${payload.total}\\nMoMo Pay: 0598952333\\n\\nNOTE: Delivery depends on rider`;
   let waUrl=`https://wa.me/233594204990?text=${encodeURIComponent(fullMsg)}`;
   // This method works on Android, iPhone, Laptop
   let a=document.createElement('a'); a.href=waUrl; a.target='_blank'; a.rel='noopener'; document.body.appendChild(a); a.click(); document.body.removeChild(a);
   setTimeout(()=>{ window.location.href='/track?phone='+encodeURIComponent(phone); }, 1000);
   alert('✅ Order #'+res.order_id+' Saved! Opening WhatsApp with full details...');
   cart=[]; saveCart();
 });
}
renderCart(); renderWish(); calcTotal();
</script></body></html>
"""

LOGIN_TEMPLATE="""
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font-family:system-ui;background:#fff0f5;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}.box{background:white;padding:30px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.1);width:90%;max-width:380px;text-align:center} input{padding:14px;width:100%;border-radius:12px;border:1px solid #ddd;margin:10px 0} button{padding:14px;width:100%;border-radius:12px;background:#ec4899;color:white;border:none;font-weight:800}</style></head><body>
<div class=box><h2>👑 Owner Login</h2><p>Enter your secret admin key</p><form method=GET action="/admin"><input type=password name=key placeholder="Admin Key" required value="JustWearWigs2024"><button>🔓 Open Admin</button></form><p style=font-size:11px;color:#999>Key: JustWearWigs2024 • MoMo: 0598952333</p><a href="/">← Shop</a></div></body></html>
"""

ADMIN_TEMPLATE="""
<html><head><meta name=viewport content="width=device-width,initial-scale=1"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"><style>body{font-family:system-ui;padding:14px;background:#fff0f5} input,select{padding:11px;width:100%;max-width:420px;margin:5px 0;border-radius:10px;border:1px solid #ddd} button{padding:10px 14px;border-radius:10px;background:#ec4899;color:white;border:none;font-weight:800;margin:3px}.card{background:white;padding:10px;border-radius:14px;margin:8px 0;display:flex;gap:10px;align-items:center} img.th{width:60px;height:60px;object-fit:cover;border-radius:10px}.order{background:white;padding:14px;border-radius:16px;margin:10px 0;border:1px solid #ffd6e7}</style></head><body>
<h1 style=color:#ec4899>👑 ADMIN v9.5 — Secure</h1><a href="/?key={{admin_key}}">← Shop</a> | <a href="/track">Track</a>
<p style=background:#e6ffe6;padding:10px;border-radius:10px>✅ Owner access — MoMo 0598952333 — Key: {{admin_key}}</p>
<div style=background:white;padding:16px;border-radius:16px;margin:12px 0>
<h3>📸 LOGO</h3>
<form action="/upload-logo?key={{admin_key}}" method=post enctype=multipart/form-data><input type=file name=logo required accept=image/*><br><button>✅ Upload Logo</button></form>
{% if data.logo %}<img src="/{{data.logo}}" style=width:90px;height:90px;object-fit:cover;border-radius:14px;margin-top:6px>{% endif %}
</div>
<div style=background:white;padding:16px;border-radius:16px;margin:12px 0>
<h2>📦 Orders — MoMo 0598952333</h2>
{% for o in orders|reverse %}<div class=order><b>#{{o.id[:8]}} — {{o.status}}</b> — {{o.date}}<br>👤 {{o.customer_name}} — {{o.customer_phone}} — {{o.customer_loc}}<br>{{o.delivery_label}} — GHS {{o.total}}<br>{% for it in o.items %}<small>{{it.name}} x{{it.qty}}</small><br>{% endfor %}<br><a href="/update-status/{{o.id}}/Packaging?key={{admin_key}}"><button>📦 Packaging</button></a><a href="/update-status/{{o.id}}/OnTheWay?key={{admin_key}}"><button>🚚 On The Way</button></a><a href="/update-status/{{o.id}}/Delivered?key={{admin_key}}"><button>✔️ Delivered</button></a><a href="https://wa.me/{{o.customer_phone|replace('+','')|replace(' ', '')}}?text=Hi {{o.customer_name}} 👑 JustWearWiG's Order #{{o.id[:8]}} is {{o.status}}! MoMo 0598952333" target=_blank><button style=background:#25D366>💬 Notify</button></a><a href="/delete-order/{{o.id}}?key={{admin_key}}"><button style=background:#ff4444>❌ Delete</button></a></div>{% endfor %}
</div>
<h3>Upload Wig</h3><form action="/add-wig?key={{admin_key}}" method=post enctype=multipart/form-data><input name=name placeholder="Name" required><input name=price type=number placeholder="Price" required><input name=stock type=number value=5 required><select name=category required>{% for c in cats %}<option>{{c}}</option>{% endfor %}</select><input type=file name=image required accept=image/*><button>🚀 Add</button></form>
<h3>Edit Wigs</h3>{% for w in data.wigs %}<div class=card><img class=th src="/{{w.image}}"><form action="/edit-wig/{{w.id}}?key={{admin_key}}" method=post style=display:flex;gap:5px;flex-wrap:wrap><input name=name value="{{w.name}}" style=width:130px><input name=price type=number value="{{w.price}}" style=width:65px><input name=stock type=number value="{{w.stock}}" style=width:50px><select name=category style=width:120px>{% for c in cats %}<option {% if c==w.category %}selected{% endif %}>{{c}}</option>{% endfor %}</select><button>Save</button></form><a href="/delete-wig/{{w.id}}?key={{admin_key}}" style=color:red>❌</a></div>{% endfor %}
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
    filtered=[o for o in orders if phone.lower() in o.get('customer_phone','').lower()] if phone else []
    return render_template_string("<html><head><meta name=viewport content='width=device-width,initial-scale=1'><style>body{font-family:system-ui;padding:16px;background:#fff0f5}.order{background:white;padding:14px;border-radius:14px;margin:10px 0} input{padding:12px;border-radius:10px;border:1px solid #ddd;width:100%;max-width:400px} button{padding:12px 18px;border-radius:10px;background:#ec4899;color:white;border:none}</style></head><body><h2>📦 Track JustWearWiG's Order</h2><a href='/'>← Shop</a><br><br><form><input name=phone placeholder='WhatsApp' value='{{phone}}'><button>Track</button></form>{% for o in orders %}<div class=order><b>#{{o.id[:8]}} — {{o.status}} — {{o.date}}</b><br>👤 {{o.customer_name}} — 📍 {{o.customer_loc}}<br>GHS {{o.total}} — MoMo 0598952333</div>{% endfor %}</body></html>", orders=filtered, phone=phone)

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
    if not is_admin(): return "Unauthorized - Add?key=JustWearWigs2024", 401
    orders=load_orders()
    for o in orders:
        if o['id']==oid:
            o['status']=status
    save_orders(orders)
    return redirect(f'/admin?key={ADMIN_KEY}')

@app.route('/delete-order/<oid>')
def delete_order(oid):
    if not is_admin(): return "Unauthorized", 401
    orders=load_orders()
    orders=[o for o in orders if o['id']!=oid]
    save_orders(orders)
    return redirect(f'/admin?key={ADMIN_KEY}')

@app.route('/add-review', methods=['POST'])
def add_review():
    j=request.json
    revs=load_reviews()
    wid=j.get('wig_id')
    if wid not in revs: revs[wid]=[]
    revs[wid].append({"name":j.get('name'),"stars":j.get('stars',5),"text":j.get('text'),"date":datetime.datetime.now().strftime("%Y-%m-%d")})
    save_reviews(revs)
    return jsonify({"ok":True})

@app.route('/admin', methods=['GET','POST'])
def admin():
    if not is_admin():
        return render_template_string(LOGIN_TEMPLATE)
    return render_template_string(ADMIN_TEMPLATE, data=load_data(), cats=CATEGORIES, orders=load_orders(), reviews=load_reviews(), admin_key=ADMIN_KEY)

@app.route('/upload-logo', methods=['POST'])
def upload_logo():
    if not is_admin(): return "Unauthorized", 401
    data=load_data()
    f=request.files.get('logo')
    if f and f.filename:
        fname='logo_'+secure_filename(f.filename)
        path=os.path.join(UPLOAD_FOLDER,fname)
        f.save(path)
        data['logo']=path
        save_data(data)
    return redirect(f'/admin?key={ADMIN_KEY}')

@app.route('/add-wig', methods=['POST'])
def add_wig():
    if not is_admin(): return "Unauthorized", 401
    data=load_data()
    f=request.files.get('image')
    if f and f.filename:
        fname=str(uuid.uuid4())[:8]+'_'+secure_filename(f.filename)
        path=os.path.join(UPLOAD_FOLDER,fname)
        f.save(path)
        data['wigs'].append({"id":str(uuid.uuid4()),"name":request.form.get('name'),"price":int(request.form.get('price',0)),"stock":int(request.form.get('stock',5)),"category":request.form.get('category'),"image":path})
        save_data(data)
    return redirect(f'/admin?key={ADMIN_KEY}')

@app.route('/edit-wig/<wid>', methods=['POST'])
def edit_wig(wid):
    if not is_admin(): return "Unauthorized", 401
    data=load_data()
    for w in data['wigs']:
        if w['id']==wid:
            w['name']=request.form.get('name')
            w['price']=int(request.form.get('price',0))
            w['stock']=int(request.form.get('stock',0))
            w['category']=request.form.get('category')
    save_data(data)
    return redirect(f'/admin?key={ADMIN_KEY}')

@app.route('/delete-wig/<wid>')
def del_wig(wid):
    if not is_admin(): return "Unauthorized", 401
    data=load_data()
    data['wigs']=[w for w in data['wigs'] if w['id']!=wid]
    save_data(data)
    return redirect(f'/admin?key={ADMIN_KEY}')

if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)




