"""Validação independente de briefing por serviço, baseada em casos do legado NEXO.
Não importa JavaScript nem componentes da aplicação anterior.
"""
from __future__ import annotations

from datetime import date
from zoneinfo import ZoneInfo
from datetime import datetime
import math
import re

SERVICE_FIELDS = {
    "svcAereo": ("airlinePreference", "specificAirline", "restrictedAirline", "departureTimes", "returnTimes", "cabinClass", "cabinClassNotes", "flightConnection", "maxLayoverHours", "baggageType", "aereoNotes", "aereoGuidance"),
    "svcHospedagem": ("hotelStandard", "hotelLocationPref", "eventAddress", "hotelLocationOther", "roomsSingle", "roomsDoubleTwin", "roomsDoubleCasal", "roomsTriple", "mealRegime", "roomingList", "hospedagemNotes", "hospedagemGuidance"),
    "svcEspacoAlimentacao": ("plenaryCapacity", "roomLayout", "roomLayoutOther", "breakoutRoomsCount", "avServices", "avOtherNotes", "cateringServices", "coffeeBreakPerDay", "espacoAlimentacaoNotes", "espacoGuidance"),
    "svcTransfers": ("transferTypes", "vehicleType", "dedicatedVehicleHoursDays", "transfersNotes", "transfersGuidance"),
}
ARRAY_FIELDS = {"departureTimes", "returnTimes", "avServices", "cateringServices", "transferTypes"}
FLAGS = set(SERVICE_FIELDS) | {"costCenterNotApplicable", "datesUnknown", "datesFlexible", "participantsUnknown", "participantsEstimated", "aereoGuidance", "hospedagemGuidance", "espacoGuidance", "transfersGuidance"}
BASIC = ("companyName", "cnpj", "requesterName", "requesterRole", "email", "phone", "costCenter", "extraBillingType", "eventName", "totalPassengers", "destination", "departureDate", "returnDate", "desiredBudget", "generalNotes")
KEYS = tuple(dict.fromkeys((*BASIC, *sorted(FLAGS), *(f for fields in SERVICE_FIELDS.values() for f in fields))))

def today_in_brazil() -> str:
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()

def valid_date(value:object) -> bool:
    if type(value) is not str or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        return False
    try:
        return date.fromisoformat(value).isoformat()==value
    except ValueError:
        return False

def email_valid(value:object) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",str(value or "").strip()))

def blank(value:object) -> bool:
    return value is None or str(value).strip()==""

def integer(value:object,minimum:int=0) -> bool:
    if blank(value) or type(value) is bool or not re.fullmatch(r"\d+",str(value)):
        return False
    number=int(str(value))
    return minimum<=number<=100000

