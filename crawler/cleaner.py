def clean_synopysis(text):
    t = text.replace("Classificação indicativa a definir por http://www.culturadigital.br/classind.", "")
    t = text.replace("\n", "").replace("\t", "")
    t = " ".join(t.split(" "))
    
    return t.strip()