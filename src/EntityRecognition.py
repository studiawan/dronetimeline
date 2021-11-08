import time
import spacy
from matcher_loader import MatcherLoader
from spacy.tokens import Span
time_start = time.time()

class EntityRecognition:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = MatcherLoader(self.nlp).matcher
        
    # Function to give rich text anotation to mark the entity
    def skadi_string_slicer(self,text, start, end,matched_string,string_id):
        strings = text.text
        start_char_index = text[start:end].start_char
        end_char_index = text[start:end].end_char
        
        markedstrings = "<b style=""background-color:yellow;""> {} <sub>{}</sub> </b>".format(matched_string,string_id)
        strings = strings.replace(strings,markedstrings)
        
        return strings, start_char_index, end_char_index


    def find_entity(self,string):
        doc = self.nlp(string)
        matches = self.matcher(doc)
        list = []
        
        for match_id, start, end in matches:
            
            span = Span(doc, start, end, label=match_id)
            matched_string = span.text #string that matched the rule
            string_id = self.nlp.vocab.strings[match_id]#id of the entity based on the rules created
            list.append(self.skadi_string_slicer(doc, start, end,matched_string,string_id))#add every entity to a list



        # assuming spaCy finds entity from start of the string to the end,
        # entity marking implemented from end of the string to start of the string
        for x in reversed(list):
            marked_string = x[0]
            entity_start = x[1]
            entity_end = x[2]
    
            string = string[0:entity_start]+string[entity_start:entity_end].replace(string[entity_start:entity_end],marked_string)+ string[entity_end:]            
        return string
