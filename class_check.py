import csv
import jellyfish

def find_similar_trademarks(trademark_class):
    trademark_class_number = ''
    similar_trademarks = []
    
    with open('sample.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Find the trademark class number for the given trademark class
        for row in csv_reader:
            if row['trademark class'] == trademark_class:
                trademark_class_number = row['trademark class number']
                break
        
        # Check all trademark names in the trademark class and calculate similarity scores
        csv_file.seek(0)
        for row in csv_reader:
            if row['trademark class number'] == trademark_class_number:
                similarity_score = jellyfish.jaro_winkler(row['trademark name'], trademark_class)
                similar_trademarks.append((row['trademark name'], similarity_score))
                
        # Sort the list of similar trademarks by similarity score
        similar_trademarks.sort(key=lambda x: x[1], reverse=True)
        
        return similar_trademarks