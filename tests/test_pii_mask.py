from corpus.mask import mask_pii

def test_name_masked():
    raw_sample_text = "Patient Rohan Mehta his cell phone number is 9945154999"
    masked_sample = mask_pii(raw_sample_text)

    assert "Rohan Mehta" in raw_sample_text
    assert "Rohan Mehta" not in masked_sample
    assert "<PERSON>" in masked_sample

def test_number_masked():
    raw_sample = "patient has a number 9945154999"
    masked_sample = mask_pii(raw_sample)

    assert "9945154999" in raw_sample
    assert "9945154999" not in masked_sample
    assert "<PHONE_NUMBER>" in masked_sample

def test_remaining_text_untouched():
    sample = "patient is happy"
    masked = mask_pii(sample)

    assert masked == sample # cant use "in" since "" also is vakidated which we shouldnt

def test_one_actual_data():
    from corpus.parse import extract_note_chunks
    raw = extract_note_chunks("data/raw/P002/notes.pdf")[0].text
    masked = mask_pii(raw)
    assert "Rohan Mehta" not in masked
    assert "9945154999" not in masked 
    assert "<PHONE_NUMBER>" in masked


