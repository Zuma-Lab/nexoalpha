"""NEXO Alpha: standalone FastAPI/SQLite backend, newly authored. 
Run: uvicorn backend.main:app --reload
"""
from __future__ import annotations
import json
import os
import hmac
import hashlib
import secrets
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Header, Body, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .db import init_db, connect, rows
from .security import hash_password, verify_password, make_token, token_hash
from .briefing_rules import collect_issues, prepare_submission

FRONTEND = Path(__file__).resolve().parents[1]/'workspace-v2'
HOMEPAGE = Path(__file__).resolve().parents[2]/'homepage'/'dist'
COOKIE_NAME = 'nexo_session'
RATE_KEY = os.environ.get('NEXO_RATE_LIMIT_SECRET','').encode() or secrets.token_bytes(32)

def jload(x):
    try: return json.loads(x or 'null')
    except json.JSONDecodeError: return None

def required(db, query, params=(), status=404):
    row=db.execute(query,params).fetchone()
    if row is None: raise HTTPException(status, 'Recurso não encontrado ou sem acesso')
    return dict(row)

def audit(db,co,actor,action,project=None,detail=''):
    db.execute('INSERT INTO audit_logs(company_id,project_id,actor_id,action,detail) VALUES (?,?,?,?,?)',(co,project,actor,action,detail))

def now(): return datetime.now(timezone.utc).isoformat()

def money_item(item):
    net=item['quantity']*item['unit_net_cents']
    tax=(net*item['tax_bps']+5000)//10000
    fee=((net+tax)*item['fee_bps']+5000)//10000
    return {**item,'net_total_cents':net,'tax_cents':tax,'fee_cents':fee,'sale_total_cents':net+tax+fee}

