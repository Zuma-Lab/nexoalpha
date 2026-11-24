/* NEXO Alpha — workspace V2. New client, no styles/components imported from snapshot.
   Server remains the authority for permissions, calculations and versioning. */
"use strict";
const root=document.getElementById("app");
const fmtMoney=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
const fmtInt=new Intl.NumberFormat("pt-BR");
const esc=value=>String(value??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
const money=cents=>fmtMoney.format((Number(cents)||0)/100);
const quantity=n=>fmtInt.format(Number(n)||0);
const date=value=>{if(!value)return "A definir";const s=String(value).slice(0,10);const [y,m,d]=s.split("-");return y&&m&&d?d+"/"+m+"/"+y:esc(value);};
const icon=(name)=>{const data={
 arrow:'<path d="M4 12h16m-7-7 7 7-7 7"/>',
 back:'<path d="M20 12H4m7-7-7 7 7 7"/>',
 menu:'<path d="M4 7h16M4 12h16M4 17h16"/>',
 close:'<path d="M5 5l14 14M19 5L5 19"/>',
 chevron:'<path d="m9 18 6-6-6-6"/>',
 folder:'<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 9V5a2 2 0 0 1 2-2h5l2 3"/>',
 home:'<path d="m3 11 9-8 9 8M5 10v11h14V10M9 21v-8h6v8"/>',
 clipboard:'<rect x="5" y="4" width="14" height="17" rx="2"/><rect x="9" y="2" width="6" height="4" rx="1"/>',
 suppliers:'<path d="M3 7h18v14H3zM2 7l3-4h14l3 4M7 12h10M7 16h8"/>',
 quote:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M8 15h4"/>',
 proposal:'<path d="M6 2h9l4 4v16H6zM15 2v5h4M9 12h7m-7 4h7"/>',
 task:'<path d="M4 4h16v16H4zM8 12l3 3 6-7"/>',
 plus:'<path d="M12 5v14M5 12h14"/>',
 check:'<path d="m4 12 5 5L20 6"/>',
 clock:'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 3"/>',
 copy:'<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
 warning:'<path d="m12 2 10 19H2L12 2zM12 9v5m0 3v1"/>',
 logout:'<path d="M10 4H4v16h6M15 8l4 4-4 4m4-4H9"/>',
 search:'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
 calendar:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18"/>'
};return '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" aria-hidden="true">'+(data[name]||data.folder)+'</svg>';};
const statusMap={briefing:"Briefing",qualifying:"Qualificação",sourcing:"Fornecedores",quoting:"Em cotação",proposal:"Em proposta",approved:"Aprovado",closed:"Concluído",draft:"Rascunho",published:"Publicada",responded:"Respondida",sent:"Enviada",prepared:"Preparada",available:"Disponível",partial:"Parcial",unavailable:"Indisponível",changes_requested:"Ajustes solicitados",pending:"Pendente",in_progress:"Em andamento",done:"Concluída",rejected:"Rejeitada"};
function status(value){const cls=["approved","responded","available","done"].includes(value)?"success":["sourcing","quoting","partial","in_progress"].includes(value)?"warn":["rejected","unavailable"].includes(value)?"danger":["draft","briefing"].includes(value)?"changed":"neutral";return '<span class="tag '+cls+'">'+esc(statusMap[value]||value||"Não definido")+'</span>';}
const state={user:null,csrf:"",route:"queue",tab:"overview",pid:null,project:null,projects:[],clients:[],suppliers:[],dashboard:null,rfqBatch:null,proposalLink:null,wizardStep:0,draft:null,notice:"",mobile:false};
const canEdit=()=>["admin","consultant"].includes(state.user?.role);
const canCreate=()=>["admin","consultant","client"].includes(state.user?.role);
const canSeeMoney=()=>state.user?.role!=="client";
let toastTimer;
function notify(text,type="success"){const old=document.querySelector(".toast");if(old)old.remove();const div=document.createElement("div");div.className="toast "+type;div.setAttribute("role","status");div.textContent=text;document.body.appendChild(div);clearTimeout(toastTimer);toastTimer=setTimeout(()=>div.remove(),5500);}
function errorMessage(err){const obj=err?.detail;if(typeof obj==="string")return obj;if(obj?.issues?.length)return obj.issues.map(i=>i.message).join(" ");if(Array.isArray(obj))return obj.map(x=>x.msg||"Campo inválido").join("; ");return err.message||"Não foi possível concluir a ação.";}
async function api(path,opts={}){
 const method=opts.method||"GET";
 const headers={"Accept":"application/json",...(opts.body!==undefined?{"Content-Type":"application/json"}:{})};
 if(!["GET","HEAD"].includes(method)&&state.csrf)headers["X-Nexo-CSRF"]=state.csrf;
 const response=await fetch(path,{method,credentials:"same-origin",headers,body:opts.body===undefined?undefined:JSON.stringify(opts.body)});
 const value=await response.json().catch(()=>null);
 if(!response.ok){const err=new Error(response.status===401?"Sessão expirada ou acesso não autenticado.":response.status===429?"Muitas tentativas. Tente novamente mais tarde.":"A operação não foi concluída.");err.status=response.status;err.detail=value?.detail;throw err;}
 return value;
}
const field=(label,name,value="",type="text",extra="")=>'<label class="field"><span>'+esc(label)+'</span><input name="'+esc(name)+'" type="'+esc(type)+'" value="'+esc(value)+'" '+extra+'></label>';
const textarea=(label,name,value="",help="")=>'<label class="field"><span>'+esc(label)+'</span><textarea name="'+esc(name)+'" rows="3">'+esc(value)+'</textarea>'+(help?'<small>'+esc(help)+'</small>':"")+'</label>';
const select=(label,name,items,value="",extra="")=>'<label class="field"><span>'+esc(label)+'</span><select name="'+esc(name)+'" '+extra+'>'+items.map(([v,t])=>'<option value="'+esc(v)+'" '+(String(value)===String(v)?"selected":"")+'>'+esc(t)+'</option>').join("")+'</select></label>';
const check=(label,name,checked=false,value="on")=>'<label class="check-tile"><input type="checkbox" name="'+esc(name)+'" value="'+esc(value)+'" '+(checked?"checked":"")+'><span>'+esc(label)+'</span></label>';
const option=(str)=>[str,str];
function getForm(form){const d=new FormData(form),obj={};for(const [k,v] of d)if(k.endsWith("[]"))(obj[k.slice(0,-2)]??=[]).push(v);else obj[k]=v;return obj;}
function header(tag,title,desc,actions=""){return '<div class="page-head"><div><div class="kicker">'+esc(tag)+'</div><h1 class="page-title">'+esc(title)+'</h1><p class="page-description">'+esc(desc)+'</p></div>'+(actions?'<div class="actions">'+actions+'</div>':"")+'</div>';}
const button=(text,action,primary=false,attrs="")=>'<button type="button" class="btn '+(primary?"btn-primary":"")+'" data-action="'+esc(action)+'" '+attrs+'>'+text+'</button>';
const linkButton=(text,href,primary=false)=>'<a class="btn '+(primary?"btn-primary":"")+'" href="'+esc(href)+'">'+text+'</a>';
const surf=(title,subtitle,content,action="")=>'<section class="surface"><header class="surface-head"><div><h2>'+esc(title)+'</h2>'+(subtitle?'<p>'+esc(subtitle)+'</p>':"")+'</div>'+action+'</header>'+content+'</section>';
const empty=(title,body,action="")=>'<div class="state-empty"><h3>'+esc(title)+'</h3><p>'+esc(body)+'</p>'+action+'</div>';
const row=(label,value)=>'<div class="pair"><span>'+esc(label)+'</span><strong>'+esc(value||"—")+'</strong></div>';
function projectName(){return state.project?.title||"Operação";}
function routeLabel(){if(state.pid)return projectName();return({queue:"Fila de trabalho",projects:"Projetos",suppliers:"Fornecedores",new_project:"Novo projeto",new_client:"Novo cliente",new_supplier:"Novo fornecedor"})[state.route]||"Ambiente de trabalho";}
function sidebar(){
 const links=[["queue","home","Fila de trabalho"],["projects","folder","Projetos"],["suppliers","suppliers","Fornecedores"]];
 return '<aside class="sidebar '+(state.mobile?"is-open":"")+'" id="side-panel" aria-label="Navegação do workspace"><div class="brand-row"><span class="brand-symbol" aria-hidden="true">↗</span><span class="brand-word">nexo</span><span class="brand-note">Alpha</span></div><nav class="nav-block"><p class="nav-label">Operação</p>'+links.filter(x=>x[0]!=="suppliers"||canSeeMoney()).map(([k,ic,label])=>'<button class="side-link '+(state.route===k?"is-active":"")+'" data-action="nav" data-route="'+k+'" '+(state.route===k?'aria-current="page"':"")+'>'+icon(ic)+'<span>'+label+'</span></button>').join("")+'<p class="nav-label" style="margin-top:25px">Contexto</p><p class="nav-small" style="margin:0 12px;line-height:1.6">Os projetos reúnem briefing, cotações, proposta e execução. Use a fila para priorizar o que precisa de decisão.</p></nav><div class="sidebar-bottom"><div class="identity-name">'+esc(state.user?.full_name)+'</div><div class="identity-sub">'+esc(({admin:"Administrador",consultant:"Consultor",client:"Solicitante",viewer:"Visualização"})[state.user?.role]||"Operador")+'</div><button data-action="logout">Encerrar sessão</button></div></aside>';
}
function shell(content){
 root.innerHTML='<div class="shell">'+(state.mobile?'<button class="sidebar-backdrop" data-action="toggle-nav" aria-label="Fechar navegação"></button>':"")+sidebar()+'<div class="workspace"><header class="topbar"><div class="crumbs"><button class="btn btn-small mobile-nav" aria-label="Abrir navegação" data-action="toggle-nav">'+icon("menu")+'</button><span>Operação</span>'+icon("chevron")+'<strong>'+esc(routeLabel())+'</strong></div><div class="top-actions"><span class="top-role">'+esc(({admin:"Administrador",consultant:"Consultor",client:"Cliente",viewer:"Leitura"})[state.user?.role]||"")+'</span><span class="user-chip" aria-hidden="true">'+esc((state.user?.full_name||"U").split(" ").slice(0,2).map(x=>x[0]||"").join("").toUpperCase())+'</span></div></header><main id="work-main" class="page">'+content+'</main></div></div>';
}
function nextAction(p){const status=p.status;const action=({briefing:"Conferir briefing",qualifying:"Validar escopo",sourcing:"Acompanhar respostas",quoting:"Revisar comparação",proposal:"Aguardar decisão",approved:"Preparar execução",closed:"Consultar histórico"})[status]||"Abrir operação";return action;}
function projectRow(p){
 return '<button class="project-row" type="button" data-action="open-project" data-id="'+Number(p.id)+'"><span><span class="row-title">'+esc(p.title)+'</span><span class="row-meta"><span>'+esc(p.protocol)+'</span><span>'+esc(p.client_name||"Cliente")+'</span><span>'+esc(p.destination||"Destino a definir")+'</span></span></span><span class="row-aside">'+status(p.status)+'<span class="row-action">'+esc(nextAction(p))+' '+icon("arrow")+'</span></span></button>';
}
function queue(){
 const d=state.dashboard||{projects:[],counts:{},active:0,tasks_pending:0,suppliers:0};
 const ps=state.projects||[];const open=ps.filter(p=>p.status!=="closed");
 const action=canCreate()?button(icon("plus")+" Novo projeto","new-project",true):"";
 const intro=header("Central de operação","O que precisa avançar agora","Acompanhe briefings, respostas e decisões. Cada linha abre a operação e seu histórico.",action);
 const rows=open.length?open.map(projectRow).join(""):empty("Nenhuma operação em andamento","Crie uma solicitação para iniciar o briefing e organizar fornecedores.",canCreate()?button("Criar projeto","new-project",true):"");
 const info=surf("Ponto de atenção","A fila indica a próxima etapa provável de cada projeto.",'<div class="work-note"><strong>Briefing e versões</strong><p>Alterações não substituem o histórico. O próximo lote de RFQs usa a versão mais recente.</p></div><div class="work-note"><strong>Fornecedor e decisão</strong><p>As respostas não alteram automaticamente a proposta publicada. Revise valores antes de publicar uma nova versão.</p></div><div class="work-note"><strong>Entrega por link</strong><p>O envio de RFQs e propostas ainda é manual. Não há disparo de e-mail integrado.</p></div>');
 const counters=surf("Panorama operacional","Valores do ambiente conectado, não números promocionais.",'<div class="surface-body">'+[['Operações abertas',open.length],['Aguardando cotação',ps.filter(p=>["sourcing","quoting"].includes(p.status)).length],['Tarefas pendentes',d.tasks_pending||0],['Fornecedores cadastrados',d.suppliers||0]].map(([k,v])=>'<div class="count-row"><span class="count-label">'+esc(k)+'</span><strong class="count-value">'+quantity(v)+'</strong></div>').join("")+'</div>');
 return intro+'<div class="notice neutral">Ambiente Alpha de desenvolvimento. A interface apresenta dados registrados na API; exemplos de demonstração devem ser tratados como fictícios.</div><div class="overview-layout"><div>'+surf("Sua fila de operações",open.length+" projetos por acompanhar",'<div class="surface-flush">'+rows+'</div>',button("Ver todos","all-projects"))+'</div><div>'+info+counters+'</div></div>';
}
function projectsPage(){
 const actions=canCreate()?button(icon("plus")+" Novo projeto","new-project",true):"";
 return header("Carteira de projetos","Projetos e solicitações","Escolha um projeto para acompanhar seu briefing, fornecedores, cotação e proposta.",actions)+surf("Projetos cadastrados",state.projects.length+" registros",'<div class="surface-flush">'+(state.projects.length?state.projects.map(projectRow).join(""):empty("Nenhum projeto cadastrado","Registre um novo projeto para começar.",actions))+'</div>');
}
function newProject(){
 const customers=state.clients.map(x=>[String(x.id),x.name]);
 if(!customers.length)return header("Cadastro","Novo projeto","A operação precisa de um cliente vinculado.")+empty("Cadastre um cliente primeiro","O projeto exige uma empresa cliente para preservar os acessos e a origem das propostas.",canEdit()?button("Cadastrar cliente","new-client",true):"");
 const services=["Aéreo","Hospedagem","Salas e A&B","Transfers","Audiovisual","Staff","Outros"];
 return header("Nova operação","Criar projeto","Registre os dados mínimos; o briefing detalhado será criado dentro do projeto.")+surf("Identificação","Os campos marcados são obrigatórios.",'<form class="form surface-body" data-form="new-project"><div class="form-row">'+field("Nome do projeto *","title","","text",'required minlength="3" maxlength="160"')+select("Cliente *","client_id",customers,customers[0][0],'required')+'</div><div class="form-row">'+field("Destino","destination")+field("Participantes estimados","attendees","","number",'min="0" step="1"')+'</div><div class="form-row">'+field("Início","starts_at","","date")+field("Fim","ends_at","","date")+'</div><div class="form-group"><h3>Serviços previstos</h3><div class="check-grid">'+services.map(x=>check(x,"services[]",x==="Hospedagem",x)).join("")+'</div></div><div class="form-footer"><button class="btn" type="button" data-action="all-projects">Cancelar</button><div class="actions">'+(canEdit()?button("Novo cliente","new-client"):"")+'<button class="btn btn-primary" type="submit">Criar e abrir briefing '+icon("arrow")+'</button></div></div></form>') ;
}
function newClient(){
 return header("Cadastro","Novo cliente","Cada projeto pertence a um cliente da empresa, respeitando os acessos da API.")+surf("Dados da empresa","Cadastro mínimo para vincular projetos.",'<form class="form surface-body" data-form="new-client">'+field("Razão social / Nome *","name","","text",'required minlength="2" maxlength="160"')+field("E-mail de contato","contact_email","","email")+'<div class="form-footer">'+button("Voltar","new-project")+'<button class="btn btn-primary" type="submit">Salvar cliente</button></div></form>');
}
function projectHeader(){
 const p=state.project||{},actions=canCreate()?button("Nova versão","start-briefing",true):"";
 const h=header(esc(p.protocol||"Projeto"),p.title||"Projeto",p.client_name||"Cliente",actions);
 const context='<div class="context-bar">'+[['Cliente',p.client_name],['Destino',p.destination],['Período',date(p.starts_at)+" — "+date(p.ends_at)],['Participantes',p.attendees?quantity(p.attendees):"A definir"]].map(([label,value])=>'<div class="context-item"><div class="context-label">'+esc(label)+'</div><div class="context-value">'+esc(value||"A definir")+'</div></div>').join("")+'</div>';
 const tabs=[["overview","Visão da operação"],["briefing","Briefing"],["rfq","Fornecedores"],["quotes","Comparativo"],["proposal","Propostas"],["planning","Planejamento"]];
 const navigation='<nav class="tabbar" aria-label="Áreas do projeto">'+tabs.filter(([k])=>!(["rfq","quotes"].includes(k)&&!canSeeMoney())).map(([k,l])=>'<button type="button" class="tab" data-action="project-tab" data-tab="'+k+'" '+(state.tab===k?'aria-current="page"':"")+'>'+esc(l)+'</button>').join("")+'</nav>';
 return h+context+navigation;
}
function timeline(){
 const p=state.project||{};
 const steps=[["briefing","Briefing","Escopo e versões preservadas"],["sourcing","Fornecedores","Seleção e respostas a RFQs"],["quoting","Cotação","Valores, taxas e condições"],["proposal","Proposta","Publicação e decisão"],["approved","Planejamento","Confirmação e execução"]];
 const index={briefing:0,qualifying:0,sourcing:1,quoting:2,proposal:3,approved:4,closed:4}[p.status]||0;
 return '<ol class="step-list">'+steps.map(([key,label,desc],i)=>'<li class="step-line '+(i<index?"done":i===index?"current":"")+'"><span class="step-circle">'+(i<index?icon("check"):i+1)+'</span><div><strong>'+label+'</strong><p>'+desc+'</p></div></li>').join("")+'</ol>';
}
function changes(){
 const b=state.project?.briefings||[];
 if(b.length<2)return empty("Primeira versão registrada","Quando houver outra versão, esta área mostrará o que foi alterado sem modificar a anterior.");
 const cur=b[0].payload||{},prev=b[1].payload||{};
 const fields=[["Participantes",cur.totalPassengers??cur.attendees,prev.totalPassengers??prev.attendees],["Destino",cur.destination,prev.destination],["Início",cur.departureDate??cur.start_date,prev.departureDate??prev.start_date],["Término",cur.returnDate??cur.end_date,prev.returnDate??prev.end_date],["Singles",cur.roomsSingle??cur.lodging?.single,prev.roomsSingle??prev.lodging?.single],["Twins",cur.roomsDoubleTwin??cur.lodging?.twin,prev.roomsDoubleTwin??prev.lodging?.twin],["Plenária",cur.plenaryCapacity,prev.plenaryCapacity]];
 const diffs=fields.filter(([name,c,p])=>String(c??"")!==String(p??""));
 if(!diffs.length)return '<div class="change-empty">V'+esc(b[0].version)+' e V'+esc(b[1].version)+' registradas. Não houve alteração nos campos acompanhados nesta visão.</div>';
 return '<div class="changes">'+diffs.map(([name,c,p])=>'<div class="change"><span class="change-name">'+esc(name)+'</span><div class="change-values"><s>'+esc(p??"—")+'</s>'+esc(c??"—")+'</div><span class="tag changed">Alterado</span></div>').join("")+'</div>';
}
function projectOverview(){
 const p=state.project,b=p.briefings||[],last=b[0],pending=(p.tasks||[]).filter(x=>x.status!=="done");
 const alerts=[];
 if(b.length>1)alerts.push("Briefing V"+b[0].version+" registrada. Confira se os fornecedores precisam receber o novo escopo.");
 if((p.rfqs||[]).some(x=>x.status==="prepared"))alerts.push("Existem RFQs preparadas: os links devem ser enviados manualmente.");
 if((p.proposals||[]).some(x=>x.status==="published"))alerts.push("Há proposta publicada aguardando decisão.");
 if(!alerts.length)alerts.push("Confirme as informações do briefing antes de solicitar valores aos fornecedores.");
 const left=surf("Próxima ação","Orientação contextual, calculada a partir dos estados registrados.",'<div class="surface-body"><p class="kicker accent">Situação atual</p><h2 style="font-size:23px;letter-spacing:-.03em;margin:7px 0 8px">'+esc(nextAction(p))+'</h2><p class="page-description">'+esc(alerts[0])+'</p><div class="actions" style="margin-top:19px">'+button("Abrir briefing","go-briefing",true)+(canEdit()?button("Ver comparativo","go-quotes"):"")+'</div></div>')+surf("O que mudou","Comparação entre as últimas duas versões do briefing.",changes())+surf("Histórico recente","Ações registradas pela API.",'<div class="surface-body">'+((p.audit||[]).length?p.audit.slice(0,7).map(x=>'<div class="activity-entry"><time>'+esc(date(x.created_at))+'</time><div><strong>'+esc(x.action?.replaceAll("."," · ")||"Registro")+'</strong><p>'+esc(x.actor_name||"Sistema")+(x.detail?' · '+esc(x.detail):"")+'</p></div></div>').join(""):'<p class="page-description">Ainda não há registros exibidos para este perfil.</p>')+'</div>');
 const right=surf("Etapas da operação","A ordem representa o ciclo comercial; não é um conjunto de aplicativos isolados.",timeline())+surf("Pendências do projeto",pending.length+" tarefa(s) em aberto",'<div class="surface-body">'+(pending.length?'<ul class="list-plain">'+pending.slice(0,6).map(x=>'<li><span><strong>'+esc(x.title)+'</strong><small>'+esc(date(x.due_date))+'</small></span>'+status(x.status)+'</li>').join("")+'</ul>':empty("Sem tarefas abertas","As tarefas de execução aparecem aqui quando cadastradas."))+'</div>');
 return '<div class="project-grid"><div>'+left+'</div><aside>'+right+'</aside></div>';
}
function briefingOverview(){
 const b=state.project?.briefings||[];
 return '<div class="project-grid"><div>'+surf("Versões do briefing","O histórico é imutável. Cada nova versão preserva a anterior.",'<div class="surface-body">'+(b.length?b.map((x,i)=>'<div class="pair"><span>Versão '+esc(x.version)+(i===0?" · mais recente":"")+'</span><strong>'+esc(date(x.created_at))+'</strong></div>').join(""):'<p class="page-description">Nenhuma versão registrada.</p>')+'<div class="actions" style="margin-top:19px">'+(canCreate()?button(icon("plus")+" Nova versão do briefing","start-briefing",true):"")+'</div></div>')+surf("Campos alterados","Diferenças entre as duas últimas versões.",changes())+'</div><aside>'+surf("Imutabilidade","A base para novos pedidos de cotação é a última versão registrada.",'<div class="surface-body"><div class="notice neutral">O sistema não substitui automaticamente pedidos enviados com uma versão anterior. Avalie o impacto antes de reenviar RFQs.</div><p class="page-description">Para corrigir o escopo, crie uma nova versão. A publicação de versões e a validação detalhada são controladas no servidor.</p></div>')+'</aside></div>';
}
function suppliersPage(){
 const action=canEdit()?button(icon("plus")+" Cadastrar fornecedor","new-supplier",true):"";
 const list=state.suppliers||[];
 return header("Rede comercial","Fornecedores","Cadastre a especialidade e a praça de atendimento; cada convite será vinculado a uma versão do briefing.",action)+surf("Rede cadastrada",list.length+" parceiros",'<div class="table-wrap" tabindex="0" aria-label="Tabela de fornecedores"><table class="data-table compact"><thead><tr><th>Fornecedor</th><th>Categoria</th><th>Praça</th><th>Contato</th></tr></thead><tbody>'+list.map(x=>'<tr><th>'+esc(x.name)+'</th><td>'+esc(x.category)+'</td><td>'+esc(x.city||"—")+'</td><td>'+esc(x.email||"—")+'</td></tr>').join("")+'</tbody></table></div>'+(!list.length?empty("Ainda sem fornecedores","Cadastre um parceiro para criar pedidos de cotação."):'' ));
}
function newSupplier(){
 return header("Rede comercial","Novo fornecedor","Informações mínimas para identificar e convidar um parceiro.")+surf("Cadastro comercial","O envio de solicitações continuará manual até a integração de e-mail.",'<form class="form surface-body" data-form="new-supplier">'+field("Empresa fornecedora *","name","","text",'required minlength="2"')+select("Categoria", "category",["Hospedagem","Salas e A&B","Transfers","Aéreo","Audiovisual","Staff","Outros"].map(option),"Hospedagem")+'<div class="form-row">'+field("Cidade / praça","city")+field("Contato comercial","contact_name")+'</div><div class="form-row">'+field("E-mail","email","","email")+field("Telefone","phone","","tel")+'</div><div class="form-footer">'+button("Cancelar","suppliers")+'<button class="btn btn-primary" type="submit">Cadastrar fornecedor</button></div></form>');
}
function rfqPage(){
 const p=state.project||{},suppliers=state.suppliers||[],available=suppliers.filter(s=>s.category&&p.services?.length?p.services.includes(s.category):true);
 const list=p.rfqs||[];
 const checkList=available.map(s=>check(s.name+" · "+s.category,"supplier_ids[]",false,String(s.id))).join("");
 const creating=canEdit()?surf("Solicitar cotação","O convite fica vinculado à versão mais recente do briefing. Os links são entregues manualmente.",'<form class="form surface-body" data-form="rfq-batch"><div class="check-grid">'+(checkList||'<p class="page-description">Cadastre fornecedores para solicitar cotações.</p>')+'</div>'+field("Prazo de resposta (opcional)","deadline","","date")+'<div class="form-footer"><span class="page-description">A criação não dispara e-mails.</span><button class="btn btn-primary" type="submit" '+(!available.length?"disabled":"")+'>Gerar links de RFQ</button></div></form>'):"";
 const links=state.rfqBatch?'<div class="notice success">Lote #'+state.rfqBatch.batch_id+' criado a partir do briefing V'+state.rfqBatch.briefing_version+'. Copie os links abaixo antes de sair desta tela: os tokens não são exibidos novamente.</div>'+surf("Links para envio manual","Nenhum e-mail foi enviado pelo sistema.",'<div class="surface-body">'+state.rfqBatch.links.map((x,i)=>'<div class="pair"><span>'+esc(suppliers.find(s=>s.id===x.supplier_id)?.name||("Fornecedor "+x.supplier_id))+'</span><div class="actions"><a class="btn btn-small" target="_blank" rel="noopener noreferrer" href="'+esc(x.response_path)+'">Abrir link</a><button class="btn btn-small" type="button" data-action="copy-rfq" data-index="'+i+'">'+icon("copy")+' Copiar</button></div></div>').join("")+'<div class="form-footer"><span class="page-description">Marque como enviado somente após compartilhar o convite fora da plataforma.</span>'+button("Registrar envio manual","mark-rfq-sent",true)+'</div></div>'):"";
 const table=surf("Histórico de RFQs",list.length+" solicitações",list.length?'<div class="table-wrap" tabindex="0" aria-label="Pedidos de cotação"><table class="data-table compact"><thead><tr><th>Fornecedor</th><th>Especialidade</th><th>Estado</th><th>Disponibilidade</th><th>Condições</th></tr></thead><tbody>'+list.map(x=>'<tr><th>'+esc(x.supplier_name)+'</th><td>'+esc(x.category)+'</td><td>'+status(x.status)+'</td><td>'+esc(x.available||"Aguardando")+'</td><td>'+esc(x.cancellation||x.conditions||"—")+'</td></tr>').join("")+'</tbody></table></div>':empty("Nenhuma RFQ criada","Selecione os fornecedores adequados ao serviço e gere os convites.") );
 return '<div class="notice neutral">A aplicação registra os convites e suas respostas; a entrega é feita por link manual. Cada fornecedor enxerga apenas seu próprio pedido.</div>'+links+'<div class="project-grid"><div>'+table+'</div><aside>'+creating+'</aside></div>';
}
function moneyBreakdown(item){
 const net=Number(item.quantity)*Number(item.unit_net_cents),tax=Math.floor((net*Number(item.tax_bps)+5000)/10000),fee=Math.floor(((net+tax)*Number(item.fee_bps)+5000)/10000);
 return {net,tax,fee,total:net+tax+fee};
}
function quotePage(){
 const p=state.project||{},items=p.quote_items||[],rfqs=p.rfqs||[],total=items.reduce((a,x)=>a+(Number(x.sale_total_cents)||0),0);
 const net=items.reduce((a,x)=>a+(Number(x.net_total_cents)||0),0),tax=items.reduce((a,x)=>a+(Number(x.tax_cents)||0),0),fee=items.reduce((a,x)=>a+(Number(x.fee_cents)||0),0);
 const totals='<div class="inline-totals">'+[['Custo NET',net],['Tributos parametrizados',tax],['Fee',fee],['Venda total',total]].map(([k,v])=>'<div><small>'+esc(k)+'</small><strong>'+money(v)+'</strong></div>').join("")+'</div>';
 const quote=surf("Orçamento por item","Cálculo em centavos na API. NET, impostos e fee são informações internas.",items.length?'<div class="table-wrap" tabindex="0" aria-label="Itens financeiros da cotação"><table class="data-table wide"><thead><tr><th>Serviço</th><th>Descrição</th><th>Qtd.</th><th class="money">NET unit.</th><th class="money">Impostos</th><th class="money">Fee</th><th class="money">Venda</th><th></th></tr></thead><tbody>'+items.map(x=>'<tr><td>'+esc(x.category)+'</td><th>'+esc(x.description)+'</th><td>'+quantity(x.quantity)+'</td><td class="money">'+money(x.unit_net_cents)+'</td><td class="money">'+money(x.tax_cents)+'</td><td class="money">'+money(x.fee_cents)+'</td><td class="money"><strong>'+money(x.sale_total_cents)+'</strong></td><td>'+(canEdit()?'<button class="btn btn-small" data-action="remove-item" data-id="'+Number(x.id)+'" aria-label="Excluir item '+esc(x.description)+'">Excluir</button>':"")+'</td></tr>').join("")+'</tbody></table></div>'+totals:empty("Orçamento ainda sem itens","Adicione os serviços contratáveis, suas quantidades e custos para gerar uma proposta rastreável."));
 const responseRows=rfqs.filter(x=>x.status==="responded");
 const matrix=surf("Respostas dos fornecedores","Comparação preliminar; disponibilidade e condições importam além do preço.",responseRows.length?'<div class="table-wrap" tabindex="0" aria-label="Matriz de respostas recebidas"><table class="data-table compact"><thead><tr><th>Fornecedor</th><th>Disponibilidade</th><th class="money">NET informado</th><th>Cancelamento</th></tr></thead><tbody>'+responseRows.map(x=>'<tr><th>'+esc(x.supplier_name)+'</th><td>'+status(x.available)+'</td><td class="money">'+money(x.net_cents)+'</td><td>'+esc(x.cancellation||"Não informado")+'</td></tr>').join("")+'</tbody></table></div><div class="table-hint">Valor informado na resposta do fornecedor. Não combinar automaticamente com a grade financeira sem validar escopo, unidade e tributos.</div>':empty("Nenhuma resposta recebida","A matriz será preenchida com as respostas dos fornecedores enviados ao projeto."));
 const adding=canEdit()?surf("Adicionar item ao orçamento","Impostos e fee parametrizados por item. Não assumir taxas universais.",'<form class="form surface-body" data-form="quote-item">'+select("Categoria","category",["Hospedagem","Salas e A&B","Transfers","Aéreo","Audiovisual","Staff","Outros"].map(option),"Hospedagem")+field("Descrição do serviço *","description","","text",'required minlength="2"')+'<div class="form-row">'+field("Quantidade *","quantity","1","number",'required min="1" step="1"')+field("Custo NET unitário (R$) *","unit_net","0,00","text",'required inputmode="decimal"')+'</div><div class="form-row">'+field("Impostos (%)","tax_pct","0","number",'min="0" max="100" step=".01"')+field("Fee (%)","fee_pct","0","number",'min="0" max="100" step=".01"')+'</div><div class="review-box" id="quote-preview" aria-live="polite">Informe os valores para conferir o cálculo antes de gravar.</div><div class="form-footer"><span class="page-description">Arredondamento realizado por item em centavos.</span><button class="btn btn-primary" type="submit">Adicionar item</button></div></form>'):"";
 return '<div class="notice neutral">O comparativo só pode refletir serviços e quantidades equivalentes. Hotel com café à parte não deve ser selecionado automaticamente apenas pela menor tarifa.</div>'+matrix+'<div style="height:18px"></div>'+quote+'<div style="height:18px"></div>'+adding;
}
function proposalPage(){
 const p=state.project||{},list=p.proposals||[],items=p.quote_items||[];
 const current=state.proposalLink;
 const link=current?'<div class="notice success">Proposta V'+current.version+' criada com total '+money(current.total_cents)+'. Guarde o link privado abaixo; ele não pode ser recuperado nesta tela depois de sair.</div>'+surf("Publicar e compartilhar","A proposta é um snapshot: mudanças posteriores exigem uma nova versão.",'<div class="surface-body"><div class="pair"><span>Versão</span><strong>V'+current.version+'</strong></div><div class="pair"><span>Total de venda</span><strong>'+money(current.total_cents)+'</strong></div><div class="pair"><span>Válida até</span><strong>'+esc(date(current.expires_at))+'</strong></div><div class="form-footer"><div class="actions"><a class="btn btn-small" href="'+esc(current.review_path)+'" target="_blank" rel="noopener noreferrer">Abrir link</a>'+button(icon("copy")+" Copiar link","copy-proposal")+'</div>'+(current.status==="draft"?button("Publicar versão","publish-proposal",true):'<span class="tag success">Publicada</span>')+'</div></div>'):"";
 const entries=list.length?'<div class="surface-flush">'+list.map(x=>'<div class="pair" style="padding:17px 20px"><span><strong>Proposta V'+esc(x.version)+'</strong><small style="display:block">'+esc(date(x.created_at))+'</small></span><span>'+money(x.total_cents)+' · '+status(x.status)+'</span></div>').join("")+'</div>':empty("Nenhuma proposta publicada","A proposta depende de ao menos um item de orçamento. Toda publicação preserva o valor e os itens daquela versão.");
 return '<div class="notice neutral">A versão pública omite custos NET, taxas e fee internos. A entrega ainda é manual por link, com prazo de validade.</div>'+link+'<div class="project-grid"><div>'+surf("Versões de proposta","Histórico comercial do projeto.",entries)+'</div><aside>'+surf("Próximo passo","O orçamento serve de fonte para uma versão nova.",'<div class="surface-body">'+row("Itens de orçamento",String(items.length))+row("Venda total",money(p.quote_total_cents))+'<div class="actions" style="margin-top:20px">'+(canEdit()?'<button class="btn btn-primary" data-action="create-proposal" '+(!items.length?"disabled":"")+'>Criar versão da proposta</button>':"")+'</div></div>')+'</aside></div>';
}
function planningPage(){
 const tasks=state.project?.tasks||[];
 const create=canEdit()?surf("Nova tarefa","Acompanhamento operacional vinculado ao projeto.",'<form class="form surface-body" data-form="new-task">'+field("Entrega / pendência *","title","","text",'required minlength="2"')+field("Prazo","due_date","","date")+'<button class="btn btn-primary" type="submit">Adicionar tarefa</button></form>'):"";
 const list=surf("Checklist de execução",tasks.length+" tarefas",tasks.length?'<div class="surface-flush">'+tasks.map(x=>'<div class="pair" style="padding:16px 21px"><span><strong>'+esc(x.title)+'</strong><small style="display:block;color:var(--muted)">'+date(x.due_date)+'</small></span><span class="actions">'+status(x.status)+(canEdit()?'<button class="btn btn-small" data-action="toggle-task" data-id="'+Number(x.id)+'" data-status="'+esc(x.status)+'">'+(x.status==="done"?"Reabrir":"Concluir")+'</button>':"")+'</span></div>').join("")+'</div>':empty("Nenhuma tarefa cadastrada","Adicione entregas, responsáveis e prazos após a aprovação comercial."));
 return '<div class="project-grid"><div>'+list+'</div><aside>'+create+'</aside></div>';
}
function wizardPayload(){
 const p=state.project||{},last=p.briefings?.[0]?.payload||{};
 const newer=Object.prototype.hasOwnProperty.call(last,"eventName");
 const v={
 eventName:newer?last.eventName:p.title||"",
 destination:last.destination||p.destination||"",
 departureDate:newer?last.departureDate:(last.start_date||p.starts_at||""),
 returnDate:newer?last.returnDate:(last.end_date||p.ends_at||""),
 totalPassengers:newer?last.totalPassengers:String(last.attendees||p.attendees||""),
 datesUnknown:newer?!!last.datesUnknown:false,
 participantsUnknown:newer?!!last.participantsUnknown:false,
 companyName:newer?last.companyName:p.client_name||"",
 requesterName:newer?last.requesterName:state.user?.full_name||"",
 email:newer?last.email:state.user?.email||"",
 generalNotes:newer?last.generalNotes:last.notes||"",
 svcAereo:newer?!!last.svcAereo:(p.services||[]).includes("Aéreo"),
 svcHospedagem:newer?!!last.svcHospedagem:(p.services||[]).includes("Hospedagem"),
 svcEspacoAlimentacao:newer?!!last.svcEspacoAlimentacao:(p.services||[]).includes("Salas e A&B"),
 svcTransfers:newer?!!last.svcTransfers:(p.services||[]).includes("Transfers"),
 roomsSingle:newer?last.roomsSingle:(last.lodging?.single??""),
 roomsDoubleTwin:newer?last.roomsDoubleTwin:(last.lodging?.twin??""),
 roomsDoubleCasal:last.roomsDoubleCasal||"",roomsTriple:last.roomsTriple||"",
 hotelStandard:last.hotelStandard||"",hotelLocationPref:last.hotelLocationPref||"",
 hotelLocationOther:last.hotelLocationOther||"",eventAddress:last.eventAddress||"",mealRegime:last.mealRegime||"",roomingList:last.roomingList||"",
 plenaryCapacity:last.plenaryCapacity||"",roomLayout:last.roomLayout||"",breakoutRoomsCount:last.breakoutRoomsCount||"",
 cateringServices:Array.isArray(last.cateringServices)?last.cateringServices:[],coffeeBreakPerDay:last.coffeeBreakPerDay||"",
 transferTypes:Array.isArray(last.transferTypes)?last.transferTypes:[],vehicleType:last.vehicleType||"",
 airlinePreference:last.airlinePreference||"",specificAirline:last.specificAirline||"",restrictedAirline:last.restrictedAirline||"",
 flightConnection:last.flightConnection||"",cabinClass:last.cabinClass||"",cabinClassNotes:last.cabinClassNotes||""
 };
 return v;
}
function wizard(){
 const d=state.draft||wizardPayload(),step=state.wizardStep;
 const steps=["Evento","Serviços","Especificações","Revisão"];
 const nav='<div class="wizard-nav" aria-label="Etapas do briefing">'+steps.map((name,i)=>'<button type="button" class="wizard-step '+(i===step?"active":"")+'" data-action="wizard-jump" data-step="'+i+'" '+(i>step?"disabled":"")+'>'+String(i+1).padStart(2,"0")+' · '+name+'</button>').join("")+'</div>';
 let body="";
 if(step===0)body='<h2 class="form-heading">Identificação do evento</h2><p class="form-intro">Registre o escopo compartilhado com os fornecedores; nenhuma alteração substitui uma versão enviada.</p>'+field("Nome do evento *","eventName",d.eventName,"text",'required minlength="3"')+'<div class="form-row">'+field("Destino *","destination",d.destination,"text",'required')+field("Participantes", "totalPassengers",d.totalPassengers,"number",d.participantsUnknown?'min="1" disabled':'min="1" required')+'</div><div class="form-row">'+field("Data de início","departureDate",d.departureDate,"date",d.datesUnknown?"disabled":"required")+field("Data de término","returnDate",d.returnDate,"date",d.datesUnknown?"disabled":"required")+'</div><div class="check-grid">'+check("Participantes ainda não definidos","participantsUnknown",d.participantsUnknown)+check("Datas ainda não definidas","datesUnknown",d.datesUnknown)+'</div><div class="form-group"><h3>Solicitante</h3><div class="form-row">'+field("Empresa *","companyName",d.companyName,"text","required")+field("Nome do solicitante *","requesterName",d.requesterName,"text","required")+'</div>'+field("E-mail de contato *","email",d.email,"email","required")+'</div>'+textarea("Observações gerais","generalNotes",d.generalNotes);
 if(step===1)body='<h2 class="form-heading">Quais serviços fazem parte da solicitação?</h2><p class="form-intro">Selecione apenas os serviços necessários. As especificações aparecerão na próxima etapa.</p><div class="check-grid">'+check("Aéreo","svcAereo",d.svcAereo)+check("Hospedagem","svcHospedagem",d.svcHospedagem)+check("Salas e alimentação","svcEspacoAlimentacao",d.svcEspacoAlimentacao)+check("Transfers","svcTransfers",d.svcTransfers)+'</div><p class="field-help" style="margin-top:15px">Audiovisual, staff e serviços adicionais continuam como requisitos a ampliar em versões futuras do wizard; descreva necessidades extraordinárias nas observações.</p>';
 if(step===2){
 body='<h2 class="form-heading">Especificações por serviço</h2><p class="form-intro">Os campos apresentados dependem dos serviços selecionados. As regras condicionais são verificadas pela API ao criar a versão.</p>';
 if(d.svcHospedagem)body+='<div class="form-group"><h3>Hospedagem</h3><div class="form-row">'+select("Padrão de hotel","hotelStandard",["","Econômico","Executivo","Superior","Luxo"].map(option),d.hotelStandard)+select("Preferência de localização","hotelLocationPref",["","Próximo ao Local do Evento","Centro","Outro"].map(option),d.hotelLocationPref)+'</div>'+(d.hotelLocationPref==="Outro"?field("Localização desejada *","hotelLocationOther",d.hotelLocationOther,"text","required"):"")+(d.hotelLocationPref==="Próximo ao Local do Evento"?field("Endereço do evento","eventAddress",d.eventAddress):"")+'<div class="form-row three">'+field("Apartamentos single","roomsSingle",d.roomsSingle,"number",'min="0" step="1"')+field("Apartamentos twin","roomsDoubleTwin",d.roomsDoubleTwin,"number",'min="0" step="1"')+field("Casal","roomsDoubleCasal",d.roomsDoubleCasal,"number",'min="0" step="1"')+'</div><div class="form-row">'+field("Triplos","roomsTriple",d.roomsTriple,"number",'min="0" step="1"')+select("Refeições","mealRegime",["","Café da manhã","Meia pensão","Pensão completa"].map(option),d.mealRegime)+'</div>'+textarea("Rooming / observações","roomingList",d.roomingList,"Informe condições de ocupação e separação de quartos, quando aplicável.")+'</div>';
 if(d.svcEspacoAlimentacao)body+='<div class="form-group"><h3>Salas e alimentação</h3><div class="form-row">'+field("Capacidade da plenária","plenaryCapacity",d.plenaryCapacity,"number",'min="0" step="1"')+field("Salas de apoio","breakoutRoomsCount",d.breakoutRoomsCount,"number",'min="0" step="1"')+'</div><div class="form-row">'+select("Montagem","roomLayout",["","Auditório","Escolar","U","Banquete","Outro"].map(option),d.roomLayout)+select("Coffee breaks por dia","coffeeBreakPerDay",[["","A definir"],["1","1"],["2","2"],["3","3"],["Preciso de orientação","Preciso de orientação"]],d.coffeeBreakPerDay)+'</div><div class="check-grid">'+check("Incluir coffee break","cateringServices[]",d.cateringServices.includes("Coffee Break"),"Coffee Break")+check("Almoço","cateringServices[]",d.cateringServices.includes("Almoço"),"Almoço")+check("Jantar","cateringServices[]",d.cateringServices.includes("Jantar"),"Jantar")+'</div></div>';
 if(d.svcTransfers)body+='<div class="form-group"><h3>Transfers</h3><div class="check-grid">'+check("Aeroporto → hotel","transferTypes[]",d.transferTypes.includes("Aeroporto / Hotel"),"Aeroporto / Hotel")+check("Hotel → aeroporto","transferTypes[]",d.transferTypes.includes("Hotel / Aeroporto"),"Hotel / Aeroporto")+check("Veículo à disposição","transferTypes[]",d.transferTypes.includes("Veículo Exclusivo à Disposição"),"Veículo Exclusivo à Disposição")+'</div>'+select("Tipo de veículo","vehicleType",["","Van","Micro-ônibus","Ônibus","Executivo"].map(option),d.vehicleType)+'</div>';
 if(d.svcAereo)body+='<div class="form-group"><h3>Aéreo</h3><div class="form-row">'+select("Companhia","airlinePreference",["","Qualquer companhia","Somente Companhia Específica","Restrição de Companhia Aérea por Política Interna"].map(option),d.airlinePreference)+select("Conexões","flightConnection",["","Aceita Conexão","Somente Voo Direto"].map(option),d.flightConnection)+'</div>'+(d.airlinePreference==="Somente Companhia Específica"?field("Companhia aérea obrigatória *","specificAirline",d.specificAirline,"text","required"):"")+(d.airlinePreference==="Restrição de Companhia Aérea por Política Interna"?field("Companhia restrita *","restrictedAirline",d.restrictedAirline,"text","required"):"")+select("Cabine","cabinClass",["","Econômica","Executiva","Misto / Por Cargo"].map(option),d.cabinClass)+(d.cabinClass==="Misto / Por Cargo"?textarea("Distribuição de cabines *","cabinClassNotes",d.cabinClassNotes):"")+'</div>';
 }
 if(step===3){
 const services=[["Aéreo",d.svcAereo],["Hospedagem",d.svcHospedagem],["Salas e alimentação",d.svcEspacoAlimentacao],["Transfers",d.svcTransfers]].filter(x=>x[1]).map(x=>x[0]);
 body='<h2 class="form-heading">Revise antes de registrar V'+((state.project?.briefings?.[0]?.version||0)+1)+'</h2><p class="form-intro">A versão anterior continuará acessível. Após salvar, não será possível editar este snapshot; para alterar, crie outra versão.</p><div class="review-box">'+row("Evento",d.eventName)+row("Destino",d.destination)+row("Participantes",d.participantsUnknown?"Não definidos":d.totalPassengers)+row("Período",d.datesUnknown?"Indefinido":date(d.departureDate)+" — "+date(d.returnDate))+row("Serviços",services.join(", "))+'<p class="field-help" style="margin-top:15px">Validação de campos condicionais no servidor. RFQs já existentes não mudam automaticamente.</p></div>';
 }
 const footer='<div class="form-footer"><button type="button" class="btn" data-action="wizard-back">'+(step===0?"Cancelar":"Voltar")+'</button><button class="btn btn-primary" type="submit">'+(step===3?"Registrar nova versão imutável":"Continuar "+icon("arrow"))+'</button></div>';
 return header("Briefing versionado","Nova versão do briefing","Estruture o pedido de forma guiada e preserve exatamente o escopo usado nos convites anteriores.")+nav+surf(steps[step],"Etapa "+(step+1)+" de 4",'<form class="form surface-body" data-form="wizard">'+body+footer+'</form>');
}
function render(){
 if(!state.user)return renderLogin();
 let body="";
 if(state.route==="queue")body=queue();
 else if(state.route==="projects")body=projectsPage();
 else if(state.route==="new_project")body=newProject();
 else if(state.route==="new_client")body=newClient();
 else if(state.route==="suppliers")body=suppliersPage();
 else if(state.route==="new_supplier")body=newSupplier();
 else if(state.route==="wizard")body=wizard();
 else if(state.route==="project"){
  if(!state.project){body=header("Projeto","Carregando projeto","Consultando histórico e permissões.");}
  else {body=projectHeader();
    body+=({overview:projectOverview,briefing:briefingOverview,rfq:rfqPage,quotes:quotePage,proposal:proposalPage,planning:planningPage})[state.tab]?.()||projectOverview();}
 }
 shell(body);
 updateQuotePreview();
}
function renderLogin(message=""){
 root.innerHTML='<div class="auth-layout"><div class="auth-panel"><div class="brand-row"><span class="brand-symbol">↗</span><span class="brand-word">nexo</span><span class="brand-note">Alpha</span></div><div><div class="kicker" style="color:#FF850D">AMBIENTE DE OPERAÇÃO</div><h1>Da solicitação à decisão, sem perder o histórico.</h1><p>Briefings versionados, fornecedores no contexto do projeto e cotações auditáveis. Sem painéis decorativos ou métricas fictícias.</p></div><p>Nome e marca de trabalho. Produto em desenvolvimento.</p></div><div class="auth-form-area"><form class="auth-card form" data-form="login"><h2>Entrar no ambiente</h2><p>Utilize suas credenciais de acesso.</p>'+field("E-mail","email","","email",'autocomplete="username" required')+field("Senha","password","","password",'autocomplete="current-password" required')+'<button class="btn btn-primary" type="submit">Acessar workspace</button><div class="status-message" aria-live="polite">'+esc(message)+'</div></form></div></div>';
}
async function refreshProject(){if(!state.pid)return;state.project=await api("/api/projects/"+state.pid);}
async function loadLists(){
 const [ps,cs,d,s]=await Promise.all([api("/api/projects"),api("/api/clients"),api("/api/dashboard"),canSeeMoney()?api("/api/suppliers"):Promise.resolve([])]);
 state.projects=ps;state.clients=cs;state.dashboard=d;state.suppliers=s;
}
function pathState(){const q=new URLSearchParams(location.search);const id=Number(q.get("project"));if(id>0){state.pid=id;state.route="project";state.tab=q.get("tab")||"overview";}else state.route=q.get("page")||"queue";}
function updateURL(){
 const q=new URLSearchParams();
 if(state.route==="project"||state.route==="wizard"){q.set("project",String(state.pid));q.set("tab",state.route==="wizard"?"briefing":state.tab);}
 else if(state.route!=="queue")q.set("page",state.route);
 history.pushState({}, "", "/app"+(q.size?"?"+q.toString():""));
}
async function navigate(route,tab="overview",pid=null){
 state.mobile=false;
 state.route=route;state.tab=tab;
 if(pid){state.pid=pid;state.rfqBatch=null;state.proposalLink=null;await refreshProject();}
 if(route!=="project"&&route!=="wizard")state.pid=null;
 updateURL();render();window.scrollTo(0,0);
}
async function openProject(id){state.pid=id;state.project=null;await navigate("project","overview",id);}
function captureWizard(form){
 const value=getForm(form);
 if(state.wizardStep===0){Object.assign(state.draft,value);state.draft.participantsUnknown=!!value.participantsUnknown;state.draft.datesUnknown=!!value.datesUnknown;if(state.draft.participantsUnknown)state.draft.totalPassengers="";if(state.draft.datesUnknown){state.draft.departureDate="";state.draft.returnDate="";}}
 if(state.wizardStep===1){for(const name of ["svcAereo","svcHospedagem","svcEspacoAlimentacao","svcTransfers"])state.draft[name]=!!value[name];}
 if(state.wizardStep===2){Object.assign(state.draft,value);state.draft.cateringServices=value.cateringServices||[];state.draft.transferTypes=value.transferTypes||[];}
}
function startWizard(){state.wizardStep=0;state.draft=wizardPayload();state.route="wizard";updateURL();render();window.scrollTo(0,0);}
function calcPreviewFromForm(f){
 const obj=getForm(f);let unit=0;try{unit=toCents(obj.unit_net);}catch{return "Revise o custo NET unitário.";}
 const q=Number(obj.quantity)||0,tax=Number(obj.tax_pct)||0,fee=Number(obj.fee_pct)||0;
 if(!Number.isInteger(q)||q<=0||tax<0||tax>100||fee<0||fee>100)return "Revise quantidade e percentuais.";
 const amounts=moneyBreakdown({quantity:q,unit_net_cents:unit,tax_bps:Math.round(tax*100),fee_bps:Math.round(fee*100)});
 return "NET total: "+money(amounts.net)+" · Tributos: "+money(amounts.tax)+" · Fee: "+money(amounts.fee)+" · Venda: "+money(amounts.total);
}
function updateQuotePreview(){const f=document.querySelector('form[data-form="quote-item"]');const out=document.getElementById("quote-preview");if(f&&out)out.textContent=calcPreviewFromForm(f);}
function toCents(value){
 const s=String(value??"").trim().replace(/\s/g,"").replace(/^R\$/i,"");
 const norm=s.includes(",")?s.replace(/\./g,"").replace(",","."):s;
 if(!/^\d+(?:\.\d{1,2})?$/.test(norm))throw new Error("Informe valores em reais com até duas casas decimais, por exemplo 612,00.");
 const cents=Math.round(Number(norm)*100);
 if(!Number.isSafeInteger(cents)||cents<0)throw new Error("Valor fora do limite permitido.");
 return cents;
}
function toBps(value){const v=Number(String(value||"0").replace(",","."));if(!Number.isFinite(v)||v<0||v>100)throw new Error("Percentual deve estar entre 0 e 100.");return Math.round(v*100);}
async function submitForm(form){
 const kind=form.dataset.form,data=getForm(form);
 try{
  if(kind==="login"){
   const r=await api("/api/auth/login",{method:"POST",body:{email:data.email,password:data.password}});
   state.user=r.user;state.csrf=r.csrf_token;await loadLists();pathState();if(state.pid)await refreshProject();render();notify("Acesso validado.");
  } else if(kind==="new-client"){
   await api("/api/clients",{method:"POST",body:{name:data.name,contact_email:data.contact_email||""}});
   await loadLists();await navigate("new_project");notify("Cliente registrado.");
  }else if(kind==="new-project"){
   const resp=await api("/api/projects",{method:"POST",body:{title:data.title,client_id:Number(data.client_id),destination:data.destination||"",starts_at:data.starts_at||"",ends_at:data.ends_at||"",attendees:Number(data.attendees||0),services:data.services||[]}});
   await loadLists();await openProject(resp.id);startWizard();notify("Projeto criado. Preencha a primeira revisão do briefing.");
  }else if(kind==="new-supplier"){
   await api("/api/suppliers",{method:"POST",body:{name:data.name,category:data.category,city:data.city||"",contact_name:data.contact_name||"",email:data.email||"",phone:data.phone||""}});
   await loadLists();await navigate("suppliers");notify("Fornecedor cadastrado.");
  }else if(kind==="wizard"){
   captureWizard(form);
   if(state.wizardStep===1&&!["svcAereo","svcHospedagem","svcEspacoAlimentacao","svcTransfers"].some(x=>state.draft[x]))throw new Error("Selecione ao menos um serviço.");
   if(state.wizardStep<3){state.wizardStep++;render();window.scrollTo(0,0);}
   else{
    const r=await api("/api/projects/"+state.pid+"/briefings",{method:"POST",body:{payload:state.draft}});
    state.draft=null;await refreshProject();await navigate("project","briefing");notify("Briefing V"+r.version+" registrada. Versões anteriores preservadas.");
   }
  }else if(kind==="rfq-batch"){
   const ids=(data.supplier_ids||[]).map(Number);
   if(!ids.length)throw new Error("Selecione ao menos um fornecedor.");
   state.rfqBatch=await api("/api/projects/"+state.pid+"/rfq-batches",{method:"POST",body:{supplier_ids:ids,deadline:data.deadline||""}});
   await refreshProject();render();notify("Links privados gerados. Ainda não enviados.");
  }else if(kind==="quote-item"){
   const body={category:data.category,description:data.description,quantity:Number(data.quantity),unit_net_cents:toCents(data.unit_net),tax_bps:toBps(data.tax_pct),fee_bps:toBps(data.fee_pct)};
   await api("/api/projects/"+state.pid+"/quote-items",{method:"POST",body});
   await refreshProject();render();notify("Item gravado e recalculado pela API.");
  }else if(kind==="new-task"){
   await api("/api/projects/"+state.pid+"/tasks",{method:"POST",body:{title:data.title,due_date:data.due_date||""}});
   await refreshProject();render();notify("Tarefa adicionada.");
  }else if(kind==="rfq-response"){
   await api("/api/public/rfq/"+encodeURIComponent(state.publicToken)+"/response",{method:"POST",body:{available:data.available,net_cents:toCents(data.net),tax_bps:toBps(data.tax_pct),conditions:data.conditions||"",cancellation:data.cancellation||"",notes:data.notes||""}});
   root.innerHTML=publicPage("Resposta registrada","Obrigado. Sua resposta foi vinculada ao pedido. Não é necessário reenviar.",'<span class="tag success">Recebida</span>');notify("Resposta enviada.");
  }else if(kind==="public-decision"){
   await api("/api/public/proposal/"+encodeURIComponent(state.publicToken)+"/decision",{method:"POST",body:{decision:data.decision,actor:data.actor||"Cliente",comment:data.comment||""}});
   root.innerHTML=publicPage("Decisão registrada","Sua decisão foi vinculada à versão publicada da proposta.",'<span class="tag success">Registrada</span>');
  }
 }catch(err){const msg=errorMessage(err);notify(msg,"error");if(kind==="login"){const node=form.querySelector(".status-message");if(node)node.textContent=msg;}if(err.status===401&&kind!=="login")renderLogin(msg);}
}
async function action(button){
 const name=button.dataset.action;
 try{
 if(name==="toggle-nav"){state.mobile=!state.mobile;render();}
 else if(name==="logout"){await api("/api/auth/logout",{method:"POST"});state.user=null;state.csrf="";history.replaceState({},"","/app");renderLogin();}
 else if(name==="nav"){await navigate(button.dataset.route);}
 else if(name==="all-projects"){await navigate("projects");}
 else if(name==="suppliers"){await navigate("suppliers");}
 else if(name==="new-project"){await navigate("new_project");}
 else if(name==="new-client"){await navigate("new_client");}
 else if(name==="new-supplier"){await navigate("new_supplier");}
 else if(name==="open-project"){await openProject(Number(button.dataset.id));}
 else if(name==="project-tab"){state.tab=button.dataset.tab;state.route="project";updateURL();render();}
 else if(name==="go-briefing"){state.tab="briefing";state.route="project";updateURL();render();}
 else if(name==="go-quotes"){state.tab="quotes";state.route="project";updateURL();render();}
 else if(name==="start-briefing"){startWizard();}
 else if(name==="wizard-back"){if(state.wizardStep===0){state.draft=null;await navigate("project","briefing");}else{state.wizardStep--;render();}}
 else if(name==="wizard-jump"){const jump=Number(button.dataset.step);if(jump<=state.wizardStep){state.wizardStep=jump;render();}}
 else if(name==="remove-item"){if(confirm("Excluir este item do orçamento? O valor da cotação será recalculado.")){await api("/api/projects/"+state.pid+"/quote-items/"+Number(button.dataset.id),{method:"DELETE"});await refreshProject();render();notify("Item excluído.");}}
 else if(name==="mark-rfq-sent"){const batch=state.rfqBatch;if(!batch)return;await api("/api/rfq-batches/"+batch.batch_id+"/send",{method:"POST"});state.rfqBatch=null;await refreshProject();render();notify("Envio manual registrado. O sistema não despachou e-mails.");}
 else if(name==="copy-rfq"){const item=state.rfqBatch?.links[Number(button.dataset.index)];if(item){await navigator.clipboard.writeText(location.origin+item.response_path);notify("Link copiado. Compartilhe apenas com o fornecedor indicado.");}}
 else if(name==="create-proposal"){const r=await api("/api/projects/"+state.pid+"/proposals",{method:"POST"});state.proposalLink=r;await refreshProject();render();notify("Snapshot da proposta V"+r.version+" criado. Publique antes de enviar.");}
 else if(name==="copy-proposal"){const p=state.proposalLink;if(p){await navigator.clipboard.writeText(location.origin+p.review_path);notify("Link da proposta copiado.");}}
 else if(name==="publish-proposal"){const p=state.proposalLink;if(!p)return;if(confirm("Publicar esta versão? O snapshot não poderá ser alterado.")){await api("/api/proposals/"+p.id+"/publish",{method:"POST"});p.status="published";await refreshProject();render();notify("Proposta publicada. Envie o link manualmente ao cliente.");}}
 else if(name==="toggle-task"){const id=Number(button.dataset.id);const next=button.dataset.status==="done"?"pending":"done";await api("/api/projects/"+state.pid+"/tasks/"+id,{method:"PATCH",body:{status:next}});await refreshProject();render();notify("Status da tarefa atualizado.");}
 }catch(err){notify(errorMessage(err),"error");if(err.status===401)renderLogin(errorMessage(err));}
}
function publicPage(title,subtitle,content){return '<div class="public-layout"><header class="public-top"><span class="brand-symbol">↗</span><strong style="font-size:21px">nexo</strong><span style="margin-left:auto;color:#B8BDC4;font-size:11px">Alpha · acesso por link</span></header><main id="work-main" class="public-body"><div class="kicker">Operação compartilhada</div><h1>'+esc(title)+'</h1><p>'+esc(subtitle)+'</p><div style="height:22px"></div>'+content+'<p class="public-footer">Acesso restrito ao destinatário do link. Não encaminhe a terceiros.</p></main></div>';}
async function openPublic(){
 const path=location.pathname,parts=path.split("/").filter(Boolean);
 const type=parts[0],token=parts[1];state.publicToken=token;
 try{
  if(type==="rfq"){
   const r=await api("/api/public/rfq/"+encodeURIComponent(token));
   const body=surf("Solicitação recebida","Conferir escopo antes de responder.",'<div class="surface-body">'+row("Projeto",r.title)+row("Destino",r.destination)+row("Período",date(r.starts_at)+" — "+date(r.ends_at))+row("Briefing",String(r.briefing_version))+row("Prazo",date(r.deadline))+'</div>');
   const response=r.status==="responded"?'<div class="notice success">Resposta já registrada para esta solicitação.</div>':surf("Responder ao pedido","Os dados são enviados somente ao solicitante desta RFQ.",'<form class="form surface-body" data-form="rfq-response">'+select("Disponibilidade", "available",[["available","Disponível"],["partial","Parcial"],["unavailable","Indisponível"]],"available")+'<div class="form-row">'+field("Custo NET informado (R$) *","net","0,00","text",'required inputmode="decimal"')+field("Impostos estimados (%)","tax_pct","0","number",'min="0" max="100" step=".01"')+'</div>'+textarea("Condições comerciais","conditions")+textarea("Política de cancelamento","cancellation")+textarea("Observações adicionais","notes")+'<button class="btn btn-primary" type="submit">Enviar resposta</button></form>');
   root.innerHTML=publicPage("Pedido de cotação · "+r.supplier_name,"Confira os dados do projeto e responda apenas ao escopo recebido.",body+'<div style="height:18px"></div>'+response);
  }else if(type==="proposal"){
   const r=await api("/api/public/proposal/"+encodeURIComponent(token)),snap=r.snapshot||{},items=snap.items||[];
   const table=surf("Serviços incluídos","Valores de venda, sem custos internos da operação.",'<div class="table-wrap" tabindex="0" aria-label="Itens da proposta"><table class="data-table compact"><thead><tr><th>Categoria</th><th>Serviço</th><th>Quantidade</th><th class="money">Total</th></tr></thead><tbody>'+items.map(x=>'<tr><td>'+esc(x.category)+'</td><th>'+esc(x.description)+'</th><td>'+quantity(x.quantity)+'</td><td class="money">'+money(x.sale_total_cents)+'</td></tr>').join("")+'</tbody></table></div><div class="inline-totals"><div><small>Total da proposta</small><strong>'+money(r.total_cents)+'</strong></div></div>');
   const decision=r.status==="published"?surf("Registrar decisão","Esta decisão ficará registrada junto à versão publicada.",'<form class="form surface-body" data-form="public-decision">'+field("Seu nome *","actor","","text","required")+select("Decisão","decision",[["approved","Aprovar"],["changes_requested","Solicitar ajustes"],["rejected","Rejeitar"]],"approved")+textarea("Comentário","comment")+ '<button class="btn btn-primary" type="submit">Confirmar decisão</button></form>'):'<div class="notice neutral">Esta versão está no estado: '+esc(statusMap[r.status]||r.status)+'.</div>';
   root.innerHTML=publicPage(snap.project?.title||"Proposta comercial","Versão "+r.version+" · "+(snap.project?.protocol||"Projeto")+" · "+date(snap.project?.starts_at),table+'<div style="height:18px"></div>'+decision);
  }else root.innerHTML=publicPage("Página não encontrada","Este endereço não corresponde a um link público reconhecido.","");
 }catch(err){root.innerHTML=publicPage("Link indisponível","O link pode ter vencido, sido revogado ou não existir. Peça um novo convite ao responsável.",'<div class="notice error">'+esc(errorMessage(err))+'</div>');}
}
root.addEventListener("click",event=>{const btn=event.target.closest("[data-action]");if(btn){event.preventDefault();action(btn);}});
root.addEventListener("submit",event=>{const form=event.target.closest("form[data-form]");if(form){event.preventDefault();if(form.reportValidity())submitForm(form);}});
root.addEventListener("input",event=>{if(event.target.closest('form[data-form="quote-item"]'))updateQuotePreview();});
root.addEventListener("change",event=>{
 if(state.route!=="wizard"||!state.draft||![0,2].includes(state.wizardStep))return;
 const t=event.target;
 if(["participantsUnknown","datesUnknown"].includes(t.name)&&state.wizardStep===0){captureWizard(t.form);render();}
 else if(["hotelLocationPref","airlinePreference","cabinClass"].includes(t.name)&&state.wizardStep===2){captureWizard(t.form);render();}
});
window.addEventListener("popstate",()=>{if(state.user){pathState();(state.pid?refreshProject():Promise.resolve()).then(render).catch(err=>notify(errorMessage(err),"error"));}});
(async function init(){
 if(/^\/(rfq|proposal)\//.test(location.pathname)){await openPublic();return;}
 try{
  const me=await api("/api/auth/me");state.user=me;state.csrf=me.csrf_token;await loadLists();pathState();if(state.pid)await refreshProject();render();
 }catch(err){renderLogin(err.status===401?"":"Não foi possível conectar ao ambiente. Tente entrar novamente.");}
})();
