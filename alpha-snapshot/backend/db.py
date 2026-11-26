"""Fresh NEXO Alpha relational schema. No code or migrations imported from legacy."""
import os
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.environ.get('NEXO_DB_PATH', str(BASE / 'data' / 'nexo-alpha.sqlite3')))

DDL = """
CREATE TABLE IF NOT EXISTS companies (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS clients (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  name TEXT NOT NULL, contact_email TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  client_id INTEGER REFERENCES clients(id), full_name TEXT NOT NULL,
  email TEXT NOT NULL COLLATE NOCASE, password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('admin','consultant','client','viewer')),
  active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(company_id,email)
);
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
  token_hash TEXT NOT NULL UNIQUE, csrf_token TEXT NOT NULL DEFAULT '', expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  client_id INTEGER NOT NULL REFERENCES clients(id), owner_id INTEGER REFERENCES users(id),
  protocol TEXT NOT NULL UNIQUE, title TEXT NOT NULL, destination TEXT NOT NULL DEFAULT '',
  starts_at TEXT NOT NULL DEFAULT '', ends_at TEXT NOT NULL DEFAULT '',
  attendees INTEGER NOT NULL DEFAULT 0, budget_cents INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'briefing' CHECK(status IN ('briefing','qualifying','sourcing','quoting','proposal','approved','closed')),
  services TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS briefing_versions (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), version INTEGER NOT NULL,
  payload TEXT NOT NULL, created_by INTEGER NOT NULL REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(project_id,version)
);
CREATE TABLE IF NOT EXISTS briefing_drafts (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), user_id INTEGER NOT NULL REFERENCES users(id),
  payload TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(company_id,project_id,user_id)
);
CREATE INDEX IF NOT EXISTS ix_briefing_drafts_owner ON briefing_drafts(company_id,project_id,user_id);
CREATE TABLE IF NOT EXISTS suppliers (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  name TEXT NOT NULL, category TEXT NOT NULL, city TEXT NOT NULL DEFAULT '',
  contact_name TEXT NOT NULL DEFAULT '', email TEXT NOT NULL DEFAULT '', phone TEXT NOT NULL DEFAULT '',
  preferred INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS rfq_batches (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), briefing_version_id INTEGER NOT NULL REFERENCES briefing_versions(id),
  deadline TEXT NOT NULL DEFAULT '', created_by INTEGER NOT NULL REFERENCES users(id),
  sent_at TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS rfqs (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  batch_id INTEGER NOT NULL REFERENCES rfq_batches(id), supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  token_hash TEXT NOT NULL UNIQUE, status TEXT NOT NULL DEFAULT 'prepared',
  sent_at TEXT, responded_at TEXT, expires_at TEXT, revoked_at TEXT,
  UNIQUE(batch_id,supplier_id)
);
CREATE TABLE IF NOT EXISTS rfq_responses (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  rfq_id INTEGER NOT NULL UNIQUE REFERENCES rfqs(id),
  available TEXT NOT NULL DEFAULT 'available', currency TEXT NOT NULL DEFAULT 'BRL',
  net_cents INTEGER NOT NULL DEFAULT 0, tax_bps INTEGER NOT NULL DEFAULT 0,
  conditions TEXT NOT NULL DEFAULT '', cancellation TEXT NOT NULL DEFAULT '',
  notes TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS quote_items (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), supplier_id INTEGER REFERENCES suppliers(id),
  category TEXT NOT NULL, description TEXT NOT NULL,
  quantity INTEGER NOT NULL CHECK(quantity > 0), unit_net_cents INTEGER NOT NULL CHECK(unit_net_cents >= 0),
  tax_bps INTEGER NOT NULL DEFAULT 0, fee_bps INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS proposals (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), version INTEGER NOT NULL,
  snapshot TEXT NOT NULL, total_cents INTEGER NOT NULL, token_hash TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','published','approved','changes_requested','rejected')),
  created_by INTEGER NOT NULL REFERENCES users(id), published_at TEXT,
  expires_at TEXT, revoked_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(project_id,version)
);
CREATE TABLE IF NOT EXISTS approval_decisions (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  proposal_id INTEGER NOT NULL REFERENCES proposals(id),
  actor TEXT NOT NULL, decision TEXT NOT NULL CHECK(decision IN ('approved','changes_requested','rejected')),
  comment TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS plan_tasks (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER NOT NULL REFERENCES projects(id), title TEXT NOT NULL,
  owner_id INTEGER REFERENCES users(id), due_date TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','in_progress','done')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(id),
  project_id INTEGER REFERENCES projects(id), actor_id INTEGER REFERENCES users(id),
  action TEXT NOT NULL, detail TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS login_attempts (
  id INTEGER PRIMARY KEY, key TEXT NOT NULL, occurred_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_login_attempts_key ON login_attempts(key,occurred_at);
CREATE TABLE IF NOT EXISTS demo_requests (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
  company TEXT NOT NULL, event_type TEXT NOT NULL DEFAULT '',
  source_ip_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_demo_requests_ip ON demo_requests(source_ip_hash,created_at);
CREATE INDEX IF NOT EXISTS ix_projects_company ON projects(company_id,created_at);
CREATE INDEX IF NOT EXISTS ix_projects_client ON projects(company_id,client_id);
CREATE INDEX IF NOT EXISTS ix_suppliers_company ON suppliers(company_id,category);
CREATE INDEX IF NOT EXISTS ix_rfq_batch ON rfqs(batch_id);
CREATE INDEX IF NOT EXISTS ix_quote_project ON quote_items(project_id);
CREATE INDEX IF NOT EXISTS ix_audit_project ON audit_logs(project_id,created_at);
"""

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db=sqlite3.connect(str(DB_PATH),timeout=5,check_same_thread=False)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    db.execute('PRAGMA journal_mode = WAL')
    db.execute('PRAGMA busy_timeout = 5000')
    return db

def init_db():
    with connect() as db:
        db.executescript(DDL)
        # Migração aditiva, preservando todos os registros comerciais existentes.
        for table, columns in {
            'quote_items': {'rooms':'INTEGER', 'nights':'INTEGER', 'source_rfq_id':'INTEGER REFERENCES rfqs(id)'},
            'sessions': {'csrf_token': "TEXT NOT NULL DEFAULT ''"},
            'rfqs': {'expires_at':'TEXT', 'revoked_at':'TEXT'},
            'proposals': {'expires_at':'TEXT', 'revoked_at':'TEXT'},
        }.items():
            existing = {row['name'] for row in db.execute(f'PRAGMA table_info({table})')}
            for column, decl in columns.items():
                if column not in existing:
                    db.execute(f'ALTER TABLE {table} ADD COLUMN {column} {decl}')
        # Tokens legados sem data de expiração deixam de valer após migração.
        db.execute("UPDATE rfqs SET expires_at='1970-01-01T00:00:00+00:00' WHERE expires_at IS NULL")
        db.execute("UPDATE proposals SET expires_at='1970-01-01T00:00:00+00:00' WHERE expires_at IS NULL")

def rows(cur):
    return [dict(x) for x in cur.fetchall()]