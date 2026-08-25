-- Extensions enabled on first initialization of the database volume.
-- pgvector stays unused until Phase 3 (RAG); creating it here keeps that
-- phase free of database bootstrapping concerns.
CREATE EXTENSION IF NOT EXISTS vector;
