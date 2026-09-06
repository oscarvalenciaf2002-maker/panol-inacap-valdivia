async function loadUserDashboard(){
 const d=await api('/api/solicitudes/');
 const items=d.items||[];
 document.getElementById('uTotal').textContent=items.length;
 document.getElementById('uPend').textContent=items.filter(x=>x.estado_solicitud==='PENDIENTE DE APROBACIÓN').length;
 document.getElementById('uUso').textContent=items.flatMap(x=>x.items).filter(x=>x.estado==='P').length;
 document.getElementById('uRecent').innerHTML=items.slice(0,5).map(x=>`<tr class="border-t"><td class="p-4 font-bold">#${x.id}</td><td class="p-4">${x.asignatura}</td><td class="p-4">${x.fecha}</td><td class="p-4"><span class="badge ${x.estado_solicitud==='PENDIENTE DE APROBACIÓN'?'bg-amber-50 text-amber-700':'bg-green-50 text-green-700'}">${x.estado_solicitud}</span></td></tr>`).join('');
}
let carrito=[];
async function initSolicitud(){
 const [as,cat]=await Promise.all([api('/api/asignaturas/'),api('/api/catalogo/')]);
 document.getElementById('asignatura').innerHTML='<option value="">Seleccionar...</option>'+as.items.map(x=>`<option value="${x.id_asignatura}">${x.codigo_asignatura} · ${x.nombre_asignatura}</option>`).join('');
 renderCatalogo(cat.items);
 window.catalogo=cat.items;
 document.getElementById('buscarArticulo').addEventListener('input',e=>renderCatalogo(window.catalogo.filter(x=>x.nombre.toLowerCase().includes(e.target.value.toLowerCase()))));
 document.getElementById('solicitudForm').addEventListener('submit',submitSolicitud);
}
function renderCatalogo(items){
 document.getElementById('catalogo').innerHTML=items.map(x=>`<div class="border border-line rounded-2xl p-4 hover:border-red-200 transition"><div class="flex justify-between gap-3"><div><p class="font-bold">${x.nombre}</p><p class="text-xs text-steel">${x.categoria} · ${x.lugar||'Sin ubicación'}</p></div><span class="badge ${x.disponible>0?'bg-green-50 text-green-700':'bg-red-50 text-red-700'}">${x.disponible} disp.</span></div><button ${x.disponible<1?'disabled':''} onclick="addItem(${x.id})" class="btn btn-secondary w-full mt-3 ${x.disponible<1?'opacity-40 cursor-not-allowed':''}">Agregar</button></div>`).join('');
}
function addItem(id){
 if(carrito.length>=10)return alert('Máximo 10 ítems.');
 const a=window.catalogo.find(x=>x.id===id); const existing=carrito.find(x=>x.id===id);
 if(existing){ if(existing.cantidad<a.disponible) existing.cantidad++; } else carrito.push({id:a.id,nombre:a.nombre,cantidad:1,max:a.disponible});
 renderCarrito();
}
function renderCarrito(){
 document.getElementById('carrito').innerHTML=carrito.length?carrito.map((x,i)=>`<div class="flex items-center gap-3 border rounded-xl p-3"><div class="flex-1"><b>${x.nombre}</b><p class="text-xs text-steel">Disponible: ${x.max}</p></div><input type="number" min="1" max="${x.max}" value="${x.cantidad}" onchange="setQty(${i},this.value)" class="input w-24"><button onclick="removeItem(${i})" class="text-inacap font-bold">Eliminar</button></div>`).join(''):'<p class="text-sm text-steel">Aún no agregas herramientas.</p>';
}
function setQty(i,v){carrito[i].cantidad=Math.min(Math.max(1,parseInt(v)||1),carrito[i].max);renderCarrito()}
function removeItem(i){carrito.splice(i,1);renderCarrito()}
async function submitSolicitud(e){
 e.preventDefault();
 if(!carrito.length)return alert('Agrega al menos una herramienta.');
 try{
  const d=await api('/api/solicitudes/',{method:'POST',body:JSON.stringify({id_asignatura:document.getElementById('asignatura').value,seccion:document.getElementById('seccion').value,nombre_docente:document.getElementById('docente').value,firma_solicitante:true,items:carrito.map(x=>({id_articulo:x.id,cantidad:x.cantidad}))})});
  const m=document.getElementById('msg');m.className='mt-4 p-3 rounded-xl text-sm bg-green-50 text-green-700';m.textContent=`Solicitud #${d.id_solicitud} enviada correctamente.`;m.classList.remove('hidden');
  carrito=[];renderCarrito();
 }catch(err){alert(err.message)}
}
async function loadMisPrestamos(){
 const d=await api('/api/solicitudes/');
 document.getElementById('misPrestamos').innerHTML=d.items.map(x=>`<article class="card p-5"><div class="flex justify-between gap-3"><div><p class="text-xs text-steel">Solicitud #${x.id}</p><h2 class="font-extrabold mt-1">${x.asignatura}</h2></div><span class="badge ${x.estado_solicitud==='PENDIENTE DE APROBACIÓN'?'bg-amber-50 text-amber-700':'bg-green-50 text-green-700'}">${x.estado_solicitud}</span></div><p class="text-sm text-steel mt-3">${x.seccion} · Docente: ${x.docente}</p><div class="mt-4 space-y-2">${x.items.map(i=>`<div class="flex justify-between border rounded-xl p-3"><span>${i.nombre} × ${i.cantidad}</span>${badgeEstado(i.estado)}</div>`).join('')}</div></article>`).join('')||'<p class="text-steel">No hay solicitudes.</p>';
}