def collect_issues(input:object,today:str|None=None)->list[dict]:
    f=input if isinstance(input,dict) else {}
    today=today or today_in_brazil()
    issues=[]
    def add(step,field,field_id,label,message):
        issues.append({"step":step,"field":field,"fieldId":field_id,"label":label,"message":message})
    def required(field,step,field_id,label):
        if type(f.get(field)) is not str or not f[field].strip():
            add(step,field,field_id,label,"Informe "+label.lower()+".")
    for flag in FLAGS:
        if flag in f and type(f[flag]) is not bool:
            add("evento",flag,"section-heading","Opções do briefing","Revise as opções selecionadas.")
    for field in KEYS:
        if field in FLAGS or field not in f:
            continue
        value=f[field]
        if field in ARRAY_FIELDS:
            if type(value) is not list or len(value)>30 or any(type(x) is not str or len(x)>300 for x in value):
                add("evento",field,"section-heading","Seleções","Revise as opções selecionadas.")
        elif type(value) not in (str,int,float) or (type(value) is float and not math.isfinite(value)) or len(str(value))>10000:
            add("evento",field,"section-heading","Informações","Revise o formato ou o tamanho das informações.")
    required("eventName","evento","event-name","Nome do evento")
    required("destination","evento","event-destination","Destino")
    if f.get("participantsUnknown") is not True and not integer(f.get("totalPassengers"),1):
        add("evento","totalPassengers","participants","Participantes","Informe um número inteiro de participantes ou marque que ainda não sabe.")
    if f.get("datesUnknown") is not True:
        start=f.get("departureDate")
        end=f.get("returnDate")
        if not valid_date(start):
            add("evento","departureDate","event-period","Data de início","Informe a data de início ou marque que as datas estão indefinidas.")
        elif start<today:
            add("evento","departureDate","event-period","Data de início","A data de início não pode estar no passado.")
        if not valid_date(end):
            add("evento","returnDate","brief-field-6","Data de término","Informe a data de término.")
        elif valid_date(start) and end<start:
            add("evento","returnDate","brief-field-6","Data de término","O término deve ser na data de início ou depois.")
    if not any(f.get(flag) is True for flag in SERVICE_FIELDS):
        add("evento","services","event-services","Serviços","Selecione pelo menos um serviço.")
    required("companyName","empresa","company-name","Empresa")
    required("requesterName","empresa","brief-field-2","Nome do solicitante")
    if not email_valid(f.get("email")):
        add("empresa","email","brief-field-4","E-mail","Informe um e-mail válido para contato.")
    phone=f.get("phone")
    if not blank(phone) and len(re.sub(r"\D","",str(phone))) not in (10,11):
        add("empresa","phone","brief-field-5","Telefone","Informe telefone com DDD (10 ou 11 dígitos) ou deixe em branco.")
    cnpj=f.get("cnpj")
    if not blank(cnpj) and len(re.sub(r"\D","",str(cnpj)))!=14:
        add("empresa","cnpj","brief-field-1","CNPJ","Confira o CNPJ: informe os 14 dígitos ou deixe em branco.")
    if f.get("svcAereo") is True:
        if f.get("airlinePreference")=="Somente Companhia Específica":
            required("specificAirline","aereo","brief-field-7","Companhia aérea")
        if f.get("airlinePreference")=="Restrição de Companhia Aérea por Política Interna":
            required("restrictedAirline","aereo","brief-field-8","Companhia restrita")
        if f.get("cabinClass")=="Misto / Por Cargo":
            required("cabinClassNotes","aereo","cabin-notes","Distribuição das cabines")
        value=f.get("maxLayoverHours")
        if f.get("flightConnection")=="Aceita Conexão" and not blank(value):
            try:
                numeric=float(value)
                if not math.isfinite(numeric) or numeric<=0:raise ValueError()
            except (ValueError,TypeError,OverflowError):
                add("aereo","maxLayoverHours","layover-hours","Tempo de conexão","Informe um tempo de conexão maior que zero.")
    if f.get("svcHospedagem") is True:
        if f.get("hotelLocationPref")=="Outro":
            required("hotelLocationOther","hospedagem","brief-field-9","Localização do hotel")
        for field in ("roomsSingle","roomsDoubleTwin","roomsDoubleCasal","roomsTriple"):
            if not blank(f.get(field)) and not integer(f[field]):
                add("hospedagem",field,"rooms-distribution","Quartos","As quantidades de quartos devem ser inteiras e não negativas.")
    if f.get("svcEspacoAlimentacao") is True:
        for field,field_id in (("plenaryCapacity","brief-field-10"),("breakoutRoomsCount","brief-field-11")):
            if not blank(f.get(field)) and not integer(f[field]):
                add("espaco",field,field_id,"Quantidade de salas e participantes","Informe uma quantidade inteira e não negativa.")
        catering=f.get("cateringServices")
        if isinstance(catering,list) and "Coffee Break" in catering and f.get("coffeeBreakPerDay") not in ("","1","2","3","Preciso de orientação",None):
            add("espaco","coffeeBreakPerDay","brief-field-12","Coffee break","Selecione uma frequência válida.")
    return issues

def prepare_submission(input:object)->dict:
    f=input if isinstance(input,dict) else {}
    out={}
    for field in KEYS:
        value=f.get(field)
        if field in FLAGS:
            out[field]=value is True
        elif field in ARRAY_FIELDS:
            out[field]=[x for x in value if type(x) is str] if isinstance(value,list) else []
        else:
            out[field]="" if value is None else str(value).strip()
    for flag,fields in SERVICE_FIELDS.items():
        if out[flag] is not True:
            for field in fields:
                out[field]=False if field in FLAGS else [] if field in ARRAY_FIELDS else ""
    if out["datesUnknown"]:
        out["departureDate"]=out["returnDate"]=""
        out["datesFlexible"]=False
    if out["participantsUnknown"]:
        out["totalPassengers"]=""
        out["participantsEstimated"]=False
    if out["costCenterNotApplicable"]:
        out["costCenter"]=""
    if out["airlinePreference"]!="Somente Companhia Específica":
        out["specificAirline"]=""
    if out["airlinePreference"]!="Restrição de Companhia Aérea por Política Interna":
        out["restrictedAirline"]=""
    if out["cabinClass"]!="Misto / Por Cargo":
        out["cabinClassNotes"]=""
    if out["flightConnection"]!="Aceita Conexão":
        out["maxLayoverHours"]=""
    if out["hotelLocationPref"]!="Outro":
        out["hotelLocationOther"]=""
    if out["hotelLocationPref"]!="Próximo ao Local do Evento":
        out["eventAddress"]=""
    if "Coffee Break" not in out["cateringServices"]:
        out["coffeeBreakPerDay"]=""
    if "Veículo Exclusivo à Disposição" not in out["transferTypes"]:
        out["dedicatedVehicleHoursDays"]=""
    return out
