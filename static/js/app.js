async function api(url, options={}) {
  const opts={...options, headers:{'Content-Type':'application/json', ...(options.headers||{})}};
  const res=await fetch(url, opts);
  const data=await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data.error||'Ocurrió un error');
  return data;
}
function badgeEstado(e){
 const map={E:['Entregado','bg-blue-50 text-blue-700'],P:['Pendiente devolución','bg-amber-50 text-amber-700'],D:['Devuelto','bg-green-50 text-green-700']};
 const [t,c]=map[e]||[e,'bg-slate-100 text-slate-700'];
 return `<span class="badge ${c}">${e} · ${t}</span>`;
}
