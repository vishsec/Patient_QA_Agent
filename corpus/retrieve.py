from corpus.ingest import connect 
from corpus.embed import embed_texts 
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

def search_text(text: str, k : int=3) -> list[dict]:
    vec = embed_texts([text])[0]
    cn = connect()

    try:
        register_vector(cn)
        cur = cn.cursor(row_factory=dict_row)
        cur.execute("""SELECT patient_id, week, kind, text, 1 - (embedding <=> %s::vector) AS similarity
         FROM note_chunks WHERE embedding is NOT NULL ORDER BY embedding <=> %s::vector LIMIT %s""", (vec, vec, k),)
        return cur.fetchall()
    finally:
        cn.close()

# <=> is the pgvector ditance closer the better
# 1- is the similarity , higher the better
 