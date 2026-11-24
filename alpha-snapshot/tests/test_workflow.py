import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

@pytest.fixture()
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('NEXO_DB_PATH',str(tmp_path/'test.sqlite3'))
    monkeypatch.setenv('NEXO_DEMO','1')
    monkeypatch.setenv('NEXO_LEADS_ADMIN_EMAIL','admin@nexo.local')
    from backend import db as db_module
    monkeypatch.setattr(db_module,'DB_PATH',tmp_path/'test.sqlite3')
    from backend.main import app
    with TestClient(app) as c:
        yield c

def login(c):
    r=c.post('/api/auth/login',json={'email':'admin@nexo.local','password':'NexoDemo!2026'})
    assert r.status_code==200,r.text
    return {'X-Nexo-CSRF':r.json()['csrf_token']}

def test_bootstrap_and_auth(client):
    assert client.get('/api/health').json()['status']=='ok'
    assert client.get('/api/projects').status_code==401
    assert client.post('/api/auth/login',json={'email':'admin@nexo.local','password':'wrong'}).status_code==401
    h=login(client)
    assert client.get('/api/projects',headers=h).status_code==200
    assert len(client.get('/api/dashboard',headers=h).json()['projects'])==1


def test_complete_business_workflow(client):
    h=login(client)
    co=client.post('/api/clients',headers=h,json={'name':'Cliente de teste','contact_email':'cliente@example.com'}).json()
    proj=client.post('/api/projects',headers=h,json={'title':'Encontro comercial','client_id':co['id'],'destination':'Rio de Janeiro','starts_at':'2027-04-01','ends_at':'2027-04-03','attendees':50,'budget_cents':14000000,'services':['Hospedagem','Transfers']})
    assert proj.status_code==201,proj.text
    pid=proj.json()['id']
    original=client.get(f'/api/projects/{pid}',headers=h).json()['briefings'][0]
    new=client.post(f'/api/projects/{pid}/briefings',headers=h,json={'payload':{'objective':'Escopo atualizado','attendees':52,'destination':'Rio de Janeiro','services':['Hospedagem']}})
    assert new.status_code==201
    assert new.json()['version']==2
    briefs=client.get(f'/api/projects/{pid}',headers=h).json()['briefings']
    assert briefs[1]['payload']==original['payload']
    suppliers=client.get('/api/suppliers',headers=h).json()
    batch=client.post(f'/api/projects/{pid}/rfq-batches',headers=h,json={'supplier_ids':[suppliers[0]['id'],suppliers[1]['id']],'deadline':'2027-03-01'})
    assert batch.status_code==201,batch.text
    rfq_token=batch.json()['links'][0]['response_path'].split('/')[-1]
    bid=batch.json()['batch_id']
    assert client.get('/api/public/rfq/'+rfq_token).json()['briefing_version']==2
    assert client.post(f'/api/rfq-batches/{bid}/send',headers=h).json()['status']=='sent'
    assert client.post(f'/api/rfq-batches/{bid}/send',headers=h).json()['status']=='already_sent'
    response=client.post('/api/public/rfq/'+rfq_token+'/response',json={'net_cents':500000,'tax_bps':500,'available':'available','conditions':'Café incluso'})
    assert response.status_code==200,response.text
    assert client.post('/api/public/rfq/'+rfq_token+'/response',json={'net_cents':100}).status_code==409
    quote=client.post(f'/api/projects/{pid}/quote-items',headers=h,json={'category':'Hospedagem','description':'Quartos','quantity':3,'unit_net_cents':10000,'tax_bps':500,'fee_bps':1000})
    assert quote.status_code==201,quote.text
    assert quote.json()['net_total_cents']==30000
    assert quote.json()['tax_cents']==1500
    assert quote.json()['fee_cents']==3150
    assert quote.json()['sale_total_cents']==34650
    prop=client.post(f'/api/projects/{pid}/proposals',headers=h)
    assert prop.status_code==201,prop.text
    token=prop.json()['review_path'].split('/')[-1]
    assert client.get('/api/public/proposal/'+token).status_code==404
    propid=prop.json()['id']
    assert client.post(f'/api/proposals/{propid}/publish',headers=h).status_code==200
    published=client.get('/api/public/proposal/'+token).json()
    assert published['total_cents']==34650
    # More quote items cannot change an already published proposal.
    client.post(f'/api/projects/{pid}/quote-items',headers=h,json={'category':'Transfers','description':'Veículo','quantity':1,'unit_net_cents':20000})
    assert client.get('/api/public/proposal/'+token).json()['total_cents']==34650
    decided=client.post('/api/public/proposal/'+token+'/decision',json={'decision':'approved','actor':'Responsável comercial','comment':'Confirmado'})
    assert decided.status_code==200
    assert client.post('/api/public/proposal/'+token+'/decision',json={'decision':'rejected'}).status_code==409
    assert client.get(f'/api/projects/{pid}',headers=h).json()['status']=='approved'
    task=client.post(f'/api/projects/{pid}/tasks',headers=h,json={'title':'Revisar rooming list','due_date':'2027-03-01'}).json()
    assert client.patch(f'/api/projects/{pid}/tasks/{task["id"]}',headers=h,json={'status':'done'}).status_code==200
    audit=client.get(f'/api/projects/{pid}',headers=h).json()['audit']
    assert any(a['action']=='proposal.approved' for a in audit)


