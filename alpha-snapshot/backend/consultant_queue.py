"""Consultant-first, tenant-scoped operational inbox for NEXO Alpha.

The queue displays derived facts, not imaginary email sends or integrations.
"""
from __future__ import annotations


def _grouped(db, query, company_id):
    return {row['project_id']: dict(row) for row in db.execute(query, (company_id,))}


def build_consultant_queue(db, company_id: int, user_id: int) -> dict:
    """Return one factual next action per open project, never public tokens or NET.

    Endpoint checks role; every query has company_id scope. owner_id influences
    sorting but is not used as an access-control substitute.
    """
    projects = [dict(r) for r in db.execute("""
        SELECT p.id,p.protocol,p.title,p.status,p.owner_id,p.updated_at,
               c.name AS client_name
        FROM projects p JOIN clients c ON c.id=p.client_id AND c.company_id=p.company_id
        WHERE p.company_id=? AND p.status!='closed'
        ORDER BY p.updated_at DESC,p.id DESC
    """, (company_id,))]
    briefs = _grouped(db, """
        SELECT project_id,MAX(version) AS latest_version
        FROM briefing_versions WHERE company_id=? GROUP BY project_id
    """, company_id)
    requests = _grouped(db, """
        SELECT b.project_id,
               SUM(CASE WHEN r.status='prepared' THEN 1 ELSE 0 END) AS prepared,
               SUM(CASE WHEN r.status='sent' THEN 1 ELSE 0 END) AS awaiting,
               SUM(CASE WHEN r.status='responded' THEN 1 ELSE 0 END) AS responded,
               MIN(CASE WHEN r.status IN ('prepared','sent','responded') THEN v.version END) AS oldest_rfq_version
        FROM rfq_batches b JOIN rfqs r ON r.batch_id=b.id AND r.company_id=b.company_id AND r.revoked_at IS NULL
        JOIN briefing_versions v ON v.id=b.briefing_version_id AND v.company_id=b.company_id
        WHERE b.company_id=? GROUP BY b.project_id
    """, company_id)
    quotes = _grouped(db, """
        SELECT project_id,COUNT(*) AS count FROM quote_items
        WHERE company_id=? GROUP BY project_id
    """, company_id)
    proposals = _grouped(db, """
        SELECT p.project_id,p.version,p.status FROM proposals p
        WHERE p.company_id=? AND p.version=(
            SELECT MAX(p2.version) FROM proposals p2
            WHERE p2.project_id=p.project_id AND p2.company_id=p.company_id)
    """, company_id)
    tasks = _grouped(db, """
        SELECT project_id,COUNT(*) AS pending FROM plan_tasks
        WHERE company_id=? AND status!='done' GROUP BY project_id
    """, company_id)

    items = []
    for p in projects:
        pid=p['id']; b=briefs.get(pid, {}); r=requests.get(pid, {})
        quote_count=int(quotes.get(pid, {}).get('count') or 0)
        pending_tasks=int(tasks.get(pid, {}).get('pending') or 0)
        latest=int(b.get('latest_version') or 0)
        rfq_version=int(r.get('oldest_rfq_version') or 0)
        prepared=int(r.get('prepared') or 0)
        awaiting=int(r.get('awaiting') or 0)
        responded=int(r.get('responded') or 0)
        proposal=proposals.get(pid, {})
        act='review_project'; label='Conferir a operação'; detail='Consulte o contexto e os próximos passos.'
        tab='overview'; priority=3
        if rfq_version and latest>rfq_version:
            act='review_scope_change'; label=f'Revisar impacto do briefing V{latest}'
            detail=f'Existem RFQs vinculadas a uma versão anterior (desde V{rfq_version}). Não houve reenvio automático.'
            tab='briefing'; priority=1
        elif prepared:
            act='verify_manual_invites'; label='Regularizar convites de cotação'
            detail=f'{prepared} RFQ(s) preparada(s) sem envio registrado. Links antigos podem exigir renovação.'
            tab='rfq'; priority=1
        elif responded and quote_count==0:
            act='review_supplier_answers'; label='Conferir respostas recebidas'
            detail=f'{responded} resposta(s) registrada(s); valide unidade e escopo antes do orçamento.'
            tab='quotes'; priority=1
        elif p['status'] in ('briefing','qualifying'):
            act='validate_briefing'; label='Validar escopo do briefing'
            detail='Confira dados e serviços antes de solicitar valores aos fornecedores.'
            tab='briefing'; priority=1
        elif proposal.get('status')=='draft':
            act='review_proposal_draft'; label='Revisar proposta em rascunho'
            detail='Há uma versão não publicada. O link original não é recuperado automaticamente nesta interface.'
            tab='proposal'; priority=1
        elif p['status']=='approved' and pending_tasks:
            act='plan_deliveries'; label='Acompanhar entregas aprovadas'
            detail=f'{pending_tasks} tarefa(s) de planejamento em aberto.'
            tab='planning'; priority=1
        elif quote_count and proposal.get('status') not in ('published','approved','changes_requested','rejected'):
            act='review_budget'; label='Revisar orçamento e proposta'
            detail=f'{quote_count} item(ns) registrado(s); confira NET, taxas, unidades e condições.'
            tab='quotes'; priority=1
        elif awaiting:
            act='track_supplier_responses'; label='Acompanhar respostas dos fornecedores'
            detail=f'{awaiting} convite(s) sem resposta; entrega e cobranças são manuais.'
            tab='rfq'; priority=2
        elif proposal.get('status')=='published':
            act='follow_proposal_decision'; label='Acompanhar decisão sobre a proposta'
            detail=f'Proposta V{proposal["version"]} publicada; ainda não há decisão registrada nesta versão.'
            tab='proposal'; priority=2
        elif p['status']=='approved':
            act='review_approved_project'; label='Conferir execução aprovada'
            detail='Confira entregas e informações da operação.'
            tab='planning'; priority=2
        elif responded:
            act='review_supplier_answers'; label='Conferir respostas e comparativo'
            detail=f'{responded} resposta(s) registrada(s); confira condições e itens.'
            tab='quotes'; priority=2

        items.append({
            'project_id':pid,'protocol':p['protocol'],'project_title':p['title'],
            'client_name':p['client_name'],'owner_is_me':p['owner_id']==user_id,
            'project_status':p['status'],'action_type':act,'title':label,
            'detail':detail,'tab':tab,'priority':priority,
            'briefing_version':latest,'prepared_rfqs':prepared,
            'awaiting_rfqs':awaiting,'responded_rfqs':responded,
            'pending_tasks':pending_tasks,'updated_at':p['updated_at']
        })
    # Stable secondary recency ordering, then severity and responsibility.
    items.sort(key=lambda x:(str(x['updated_at']),x['project_id']),reverse=True)
    items.sort(key=lambda x:(x['priority'],not x['owner_is_me']))
    return {
        'items':items,
        'summary':{
            'open_projects':len(projects),
            'needs_attention':sum(i['priority']==1 for i in items),
            'awaiting_followup':sum(i['priority']==2 for i in items),
        },
        'scope':'company',
        'limitations':'Links de RFQ/proposta não são recuperáveis automaticamente; integração de e-mail não implementada.'
    }
