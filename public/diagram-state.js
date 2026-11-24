/* DF-e V2.3.4 — estado do diagrama: expansão independente, sem alteração da seleção de impressão. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.DfeDiagramState=factory();})(typeof globalThis==='object'?globalThis:this,function(){'use strict';
class DiagramState{
 constructor(nodes){this.reset(nodes)}
 reset(nodes){this.nodes=nodes||[];this.map=new Map(this.nodes.map(n=>[n.key,n]));this.parent=new Map();this.children=new Map();const ids=new Map();for(const n of this.nodes){if(!ids.has(n.id))ids.set(n.id,[]);ids.get(n.id).push(n)}for(const n of this.nodes){const candidates=ids.get(n.parentRef)||[];if(candidates.length!==1||candidates[0].key===n.key)continue;const p=candidates[0];this.parent.set(n.key,p.key);const arr=this.children.get(p.key)||[];arr.push(n.key);this.children.set(p.key,arr)}this.open=new Set();for(const n of this.nodes)if(n.id==='ROOT'||n.id==='A01')this.open.add(n.key)}
 hasChildren(key){return (this.children.get(key)||[]).length>0}
 toggle(key){if(this.open.has(key))this.open.delete(key);else if(this.hasChildren(key))this.open.add(key)}
 setOpen(key,value){if(value&&this.hasChildren(key))this.open.add(key);else this.open.delete(key)}
 expandAll(){this.open=new Set([...this.children.keys()])}
 collapseAll(){this.open.clear();for(const n of this.nodes)if(n.id==='ROOT'||n.id==='A01')this.open.add(n.key)}
 reveal(key){const seen=new Set();let cur=key;while(this.parent.has(cur)&&!seen.has(cur)){seen.add(cur);cur=this.parent.get(cur);this.open.add(cur)}}
 branchRoots(group,focus){if(focus&&this.map.has(focus))return [focus];if(group==='__ALL__'){const r=this.nodes.filter(n=>n.id==='ROOT');return r.length?r.map(n=>n.key):this.nodes.filter(n=>!this.parent.has(n.key)).map(n=>n.key)}const scoped=this.nodes.filter(n=>n.group===group),set=new Set(scoped.map(n=>n.key));return scoped.filter(n=>!set.has(this.parent.get(n.key))).map(n=>n.key)}
 visible(group,focus,all=false){const items=[],seen=new Set(),roots=this.branchRoots(group,focus),stack=roots.map(key=>({key,d:0})).reverse();while(stack.length){const {key,d}=stack.pop();if(seen.has(key))continue;seen.add(key);const n=this.map.get(key);if(!n)continue;if(group!=='__ALL__'&&n.group!==group)continue;items.push({n,d});if(all||this.open.has(key)){const kids=this.children.get(key)||[];for(let i=kids.length-1;i>=0;i--)stack.push({key:kids[i],d:d+1})}}return items}
}
return {DiagramState};
});
