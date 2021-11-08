import spacy
from spacy.matcher import Matcher

# This dictionary contains all the rules that have been defined
dictionary = {
    "IP Address" : [{"TEXT": {"REGEX": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"}}],
    # "MAC Address" : [{"TEXT": {"REGEX": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"}}],
    "Root User" : [{"TEXT": "root"}],
    "Proccess Identifier" : [{"TEXT": "pid"}, {"IS_PUNCT": True}, {"IS_DIGIT" : True}],
    "Authentication Server" : [{"TEXT": "sshd"}],
    
    # "Authentication Process" : [{"TEXT": "pam_unix"}, {"IS_PUNCT" : True}, {"TEXT" : "sshd"} , {"IS_PUNCT" : True}, {"TEXT" : "auth"}, {"IS_PUNCT" : True}]
    "CRON Process" : [{"TEXT": "CRON"}],
    "Port" : [{"TEXT" : "port"}, {"IS_DIGIT" : True}],
    "Sudo Command" : [{"TEXT" : "sudo"}],
    "Kernel Proccess" : [{"IS_PUNCT" : True}, {"TEXT" : "kernel"}, {"IS_PUNCT" : True}],


    "Website" : [{"LIKE_URL": True}],
    "E-mail" : [{"LIKE_EMAIL": True}],
}

class MatcherLoader:
    def __init__(self, nlp):
        self.matcher = Matcher(nlp.vocab, validate=True)
        for element in dictionary:
            self.matcher.add(element, [dictionary[element]])
        
        