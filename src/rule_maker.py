import sys
import json
from PyQt5.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QApplication,
)
import spacy
from spacy.tokens import Span
import json
from spacy.matcher import Matcher

class EntityRecognitionModified:
    def __init__(self):
        return 

    # Function to give rich text anotation to marking entities
    def string_slicer(self,doc, start, end,matched_string,string_id):
        strings = doc.text
        start_char_index = doc[start:end].start_char
        end_char_index = doc[start:end].end_char
        
        markedstrings = "<b style=""background-color:yellow;""> {} <sub>{}</sub> </b>".format(matched_string,string_id)
        strings = strings.replace(strings,markedstrings)
        
        return strings, start_char_index, end_char_index


    def find_entity(self,string, entity_tag, IOB_TAG, patterntextboxValue):
        nlp = spacy.load("en_core_web_sm")
        patterntextboxValue = patterntextboxValue.split(';')
        patterns = []

        i = 0
        for pattern in patterntextboxValue:
            ruler = nlp.add_pipe("entity_ruler", name=entity_tag[i], config={"overwrite_ents": "true"})
            formats = '{}"id": "{}", "label" : "{}", "pattern": {}{}'.format('{', entity_tag[i], IOB_TAG[i], pattern, '}')
            patterns = json.loads(formats)
            ruler.add_patterns([patterns])
            i+=1
        

        # self.matcher = Matcher(self.nlp.vocab, validate=True)
        # self.matcher.add(entity_tag[0], [pattern], "label")
        doc = nlp(string)
        # matches = self.matcher(doc)
        list_of_matches = []
        for entity in doc:
            print(entity)
            
        for ent in doc.ents:
            
            matched_string = ent.text #string that matched the rule
            string_id = ent.ent_id_ #id of the entity based on the rules created
            if(string_id==''): continue
            matched_details = self.string_slicer(doc, ent.start, ent.end, matched_string, string_id)
            list_of_matches.append(matched_details)

        # assuming spaCy finds entity from start of the string to the end of the string,
        # entity marking implemented from end of the string to start of the string
        for matched_details in reversed(list_of_matches):
            marked_string = matched_details[0]
            start_char_index = matched_details[1]
            end_char_index = matched_details[2]

            string = string[0:start_char_index]+string[start_char_index:end_char_index].replace(string[start_char_index:end_char_index],marked_string)+ string[end_char_index:]            
        return string

class rule_tester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.entity_recog_mod = EntityRecognitionModified()
        self.main_window_title = 'Rule maker to test and make rules'

        self.patterns_text_box = QLineEdit(self)
        self.patterns_text_box.move(20, 20)
        self.patterns_text_box.resize(800,40)
        self.patterns_text_box.setPlaceholderText("Insert patterns here")


        self.example_text_textbox = QLineEdit(self)
        self.example_text_textbox.move(20, 70)
        self.example_text_textbox.resize(800,40)
        self.example_text_textbox.setPlaceholderText("Insert text to be checked here")

        self.results = QTextEdit(self)
        self.results.move(20, 140)
        self.results.resize(800,40)
        self.results.setReadOnly(True)
        self.results.setText("Result here")

        self.button = QPushButton('Test Entity Recognition', self)
        self.button.move(20,200)
        self.button.clicked.connect(self.entity_recognition)
        self.button.resize(800,40)


        self.entity_tag = QLineEdit(self)
        self.entity_tag.move(20,250)
        self.entity_tag.resize(800,40)
        self.entity_tag.setPlaceholderText("Insert entity tag here")


        self.IOB = QLineEdit(self)
        self.IOB.move(20,300)
        self.IOB.resize(800,40)
        self.IOB.setPlaceholderText("Insert IOB tag here")


        self.final_rule = QTextEdit(self)
        self.final_rule.move(20,350)
        self.final_rule.resize(800,400)
        self.final_rule.setPlaceholderText("Generated rule will be put here")


        self.show()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle(self.main_window_title)

        self.show()

    
    def entity_recognition(self):
        entity_tag = self.entity_tag.text() if self.entity_tag.text()!='' else "example_tag"
        IOB_Tag = self.IOB.text() if self.IOB.text()!='' else "example_IOB"
        example_text_textbox = self.example_text_textbox.text()
        IOB_Tag = IOB_Tag.split(';')
        entity_tag = entity_tag.split(";")
        try:
            patternstextboxValue = self.patterns_text_box.text()
            results = self.entity_recog_mod.find_entity(example_text_textbox, entity_tag, IOB_Tag, patternstextboxValue)
            self.results.setText(results)

            # formating the text
            formats = ""
            i = 0
            val = str(self.patterns_text_box.text())
            val = val.split(';')
            for tag in IOB_Tag:
                formats += '{}"id": "{}", "label" : "{}", "pattern": {}{}'.format('{', entity_tag[i], tag, val[i], '}\n')
                i+=1
            self.final_rule.setText(formats)
        except Exception as e:
            self.results.setText(str(e))
            self.final_rule.setText("")

def main():
    app = QApplication(sys.argv)
    _ = rule_tester()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
