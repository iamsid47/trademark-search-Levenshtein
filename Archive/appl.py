import requests

def search_trademarks(trademark_name, api_key):
    base_url = 'https://api.data.gov/regulations/v3/documents'
    query = {
        'api_key': api_key,
        's': trademark_name,
        'rpp': 100
    }

    response = requests.get(base_url, params=query)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results')
        if results:
            for result in results:
                similarity_score = result.get('similarity_score')
                if similarity_score and similarity_score > 0:
                    print(f"Trademark: {result['title']}")
                    print(f"Similarity Score: {similarity_score}")
                    print('---')
        else:
            print('No similar trademarks found.')
    else:
        print('Failed to retrieve trademark data.')

if __name__ == '__main__':
    trademark_name = input('Enter a trademark name: ')
    api_key = 'Gyx95CKPbef803redgLwuTohY84MZT3k'
    search_trademarks(trademark_name, api_key)
