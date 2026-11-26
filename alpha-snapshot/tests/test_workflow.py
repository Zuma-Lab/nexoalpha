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
    assert 'O evento é um só.' in home.text
    assert 'Sua equipe precisa conduzir eventos.' in home.text
    assert 'E-mails, planilhas e versões desencontradas' in home.text
    assert 'Menos informação dispersa.' in home.text
    assert 'id="retrabalho"' not in home.text
    # Ajuste de copy não introduz novas imagens ou novas estruturas.
    assert 'class="hero-note"' in home.text
    assert 'class="hero-visual"' not in home.text
    assert 'class="briefing-visual"' not in home.text
    assert client.get('/styles.css').status_code==200
    assert client.get('/app.js').status_code==200
    assert client.get('/assets/logo-white.svg').status_code==200
    assert client.get('/app-assets/app.js').status_code==200
    workspace=client.get('/app')
    assert workspace.status_code==200
    assert 'Operação | NEXO Alpha' in workspace.text
    assert client.get('/app-assets/styles.css').status_code==200
    assert 'NEXO Alpha — workspace V2' in client.get('/app-assets/app.js').text


def test_briefing_draft_is_private_validated_by_csrf_and_cleared_on_publish(client):
    h=login(client)
    pid=client.get('/api/projects',headers=h).json()[0]['id']
    path=f'/api/projects/{pid}/briefing-draft'
    assert client.get(path,headers=h).json()['payload'] is None
    draft={'eventName':'Revisão interna','destination':'São Paulo','totalPassengers':'130'}
    assert client.put(path,json={'payload':draft}).status_code==403
    saved=client.put(path,headers=h,json={'payload':draft})
    assert saved.status_code==200,saved.text
    assert client.get(path,headers=h).json()['payload']==draft
    assert client.put(path,headers=h,json={'payload':{'long':'x'*70000}}).status_code==422
    versions_before=len(client.get(f'/api/projects/{pid}',headers=h).json()['briefings'])
    assert versions_before==1
    r=client.post(f'/api/projects/{pid}/briefings',headers=h,json={'payload':{
        'objective':'Nova versão imutável','attendees':130,'destination':'São Paulo',
        'services':['Hospedagem']}})
    assert r.status_code==201,r.text
    assert r.json()['version']==2
    assert client.get(path,headers=h).json()['payload'] is None
    assert len(client.get(f'/api/projects/{pid}',headers=h).json()['briefings'])==2


def test_viewer_cannot_create_or_read_private_briefing_draft(client):
    h=login(client)
    user=client.post('/api/users',headers=h,json={
      'full_name':'Auditor Externo','email':'auditor@example.com',
      'password':'AValidPassword_2026','role':'viewer'})
    assert user.status_code==201,user.text
    viewer=client.post('/api/auth/login',json={
      'email':'auditor@example.com','password':'AValidPassword_2026'})
    assert viewer.status_code==200
    path='/api/projects/1/briefing-draft'
    assert client.get(path).status_code==403
    assert client.put(path,headers={'X-Nexo-CSRF':viewer.json()['csrf_token']},
       json={'payload':{'eventName':'Test'}}).status_code==403


def test_proposal_editor_snapshots_terms_and_hides_internal_costs(client):
    h=login(client)
    pid=client.get('/api/projects',headers=h).json()[0]['id']
    payload={'introduction':'Convenção anual — hospedagem e salas confirmadas',
             'terms':'Café incluso. Cancelamento conforme política do fornecedor.'}
    r=client.post(f'/api/projects/{pid}/proposals',headers=h,json=payload)
    assert r.status_code==201,r.text
    saved=r.json()
    token=saved['review_path'].split('/')[-1]
    assert client.get('/api/public/proposal/'+token).status_code==404
    assert client.post(f"/api/proposals/{saved['id']}/publish",headers=h).status_code==200
    public=client.get('/api/public/proposal/'+token)
    assert public.status_code==200,public.text
    data=public.json()
    assert data['snapshot']['introduction']==payload['introduction']
    assert data['snapshot']['terms']==payload['terms']
    raw=str(data['snapshot'])
    assert 'unit_net_cents' not in raw
    assert 'net_total_cents' not in raw
    assert 'fee_bps' not in raw
    assert 'tax_bps' not in raw
    # Revisões criam snapshots novos, sem alterar a proposta publicada.
    next_r=client.post(f'/api/projects/{pid}/proposals',headers=h,json={'terms':'Nova condição'})
    assert next_r.status_code==201,next_r.text
    assert next_r.json()['version']==saved['version']+1
    still=client.get('/api/public/proposal/'+token).json()
    assert still['snapshot']['terms']==payload['terms']


