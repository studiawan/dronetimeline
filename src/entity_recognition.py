from spacy.lang.en import English
import csv 
import time
nlp = English()
ruler = nlp.add_pipe("entity_ruler", config={"validate": True}).from_disk('/home/mhdfadlyhasan/Codes/dronetimeline/src/patterns.jsonl')
time_start = time.time()
with open('/home/mhdfadlyhasan/Codes/dronetimeline/src/hasilfinal.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # do nlp in description row
            doc = nlp(row[10]) # gonna change later!
            line_count += 1
            if len(doc.ents)!=0: 
                print(line_count + [(ent.text, ent.label_) for ent in doc.ents])
                i = 0
    
print("done")