def seed_demo():
    if os.environ.get('NEXO_DEMO') != '1': return
    with connect() as db:
        if db.execute('SELECT COUNT(*) FROM companies').fetchone()[0]: return
        co=db.execute('INSERT INTO companies(name) VALUES(?)',('NEXO Workspace',)).lastrowid
        admin=db.execute('INSERT INTO users(company_id,full_name,email,password_hash,role) VALUES (?,?,?,?,?)',(co,'Administrador Nexo','admin@nexo.local',hash_password('NexoDemo!2026'),'admin')).lastrowid
        client=db.execute('INSERT INTO clients(company_id,name,contact_email) VALUES (?,?,?)',(co,'Aurora Tecnologia','eventos@aurora.exemplo')).lastrowid
        for name,cat,city,email in [
            ('Hotel Arcos','Hospedagem','São Paulo','contato@arcos.exemplo'),
            ('Vista Convention','Salas e A&B','São Paulo','eventos@vista.exemplo'),
            ('Mobilis Transfer','Transfers','São Paulo','comercial@mobilis.exemplo'),
            ('Atlas Travel','Aéreo','São Paulo','reservas@atlas.exemplo')]:
            db.execute('INSERT INTO suppliers(company_id,name,category,city,email) VALUES (?,?,?,?,?)',(co,name,cat,city,email))
        p=db.execute('''INSERT INTO projects(company_id,client_id,owner_id,protocol,title,destination,starts_at,ends_at,attendees,budget_cents,status,services)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(co,client,admin,'NX-2026-00001','Encontro de Lideranças 2027','São Paulo','2027-02-18','2027-02-20',120,28000000,'qualifying',json.dumps(['Hospedagem','Salas e A&B','Transfers']))).lastrowid
        brief={'objective':'Encontro anual de planejamento estratégico','event_type':'Convenção','attendees':120,'destination':'São Paulo','start_date':'2027-02-18','end_date':'2027-02-20','services':['Hospedagem','Salas e A&B','Transfers'],'lodging':{'single':20,'twin':50,'nights':2,'breakfast':True},'venue':{'room_setup':'Auditório','coffee_breaks':4},'transport':{'airport_to_hotel':True},'notes':'Preferir fornecedores com política flexível de cancelamento.'}
        db.execute('INSERT INTO briefing_versions(company_id,project_id,version,payload,created_by) VALUES (?,?,?,?,?)',(co,p,1,json.dumps(brief,ensure_ascii=False),admin))
        db.execute('INSERT INTO quote_items(company_id,project_id,category,description,quantity,unit_net_cents,tax_bps,fee_bps) VALUES (?,?,?,?,?,?,?,?)',(co,p,'Hospedagem','Aptos standard / diária',120,48000,500,1000))
        for title,due in [('Validar rooming list','2027-01-28'),('Consolidar propostas de hotéis','2027-02-02'),('Confirmar agenda e A&B','2027-02-10')]:
            db.execute('INSERT INTO plan_tasks(company_id,project_id,title,due_date) VALUES (?,?,?,?)',(co,p,title,due))
        audit(db,co,admin,'project.created',p,'Ambiente de demonstração')

@asynccontextmanager
async def lifespan(app):
    init_db();seed_demo();yield

app=FastAPI(title='NEXO Alpha API',version='0.1.0',lifespan=lifespan)

class Login(BaseModel):
    email:str
    password:str

class DemoRequestIn(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:str=Field(min_length=5,max_length=160)
    company:str=Field(min_length=2,max_length=160)
    event_type:str=Field(default='',max_length=100)
    website:str=Field(default='',max_length=200)

def fingerprint(kind:str,value:str)->str:
    return hmac.new(RATE_KEY,(kind+':'+value).encode(),hashlib.sha256).hexdigest()

def attempt_count(db,key,minutes):
    cutoff=(datetime.now(timezone.utc)-timedelta(minutes=minutes)).isoformat()
    return db.execute('SELECT COUNT(*) FROM login_attempts WHERE key=? AND occurred_at>?',(key,cutoff)).fetchone()[0]
class ProjectIn(BaseModel):
    title:str=Field(min_length=3,max_length=160)
    client_id:int
    destination:str=''
    starts_at:str=''
    ends_at:str=''
    attendees:int=Field(default=0,ge=0)
    budget_cents:int=Field(default=0,ge=0)
    services:list[str]=[]
class BriefingIn(BaseModel):
    payload:dict
class SupplierIn(BaseModel):
    name:str=Field(min_length=2)
    category:str
    city:str=''
    contact_name:str=''
    email:str=''
    phone:str=''
    preferred:bool=False
class RFQBatchIn(BaseModel):
    supplier_ids:list[int]=Field(min_length=1)
    deadline:str=''
class RFQResponseIn(BaseModel):
    available:Literal['available','partial','unavailable']='available'
    net_cents:int=Field(ge=0)
    tax_bps:int=Field(default=0,ge=0,le=10000)
    conditions:str=''
    cancellation:str=''
    notes:str=''
class QuoteItemIn(BaseModel):
    category:str
    description:str=Field(min_length=1)
    quantity:int=Field(ge=1)
    unit_net_cents:int=Field(ge=0)
    tax_bps:int=Field(default=0,ge=0,le=10000)
    fee_bps:int=Field(default=0,ge=0,le=10000)
    supplier_id:int|None=None
class PlanTaskIn(BaseModel):
    title:str=Field(min_length=2)
    due_date:str=''
    owner_id:int|None=None
class StatusIn(BaseModel):
    status:Literal['pending','in_progress','done']
class DecisionIn(BaseModel):
    decision:Literal['approved','changes_requested','rejected']
    comment:str=''
    actor:str='Cliente'
class ClientIn(BaseModel):
    name:str=Field(min_length=2)
    contact_email:str=''
class UserIn(BaseModel):
    full_name:str=Field(min_length=2)
    email:str
    password:str=Field(min_length=10)
    role:Literal['admin','consultant','client','viewer']
    client_id:int|None=None

def me(request:Request):
    token=request.cookies.get(COOKIE_NAME)
    if not token:raise HTTPException(401,'Acesso não autenticado')
    with connect() as db:
        user=db.execute('''SELECT u.id,u.company_id,u.client_id,u.full_name,u.email,u.role,u.active,s.csrf_token
          FROM sessions s JOIN users u ON u.id=s.user_id
          WHERE s.token_hash=? AND s.expires_at>?''',(token_hash(token),now())).fetchone()
    if not user or not user['active']:raise HTTPException(401,'Sessão inválida ou expirada')
    if request.method not in ('GET','HEAD','OPTIONS'):
        given=request.headers.get('X-Nexo-CSRF','')
        if not given or not hmac.compare_digest(given,user['csrf_token']):
            raise HTTPException(403,'CSRF inválido')
    return dict(user)

def allow(user,roles):
    if user['role'] not in roles: raise HTTPException(403,'Sem permissão para esta operação')

def project(db,pid,user):
    r=required(db,'SELECT * FROM projects WHERE id=? AND company_id=?',(pid,user['company_id']))
    if user['role']=='client' and r['client_id']!=user['client_id']: raise HTTPException(404,'Projeto não encontrado')
    return r

def normalize_project(p):
    p['services']=jload(p['services']) or []
    return p

@app.post('/api/auth/login')
def login(body:Login,request:Request,response:Response):
    ip=request.client.host if request.client else 'unknown'
    ipkey=fingerprint('ip',ip)
    userkey=fingerprint('email',body.email.strip().lower())
    with connect() as db:
        db.execute('DELETE FROM login_attempts WHERE occurred_at<?',((datetime.now(timezone.utc)-timedelta(days=2)).isoformat(),))
        if attempt_count(db,userkey,15)>=5 or attempt_count(db,ipkey,15)>=30:
            raise HTTPException(429,'Muitas tentativas. Tente mais tarde.')
        users=db.execute('SELECT * FROM users WHERE email=? COLLATE NOCASE AND active=1',(body.email.strip(),)).fetchall()
        match=next((dict(x) for x in users if verify_password(body.password,x['password_hash'])),None)
        if not match:
            db.executemany('INSERT INTO login_attempts(key,occurred_at) VALUES (?,?)',[(userkey,now()),(ipkey,now())])
            db.commit()
            raise HTTPException(401,'E-mail ou senha inválidos')
        db.execute('DELETE FROM login_attempts WHERE key=?',(userkey,))
        token=make_token()
        csrf=make_token()
        expires=(datetime.now(timezone.utc)+timedelta(hours=12)).isoformat()
        db.execute('INSERT INTO sessions(user_id,token_hash,csrf_token,expires_at) VALUES (?,?,?,?)',(match['id'],token_hash(token),csrf,expires))
    response.set_cookie(COOKIE_NAME,token,max_age=43200,httponly=True,
        secure=(os.environ.get('NEXO_SECURE_COOKIES')=='1' or request.url.scheme=='https'),
        samesite='strict',path='/')
    response.headers['Cache-Control']='no-store'
    return {'user':{k:match[k] for k in ('id','company_id','client_id','full_name','email','role')},'csrf_token':csrf}

@app.get('/api/auth/me')
def auth_me(user=Depends(me)):return user

@app.post('/api/auth/logout')
def logout(request:Request,response:Response,user=Depends(me)):
    with connect() as db:
        db.execute('DELETE FROM sessions WHERE token_hash=?',(token_hash(request.cookies[COOKIE_NAME]),))
    response.delete_cookie(COOKIE_NAME,path='/',samesite='strict')
    return {'ok':True}

@app.post('/api/public/demo-requests',status_code=201)
def request_demo(body:DemoRequestIn,request:Request):
    if body.website:return {'ok':True}
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',body.email.strip()):
        raise HTTPException(422,'E-mail inválido')
    ip=request.client.host if request.client else 'unknown'
    iphash=fingerprint('demo',ip)
    with connect() as db:
        count=db.execute("SELECT COUNT(*) FROM demo_requests WHERE source_ip_hash=? AND created_at>datetime('now','-1 day')",(iphash,)).fetchone()[0]
        if count>=5:raise HTTPException(429,'Limite de solicitações atingido.')
        db.execute('INSERT INTO demo_requests(name,email,company,event_type,source_ip_hash) VALUES (?,?,?,?,?)',
            (body.name.strip(),body.email.strip().lower(),body.company.strip(),body.event_type.strip(),iphash))
    return {'ok':True}

@app.get('/api/demo-requests')
def get_demo_requests(user=Depends(me)):
    allow(user,('admin',))
    owner=os.environ.get('NEXO_LEADS_ADMIN_EMAIL','').strip().lower()
    if not owner or user['email'].lower()!=owner:raise HTTPException(403,'Acesso restrito ao operador da plataforma')
    with connect() as db:
        return rows(db.execute('SELECT id,name,email,company,event_type,created_at FROM demo_requests ORDER BY id DESC LIMIT 200'))

@app.get('/api/dashboard')
def dashboard(user=Depends(me)):
    with connect() as db:
        scope=' AND client_id=?' if user['role']=='client' else ''
        params=[user['company_id']]+([user['client_id']] if scope else [])
        ps=rows(db.execute('SELECT * FROM projects WHERE company_id=?'+scope+' ORDER BY updated_at DESC LIMIT 8',params))
        counts={x['status']:x['n'] for x in rows(db.execute('SELECT status,COUNT(*) n FROM projects WHERE company_id=?'+scope+' GROUP BY status',params))}
        if user['role']=='client':
            task_count=db.execute('''SELECT COUNT(*) FROM plan_tasks t JOIN projects p ON p.id=t.project_id
              WHERE t.company_id=? AND p.client_id=? AND t.status!='done' ''',(user['company_id'],user['client_id'])).fetchone()[0]
        else:task_count=db.execute('SELECT COUNT(*) FROM plan_tasks WHERE company_id=? AND status!=?',(user['company_id'],'done')).fetchone()[0]
        for p in ps:normalize_project(p)
        return {'projects':ps,'counts':counts,'active':sum(v for k,v in counts.items() if k!='closed'), 'tasks_pending':task_count,'suppliers':db.execute('SELECT COUNT(*) FROM suppliers WHERE company_id=?',(user['company_id'],)).fetchone()[0] if user['role']!='client' else 0}

@app.get('/api/clients')
def clients(user=Depends(me)):
    with connect() as db:
        q='SELECT * FROM clients WHERE company_id=?'
        p=[user['company_id']]
        if user['role']=='client':q+=' AND id=?';p.append(user['client_id'])
        return rows(db.execute(q+' ORDER BY name',p))

@app.post('/api/clients',status_code=201)
def create_client(body:ClientIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        cid=db.execute('INSERT INTO clients(company_id,name,contact_email) VALUES (?,?,?)',(user['company_id'],body.name,body.contact_email)).lastrowid
        audit(db,user['company_id'],user['id'],'client.created',detail=body.name)
        return required(db,'SELECT * FROM clients WHERE id=?',(cid,))

@app.get('/api/projects')
def projects(user=Depends(me)):
    with connect() as db:
        q='''SELECT p.*,c.name client_name,u.full_name owner_name FROM projects p
          JOIN clients c ON c.id=p.client_id LEFT JOIN users u ON u.id=p.owner_id WHERE p.company_id=?'''
        params=[user['company_id']]
        if user['role']=='client':q+=' AND p.client_id=?';params.append(user['client_id'])
        result=rows(db.execute(q+' ORDER BY p.updated_at DESC',params))
        return [normalize_project(p) for p in result]

@app.post('/api/projects',status_code=201)
def create_project(body:ProjectIn,user=Depends(me)):
    allow(user,('admin','consultant','client'))
    with connect() as db:
        required(db,'SELECT id FROM clients WHERE id=? AND company_id=?',(body.client_id,user['company_id']))
        if user['role']=='client' and body.client_id!=user['client_id']: raise HTTPException(403,'Cliente inválido')
        cur=db.execute('''INSERT INTO projects(company_id,client_id,owner_id,protocol,title,destination,starts_at,ends_at,attendees,budget_cents,services)
          VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(user['company_id'],body.client_id,user['id'],'TEMP-'+make_token(),body.title,body.destination,body.starts_at,body.ends_at,body.attendees,body.budget_cents,json.dumps(body.services,ensure_ascii=False)))
        pid=cur.lastrowid
        protocol=f'NX-{datetime.now().year}-{pid:05d}'
        db.execute('UPDATE projects SET protocol=? WHERE id=?',(protocol,pid))
        brief={'objective':'','event_type':'','attendees':body.attendees,'destination':body.destination,'start_date':body.starts_at,'end_date':body.ends_at,'services':body.services,'notes':''}
        db.execute('INSERT INTO briefing_versions(company_id,project_id,version,payload,created_by) VALUES (?,?,?,?,?)',(user['company_id'],pid,1,json.dumps(brief,ensure_ascii=False),user['id']))
        audit(db,user['company_id'],user['id'],'project.created',pid,protocol)
        return normalize_project(required(db,'SELECT * FROM projects WHERE id=?',(pid,)))