def test_consultant_queue_uses_factual_stage_without_leaking_finances(client):
    assert client.get('/api/consultant/queue').status_code == 401
    h = login(client)
    endpoint='/api/consultant/queue'
    base=client.get(endpoint,headers=h)
    assert base.status_code == 200,base.text
    data=base.json()
    assert data['scope']=='company'
    assert len(data['items'])==1
    assert data['items'][0]['action_type']=='validate_briefing'
    assert data['items'][0]['tab']=='briefing'
    assert 'net_cents' not in str(data)
    assert 'token_hash' not in str(data)

    pid=data['items'][0]['project_id']
    suppliers=client.get('/api/suppliers',headers=h).json()
    batch=client.post(f'/api/projects/{pid}/rfq-batches',headers=h,
       json={'supplier_ids':[suppliers[0]['id']], 'deadline':'2027-01-30'})
    assert batch.status_code==201,batch.text
    prepared=client.get(endpoint,headers=h).json()['items'][0]
    assert prepared['action_type']=='verify_manual_invites'
    assert prepared['tab']=='rfq'
    assert prepared['prepared_rfqs']==1

    # A new briefing may invalidate the exact scope of an existing invitation.
    r=client.post(f'/api/projects/{pid}/briefings',headers=h,json={'payload':{
        'objective':'Revisão 2','attendees':132,'destination':'São Paulo',
        'services':['Hospedagem']}})
    assert r.status_code==201,r.text
    changed=client.get(endpoint,headers=h).json()['items'][0]
    assert changed['action_type']=='review_scope_change'
    assert changed['briefing_version']==2
    assert 'reenvio automático' in changed['detail']

    # Queue cannot be used to access any other company's projects.
    from backend.db import connect
    from backend.security import hash_password
    with connect() as db:
        cid=db.execute("INSERT INTO companies(name) VALUES('Outra agência')").lastrowid
        clientid=db.execute("INSERT INTO clients(company_id,name) VALUES(?,?)",(cid,'Cliente externo')).lastrowid
        db.execute("""INSERT INTO projects(company_id,client_id,protocol,title,status)
           VALUES (?,?,?,?,?)""",(cid,clientid,'NX-OTHER-001','Evento de outro tenant','briefing'))
    after=client.get(endpoint,headers=h).json()
    assert len(after['items'])==1
    assert 'Outro tenant' not in str(after)
    assert 'Outra agência' not in str(after)


def test_consultant_queue_access_roles(client):
    h=login(client)
    co=client.get('/api/clients',headers=h).json()[0]['id']
    for role,email,client_id in [
        ('client','operadora.cliente@example.com',co),
        ('viewer','auditor.workspace@example.com',None),
        ('consultant','consultor.workspace@example.com',None)
    ]:
        user=client.post('/api/users',headers=h,json={
            'full_name':'Pessoa de Teste','email':email,
            'password':'AValidPassword_2026','role':role,'client_id':client_id})
        assert user.status_code==201,user.text
        from fastapi.testclient import TestClient
        from backend.main import app
        with TestClient(app) as c:
            session=c.post('/api/auth/login',json={
                'email':email,'password':'AValidPassword_2026'})
            assert session.status_code==200
            result=c.get('/api/consultant/queue')
            assert result.status_code==(200 if role=='consultant' else 403)
            if role=='consultant':
                assert result.json()['items'][0]['owner_is_me'] is False


