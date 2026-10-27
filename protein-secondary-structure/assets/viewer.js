const viewerMeta={
  '1tua':{title:'APE0754 · KH-domain protein',organism:'Aeropyrum pernix',resolution:'1.50 Å',method:'X-ray diffraction'},
  '1tuv':{title:'YgiN · quinol monooxygenase',organism:'Escherichia coli',resolution:'1.70 Å',method:'X-ray diffraction'},
  '1tvg':{title:'PP25 · HSPC034 protein',organism:'Homo sapiens',resolution:'1.60 Å',method:'X-ray diffraction'}
};
const aa3={ALA:'A',ARG:'R',ASN:'N',ASP:'D',CYS:'C',GLN:'Q',GLU:'E',GLY:'G',HIS:'H',ILE:'I',LEU:'L',LYS:'K',MET:'M',PHE:'F',PRO:'P',SER:'S',THR:'T',TRP:'W',TYR:'Y',VAL:'V',MSE:'M'};
const colors={H:'#9b67e5',G:'#9b67e5',I:'#9b67e5',E:'#3787ef',B:'#3787ef',T:'#ff6a24',S:'#47ca82','-':'#9c9c9c'};
const testById=Object.fromEntries(window.PROTEIN_DATA.map(item=>[item.id,item]));
const canvas=document.getElementById('structure-canvas'),ctx=canvas.getContext('2d');
let current='1tua',rotationX=-.38,rotationY=.52,zoom=1,dragging=false,lastX=0,lastY=0,autoRotate=false,frame=0;

function align(reference,observed){
  const n=reference.length,m=observed.length,gap=-2,match=2,mismatch=-1;
  const scores=Array.from({length:n+1},()=>new Int16Array(m+1));
  const path=Array.from({length:n+1},()=>new Uint8Array(m+1));
  for(let i=1;i<=n;i++){scores[i][0]=i*gap;path[i][0]=1}
  for(let j=1;j<=m;j++){scores[0][j]=j*gap;path[0][j]=2}
  for(let i=1;i<=n;i++)for(let j=1;j<=m;j++){
    const diagonal=scores[i-1][j-1]+(reference[i-1]===observed[j-1]?match:mismatch);
    const up=scores[i-1][j]+gap,left=scores[i][j-1]+gap;
    if(diagonal>=up&&diagonal>=left){scores[i][j]=diagonal;path[i][j]=0}else if(up>=left){scores[i][j]=up;path[i][j]=1}else{scores[i][j]=left;path[i][j]=2}
  }
  const mapping=new Array(m).fill(null);let i=n,j=m;
  while(i||j){const step=path[i][j];if(i&&j&&step===0){mapping[j-1]=i-1;i--;j--}else if(i&&(j===0||step===1)){i--}else{j--}}
  return mapping;
}

function getModel(){
  const geometry=window.STRUCTURE_DATA[current],prediction=testById[current];
  const observed=geometry.atoms.map(atom=>aa3[atom.res]||'X').join('');
  const mapping=align(prediction.sequence,observed);
  return {geometry,prediction,mapping};
}

function resize(){
  const ratio=Math.min(devicePixelRatio||1,2),rect=canvas.getBoundingClientRect();
  canvas.width=Math.max(1,Math.floor(rect.width*ratio));canvas.height=Math.max(1,Math.floor(rect.height*ratio));ctx.setTransform(ratio,0,0,ratio,0,0);draw();
}

function rotate(point,cx,cy,cz){
  let x=point.x-cx,y=point.y-cy,z=point.z-cz;
  const cosy=Math.cos(rotationY),siny=Math.sin(rotationY),cosx=Math.cos(rotationX),sinx=Math.sin(rotationX);
  const x1=x*cosy-z*siny,z1=x*siny+z*cosy;
  return {x:x1,y:y*cosx-z1*sinx,z:y*sinx+z1*cosx};
}

