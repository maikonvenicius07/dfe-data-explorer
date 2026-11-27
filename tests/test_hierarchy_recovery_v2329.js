const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const root=path.join(__dirname,'..'), src=fs.readFileSync(path.join(root,'public/app.js'),'utf8');
const code=src.slice(src.indexOf('function harmonizeDocumentRows()'),src.indexOf('\nfunction groupOptions()'));
function project(data,activeDocument){const nodes=data.nodes.map(n=>({...n,group:n.mocGroup}));vm.runInNewContext(code+'\nharmonizeDocumentRows();',{nodes,data,activeDocument});return nodes;}
const base=path.join(root,'public/data'), expected={nfcom:33,cte:20,bpeta:5,bpetm:5,bpe:5,cteos:5,nfag:5};
const sourceHashes={"bpeta": "77a6ad4ffb57292e6d2177cfed378b440bbb9444c1526a20c9336962fb87bb5e", "gtve": "89a96c9303af5cb00f7d1208fd54b9bef6e5bb3fbe9f8773d5f22ead8c58dfae", "bpetm": "77a6ad4ffb57292e6d2177cfed378b440bbb9444c1526a20c9336962fb87bb5e", "cteos": "89a96c9303af5cb00f7d1208fd54b9bef6e5bb3fbe9f8773d5f22ead8c58dfae", "mdfe": "6397e36096f1e51591fa50c9163a33689af19707f0afed1f9fafac7b476cccd5", "bpe": "77a6ad4ffb57292e6d2177cfed378b440bbb9444c1526a20c9336962fb87bb5e", "dce": "2eef6ce31ea0b5c3f0651400191f9145a5c0021381fc43f83b6ab15509fb0782", "nfag": "157e4598359da2cfbabfb38e95a0d4d23747d93d16f5d6f80acf03df1a60beaa", "nfcom": "2f997d953b81ff2c27c27b178739ec7e218e0ccf779ae22ae477ce43a4680339", "abi": "b95889cf8cc640713236aea364f9b857c1484b0a136f1e828df1ac98b7870369", "cte": "89a96c9303af5cb00f7d1208fd54b9bef6e5bb3fbe9f8773d5f22ead8c58dfae", "nfgas": "d103224db55810893930beaf59447f6c3aac423177b11e985779939b755e1fd9", "nf3e": "9b7fe85c763ebb07682cc96b482740432611fcfc9f287867377cfe3683152ac5"};
let total=0,before=0,recovered=0;
for(const dir of fs.readdirSync(base,{withFileTypes:true}).filter(x=>x.isDirectory())){
 const f=path.join(base,dir.name,'catalogo_atual.json');if(!fs.existsSync(f))continue;const data=JSON.parse(fs.readFileSync(f));const snapshot=JSON.stringify(data);const out=project(data,dir.name);const byId=new Map(out.map(n=>[n.id,n]));let rec=0,issues=0;
 for(let i=0;i<out.length;i++){const n=out[i],old=data.nodes[i];assert.equal(n.id,old.id);assert.equal(n.key,old.key);assert.equal(n.kind,old.kind);assert.equal(n.sourceLevel,old.sourceLevel);assert.deepEqual(n.original,old.original);if(old.parent)assert.equal(n.parent,old.parent);if(n.hierarchyRecovered){rec++;assert(old.hierarchyIssue);assert(!n.hierarchyIssue);assert(n.hierarchyEvidence);const p=byId.get(n.parent);assert(p);assert.equal(Number(n.sourceLevel),Number(p.sourceLevel)+1);if(n.sourceTable===p.sourceTable&&n.sourceSection===p.sourceSection)assert.equal(n.group,p.group);}
  if(n.hierarchyIssue)issues++;const seen=new Set([n.id]);let p=n.parent;while(byId.has(p)){assert(!seen.has(p));seen.add(p);p=byId.get(p).parent;}}
 assert.equal(JSON.stringify(data),snapshot);const isBaseline=data.metadata.sourceHash===sourceHashes[dir.name];if(isBaseline&&dir.name==='nf3e')assert.equal(issues,114);if(isBaseline&&dir.name==='nfcom'){assert(out.some(n=>n.tag==='imposto'&&n.hierarchyRecovered&&byId.get(n.parent).tag==='det'));assert(out.some(n=>n.tag==='gIBSCBS'&&n.hierarchyIssue));}
 if(isBaseline)assert.equal(rec,expected[dir.name]||0,dir.name);
 console.log(dir.name,'registros',out.length,'avisos origem',data.nodes.filter(n=>n.hierarchyIssue).length,'recuperados',rec,'pendentes',issues);
 total+=out.length;before+=data.nodes.filter(n=>n.hierarchyIssue).length;recovered+=rec;
}
console.log('TOTAL sem NF-e:',total,'avisos',before,'recuperados',recovered,'pendentes',before-recovered);
// Escopos distintos, pai explícito conflitante, nível ausente, tipo divergente, homônimos.
const row=(id,tag,level,kind,table,extra={})=>({id,key:id,tag,kind,sourceLevel:level,sourceTable:table,sourceSection:'s'+table,mocGroup:'g'+table,...extra});
const issue='Nível aponta para registro não estrutural';
let rows=[row('a','det','1','GS',1),row('b','imposto','2','G',2,{hierarchyIssue:issue}),row('c','outro','2','E',3,{hierarchyIssue:issue}),row('d','det','1','GS',3),row('e','v','2','E',3,{hierarchyIssue:issue,sourceValues:{officialParent:'outro'}}),row('f','v','','E',3,{hierarchyIssue:'Nível não numérico na fonte'}),row('g','v','2','E',3,{hierarchyIssue:issue}),row('h','pgto','1','E',3,{type:'C',sourceValues:{type:'C'}}),row('i','nPag','2','A',3,{hierarchyIssue:issue})];
let out=project({nodes:rows,metadata:{tables:[{number:1,scope:'a'},{number:2,scope:'a'},{number:3,scope:'b'}]}},'nfcom');assert.equal(out[1].parent,'a');assert.equal(out[1].group,'g2');assert(!out[2].parent);assert(!out[4].parent);assert(!out[5].parent);assert.equal(out[6].parent,'d');assert(!out[8].parent);

// Positive pgto rule, group reconciliation, source kind untouched; negative tag/level.
rows=[row('pg','pgto','2','E',1,{type:'G',sourceValues:{type:'G'}}),row('n','nPag','3','A',1,{hierarchyIssue:issue,mocGroup:'artificial'}),row('v','CNPJReceb','3','E',1,{hierarchyIssue:issue,mocGroup:'artificial'}),row('x','outro','3','E',1,{hierarchyIssue:issue})];
out=project({nodes:rows,metadata:{tables:[{number:1,scope:'a'}]}},'nfcom');assert.equal(out[1].parent,'pg');assert.equal(out[2].parent,'pg');assert.equal(out[2].group,'g1');assert.equal(out[0].kind,'E');assert(!out[3].parent);