def test_rfq_reissue_after_reopening_project(client):
    headers=login(client)
    pid=client.get('/api/projects',headers=headers).json()[0]['id']
    suppliers=client.get('/api/suppliers',headers=headers).json()
    batch=client.post(f'/api/projects/{pid}/rfq-batches',headers=headers,
        json={'supplier_ids':[supplier['id'] for supplier in suppliers[:2]]})
    assert batch.status_code==201
    original,other=batch.json()['links']
    detail=client.get(f'/api/projects/{pid}',headers=headers).json()
    invitation=next(row for row in detail['rfqs'] if row['id']==original['rfq_id'])
    assert 'token_hash' not in invitation and 'response_path' not in invitation
    path=f"/api/rfqs/{invitation['id']}/reissue-link"
    payload={'expected_expiry':invitation['expires_at']}
    assert client.post(path,json=payload).status_code==403
    assert client.post(f"/api/rfqs/{invitation['id']}/revoke-link",headers=headers).status_code==200
    result=client.post(path,headers=headers,json=payload)
    assert result.status_code==200,result.text
    assert result.headers['cache-control']=='no-store'
    new_url='/api/public'+result.json()['response_path']
    assert client.get('/api/public'+original['response_path']).status_code==404
    assert client.get('/api/public'+other['response_path']).status_code==200
    assert client.post(path,headers=headers,json=payload).status_code==409
    invitation_response=client.get(new_url)
    assert invitation_response.status_code==200
    assert invitation_response.json()['supplier_name']==invitation['supplier_name']
    assert client.post(new_url+'/response',json={'net_cents':100}).status_code==200
    assert client.post(path,headers=headers,json={'expected_expiry':result.json()['expires_at']}).status_code==409


def test_manual_delivery_of_one_invitation_after_reload(client):
    headers=login(client)
    project=client.get('/api/projects').json()[0]
    url=f"/api/projects/{project['id']}"
    suppliers=client.get('/api/suppliers').json()[:2]
    batch=client.post(url+'/rfq-batches',headers=headers,json={'supplier_ids':[s['id'] for s in suppliers],'deadline':'2027-03-01'}).json()
    first,second=batch['links']
    path=f"/api/rfqs/{first['rfq_id']}"
    rotated=client.post(path+'/reissue-link',headers=headers,json={'expected_expiry':first['expires_at']}).json()
    for _ in range(2):
        assert client.post(path+'/manual-delivery',headers=headers,json={'expected_expiry':rotated['expires_at']}).status_code==200
    rows={row['id']:row for row in client.get(url).json()['rfqs']}
    assert rows[first['rfq_id']]['deadline']=='2027-03-01'
    assert rows[first['rfq_id']]['sent_at']
    assert rows[second['rfq_id']]['status']=='prepared'
    assert rows[second['rfq_id']]['sent_at'] is None
    assert rows[first['rfq_id']]['batch_id']==rows[second['rfq_id']]['batch_id']


def test_saved_proposal_review_and_reshare(client):
    headers=login(client)
    pid=client.get('/api/projects').json()[0]['id']
    created=client.post(f'/api/projects/{pid}/proposals',headers=headers,json={'terms':'Condição original'}).json()
    path=f"/api/proposals/{created['id']}"
    preview=client.get(path+'/preview').json()
    assert preview['snapshot']['terms']=='Condição original'
    assert 'unit_net_cents' not in preview['snapshot']['items'][0]
    assert client.post(path+'/publish',headers=headers).status_code==200
    payload={'expected_expiry':preview['expires_at']}
    rotated=client.post(path+'/reissue-link',headers=headers,json=payload)
    assert rotated.status_code==200
    assert client.get('/api/public'+created['review_path']).status_code==404
    assert client.get('/api/public'+rotated.json()['review_path']).json()['snapshot']==preview['snapshot']
    assert client.post(path+'/reissue-link',headers=headers,json=payload).status_code==409