@app.get('/api/projects/{pid}')
def get_project(pid:int,user=Depends(me)):
    with connect() as db:
        p=normalize_project(project(db,pid,user))
        p['client_name']=required(db,'SELECT name FROM clients WHERE id=?',(p['client_id'],))['name']
        p['briefings']=[dict(x, payload=jload(x['payload'])) for x in rows(db.execute('SELECT * FROM briefing_versions WHERE project_id=? ORDER BY version DESC',(pid,)))]
        p['quote_items']=[money_item(x) for x in rows(db.execute('SELECT * FROM quote_items WHERE project_id=? ORDER BY id',(pid,)))] if user['role']!='client' else []
        p['quote_total_cents']=sum(x['sale_total_cents'] for x in p['quote_items'])
        p['tasks']=rows(db.execute('SELECT t.*,u.full_name owner_name FROM plan_tasks t LEFT JOIN users u ON u.id=t.owner_id WHERE t.project_id=? ORDER BY due_date,id',(pid,)))
        p['proposals']=rows(db.execute('SELECT id,version,total_cents,status,published_at,created_at FROM proposals WHERE project_id=? ORDER BY version DESC',(pid,)))
        p['rfqs']=rows(db.execute('''SELECT r.id,r.batch_id,r.status,r.sent_at,r.responded_at,s.name supplier_name,s.category,s.city,
             rr.available,rr.net_cents,rr.conditions,rr.cancellation
             FROM rfqs r JOIN rfq_batches b ON b.id=r.batch_id JOIN suppliers s ON s.id=r.supplier_id
             LEFT JOIN rfq_responses rr ON rr.rfq_id=r.id WHERE b.project_id=? ORDER BY r.id DESC''',(pid,))) if user['role']!='client' else []
        p['audit']=rows(db.execute('''SELECT a.*,u.full_name actor_name FROM audit_logs a LEFT JOIN users u ON u.id=a.actor_id
          WHERE a.project_id=? ORDER BY a.id DESC LIMIT 75''',(pid,))) if user['role']!='client' else []
        return p