def test_tenant_client_permissions(client):
    h=login(client)
    company=client.get('/api/clients',headers=h).json()[0]
    created=client.post('/api/users',headers=h,json={'full_name':'Solicitante Externo','email':'cliente@nexo.local','password':'supersecret123','role':'client','client_id':company['id']})
    assert created.status_code==201,created.text
    ch={'X-Nexo-CSRF':client.post('/api/auth/login',json={'email':'cliente@nexo.local','password':'supersecret123'}).json()['csrf_token']}
    assert client.get('/api/suppliers',headers=ch).status_code==403
    assert client.post('/api/suppliers',headers=ch,json={'name':'Hotel Novo','category':'Hospedagem'}).status_code==403
    visible=client.get('/api/projects',headers=ch).json()
    assert visible and all(x['client_id']==company['id'] for x in visible)
    detail=client.get('/api/projects/'+str(visible[0]['id']),headers=ch).json()
    assert detail['quote_items']==[]
    assert detail['rfqs']==[]
    assert detail['audit']==[]
    # Reautenticar administrador: cookie substitui a sessão anterior do cliente.
    h=login(client)
    other=client.post('/api/clients',headers=h,json={'name':'Cliente Isolado'}).json()
    p=client.post('/api/projects',headers=h,json={'title':'Projeto de outra empresa','client_id':other['id']}).json()
    ch={'X-Nexo-CSRF':client.post('/api/auth/login',json={'email':'cliente@nexo.local','password':'supersecret123'}).json()['csrf_token']}
    assert client.get(f'/api/projects/{p["id"]}',headers=ch).status_code==404
    assert client.post(f'/api/projects/{p["id"]}/briefings',headers=ch,json={'payload':{'objective':'leak'}}).status_code==404
def test_login_rate_limit_cookie_and_csrf(client):
    for _ in range(5):
        assert client.post('/api/auth/login',json={'email':'admin@nexo.local','password':'errada'}).status_code==401
    assert client.post('/api/auth/login',json={'email':'admin@nexo.local','password':'NexoDemo!2026'}).status_code==429
    # O segundo usuário nunca autenticado não pode reutilizar o cookie da tentativa bloqueada.
    assert client.get('/api/auth/me').status_code==401


def test_csrf_enforced_on_authenticated_writes(client):
    h=login(client)
    auth=client.get('/api/auth/me')
    assert auth.status_code==200
    assert auth.json()['csrf_token']==h['X-Nexo-CSRF']
    assert client.post('/api/clients',json={'name':'Bloqueado'}).status_code==403
    assert client.post('/api/clients',headers={'X-Nexo-CSRF':'wrong'},json={'name':'Bloqueado'}).status_code==403
    assert client.post('/api/clients',headers=h,json={'name':'Autorizado'}).status_code==201
    assert 'httponly' in client.post('/api/auth/login',json={'email':'admin@nexo.local','password':'NexoDemo!2026'}).headers['set-cookie'].lower()


