const root=document.documentElement;
const themeButton=document.getElementById('theme');
const themeLabel=themeButton?.querySelector('span');
const setTheme=theme=>{
  root.dataset.theme=theme;
  const dark=theme==='dark';
  if(themeLabel) themeLabel.textContent=dark?'Light mode':'Dark mode';
  if(themeButton) themeButton.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');
};
setTheme(localStorage.getItem('protein-report-theme')||'light');
themeButton?.addEventListener('click',()=>{
  const next=root.dataset.theme==='dark'?'light':'dark';
  setTheme(next);
  localStorage.setItem('protein-report-theme',next);
});

const progress=document.getElementById('progress');
const updateProgress=()=>{
  const max=document.documentElement.scrollHeight-innerHeight;
  if(progress) progress.style.width=`${max>0?scrollY/max*100:0}%`;
};
addEventListener('scroll',updateProgress,{passive:true});
updateProgress();

const notes={
  prep:'The tokenizer converts sequences to indices and post-pads them to a fixed width.',
  metric:'The custom metric removes class 0, which represents padding, before comparing predicted and true labels.',
  train:'The training loop fits 20 epochs, then continues training the same model for one epoch in each fold. The fold counter is omitted here for brevity; open main.py for the complete script.'
};
document.querySelectorAll('.code-tab').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.code-tab').forEach(item=>{item.classList.remove('on');item.setAttribute('aria-selected','false')});
  document.querySelectorAll('.code-panel').forEach(panel=>panel.classList.remove('on'));
  button.classList.add('on');
  button.setAttribute('aria-selected','true');
  document.getElementById(`code-${button.dataset.code}`)?.classList.add('on');
  const note=document.getElementById('code-note');
  if(note) note.textContent=notes[button.dataset.code];
}));
