"""Casos de paridade funcional com NEXO/briefing-rules.js; implementação Python independente."""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.briefing_rules import collect_issues, prepare_submission

TODAY='2030-01-01'

def valid(**overrides):
    return {
        'companyName':'Empresa de Teste',
        'requesterName':'Solicitante Silva',
        'email':'solicitante@empresa.com.br',
        'eventName':'Encontro de lideranças',
        'destination':'São Paulo - SP',
        'totalPassengers':'40',
        'departureDate':'2030-01-10',
        'returnDate':'2030-01-12',
        'svcAereo':True,
        **overrides
    }

def fields(payload):
    return {x['field'] for x in collect_issues(payload,TODAY)}

def test_missing_fields_give_actionable_errors():
    expected={'companyName','requesterName','email','eventName','destination','totalPassengers','departureDate','returnDate','services'}
    for data in (None,[],{}):
        issues=collect_issues(data,TODAY)
        assert expected<={x['field'] for x in issues}
        assert all(set(x)=={'step','field','fieldId','label','message'} for x in issues)

def test_valid_base_and_plus_alias_email():
    assert collect_issues(valid(),TODAY)==[]
    assert 'email' not in fields(valid(email='ana+eventos@empresa.com.br'))

@pytest.mark.parametrize('email',['ana souza@exemplo.com','ana@empresa .com','ana@','exemplo.com','ana@@empresa.com'])
def test_invalid_emails(email):
    assert 'email' in fields(valid(email=email))

@pytest.mark.parametrize('d',['2030-02-29','2030-04-31','2030-13-01','2030-00-10','2030-01-00','2030-1-10','10/01/2030'])
def test_invalid_dates(d):
    assert 'departureDate' in fields(valid(departureDate=d))
    assert 'returnDate' in fields(valid(returnDate=d))

def test_date_and_participant_unknown_flags():
    data=valid(datesUnknown=True,datesFlexible=True,departureDate='2020-01-01',
        returnDate='bad',participantsUnknown=True,participantsEstimated=True,totalPassengers='-1')
    assert not {'departureDate','returnDate','totalPassengers'} & fields(data)
    clean=prepare_submission(data)
    assert clean['departureDate']==clean['returnDate']==clean['totalPassengers']==''
    assert clean['datesFlexible'] is False and clean['participantsEstimated'] is False

@pytest.mark.parametrize('value',['0','-1','1.5','1e2','abc','100001'])
def test_participants_must_be_safe_positive_integers(value):
    assert 'totalPassengers' in fields(valid(totalPassengers=value,participantsEstimated=True))

@pytest.mark.parametrize('service',['true',1,{}])
def test_service_selection_is_strict_boolean(service):
    got=fields(valid(svcAereo=service))
    assert {'svcAereo','services'}<=got

def test_flight_conditional_fields():
    assert 'specificAirline' in fields(valid(airlinePreference='Somente Companhia Específica'))
    assert 'specificAirline' not in fields(valid(airlinePreference='Somente Companhia Específica',specificAirline='LATAM'))
    assert 'restrictedAirline' in fields(valid(airlinePreference='Restrição de Companhia Aérea por Política Interna'))
    assert 'cabinClassNotes' in fields(valid(cabinClass='Misto / Por Cargo'))
    assert 'maxLayoverHours' in fields(valid(flightConnection='Aceita Conexão',maxLayoverHours='0'))
    assert 'maxLayoverHours' not in fields(valid(flightConnection='Aceita Conexão',maxLayoverHours='1.5'))

def test_lodging_and_meeting_rooms_validation():
    assert 'hotelLocationOther' in fields(valid(svcHospedagem=True,hotelLocationPref='Outro'))
    assert 'hotelLocationOther' not in fields(valid(svcHospedagem=True,hotelLocationPref='Outro',hotelLocationOther='Centro'))
    for field in ('roomsSingle','roomsDoubleTwin','roomsDoubleCasal','roomsTriple'):
        assert field in fields(valid(svcHospedagem=True,**{field:'-1'}))
        assert field not in fields(valid(svcHospedagem=True,**{field:'0'}))
    assert 'plenaryCapacity' in fields(valid(svcEspacoAlimentacao=True,plenaryCapacity='0.5'))

def test_coffee_break_and_transfer_conditions():
    assert 'coffeeBreakPerDay' in fields(valid(svcEspacoAlimentacao=True,cateringServices=['Coffee Break'],coffeeBreakPerDay='9'))
    assert 'coffeeBreakPerDay' not in fields(valid(svcEspacoAlimentacao=True,cateringServices=['Coffee Break'],coffeeBreakPerDay='2'))
    prepared=prepare_submission(valid(svcTransfers=True,transferTypes=['Aeroporto ↔ Hotel'],dedicatedVehicleHoursDays='8 horas'))
    assert prepared['dedicatedVehicleHoursDays']==''
    assert prepared['transferTypes']==['Aeroporto ↔ Hotel']

def test_normalize_excludes_injected_and_inactive_data():
    data=valid(svcAereo=False,svcTransfers=True,departureTimes=['Manhã'],
        specificAirline='LATAM',aereoGuidance=True,transferTypes=['Aeroporto ↔ Hotel',1],
        companyName='  Empresa  ',injectedAdmin=True)
    cleaned=prepare_submission(data)
    assert 'injectedAdmin' not in cleaned
    assert cleaned['companyName']=='Empresa'
    assert cleaned['specificAirline']==''
    assert cleaned['departureTimes']==[]
    assert cleaned['aereoGuidance'] is False
    assert cleaned['transferTypes']==['Aeroporto ↔ Hotel']
    assert data['companyName']=='  Empresa  '

def test_tampered_types_and_arrays_rejected():
    assert 'datesUnknown' in fields(valid(datesUnknown='true'))
    assert 'departureTimes' in fields(valid(departureTimes=[1]))
    assert 'departureTimes' in fields(valid(departureTimes=['x'*301]))
    assert 'generalNotes' in fields(valid(generalNotes='x'*10001))

def test_api_uses_service_validation_and_preserves_briefing_v1(tmp_path,monkeypatch):
    monkeypatch.setenv('NEXO_DEMO','1')
    monkeypatch.setenv('NEXO_DB_PATH',str(tmp_path/'service-test.sqlite3'))
    from backend import db
    monkeypatch.setattr(db,'DB_PATH',tmp_path/'service-test.sqlite3')
    from backend.main import app
    with TestClient(app) as c:
        auth=c.post('/api/auth/login',json={'email':'admin@nexo.local','password':'NexoDemo!2026'}).json()
        headers={'X-Nexo-CSRF':auth['csrf_token']}
        pid=c.get('/api/projects',headers=headers).json()[0]['id']
        original=c.get(f'/api/projects/{pid}',headers=headers).json()['briefings'][0]['payload']
        bad=c.post(f'/api/projects/{pid}/briefings',headers=headers,json={'payload':valid(email='invalido')})
        assert bad.status_code==422
        assert 'email' in {x['field'] for x in bad.json()['detail']['issues']}
        good=c.post(f'/api/projects/{pid}/briefings',headers=headers,json={'payload':valid(svcHospedagem=True,roomsSingle='8')})
        assert good.status_code==201,good.text
        v=c.get(f'/api/projects/{pid}',headers=headers).json()['briefings']
        assert v[0]['version']==2 and v[1]['version']==1
        assert v[1]['payload']==original
        assert v[0]['payload']['roomsSingle']=='8'
        assert 'injectedAdmin' not in v[0]['payload']
