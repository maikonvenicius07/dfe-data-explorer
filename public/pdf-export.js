/* PDF vetorial local, sem dependências externas. Consome o documento de impressão já selecionado.
 * Fontes PDF padrão Helvetica/WinAnsi; português e pontuação ocidental pesquisáveis.
 * Não usa driver do Windows nem imprime a captura da tela. */
(function(global){
'use strict';
function createPDF(root,opts={}){
 const mm=72/25.4,land=opts.orientation==='landscape',paper=opts.paper==='A3'?[297,420]:[210,297],W=paper[land?1:0]*mm,H=paper[land?0:1]*mm,M=(opts.margin||12)*mm,F=opts.font||10,mono=!!opts.mono,U=W-2*M,B=H-M-15;
 const profile=opts.profile||{},compact=!!profile.compact;
 const cv=document.createElement('canvas').getContext('2d'),pages=[];let ops=[],y=M;
 const num=n=>Number(n.toFixed(3));
 const cp={ '€':128,'‚':130,'ƒ':131,'„':132,'…':133,'†':134,'‡':135,'ˆ':136,'‰':137,'Š':138,'‹':139,'Œ':140,'Ž':142,'‘':145,'’':146,'“':147,'”':148,'•':149,'–':150,'—':151,'˜':152,'™':153,'š':154,'›':155,'œ':156,'ž':158,'Ÿ':159 };
 function normalized(v){return String(v??'').replace(/[├└┌┬┼]/g,'+').replace(/[─━]/g,'-').replace(/[│┃]/g,'|').replace(/→/g,'->').replace(/←/g,'<-').replace(/−/g,'-').replace(/\u00a0/g,' ').replace(/\s+/g,' ').trim();}
 function hex(v){return [...normalized(v)].map(c=>{let n=c.charCodeAt(0);if(n>255)n=cp[c]||63;return n.toString(16).padStart(2,'0');}).join('');}
 function rgb(c){if(mono&&c!=='#ffffff'&&c!=='#fff'){if(/^#(?:e|f|d)/i.test(c))return '.95 .95 .95';return '.22 .22 .22';}let a=String(c||'#000').replace('#','');if(a.length===3)a=a.replace(/./g,x=>x+x);if(!/^[0-9a-f]{6}$/i.test(a))a='000000';return [0,2,4].map(i=>num(parseInt(a.slice(i,i+2),16)/255)).join(' ');}
 function text(t,x,top,fs=F,bold=false,color='#17384f'){if(!t)return;ops.push(`${rgb(color)} rg BT /${bold?'F2':'F1'} ${num(fs)} Tf 1 0 0 1 ${num(x)} ${num(H-top)} Tm <${hex(t)}> Tj ET`);}
 function rect(x,top,w,h,fill,stroke=null,sw=.7,dash=false,radius=0){const r=Math.min(radius,w/2,h/2),Y=H-top;let shape=`${num(x)} ${num(Y-h)} ${num(w)} ${num(h)} re`;if(r>0){const a=.55228475*r,pt=(u,v)=>`${num(u)} ${num(v)}`;shape=`${pt(x+r,Y)} m ${pt(x+w-r,Y)} l ${pt(x+w-r+a,Y)} ${pt(x+w,Y-r+a)} ${pt(x+w,Y-r)} c ${pt(x+w,Y-h+r)} l ${pt(x+w,Y-h+r-a)} ${pt(x+w-r+a,Y-h)} ${pt(x+w-r,Y-h)} c ${pt(x+r,Y-h)} l ${pt(x+r-a,Y-h)} ${pt(x,Y-h+r-a)} ${pt(x,Y-h+r)} c ${pt(x,Y-r)} l ${pt(x,Y-r+a)} ${pt(x+r-a,Y)} ${pt(x+r,Y)} c h`;}ops.push(`q ${fill?rgb(fill)+' rg':''} ${stroke?rgb(stroke)+' RG '+num(sw)+' w '+(dash?'[3 2] 0 d':'[] 0 d'):''} ${shape} ${fill&&stroke?'B':fill?'f':'S'} Q`);}
 function line(x1,t1,x2,t2,color='#b5cad3',sw=.7){ops.push(`q ${rgb(color)} RG ${num(sw)} w ${num(x1)} ${num(H-t1)} m ${num(x2)} ${num(H-t2)} l S Q`);}
 function measure(t,fs,bold=false){cv.font=`${bold?'bold ':''}${fs*96/72}px Arial`;return cv.measureText(t).width*72/96;}
 function wrap(t,width,fs,bold=false){const a=[];let cur='';for(let w of normalized(t).split(' ')){if(cur&&measure(cur+' '+w,fs,bold)>width){a.push(cur);cur='';}while(w.length>1&&measure(w,fs,bold)>width){let n=1;while(n<w.length&&measure(w.slice(0,n+1),fs,bold)<=width)n++;a.push(w.slice(0,n));w=w.slice(n);}if(w)cur+=(cur?' ':'')+w;}if(cur)a.push(cur);return a.length?a:[''];}
 function finish(){if(!ops.length)return;line(M,H-M-9,W-M,H-M-9);text('DF-e Data Explorer · V2.3.25',M,H-M+2,7,false,'#526779');text('Página '+(pages.length+1),W-M-45,H-M+2,7,false,'#526779');pages.push(ops.join('\n'));ops=[];y=M;}
 function need(h){if(y+h>B&&ops.length)finish();}
 function paragraph(t,fs=F,bold=false,color='#17384f',indent=0){const a=wrap(t,U-indent,fs,bold);for(const l of a){need(fs+4);y+=fs+(compact?0:2);text(l,M+indent,y,fs,bold,color);y+=compact?1:2;}y+=compact?2:4;}
 function heading(t,fs=F+4){need(fs*2+12);paragraph(t,fs,true);line(M,y,W-M,y,'#286080',.9);y+=6;}
 function table(el){
 const hierarchical=el.classList.contains('print-hierarchy-table');
 const hr=el.tHead?.querySelector('tr:has(th)')||el.querySelector('tr');if(!hr)return;
 const hs=[...hr.children],header=hs.map(c=>normalized(c.textContent)),n=header.length;if(!n)return;
 const rs=[...el.querySelectorAll('tbody tr')],weights=hs.map((h,i)=>Number(h.dataset.weight)||(/descri|observa|xpath/i.test(header[i])?3.4:/campo|grupo|elemento/i.test(header[i])?1.6:/^#|^ele$|^pai$|ocor|tam|tipo/i.test(header[i])?.8:1.1)),total=weights.reduce((a,b)=>a+b,0),widths=weights.map(w=>U*w/total),fs=profile.fs||Math.max(7,F-1.5),lh=compact?fs*(profile.line||1.1):fs+3,pad=compact?Math.max(2,profile.pad*1.5):7,topPad=compact?pad/2:4;
 const fieldIndex=hs.findIndex(h=>h.dataset.mocCol==='2'),step=Number(el.dataset.indentStep)||0;
 const groupTitle=el.dataset.groupTitle||'';const cellPad=i=>el.closest('.print-physical-page')&&['0','1','4','5','6','7','8'].includes(hs[i].dataset.mocCol)?1:3.5;
 const kind=r=>hierarchical?r.dataset.kind||'element':'element';
 const indent=r=>hierarchical&&fieldIndex>=0?(Number(r.dataset.depth)||0)*step:0;
 const cells=(r,head=false)=>hs.map((_,i)=>{const c=r.children[i],isField=i===fieldIndex&&!head,off=isField?indent(r)+8:0;
 if(isField){const tag=c?.querySelector('.print-field-tag')?.textContent||'',ctx=c?.querySelector('.print-field-context')?.textContent||'',label=c?.querySelector('.print-branch-label')?.textContent||'',width=Math.max(8,widths[i]-7-off);return [...wrap(tag,width,fs,kind(r)==='structural').map(t=>({t,b:kind(r)==='structural'})),...(label?wrap(label,width,fs-1,true).map(t=>({t,b:true,label:true})):[]),...(ctx?wrap(ctx,width,fs-1,false).map(t=>({t,b:false,context:true})):[])];}
 return wrap(c?.textContent||'',Math.max(8,widths[i]-2*cellPad(i)),fs,head).map(t=>({t,b:head}));});
 function draw(r,a,start,count,head,index){const hh=count*lh+pad;let x=M;const structural=kind(r)==='structural',depth=Number(r.dataset.depth)||0,attr=kind(r)==='attribute';
 const fills=mono?['#dedede','#dddddd','#e8e8e8','#f0f0f0']:['#c5dce8','#c9e3d2','#d5e9db','#e3efdf'];
 for(let i=0;i<n;i++){const isField=i===fieldIndex&&!head,d=isField?indent(r):0,off=isField?d+8:0;const fill=head?(mono?'#444444':i%2?'#347958':'#28658e'):structural?fills[Math.min(depth,3)]:attr?(mono?'#f1f1f1':'#fffaf0'):index%2?'#f3f7fa':'#fff';
 rect(x,y,widths[i],hh,fill,'#d1dce3',.35);
 if(structural&&!head&&start===0)line(x,y,x+widths[i],y,mono?'#666666':'#67968a',1.2);
 if(isField){const ink=mono?'#333333':'#316c76',lane=l=>x+3.5+4+(l-1)*step,mid=y+fs*.55+topPad;
  for(const l of (r.dataset.rails||'').split(',').filter(Boolean).map(Number))line(lane(l),y,lane(l),y+hh,ink,1.65);
  if(depth>0){line(lane(depth),y,lane(depth),r.dataset.tail==='true'||start+count<a[i].length?y+hh:mid,ink,1.65);if(start===0)line(lane(depth),mid,lane(depth)+step+1,mid,ink,1.65);}
  if(r.dataset.child==='true')line(lane(depth+1),mid,lane(depth+1),y+hh,ink,1.65);
  const ends=(r.dataset.ends||'').split(',').filter(Boolean).map(Number);if(ends.length&&start+count>=Math.max(...a.map(c=>c.length)))line(lane(Math.min(...ends)),y+hh-1,x+widths[i],y+hh-1,mono?'#666666':'#67968a',1);
 }
 const visible=a[i].slice(start,start+count),offset=0;
 for(let j=0;j<visible.length;j++){const l=visible[j];text(l.t,x+cellPad(i)+off,y+fs+topPad+j*lh+offset,l.context||l.label?(compact?Math.max(7,fs-1):fs-1):fs,l.b,head?'#ffffff':l.context?'#576b76':l.label?'#365e54':'#17384f');}x+=widths[i];}y+=hh;}
 const ha=cells(hr,true),hn=Math.max(...ha.map(a=>a.length)),headerH=hn*lh+pad;
 const groupLines=groupTitle?wrap(groupTitle+' (continuação)',U-14,fs+1,true):[],groupH=groupLines.length?(groupLines.length*(fs+4)+8):0;
 function drawHeader(continued=false,firstRow=null){if(groupTitle){const a=wrap(groupTitle+(continued?' (continuação)':''),U-14,fs+1,true),h=a.length*(fs+(compact?2:4))+(compact?4:8);rect(M,y,U,h,mono?'#eeeeee':'#e2f2e8');rect(M,y,3,h,mono?'#444444':'#b58e42');a.forEach((l,j)=>text(l,M+8,y+fs+(compact?2:5)+j*(fs+(compact?2:4)),fs+1,true));y+=h+3;}if(continued&&firstRow?.dataset.path){const a=wrap('Caminho na continuação: '+firstRow.dataset.path,U-12,Math.max(7,fs-1));for(const l of a){text(l,M+5,y+fs,Math.max(7,fs-1),false,'#576b76');y+=fs+3;}y+=3;}draw(hr,ha,0,hn,true,0);}
 const first=rs.length?Math.max(...cells(rs[0]).map(a=>a.length)):1;
 need(groupH+3+headerH+Math.min(first,Math.max(1,Math.floor((B-M-headerH-groupH-10)/lh)))*lh+pad);drawHeader(el.dataset.continued==='true',rs[0]);
 const prepared=rs.map(r=>{const a=cells(r);return {r,a,max:Math.max(...a.map(l=>l.length))};});
 const rowHeight=o=>o.max*lh+pad;
 for(let i=0;i<prepared.length;i++){const {r,a,max}=prepared[i];let start=0;
  // Paginação por linha, sem deslocar ramificações ou caudas inteiras.
  while(start<max){let cap=Math.floor((B-y-pad)/lh);const fresh=Math.floor((B-M-headerH-groupH-45)/lh);if(cap<1||((max-start)<=fresh&&(max-start)>cap)){finish();drawHeader(true,r);cap=Math.floor((B-y-pad)/lh);}const count=Math.min(max-start,Math.max(1,cap));draw(r,a,start,count,false,i);start+=count;if(start<max){finish();drawHeader(true,r);}}
 }y+=9;}
 function svgFigure(fig){const svg=fig.querySelector('svg');if(!svg){paragraph(fig.textContent);return;}const vb=svg.getAttribute('viewBox').split(/\s+/).map(Number),sw=vb[2],sh=vb[3],widthAttr=Number(svg.getAttribute('width'))||sw,heightAttr=Number(svg.getAttribute('height'))||sh;let k=Math.min(U/sw,(B-M-24)/sh,widthAttr*.75/sw,heightAttr*.75/sh);let height=sh*k;need(height+24);paragraph(fig.querySelector('figcaption')?.textContent||'Diagrama XML',Math.max(8,F-1),true);if(y+height>B){finish();}const ox=M,oy=y;
 function path(d,dx,dy,stroke,width){let a=d.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/gi)||[],i=0,px=0,py=0,cmd=[];const X=v=>num(ox+(dx+v)*k),Y=v=>num(H-oy-(dy+v)*k),read=()=>Number(a[i++]);while(i<a.length){const op=a[i++];if(op==='M'||op==='L'){px=read();py=read();cmd.push(`${X(px)} ${Y(py)} ${op==='M'?'m':'l'}`);}else if(op==='H'){px=read();cmd.push(`${X(px)} ${Y(py)} l`);}else if(op==='V'){py=read();cmd.push(`${X(px)} ${Y(py)} l`);}else if(op==='C'){const x1=read(),y1=read(),x2=read(),y2=read();px=read();py=read();cmd.push(`${X(x1)} ${Y(y1)} ${X(x2)} ${Y(y2)} ${X(px)} ${Y(py)} c`);}else return;}
 ops.push(`q ${rgb(stroke)} RG ${num(width*k)} w ${cmd.join(' ')} S Q`);}
 function walk(el,dx=0,dy=0){const tag=el.tagName.toLowerCase(),v=(name,d=0)=>Number(el.getAttribute(name)||d),tr=el.getAttribute('transform');if(tr){const a=tr.match(/translate\(([-\d.]+)[ ,]+([-\d.]+)\)/);if(a){dx+=Number(a[1]);dy+=Number(a[2]);}}if(tag==='rect'){const x=ox+(dx+v('x'))*k,top=oy+(dy+v('y'))*k,w=v('width')*k,h=v('height')*k;rect(x,top,w,h,el.getAttribute('fill')||'#fff',el.getAttribute('stroke'),v('stroke-width',1)*k,!!el.getAttribute('stroke-dasharray'),v('rx')*k);}else if(tag==='path'){path(el.getAttribute('d')||'',dx,dy,el.getAttribute('stroke')||'#8badc1',v('stroke-width',1.7));}else if(tag==='text'){text(el.textContent,ox+(dx+v('x'))*k,oy+(dy+v('y'))*k,v('font-size',12)*k,el.getAttribute('font-weight')==='bold',el.getAttribute('fill')||'#17384f');}else for(const c of el.children)walk(c,dx,dy);}
 walk(svg);y+=height+10;}
 function visit(el){if(el.nodeType!==1)return;const tag=el.tagName.toLowerCase(),cl=el.classList;if(cl.contains('print-physical-page')||cl.contains('print-integrated-section')){if(ops.length)finish();}if(tag==='figure'&&el.querySelector('svg')){svgFigure(el);return;}if(tag==='table'){table(el);return;}if(/^h[1-4]$/.test(tag)){heading(el.textContent,tag==='h1'?F+8:tag==='h2'?F+4:F+2);return;}if(cl.contains('print-integrated-tree-row')){const d=Number(el.style.getPropertyValue('--indent'))||0;paragraph(el.textContent.replace(/(CONTEXTO|SELECIONADO)/g,' · $1'),Math.max(8,F-1),false,'#17384f',Math.min(d*10,U/3));return;}if(['p','li','pre'].includes(tag)){paragraph(el.textContent,cl.contains('print-source')?Math.max(7,F-2):F);return;}if(cl.contains('print-cover')){for(const c of el.children)visit(c);finish();return;}if(el.children.length){for(const c of el.children)visit(c);}else if(el.textContent.trim())paragraph(el.textContent);}
 visit(root);finish();if(opts.measureOnly)return pages.length;if(!pages.length)throw new Error('Nenhum conteúdo para gerar PDF.');
 const objects=['','<< /Type /Catalog /Pages 2 0 R >>','', '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>','<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>'];const refs=[];for(const stream of pages){const id=objects.length;refs.push(id+' 0 R');objects.push(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${num(W)} ${num(H)}] /Rotate 0 /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents ${id+1} 0 R >>`,`<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`);}objects[2]=`<< /Type /Pages /Count ${refs.length} /Kids [${refs.join(' ')}] >>`;let pdf='%PDF-1.4\n',offsets=[0];for(let i=1;i<objects.length;i++){offsets.push(pdf.length);pdf+=`${i} 0 obj\n${objects[i]}\nendobj\n`;}const xref=pdf.length;pdf+=`xref\n0 ${objects.length}\n0000000000 65535 f \n${offsets.slice(1).map(n=>String(n).padStart(10,'0')+' 00000 n \n').join('')}trailer\n<< /Size ${objects.length} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;return new Blob([pdf],{type:'application/pdf'});
}
global.DfePdfExport={createPDF,version:'2.3.25'};
})(globalThis);
