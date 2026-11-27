/* Registro multidocumento. Disponibilidade deriva dos catálogos publicados. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.DfeDocuments=factory()})(typeof globalThis==='object'?globalThis:this,function(){
'use strict';
const base='https://moc.sped.fazenda.pr.gov.br/';
const rows=[
 ['nfe','NF-e e NFC-e','NFe_NFCe','NFe'],['dce','DC-e','DCe','DCe'],
 ['cte','CT-e / CT-e OS / GTVe','CTe','infCte'],['cteos','CT-e OS','CTe','infCte','cte'],['gtve','GTVe','CTe','infCte','cte'],
 ['abi','NF-e ABI','NFe_ABI','NFeABI'],['nfgas','NFGAS','NFGAS','infNFGas'],['nfag','NFAG','NFAG','infNFAg'],['nf3e','NF3-e','NF3e','infNF3e'],['nfcom','NFCom','NFCom','infNFCom'],
 ['bpe','BP-e','BPe','infBPe'],['bpetm','BP-e TM','BPe','infBPe','bpe'],['bpeta','BP-e TA','BPe','infBPe','bpe'],['mdfe','MDF-e','MDFe','infMDFe']];
let registry={dce:{rows:111}};
const documents=rows.map(([id,label,folder,rootTag,family])=>Object.freeze({id,label,source:base+folder+'/Leiaute.html',rootTag,family:family||id,get available(){return id==='nfe'||Number(registry[id]?.rows)>0;}}));
const get=id=>documents.find(d=>d.id===id);
function configure(r){registry={...(r||{})};}
function validateCatalog(id,cat){
 const doc=get(id);if(!doc||!Array.isArray(cat?.nodes)||!cat.nodes.length)throw Error('Catálogo vazio ou documento desconhecido');
 if(!cat.nodes.some(n=>String(n.tag||n.field).toLowerCase()===doc.rootTag.toLowerCase()))throw Error('Catálogo não corresponde ao documento ativo');
 if((id!=='nfe'&&cat.metadata?.documentId!==id)||(cat.metadata?.documentId&&cat.metadata.documentId!==id))throw Error('Identificação do catálogo incompatível');
 const keys=cat.nodes.map(n=>String(n.key||n.id));if(id!=='nfe'&&new Set(keys).size!==keys.length)throw Error('Chaves internas duplicadas');
 return cat;
}
const presetKey=id=>id==='nfe'?'dfe.print.presets.v23':`dfe.print.presets.v23.${id}`;
return {documents,get,configure,validateCatalog,presetKey};
});
