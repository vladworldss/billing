"""
init_migration
"""

from yoyo import step

__depends__ = {}

CREATE_WALLET_TABLE = '''
DROP TYPE IF EXISTS wallet_status;
CREATE TYPE wallet_status AS ENUM ('active', 'closed');
DROP TYPE IF EXISTS currency;
CREATE TYPE currency AS ENUM ('usd');

CREATE TABLE IF NOT EXISTS wallet(
    wallet_id serial primary key,
    status wallet_status not null default 'active',
    amount Numeric(10, 2) not null default 0.0,
    created_at timestamp without time zone NOT NULL DEFAULT NOW(),
    updated_at timestamp without time zone NOT NULL DEFAULT NOW(),
    currency currency not null default 'usd',
    handshake_id varchar(64),

    CONSTRAINT positive_amount CHECK (amount > 0)
);
'''

CREATE_TRANSACTION_TABLE = '''
DROP TYPE IF EXISTS transaction_status;
CREATE TYPE transaction_status AS ENUM ('created', 'processed', 'failed');

CREATE TABLE IF NOT EXISTS transaction(
    transaction_id serial primary key,
    handshake_id varchar(64),
    status transaction_status not null default 'created',
    source_wallet_id bigint not null,
    destination_wallet_id bigint not null,
    trans_sum Numeric(8, 2) not null default 0.0,
    created_at timestamp without time zone NOT NULL DEFAULT NOW(),
    updated_at timestamp without time zone NOT NULL DEFAULT NOW(),
    info JSONB not null DEFAULT '{}'::jsonb,

    CONSTRAINT non_self_transaction CHECK (source_wallet_id != destination_wallet_id),

    FOREIGN KEY (source_wallet_id) REFERENCES wallet (wallet_id) ON DELETE CASCADE,
    FOREIGN KEY (destination_wallet_id) REFERENCES wallet (wallet_id) ON DELETE CASCADE
);
'''


steps = [
    step(CREATE_WALLET_TABLE, 'DROP TABLE wallet;'),
    step(CREATE_TRANSACTION_TABLE, 'DROP TABLE transaction;')
]
