from test_workflow import client, login


def test_lodging_rate_source(client):
    headers = login(client)
    project = client.get('/api/projects', headers=headers).json()[0]
    path = f"/api/projects/{project['id']}"
    supplier = client.get('/api/suppliers', headers=headers).json()[0]
    batch = client.post(path+'/rfq-batches', headers=headers, json={'supplier_ids':[supplier['id']]}).json()
    client.post(f"/api/rfq-batches/{batch['batch_id']}/send", headers=headers)
    token = batch['links'][0]['response_path'].split('/')[-1]
    assert client.post('/api/public/rfq/'+token+'/response', json={'net_cents':48000,'available':'available'}).status_code == 200
    rfq = client.get(path, headers=headers).json()['rfqs'][0]
    item = dict(category='Hospedagem',description='Standard',rooms=10,nights=3,quantity=30,
                unit_net_cents=48000,source_rfq_id=rfq['id'],tax_bps=500,fee_bps=300)
    response = client.post(path+'/quote-items', headers=headers, json=item)
    assert response.status_code == 201, response.text
    result = response.json()
    assert (result['rooms'],result['nights'],result['source_rfq_id'],result['supplier_id']) == (10,3,rfq['id'],supplier['id'])
    assert result['net_total_cents'] == 1440000
    assert result['sale_total_cents'] == 1557360
    for changes, expected in [({'quantity':29},422),({'nights':0},422),({'source_rfq_id':999999},404)]:
        assert client.post(path+'/quote-items',headers=headers,json={**item,**changes}).status_code == expected