function draw(){
  const {geometry,prediction,mapping}=getModel(),atoms=geometry.atoms;
  const rect=canvas.getBoundingClientRect();ctx.clearRect(0,0,rect.width,rect.height);
  const cx=atoms.reduce((s,a)=>s+a.x,0)/atoms.length,cy=atoms.reduce((s,a)=>s+a.y,0)/atoms.length,cz=atoms.reduce((s,a)=>s+a.z,0)/atoms.length;
  const rotated=atoms.map(atom=>rotate(atom,cx,cy,cz));
  const extent=Math.max(...rotated.flatMap(p=>[Math.abs(p.x),Math.abs(p.y)]))||1;
  const scale=Math.min(rect.width,rect.height)*.39/extent*zoom;
  const projected=rotated.map(p=>({x:rect.width/2+p.x*scale,y:rect.height/2-p.y*scale,z:p.z}));
  const segments=[];
  for(let i=1;i<projected.length;i++){
    const a=atoms[i-1],b=atoms[i],distance=Math.hypot(a.x-b.x,a.y-b.y,a.z-b.z);if(distance>5)continue;
    const refIndex=mapping[i]??mapping[i-1],state=refIndex==null?'-':prediction.prediction[refIndex]||'-';
    segments.push({a:projected[i-1],b:projected[i],z:(projected[i-1].z+projected[i].z)/2,state});
  }
  segments.sort((a,b)=>a.z-b.z);
  ctx.lineCap='round';ctx.lineJoin='round';
  segments.forEach(segment=>{ctx.strokeStyle='rgba(0,0,0,.28)';ctx.lineWidth=10;ctx.beginPath();ctx.moveTo(segment.a.x,segment.a.y);ctx.lineTo(segment.b.x,segment.b.y);ctx.stroke();ctx.strokeStyle=colors[segment.state]||colors['-'];ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(segment.a.x,segment.a.y);ctx.lineTo(segment.b.x,segment.b.y);ctx.stroke()});
  projected.forEach((point,i)=>{const ref=mapping[i],state=ref==null?'-':prediction.prediction[ref]||'-';ctx.fillStyle=colors[state]||colors['-'];ctx.beginPath();ctx.arc(point.x,point.y,3.2,0,Math.PI*2);ctx.fill()});
}

function updateCopy(){
  const meta=viewerMeta[current],geometry=window.STRUCTURE_DATA[current],prediction=testById[current];
  document.getElementById('structure-title').textContent=`${current.toUpperCase()} · ${meta.title}`;
  document.getElementById('structure-subtitle').textContent=`${meta.organism} · ${meta.resolution} ${meta.method} · ${geometry.atoms.length} resolved Cα positions`;
  document.getElementById('pdb-link').href=`https://www.rcsb.org/structure/${current.toUpperCase()}`;
  document.getElementById('resolved-count').textContent=geometry.atoms.length;
  document.getElementById('sequence-count').textContent=prediction.sequence.length;
  draw();
}

document.querySelectorAll('.structure-tab').forEach(button=>button.addEventListener('click',()=>{
  current=button.dataset.pdb;document.querySelectorAll('.structure-tab').forEach(item=>item.classList.toggle('on',item===button));rotationX=-.38;rotationY=.52;zoom=1;updateCopy();
}));
document.getElementById('rotate-toggle').addEventListener('click',event=>{autoRotate=!autoRotate;event.currentTarget.classList.toggle('on',autoRotate);event.currentTarget.textContent=autoRotate?'Pause rotation':'Auto-rotate'});
canvas.addEventListener('pointerdown',event=>{dragging=true;lastX=event.clientX;lastY=event.clientY;canvas.setPointerCapture(event.pointerId)});
canvas.addEventListener('pointermove',event=>{if(!dragging)return;rotationY+=(event.clientX-lastX)*.009;rotationX+=(event.clientY-lastY)*.009;lastX=event.clientX;lastY=event.clientY;draw()});
canvas.addEventListener('pointerup',()=>dragging=false);canvas.addEventListener('pointercancel',()=>dragging=false);
canvas.addEventListener('wheel',event=>{event.preventDefault();zoom=Math.max(.55,Math.min(2.7,zoom*Math.exp(-event.deltaY*.001)));draw()},{passive:false});
function animate(){if(autoRotate){rotationY+=.004;draw()}frame=requestAnimationFrame(animate)}
addEventListener('resize',resize);resize();updateCopy();animate();
