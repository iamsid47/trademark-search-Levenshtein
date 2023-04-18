import csv
import Levenshtein
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, Response
import matplotlib
from PIL import Image
import base64

def string_similarity(str1, str2):
    """
    Calculates the similarity between two strings using Levenshtein distance.
    Returns a similarity score between 0 and 100.
    """
    # Convert the strings to lowercase for case-insensitive comparison
    str1 = str1.lower() if str1 else ""
    str2 = str2.lower()

    # Calculate Levenshtein distance between the two strings
    distance = Levenshtein.distance(str1, str2)

    # Calculate similarity score as a percentage of characters that match
    max_len = max(len(str1), len(str2))
    similarity_score = (1 - (distance / max_len)) * 100

    return similarity_score

def check_similarity(str1, csv_file):
    """
    Checks similarity between a given string and trademark names in a CSV file.
    Prints all the trademark names that have a similarity score of more than 30%,
    and also plots the similarity scores using matplotlib with trademark names as labels
    for trademarks with similarity score above 60%.
    """
    trademark_names = []  # List to store trademark names for labeling in the plot
    similarity_scores = []  # List to store similarity scores for plotting
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        #next(reader)  # Skip the header row
        for row in reader:
            trademark_name = row[0]
            similarity_score = string_similarity(str1, trademark_name)
            if similarity_score > 30:
                print(f"'{trademark_name}' has a similarity score of {similarity_score}%")
            if similarity_score > 20:  # Add trademark name to the list only if similarity score > 60%
                trademark_names.append(trademark_name)
                similarity_scores.append(similarity_score)

    # Plot the similarity scores with trademark names as labels for trademarks with similarity score > 60%
    if trademark_names:
        plt.plot(similarity_scores)
        plt.xlabel('Trademark Index')
        plt.ylabel('Similarity Score')
        plt.title(f'Similarity Scores for "{str1}" in the CSV file')
        plt.xticks(range(len(trademark_names)), trademark_names, rotation='vertical')  # Set x-axis labels as trademark names
        plt.gcf().autofmt_xdate()
        plt.savefig('sim.png', dpi=100)
       # plt.show()
                
    else:
        print("No trademarks found with similarity score above 60%.")

def returnB64Img():
    with open("sim.png", "rb") as f:
        global encodedImage
        encodedImage = base64.b64encode(f.read()).decode('utf-8')
        print(encodedImage)
        return encodedImage


# Example usage
# str1 = "Saudi Aramco"
# csv_file = "trademarks.csv"
# print(f"Similarity scores for '{str1}' in the CSV file are:")
# check_similarity(str1, csv_file)


app = Flask(__name__)

@app.route('/get_similarity_plot', methods=['POST'])
def get_similarity_plot():
    try:
        str1 = request.headers.get('str1')

        # Specify the file path to the CSV file
        csv_file = 'trademarks.csv'

        check_similarity(str1, csv_file)

        img_base64 = returnB64Img()

        if img_base64:
            return jsonify({'status': 'success', 'image': img_base64})
        else:
            return jsonify({'status': 'error', 'message': 'No trademarks found with similarity score above 60%.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)