@app.post('/api/projects/{pid}/briefings',status_code=201)
def new_briefing(pid:int,body:BriefingIn,user=Depends(me)):
    allow(user,('admin','consultant','client'))
    with connect() as db:
        p=project(db,pid,user)
        payload=body.payload
        # O formato detalhado por serviço passa pela validação da lógica de negócio.
        service_format=('eventName' in payload or any(k in payload for k in ('svcAereo','svcHospedagem','svcEspacoAlimentacao','svcTransfers')))
        if service_format:
            issues=collect_issues(payload)
            if issues:raise HTTPException(422,{'issues':issues})
            payload=prepare_submission(payload)
        version=db.execute('SELECT COALESCE(MAX(version),0)+1 FROM briefing_versions WHERE project_id=?',(pid,)).fetchone()[0]
        db.execute('INSERT INTO briefing_versions(company_id,project_id,version,payload,created_by) VALUES (?,?,?,?,?)',(user['company_id'],pid,version,json.dumps(payload,ensure_ascii=False),user['id']))
        canonical=payload if not service_format else {
            'destination':payload['destination'],
            'start_date':payload['departureDate'],
            'end_date':payload['returnDate'],
            'attendees':int(payload['totalPassengers']) if payload['totalPassengers'] else 0,
        }
        for key,col in [('destination','destination'),('start_date','starts_at'),('end_date','ends_at'),('attendees','attendees')]:
            if key in canonical and type(canonical[key]) in (str,int):
                db.execute(f'UPDATE projects SET {col}=?,updated_at=CURRENT_TIMESTAMP WHERE id=?',(canonical[key],pid))
        audit(db,user['company_id'],user['id'],'briefing.versioned',pid,f'V{version}')
        return {'version':version,'project_id':pid}

