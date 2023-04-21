import csv
import Levenshtein
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import base64
import time
import os
import io

def string_similarity(str1, str2):

    str1 = str1.lower() if str1 else ""
    str2 = str2.lower()

    distance = Levenshtein.distance(str1, str2)

    # Calculate similarity score as a percentage of characters that match
    max_len = max(len(str1), len(str2))
    similarity_score = (1 - (distance / max_len)) * 100

    return similarity_score

def check_similarity(str1, csv_file):

    trademark_names = []  # List to store trademark names for labeling in the plot
    similarity_scores = []  # List to store similarity scores for plotting
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        #next(reader)  # Skip the header row
        for row in reader:
            trademark_name = row[0]
            similarity_score = string_similarity(str1, trademark_name)
            if similarity_score > 60:
                print(f"'{trademark_name}' has a similarity score of {similarity_score}%")
            if similarity_score > 60:  # Add trademark name to the list only if similarity score > 60%
                trademark_names.append(trademark_name)
                similarity_scores.append(similarity_score)

    # Plot the similarity scores with trademark names as labels for trademarks with similarity score > 60%
    if trademark_names:
        global buf, plot_bytes
        plt.plot(similarity_scores)
        plt.xlabel('Trademark Index')
        plt.ylabel('Similarity Score')
        plt.title(f'Similarity Scores for "{str1}" in the CSV file')
        plt.xticks(range(len(trademark_names)), trademark_names, rotation='vertical')  # Set x-axis labels as trademark names
        plt.gcf().autofmt_xdate()
        buf = io.BytesIO()
        plt.savefig(buf, dpi=100, format='png')
        plt.clf()
        buf.seek(0) 
        plot_bytes = base64.b64encode(buf.getvalue()).decode('utf-8')
        print(plot_bytes)
        # plt.show()

                
    else:
        plot_bytes = None
        print("No trademarks found with similarity score above 50%.")

def image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode("utf-8")



# Example usage
# str1 = "Carlos"
# csv_file = "trademarks.csv"
# print(f"Similarity scores for '{str1}' in the CSV file are:")
# check_similarity(str1, csv_file)

app = Flask(__name__)
CORS(app)

@app.route('/plot', methods=['POST'])
def get_plot():
    data = request.json
    str1 = data.get('str1')
    csv_file = 'trademarks.csv'
    check_similarity(str1, csv_file)
    time.sleep(3)
    # Return the byte string as a response with content type 'image/png'
    if plot_bytes != None:

        return jsonify({"image_b64":plot_bytes})
    else:
        return Response('No trademarks found with similarity above 50%', mimetype='text/plain')


@app.route('/get_similarity_plot', methods=['POST'])
def get_similarity_plot():
    try:
        #str1 = request.headers.get('str1')
        # Specify the file path to the CSV file
        data = request.json
        str1 = data.get('str1')

        csv_file = 'trademarks.csv'

        check_similarity(str1, csv_file)

        time.sleep(4)
        
        encoded_image = image_to_base64("sim.png")

        if encoded_image:
            return jsonify({'status': 'success', 'image': encoded_image})
        else:
            return jsonify({'status': 'success', 'message': 'No trademarks found with similarity score above 50%.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)