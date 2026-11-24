import pytest

from pgvector.psycopg import register_vector
from corpus import embed as e 


@pytest.fixture(scope="module", autouse=True)
def _load():
    e.embed_all() #make sure migratio and embedding happened before. 

def test_migrated_columns(): # to verify column embedding exists with type pgvector.
    cn = e.connect()
    try:
        cur = cn.cursor()
        cur.execute(""" SELECT data_type , udt_name FROM information_schema.columns WHERE table_name = 'note_chunks' AND column_name = 'embedding' """)
        row = cur.fetchone()

        assert row is not None, "column embedding does not exist"
        assert row[1] == "vector", f"expected pgvector column, got {row[1]}"
    finally:
        cn.close()

def test_column_and_dim(): # to test if every embedding column row has 384 dimensioanl vector
    cn = e.connect()
    try:
        cur = cn.cursor()
        cur.execute("SELECT DISTINCT vector_dims(embedding) FROM note_chunks WHERE embedding IS NOT NULL")
        # dims = cur.fetchone()[0] why we cant use this is , wokr if all rows healthy but id one is broken we give false pass and not see the other [(384,)(768,)]
        # assert dims == 384 , f"expected 384 dims and got {dims}"
        dims = [r[0] for r in cur.fetchall()]
        assert dims == [384], f"expected 384 dims and got {dims}"
       
    finally:
        cn.close()

def test_all_embedded():
    cn = e.connect()
    try:
        cur = cn.cursor()
        cur.execute("SELECT COUNT(*) FROM note_chunks WHERE embedding IS NOT NULL")
        not_null_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM note_chunks WHERE embedding IS NULL")
        null_count = cur.fetchone()[0]
        assert not_null_count == 31, f"the total emnedding count is {not_null_count}"
        assert null_count == 0, f"the null emnedding count is {null_count}"
    finally:
        cn.close()

def test_deterministic(): # test if it porduces iodentical vectors 
    v1 = e.embed_texts(["Patient is dying with cancer"])[0]
    v2 = e.embed_texts(["Patient is dying with cancer"])[0]

    assert len(v1) == 384
    assert list(v1) == list(v2)

def test_idempotency():
    cn = e.connect()
    try:
        register_vector(cn)
        cur = cn.cursor()

        count_before = e.embed_all()
        cur.execute("SELECT embedding from note_chunks ORDER BY patient_id, kind, week NULLS FIRST LIMIT 1")
        row = cur.fetchone()
        vec_before = row[0].to_list() if row and row[0] is not None else None
        cn.commit()

        count_after = e.embed_all()
        cur.execute("SELECT embedding from note_chunks ORDER BY patient_id, kind, week NULLS FIRST LIMIT 1")
        row = cur.fetchone()
        vec_after = row[0].to_list() if row and row[0] is not None else None 

        assert count_before == count_after == 31
        assert vec_before == vec_after 
    finally:
        cn.close()