@app.get('/api/suppliers')
def suppliers(user=Depends(me)):
    allow(user,('admin','consultant','viewer'))
    with connect() as db:
        return rows(db.execute('SELECT * FROM suppliers WHERE company_id=? ORDER BY name',(user['company_id'],)))

@app.post('/api/suppliers',status_code=201)
def create_supplier(body:SupplierIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        sid=db.execute('''INSERT INTO suppliers(company_id,name,category,city,contact_name,email,phone,preferred)
          VALUES (?,?,?,?,?,?,?,?)''',(user['company_id'],body.name,body.category,body.city,body.contact_name,body.email,body.phone,int(body.preferred))).lastrowid
        audit(db,user['company_id'],user['id'],'supplier.created',detail=body.name)
        return required(db,'SELECT * FROM suppliers WHERE id=?',(sid,))

@app.post('/api/projects/{pid}/rfq-batches',status_code=201)
def create_rfq_batch(pid:int,body:RFQBatchIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    if len(set(body.supplier_ids))!=len(body.supplier_ids):raise HTTPException(422,'Fornecedores duplicados')
    with connect() as db:
        project(db,pid,user)
        version=required(db,'SELECT id,version FROM briefing_versions WHERE project_id=? ORDER BY version DESC LIMIT 1',(pid,))
        for sid in body.supplier_ids:required(db,'SELECT id FROM suppliers WHERE id=? AND company_id=?',(sid,user['company_id']))
        bid=db.execute('INSERT INTO rfq_batches(company_id,project_id,briefing_version_id,deadline,created_by) VALUES (?,?,?,?,?)',(user['company_id'],pid,version['id'],body.deadline,user['id'])).lastrowid
        links=[]
        expires_at=(datetime.now(timezone.utc)+timedelta(days=14)).isoformat()
        for sid in body.supplier_ids:
            token=make_token()
            rid=db.execute('INSERT INTO rfqs(company_id,batch_id,supplier_id,token_hash,expires_at) VALUES (?,?,?,?,?)',(user['company_id'],bid,sid,token_hash(token),expires_at)).lastrowid
            links.append({'rfq_id':rid,'supplier_id':sid,'response_path':'/rfq/'+token,'expires_at':expires_at})
        db.execute('UPDATE projects SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?',('sourcing',pid))
        audit(db,user['company_id'],user['id'],'rfq.batch_created',pid,f'Lote #{bid}; briefing V{version["version"]}')
        return {'batch_id':bid,'briefing_version':version['version'],'links':links,'sent':False}

@app.post('/api/rfq-batches/{bid}/send')
def send_rfq_batch(bid:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        batch=required(db,'SELECT * FROM rfq_batches WHERE id=? AND company_id=?',(bid,user['company_id']))
        # Represents a recorded dispatch; actual email gateway not configured in Alpha.
        changed=db.execute('UPDATE rfq_batches SET sent_at=? WHERE id=? AND sent_at IS NULL',(now(),bid)).rowcount
        if not changed:return {'batch_id':bid,'status':'already_sent','delivered_via':'manual_link'}
        db.execute("UPDATE rfqs SET status='sent',sent_at=? WHERE batch_id=? AND status='prepared'",(now(),bid))
        audit(db,user['company_id'],user['id'],'rfq.batch_marked_sent',batch['project_id'],f'Lote #{bid} (envio manual por link)')
        return {'batch_id':bid,'status':'sent','delivered_via':'manual_link'}

@app.get('/api/public/rfq/{token}')
def public_rfq(token:str):
    with connect() as db:
        r=required(db,'''SELECT r.id,r.status,s.name supplier_name,p.protocol,p.title,p.destination,p.starts_at,p.ends_at,p.attendees,
          b.deadline,v.version briefing_version,v.payload briefing
          FROM rfqs r JOIN suppliers s ON s.id=r.supplier_id JOIN rfq_batches b ON b.id=r.batch_id
          JOIN projects p ON p.id=b.project_id JOIN briefing_versions v ON v.id=b.briefing_version_id WHERE r.token_hash=? AND r.revoked_at IS NULL AND r.expires_at>?''',(token_hash(token),now()))
        r['briefing']=jload(r['briefing'])
        return r

@app.post('/api/public/rfq/{token}/response')
def public_rfq_response(token:str,body:RFQResponseIn):
    with connect() as db:
        r=required(db,'SELECT * FROM rfqs WHERE token_hash=? AND revoked_at IS NULL AND expires_at>?',(token_hash(token),now()))
        if r['status']=='responded':raise HTTPException(409,'Resposta já registrada')
        db.execute('''INSERT INTO rfq_responses(company_id,rfq_id,available,net_cents,tax_bps,conditions,cancellation,notes)
          VALUES (?,?,?,?,?,?,?,?)''',(r['company_id'],r['id'],body.available,body.net_cents,body.tax_bps,body.conditions,body.cancellation,body.notes))
        db.execute("UPDATE rfqs SET status='responded',responded_at=? WHERE id=?",(now(),r['id']))
        p=db.execute('SELECT project_id FROM rfq_batches WHERE id=?',(r['batch_id'],)).fetchone()[0]
        audit(db,r['company_id'],None,'rfq.responded',p,f'RFQ #{r["id"]}')
        return {'ok':True}

@app.post('/api/projects/{pid}/quote-items',status_code=201)
def create_quote_item(pid:int,body:QuoteItemIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        project(db,pid,user)
        if body.supplier_id:required(db,'SELECT id FROM suppliers WHERE id=? AND company_id=?',(body.supplier_id,user['company_id']))
        item_id=db.execute('''INSERT INTO quote_items(company_id,project_id,supplier_id,category,description,quantity,unit_net_cents,tax_bps,fee_bps)
         VALUES (?,?,?,?,?,?,?,?,?)''',(user['company_id'],pid,body.supplier_id,body.category,body.description,body.quantity,body.unit_net_cents,body.tax_bps,body.fee_bps)).lastrowid
        db.execute("UPDATE projects SET status='quoting',updated_at=CURRENT_TIMESTAMP WHERE id=?",(pid,))
        audit(db,user['company_id'],user['id'],'quote.item_added',pid,body.description)
        return money_item(required(db,'SELECT * FROM quote_items WHERE id=?',(item_id,)))

@app.delete('/api/projects/{pid}/quote-items/{item_id}')
def delete_quote_item(pid:int,item_id:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        project(db,pid,user)
        required(db,'SELECT id FROM quote_items WHERE id=? AND project_id=?',(item_id,pid))
        db.execute('DELETE FROM quote_items WHERE id=?',(item_id,))
        audit(db,user['company_id'],user['id'],'quote.item_deleted',pid,str(item_id))
        return {'ok':True}

@app.post('/api/projects/{pid}/proposals',status_code=201)
def create_proposal(pid:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        p=project(db,pid,user)
        items=[money_item(x) for x in rows(db.execute('SELECT * FROM quote_items WHERE project_id=? ORDER BY id',(pid,)))]
        if not items:raise HTTPException(422,'Adicione itens à cotação antes da proposta')
        v=db.execute('SELECT COALESCE(MAX(version),0)+1 FROM proposals WHERE project_id=?',(pid,)).fetchone()[0]
        total=sum(i['sale_total_cents'] for i in items)
        snapshot=json.dumps({'project':{k:p[k] for k in ('title','protocol','destination','starts_at','ends_at','attendees')},'items':items,'total_cents':total},ensure_ascii=False)
        token=make_token()
        expires_at=(datetime.now(timezone.utc)+timedelta(days=30)).isoformat()
        propid=db.execute('INSERT INTO proposals(company_id,project_id,version,snapshot,total_cents,token_hash,created_by,expires_at) VALUES (?,?,?,?,?,?,?,?)',(user['company_id'],pid,v,snapshot,total,token_hash(token),user['id'],expires_at)).lastrowid
        audit(db,user['company_id'],user['id'],'proposal.created',pid,f'Versão {v}')
        return {'id':propid,'version':v,'total_cents':total,'status':'draft','review_path':'/proposal/'+token,'expires_at':expires_at}

@app.post('/api/proposals/{propid}/publish')
def publish_proposal(propid:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        p=required(db,'SELECT * FROM proposals WHERE id=? AND company_id=?',(propid,user['company_id']))
        if p['status']!='draft':raise HTTPException(409,'Proposta já publicada ou decidida')
        db.execute("UPDATE proposals SET status='published',published_at=? WHERE id=?",(now(),propid))
        db.execute("UPDATE projects SET status='proposal',updated_at=CURRENT_TIMESTAMP WHERE id=?",(p['project_id'],))
        audit(db,user['company_id'],user['id'],'proposal.published',p['project_id'],f'V{p["version"]}')
        return {'ok':True,'id':propid,'status':'published','delivery':'manual_link'}

@app.get('/api/public/proposal/{token}')
def public_proposal(token:str):
    with connect() as db:
        p=required(db,'SELECT id,project_id,company_id,version,status,snapshot,total_cents,published_at FROM proposals WHERE token_hash=? AND expires_at>? AND revoked_at IS NULL',(token_hash(token),now()))
        if p['status']=='draft':raise HTTPException(404,'Proposta ainda não publicada')
        private=jload(p['snapshot']) or {}
        # Cliente jamais recebe custos NET, tributos, fees, margens ou IDs internos.
        public_items=[{key:item.get(key) for key in ('category','description','quantity','sale_total_cents')}
          for item in private.get('items',[])]
        snapshot={'project':private.get('project',{}),'items':public_items,'total_cents':p['total_cents']}
        return {'version':p['version'],'status':p['status'],
          'snapshot':snapshot,'total_cents':p['total_cents'],'published_at':p['published_at']}

@app.post('/api/public/proposal/{token}/decision')
def public_decide(token:str,body:DecisionIn):
    with connect() as db:
        p=required(db,'SELECT * FROM proposals WHERE token_hash=? AND expires_at>? AND revoked_at IS NULL',(token_hash(token),now()))
        if p['status']!='published':raise HTTPException(409,'Proposta não está pendente de aprovação')
        db.execute('UPDATE proposals SET status=? WHERE id=?',(body.decision,p['id']))
        db.execute('INSERT INTO approval_decisions(company_id,proposal_id,actor,decision,comment) VALUES (?,?,?,?,?)',(p['company_id'],p['id'],body.actor[:100],body.decision,body.comment))
        if body.decision=='approved':db.execute("UPDATE projects SET status='approved',updated_at=CURRENT_TIMESTAMP WHERE id=?",(p['project_id'],))
        audit(db,p['company_id'],None,'proposal.'+body.decision,p['project_id'],f'V{p["version"]}: {body.comment[:200]}')
        return {'ok':True,'status':body.decision}

@app.post('/api/rfqs/{rfqid}/revoke-link')
def revoke_rfq(rfqid:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        r=required(db,'SELECT r.id,b.project_id FROM rfqs r JOIN rfq_batches b ON b.id=r.batch_id WHERE r.id=? AND r.company_id=?',(rfqid,user['company_id']))
        db.execute('UPDATE rfqs SET revoked_at=? WHERE id=? AND revoked_at IS NULL',(now(),rfqid))
        audit(db,user['company_id'],user['id'],'rfq.link_revoked',r['project_id'],str(rfqid))
    return {'ok':True}

@app.post('/api/proposals/{propid}/revoke-link')
def revoke_proposal_link(propid:int,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        p=required(db,'SELECT project_id FROM proposals WHERE id=? AND company_id=?',(propid,user['company_id']))
        db.execute('UPDATE proposals SET revoked_at=? WHERE id=? AND revoked_at IS NULL',(now(),propid))
        audit(db,user['company_id'],user['id'],'proposal.link_revoked',p['project_id'],str(propid))
    return {'ok':True}

@app.post('/api/projects/{pid}/tasks',status_code=201)
def create_task(pid:int,body:PlanTaskIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        project(db,pid,user)
        if body.owner_id:required(db,'SELECT id FROM users WHERE id=? AND company_id=?',(body.owner_id,user['company_id']))
        tid=db.execute('INSERT INTO plan_tasks(company_id,project_id,title,owner_id,due_date) VALUES (?,?,?,?,?)',(user['company_id'],pid,body.title,body.owner_id,body.due_date)).lastrowid
        audit(db,user['company_id'],user['id'],'task.created',pid,body.title)
        return required(db,'SELECT * FROM plan_tasks WHERE id=?',(tid,))

@app.patch('/api/projects/{pid}/tasks/{tid}')
def update_task(pid:int,tid:int,body:StatusIn,user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        project(db,pid,user)
        required(db,'SELECT * FROM plan_tasks WHERE id=? AND project_id=?',(tid,pid))
        db.execute('UPDATE plan_tasks SET status=? WHERE id=?',(body.status,tid))
        audit(db,user['company_id'],user['id'],'task.status_changed',pid,f'{tid}: {body.status}')
        return {'ok':True}

@app.get('/api/users')
def list_users(user=Depends(me)):
    allow(user,('admin','consultant'))
    with connect() as db:
        return rows(db.execute('SELECT id,company_id,client_id,full_name,email,role,active,created_at FROM users WHERE company_id=? ORDER BY full_name',(user['company_id'],)))

@app.post('/api/users',status_code=201)
def create_user(body:UserIn,user=Depends(me)):
    allow(user,('admin',))
    if body.role=='client' and body.client_id is None:raise HTTPException(422,'Usuário cliente precisa de empresa cliente')
    with connect() as db:
        if body.client_id:required(db,'SELECT id FROM clients WHERE id=? AND company_id=?',(body.client_id,user['company_id']))
        if db.execute('SELECT 1 FROM users WHERE company_id=? AND email=? COLLATE NOCASE',(user['company_id'],body.email)).fetchone():raise HTTPException(409,'E-mail já cadastrado')
        uid=db.execute('INSERT INTO users(company_id,client_id,full_name,email,password_hash,role) VALUES (?,?,?,?,?,?)',(user['company_id'],body.client_id,body.full_name,body.email,hash_password(body.password),body.role)).lastrowid
        audit(db,user['company_id'],user['id'],'user.created',detail=body.email)
        return required(db,'SELECT id,client_id,full_name,email,role,active FROM users WHERE id=?',(uid,))

@app.get('/api/health')
def health():return {'status':'ok','app':'nexo-alpha'}

app.mount('/assets',StaticFiles(directory=str(HOMEPAGE/'assets')),name='homepage-assets')
app.mount('/app-assets',StaticFiles(directory=str(FRONTEND)),name='app-assets')

@app.get('/',include_in_schema=False)
def homepage():
    return FileResponse(str(HOMEPAGE/'index.html'))

@app.get('/styles.css',include_in_schema=False)
def homepage_css():
    return FileResponse(str(HOMEPAGE/'styles.css'),media_type='text/css')

@app.get('/app.js',include_in_schema=False)
def homepage_js():
    return FileResponse(str(HOMEPAGE/'app.js'),media_type='application/javascript')

@app.get('/{path:path}',include_in_schema=False)
def frontend(path:str):
    return FileResponse(str(FRONTEND/'index.html'))