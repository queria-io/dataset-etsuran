{{ config(materialized='ephemeral') }}

-- raw_contractor を mart から読むための stg。列は raw のまま
SELECT * FROM {{ ref('raw_contractor') }}
