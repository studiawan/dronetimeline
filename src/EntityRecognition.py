import time
import spacy
from spacy.tokens import Span
import json
# from spacy.matcher import Matcher
from spacy.lang.en import English
# This json contains all the rules that have been defined

time_start = time.time()        
class EntityRecognition:
    def __init__(self):
        self.nlp = English()
        
        self.ruler = self.nlp.add_pipe("entity_ruler", config={"overwrite_ents": "true"}).from_disk("src/rules.jsonl")
        self.ruler_entity_dependend = self.nlp.add_pipe("entity_ruler", name = "file_ruler", config={"overwrite_ents": "true"}).from_disk("src/file_rules.jsonl")
        self.ruler_entity_dependend = self.nlp.add_pipe("entity_ruler", name = "entity_dependend_ruler", config={"overwrite_ents": "true"}).from_disk("src/entity_dependend_rules.jsonl")

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
        # matches = self.matcher(doc)
        list_of_matches = []
        entities = []
        
        for ent in doc.ents:
            matched_string = ent.text #string that matched the rule
            string_id = ent.ent_id_ #id of the entity based on the rules created

            matched_details = self.skadi_string_slicer(doc, ent.start, ent.end, matched_string, string_id)
            list_of_matches.append(matched_details)
            entities.append(ent)

        # assuming spaCy finds entity from start of the string to the end of the string,
        # entity marking implemented from end of the string to start of the string
        for matched_details in reversed(list_of_matches):
            marked_string = matched_details[0]
            start_char_index = matched_details[1]
            end_char_index = matched_details[2]

            string = string[0:start_char_index]+string[start_char_index:end_char_index].replace(string[start_char_index:end_char_index],marked_string)+ string[end_char_index:]            

        return string, doc, entities

    def saria_IOB_formater(self, doc, entities):
        array = []
        for x in doc:
            array.append(('O', x))
        for ent in entities:
            label = ent.label_ #id of the entity based on the rules created
            array[ent.start] = '{}-{}'.format('B', label), doc[ent.start]
            for i in range(ent.start+1, ent.end):
                array[i] = '{}-{}'.format('I', label), doc[i]
        return array


if __name__ == "__main__":
    EntityRecognition()
    print("done")