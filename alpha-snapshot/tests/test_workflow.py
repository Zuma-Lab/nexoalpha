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
    from backend.main import app
    with TestClient(app) as c:
        yield c

def login(c):
    r=c.post('/api/auth/login',json={'email':'admin@nexo.local','password':'NexoDemo!2026'})
    assert r.status_code==200,r.text
    return {'Authorization':'Bearer '+r.json()['access_token']}

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
    token=client.post('/api/auth/login',json={'email':'cliente@nexo.local','password':'supersecret123'}).json()['access_token']
    ch={'Authorization':'Bearer '+token}
    assert client.get('/api/suppliers',headers=ch).status_code==403
    assert client.post('/api/suppliers',headers=ch,json={'name':'Hotel Novo','category':'Hospedagem'}).status_code==403
    visible=client.get('/api/projects',headers=ch).json()
    assert visible and all(x['client_id']==company['id'] for x in visible)
    detail=client.get('/api/projects/'+str(visible[0]['id']),headers=ch).json()
    assert detail['quote_items']==[]
    assert detail['rfqs']==[]
    assert detail['audit']==[]
    other=client.post('/api/clients',headers=h,json={'name':'Cliente Isolado'}).json()
    p=client.post('/api/projects',headers=h,json={'title':'Projeto de outra empresa','client_id':other['id']}).json()
    assert client.get(f'/api/projects/{p["id"]}',headers=ch).status_code==404
    assert client.post(f'/api/projects/{p["id"]}/briefings',headers=ch,json={'payload':{'objective':'leak'}}).status_code==404