async function loadPanolDashboard(){
 const d=await api('/api/dashboard/');
 document.getElementById('dActivos').textContent=d.activos;
 document.getElementById('dDevueltos').textContent=d.devueltos_hoy;
 document.getElementById('dStock').textContent=d.fuera_stock;
 document.getElementById('dMermas').textContent=d.mermas;
 document.getElementById('dUltimas').innerHTML=d.ultimas.map(x=>`<tr class="border-t"><td class="p-4 font-bold">#${x.id}</td><td class="p-4">${x.solicitante}</td><td class="p-4">${x.asignatura}</td><td class="p-4">${x.fecha}</td><td class="p-4"><span class="badge ${x.estado==='APROBADO'?'bg-green-50 text-green-700':'bg-amber-50 text-amber-700'}">${x.estado}</span></td></tr>`).join('');
}
let prestamos=[], selectedLoan=null;
async function loadPrestamos(){
 const d=await api('/api/prestamos/');prestamos=d.items||[];renderPrestamos(prestamos);
 document.getElementById('filtroPrestamo').addEventListener('input',e=>{const q=e.target.value.toLowerCase();renderPrestamos(prestamos.filter(x=>(x.solicitante+x.articulo).toLowerCase().includes(q)))});
}
function renderPrestamos(items){
 document.getElementById('tablaPrestamos').innerHTML=items.map(x=>`<tr class="border-t"><td class="p-4">#${x.solicitud}</td><td class="p-4 font-semibold">${x.solicitante}</td><td class="p-4">${x.articulo}</td><td class="p-4 text-center">${x.cantidad}</td><td class="p-4">${badgeEstado(x.estado)}</td><td class="p-4">${x.estado!=='D'?`<button onclick="openModal(${x.id})" class="btn btn-primary text-xs">Registrar devolución</button>`:'<span class="text-success font-semibold">✓ Cerrado</span>'}</td></tr>`).join('');
}
function openModal(id){selectedLoan=id;const x=prestamos.find(p=>p.id===id);document.getElementById('modalInfo').textContent=`Solicitud #${x.solicitud} · ${x.solicitante} · ${x.articulo}`;document.getElementById('modal').classList.remove('hidden');document.getElementById('modal').classList.add('flex')}
function closeModal(){document.getElementById('modal').classList.add('hidden');document.getElementById('modal').classList.remove('flex')}
async function confirmarDevolucion(){
 await api(`/api/prestamos/${selectedLoan}/devolucion/`,{method:'POST',body:JSON.stringify({observaciones:document.getElementById('obs').value,vbo_panol:document.getElementById('vbo').value})});
 closeModal();loadPrestamos();
}
async function loadInventario(){
 const d=await api('/api/catalogo/');window.inv=d.items;
 document.getElementById('catInv').innerHTML='<option value="">Todas las categorías</option>'+d.categorias.map(c=>`<option value="${c.id_categoria}">${c.nombre_categoria}</option>`).join('');
 renderInv(d.items);
 document.getElementById('buscarInv').addEventListener('input',filterInv);document.getElementById('catInv').addEventListener('change',filterInv);
}
function filterInv(){const q=document.getElementById('buscarInv').value.toLowerCase(),c=document.getElementById('catInv').value;renderInv(window.inv.filter(x=>x.nombre.toLowerCase().includes(q)&&(!c||x.categoria===document.querySelector('#catInv option:checked').textContent)))}
function renderInv(items){document.getElementById('tablaInventario').innerHTML=items.map(x=>`<tr class="border-t"><td class="p-4 font-semibold">${x.nombre}<p class="text-xs text-steel">${x.codigo}</p></td><td class="p-4">${x.categoria}</td><td class="p-4 text-center">${x.stock}</td><td class="p-4 text-center font-bold">${x.disponible}</td><td class="p-4 text-center">${x.reparable}</td><td class="p-4 text-center">${x.malo}</td><td class="p-4">${x.lugar}</td></tr>`).join('')}
async function loadMermas(){
 const cat=await api('/api/catalogo/');document.getElementById('mArticulo').innerHTML=cat.items.map(x=>`<option value="${x.id}">${x.nombre}</option>`).join('');renderMermas((await api('/api/mermas/')).items);
 document.getElementById('mermaForm').addEventListener('submit',async e=>{e.preventDefault();await api('/api/mermas/',{method:'POST',body:JSON.stringify({id_articulo:document.getElementById('mArticulo').value,periodo_academico:document.getElementById('mPeriodo').value,tipo_merma:document.getElementById('mTipo').value,cantidad:document.getElementById('mCantidad').value,marca:document.getElementById('mMarca').value,modelo_serie:document.getElementById('mModelo').value,observaciones:document.getElementById('mObs').value})});e.target.reset();renderMermas((await api('/api/mermas/')).items);});
}
function renderMermas(items){document.getElementById('tablaMermas').innerHTML=items.map(x=>`<tr class="border-t"><td class="p-4 font-semibold">${x.articulo}</td><td class="p-4">${x.periodo}</td><td class="p-4"><span class="badge bg-red-50 text-red-700">${x.tipo}</span></td><td class="p-4 text-center">${x.cantidad}</td><td class="p-4">${x.observaciones}</td></tr>`).join('')}
