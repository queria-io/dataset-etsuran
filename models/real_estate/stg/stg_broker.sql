{{ config(materialized='ephemeral') }}

-- raw_broker を mart から読むための stg。列は raw のまま
SELECT * FROM {{ ref('raw_broker') }}
