/* Registro de documentos e estado independente. Não contém lógica de renderização. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.DfeDocuments=factory()})(typeof globalThis==='object'?globalThis:this,function(){
'use strict';
const base='https://moc.sped.fazenda.pr.gov.br/';
const documents=[
 ['nfe','NF-e e NFC-e','NFe_NFCe/Leiaute.html',true],
 ['dce','DC-e','DCe/Leiaute.html',true],
 ['cte','CT-e / CT-e OS / GTVe','CTe/index.html',false],
 ['abi','NF-e ABI','NFe_ABI/VisaoGeral.html',false],
 ['nfgas','NFGAS','NFGAS/VisaoGeral.html',false],
 ['nfag','NFAG','NFAG/VisaoGeral.html',false],
 ['nf3e','NF3-e','NF3e/VisaoGeral.html',false],
 ['nfcom','NFCom','NFCom/VisaoGeral.html',false],
 ['bpe','BP-e','BPe/VisaoGeral.html',false],
 ['mdfe','MDF-e','MDFe/VisaoGeral.html',false]
].map(([id,label,path,available])=>Object.freeze({id,label,source:base+path,available}));
const get=id=>documents.find(d=>d.id===id);
function validateCatalog(id,cat){
 if(!Array.isArray(cat?.nodes)||!cat.nodes.length)throw Error('Catálogo vazio');
 const roots=cat.nodes.filter(n=>n.id==='ROOT'||n.order==='0');
 const expected={nfe:'NFe',dce:'DCe'}[id];
 if(!expected||!roots.some(n=>(n.tag||n.field)===expected))throw Error('Catálogo não corresponde ao documento ativo');
 if(cat.metadata?.documentId&&cat.metadata.documentId!==id)throw Error('Identificação do catálogo incompatível');
 return cat;
}
const presetKey=id=>id==='nfe'?'dfe.print.presets.v23':`dfe.print.presets.v23.${id}`;
return {documents,get,validateCatalog,presetKey};
});
