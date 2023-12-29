
from googletrans import Translator

translator = Translator()

string = "car"
hindiOp = translator.translate(str(string), dest='pa')   
# a = hindiOp.text.encode('utf-8').decode('utf-8')
print("hindi version: ",hindiOp.pronunciation)
print("hindi version: ",hindiOp.src)
print("hindi version: ",hindiOp.text)