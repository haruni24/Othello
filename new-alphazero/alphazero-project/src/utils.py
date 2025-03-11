def save_results(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f)

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def preprocess_data(data):
    # Implement any necessary preprocessing steps here
    return data

def log(message, filename='log.txt'):
    with open(filename, 'a') as f:
        f.write(message + '\n')