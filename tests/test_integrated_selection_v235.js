'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {HierarchicalSelection} = require('../public/selection.js');
const {DiagramState} = require('../public/diagram-state.js');
// B02 e W38: duas escolhas independentes; tags repetidas não colidem.
const records = [
 {key:'ROOT',id:'ROOT',tag:'NFe',group:'A',parentRef:null},
 {key:'A01',id:'A01',tag:'infNFe',group:'A',parentRef:'ROOT'},
 {key:'B01',id:'B01',tag:'ide',group:'B',parentRef:'A01'},
 {key:'B02',id:'B02',tag:'cUF',group:'B',parentRef:'B01'},
 {key:'B03',id:'B03',tag:'cNF',group:'B',parentRef:'B01'},
 {key:'W01',id:'W01',tag:'total',group:'W',parentRef:'A01'},
 {key:'W34',id:'W34',tag:'IBSCBSTot',group:'W',parentRef:'W01'},
 {key:'W36',id:'W36',tag:'gIBS',group:'W',parentRef:'W34'},
 {key:'W37',id:'W37',tag:'gIBSUF',group:'W',parentRef:'W36'},
 {key:'W38',id:'W38',tag:'vDif',group:'W',parentRef:'W37'},
 {key:'W43',id:'W43',tag:'vDif',group:'W',parentRef:'W36'},
];
const s = new HierarchicalSelection(records);
assert.equal(s.count(),0,'uma nova seleção não deve marcar nenhum registro');
const graph = new DiagramState(records);
graph.expandAll(); // expansão não afeta seleção
assert.equal(s.count(),0,'expandir não marca elementos');
s.changeKeys(['B02'],true);
assert.deepEqual([...s.selected],['B02']);
s.changeKeys(['W38'],true);
assert.equal(s.count(),2);
assert.equal(s.selected.has('W43'),false,'tags idênticas em caminhos distintos não se misturam');
assert.deepEqual(s.ancestors('W38'),['ROOT','A01','W01','W34','W36','W37']);
assert(s.contextKeys().has('ROOT'));
assert(s.contextKeys().has('W36'));
assert(!s.contextKeys().has('B03'));
s.changeKeys(['W36'],true);
assert.equal(s.selected.has('W37'),false,'marcar grupo seleciona somente o registro');
s.changeKeys(s.descendants('W36'),true);
assert.equal(s.selected.has('W38'),true,'seleção explícita de descendentes');
assert.equal(s.selected.has('W43'),true,'seleção explícita alcança outro ramo');
s.changeKeys(['W43'],false);
assert.equal(s.selected.has('W38'),true,'desmarcar um ramo não remove outro');
const src=fs.readFileSync(path.join(__dirname,'../public/app.js'),'utf8');
for (const token of ['integratedMoc(scope)','integratedHierarchy(scope)','integratedDictionary(scope)','integratedDiagram(scope)', 'printSectionTree','printSectionMoc','printSectionDict','printSectionDiagram','data-diagram-check'])assert(src.includes(token),token);
assert(!src.includes('printSelection.changeNode(el.dataset.treeKey,el.checked)'), 'a caixa de seleção de um grupo não deve marcar seus descendentes');
console.log('PASS V2.3.5: seleção individual, ancestrais de contexto, campos homônimos, quatro seções e comando explícito de descendentes');
