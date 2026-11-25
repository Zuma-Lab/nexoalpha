"use strict";
const menuButton=document.querySelector(".menu-toggle");
const nav=document.querySelector("#site-nav");
const dialog=document.querySelector("#login-dialog");
menuButton?.addEventListener("click",()=>{
 const expanded=menuButton.getAttribute("aria-expanded")==="true";
 menuButton.setAttribute("aria-expanded",String(!expanded));
 nav?.classList.toggle("open",!expanded);
});
nav?.querySelectorAll("a").forEach(link=>link.addEventListener("click",()=>{
 nav.classList.remove("open");
 menuButton?.setAttribute("aria-expanded","false");
}));
document.querySelectorAll("[data-login]").forEach(button=>button.addEventListener("click",()=>{
 if(typeof dialog.showModal==="function") dialog.showModal();
 else window.location.assign("/app");
}));
document.querySelector(".close-dialog")?.addEventListener("click",()=>dialog.close());
dialog?.addEventListener("click",event=>{if(event.target===dialog)dialog.close()});
function displayStatus(node,message,kind="error"){node.textContent=message;node.className="form-status "+kind;}
async function postJson(url,data){
 const response=await fetch(url,{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(data)});
 let payload=null;
 try{payload=await response.json()}catch{}
 if(!response.ok){
   const detail=typeof payload?.detail==="string"?payload.detail:null;
   if(response.status===429)throw new Error("Muitas tentativas. Tente novamente mais tarde.");
   if(response.status>=500)throw new Error("Serviço temporariamente indisponível. Tente novamente mais tarde.");
   throw new Error(detail||"Não foi possível concluir. Confira os dados e tente novamente.");
 }
 return payload;
}
document.querySelector("#login-form")?.addEventListener("submit",async event=>{
 event.preventDefault();
 const form=event.currentTarget,status=document.querySelector("#login-status");
 if(!form.reportValidity())return;
 const button=form.querySelector("button[type=submit]");
 button.disabled=true;
 displayStatus(status,"Validando acesso…","info");
 try{
   const data=await postJson("/api/auth/login",{email:form.elements.email.value.trim(),password:form.elements.password.value});
   if(!data?.user)throw new Error("O servidor não confirmou a autenticação.");
   window.location.assign("/app");
 }catch(error){displayStatus(status,error.message)}
 finally{button.disabled=false}
});
document.querySelector("#demo-form")?.addEventListener("submit",async event=>{
 event.preventDefault();
 const form=event.currentTarget,status=document.querySelector("#demo-status");
 if(!form.reportValidity())return;
 const button=form.querySelector("button[type=submit]");
 button.disabled=true;
 displayStatus(status,"Enviando solicitação…","info");
 try{
   const data=await postJson("/api/public/demo-requests",{
     name:form.elements.name.value.trim(),
     email:form.elements.email.value.trim(),
     company:form.elements.company.value.trim(),
     event_type:form.elements.event_type.value,
     website:form.elements.website.value
   });
   if(data?.ok!==true)throw new Error("A solicitação ainda não foi confirmada pelo servidor.");
   displayStatus(status,"Solicitação recebida. Entraremos em contato pelo e-mail informado.","success");
   form.reset();
 }catch(error){displayStatus(status,error.message)}
 finally{button.disabled=false}
});