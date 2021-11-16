import time
import spacy
from spacy.tokens import Span
import json
from spacy.matcher import Matcher

# This json contains all the rules that have been defined
f = open('src/rules.json',)
dictionary = json.load(f)

time_start = time.time()        
class EntityRecognition:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab, validate=True)

        # importing rules
        for element in dictionary:
            self.matcher.add(element, [dictionary[element]["rule"]])
        
    # Function to give rich text anotation to marking entities
    def skadi_string_slicer(self,doc, start, end,matched_string,string_id):
        strings = doc.text
        start_char_index = doc[start:end].start_char
        end_char_index = doc[start:end].end_char
        
        markedstrings = "<b style=""background-color:yellow;""> {} <sub>{}</sub> </b>".format(matched_string,string_id)
        strings = strings.replace(strings,markedstrings)
        
        return strings, start_char_index, end_char_index


    def find_entity(self,string):
        doc = self.nlp(string)
        matches = self.matcher(doc)
        list_of_matches = []
        
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            matched_string = span.text #string that matched the rule
            string_id = self.nlp.vocab.strings[match_id] #id of the entity based on the rules created

            matched_details = self.skadi_string_slicer(doc, start, end,matched_string,string_id)
            list_of_matches.append(matched_details)

        # assuming spaCy finds entity from start of the string to the end of the string,
        # entity marking implemented from end of the string to start of the string
        for matched_details in reversed(list_of_matches):
            marked_string = matched_details[0]
            start_char_index = matched_details[1]
            end_char_index = matched_details[2]

            string = string[0:start_char_index]+string[start_char_index:end_char_index].replace(string[start_char_index:end_char_index],marked_string)+ string[end_char_index:]            

        return string, doc, matches, self.nlp
