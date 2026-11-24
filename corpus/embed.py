import psycopg

from corpus.ingest import connect
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

MIGRATION_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE note_chunks ADD COLUMN IF NOT EXISTS embedding vector(384);
""" 

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(text: list[str]) -> list:
    return _model.encode(text).tolist()

def embed_all():
    cn = connect()
    try:
        cur = cn.cursor()
        cur.execute("SELECT 1 FROM information_schema.columns WHERE table_name = 'note_chunks' AND column_name = 'embedding'")
        if cur.fetchone() is None: # deadlocks happened during reads when testing idempotency this 'if' prevents from running migration_sql which has Alter table which need exclusive access 
            cur.execute(MIGRATION_SQL)
        register_vector(cn)
        cur.execute("SELECT patient_id, week, kind, text FROM note_chunks WHERE embedding is NULL")
        rows = cur.fetchall()
        if not rows:
            cn.commit()
            cur.execute("SELECT COUNT(*) from note_chunks WHERE embedding is NOT NULL")
            total = cur.fetchone()[0]
            print(f"Nothing to embed {total} already embedded.")
            return total

        vectors = embed_texts([r[3] for r in rows])

        for(pid, week, kind, _) , vec in zip(rows, vectors):
            cur.execute("UPDATE note_chunks SET embedding = %s "
                        "WHERE patient_id = %s AND kind = %s AND week is NOT DISTINCT FROM %s", 
                        (vec, pid, kind, week))

        cn.commit()
        

        cur.execute("SELECT COUNT(*) FROM note_chunks WHERE embedding IS NOT NULL")
        embedded_count = cur.fetchone()[0]
        print(f"Successfully embedded {embedded_count} in note_chunks.")
        return embedded_count


    finally:
        cn.close()

if __name__ == "__main__":
    print(embed_all())













