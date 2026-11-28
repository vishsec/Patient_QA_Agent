from typing import TypedDict
import re

DISCLAIMER = "\n\nNote: For informational purposes only; verify against the patient chart."

class GateVerdict(TypedDict): # since we need the verdict to follow this shape 
    passed : bool
    reason : str

#preventing the hijacking of prompts by checking the question and the chunk

def scan_injection(text: str) -> GateVerdict:
   PATTERNS = [r"ignore\s+(all\s+)?previous\s+instructions",
               r"system\s+prompt", 
               r"(consider\s+)?you\s+are\s+now", 
               r"disregard\s+rules"]
   for p in PATTERNS:
       if re.search(p, text, re.IGNORECASE) is not None:
           return {"passed": False, "reason": f"Bad patterns found:{p}"}
   return {"passed": True, "reason": "No bad patterns found"}

# ensure the system abstains if similarity is less than the threshold. 
def should_abstain(top_similarity, threshold : float=0.35) -> bool: 
    if top_similarity is None or top_similarity < threshold:
        return True
    return False

#post LLM
# if LLM puts "" in its answer , check if it actually exists inside the retrieved chunks. 

def verify_quotes(answer_text, chunks) -> GateVerdict:
    quotes = re.findall(r'"([^"]+)"', answer_text) #^ is negation it says ^" stop at te next " so cpature everyhting isnide " "s  
    corpus_text =  " ".join(c["text"] for c in chunks).lower()

    for q in quotes:
        one_quote = " ".join(q.split()).lower()
        if one_quote not in corpus_text:
            return {"passed": False, "reason": f"chunks do not contain the quoted text {one_quote}"}
    return {"passed": True, "reason": f"chunks contain the quoted texts"}
    
#just check if disclaimer there or not 
def has_disclaimer(answer_text: str) -> bool:
    return DISCLAIMER.strip().lower() in answer_text.lower()
    

def ensure_disclaimer(answer_text: str) -> str:
    if has_disclaimer(answer_text):
        return answer_text
    return f"{answer_text.rstrip()}{DISCLAIMER}" # adds disclaimer if not present and disclaimer starts with \n as above  


    

    
       
        
       