def test_public_token_expiration_revocation_and_batch_idempotency(client):
    h=login(client)
    suppliers=client.get('/api/suppliers',headers=h).json()
    p=client.get('/api/projects',headers=h).json()[0]
    pid=p['id']
    batch=client.post(f'/api/projects/{pid}/rfq-batches',headers=h,
        json={'supplier_ids':[suppliers[0]['id']]}).json()
    token=batch['links'][0]['response_path'].rsplit('/',1)[-1]
    rfqid=batch['links'][0]['rfq_id']
    assert batch['links'][0]['expires_at']
    assert client.get('/api/public/rfq/'+token).status_code==200
    assert client.post(f"/api/rfq-batches/{batch['batch_id']}/send",headers=h).json()['status']=='sent'
    assert client.post(f"/api/rfq-batches/{batch['batch_id']}/send",headers=h).json()['status']=='already_sent'
    with __import__('backend.db',fromlist=['connect']).connect() as db:
        audit=db.execute("SELECT COUNT(*) FROM audit_logs WHERE action='rfq.batch_marked_sent' AND detail=?",
            (f"Lote #{batch['batch_id']} (envio manual por link)",)).fetchone()[0]
        assert audit==1
        db.execute('UPDATE rfqs SET expires_at=? WHERE id=?',('1970-01-01T00:00:00+00:00',rfqid))
    assert client.get('/api/public/rfq/'+token).status_code==404
    assert client.post('/api/public/rfq/'+token+'/response',json={'net_cents':20}).status_code==404
    assert client.post(f'/api/rfqs/{rfqid}/revoke-link',headers=h).status_code==200


def test_proposal_snapshots_and_public_expiration(client):
    h=login(client)
    pid=client.get('/api/projects',headers=h).json()[0]['id']
    q=client.post(f'/api/projects/{pid}/quote-items',headers=h,json={
        'category':'Hospedagem','description':'Item A','quantity':1,'unit_net_cents':101,
        'tax_bps':1250,'fee_bps':300})
    assert q.status_code==201
    assert q.json()['tax_cents']==13
    assert q.json()['fee_cents']==3
    assert q.json()['sale_total_cents']==117
    v1=client.post(f'/api/projects/{pid}/proposals',headers=h).json()
    assert client.post(f"/api/proposals/{v1['id']}/publish",headers=h).status_code==200
    t1=v1['review_path'].rsplit('/',1)[-1]
    public_v1=client.get('/api/public/proposal/'+t1).json()
    assert 'company_id' not in public_v1
    snap1=public_v1['snapshot']
    assert all('unit_net_cents' not in item and 'net_total_cents' not in item and
               'tax_cents' not in item and 'fee_cents' not in item and
               'supplier_id' not in item for item in snap1['items'])
    assert any(item['sale_total_cents']==117 for item in snap1['items'])
    client.post(f'/api/projects/{pid}/quote-items',headers=h,json={
        'category':'Aéreo','description':'Item B','quantity':1,'unit_net_cents':99})
    v2=client.post(f'/api/projects/{pid}/proposals',headers=h).json()
    assert v2['version']==v1['version']+1
    assert client.post(f"/api/proposals/{v2['id']}/publish",headers=h).status_code==200
    assert client.get('/api/public/proposal/'+t1).json()['snapshot']==snap1
    assert v2['total_cents']==v1['total_cents']+99
    t2=v2['review_path'].rsplit('/',1)[-1]
    with __import__('backend.db',fromlist=['connect']).connect() as db:
        db.execute('UPDATE proposals SET expires_at=? WHERE id=?',('1970-01-01T00:00:00+00:00',v2['id']))
    assert client.get('/api/public/proposal/'+t2).status_code==404
    assert client.post('/api/public/proposal/'+t2+'/decision',json={'decision':'approved'}).status_code==404
    assert client.post(f"/api/proposals/{v1['id']}/revoke-link",headers=h).status_code==200
    assert client.get('/api/public/proposal/'+t1).status_code==404


def test_demo_request_validation_and_persistence(client):
    good={'name':'Ana Souza','email':'ana@example.com','company':'Empresa Exemplo','event_type':'Eventos corporativos'}
    r=client.post('/api/public/demo-requests',json=good)
    assert r.status_code==201,r.text
    assert r.json()['ok'] is True
    assert client.post('/api/public/demo-requests',json={**good,'email':'inválido'}).status_code==422
    h=login(client)
    leads=client.get('/api/demo-requests',headers=h).json()
    assert len(leads)==1
    assert leads[0]['email']=='ana@example.com'

def test_product_homepage_and_workspace_routes(client):
    home=client.get('/')
    assert home.status_code==200
    assert 'Do briefing à proposta aprovada' in home.text
    assert client.get('/styles.css').status_code==200
    assert client.get('/app.js').status_code==200
    assert client.get('/assets/logo-white.svg').status_code==200
    assert client.get('/app-assets/app.js').status_code==200
    workspace=client.get('/app')
    assert workspace.status_code==200
    assert 'Operação | NEXO Alpha' in workspace.text
    assert client.get('/app-assets/styles.css').status_code==200
    assert 'workspace-v2' in client.get('/app-assets/app.js').text
