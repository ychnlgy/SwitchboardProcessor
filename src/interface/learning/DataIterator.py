import lang

@lang.interface
class DataIterator:
    
    def iterTrainingSet(self):
        "Iterates through the training set in batch-sizes."
        
    def iterValidationSet(self):
        "Iterates through the validation set in batch-sizes."
    
    def iterTestSet(self):
        "Iterates through the test set in batch sizes."
