import pickle
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    file = open('Model/Locations.pkl', 'rb')
    locations = pickle.load(file)
    file.close()
    return render_template('index.html', location=locations[1], location_label=locations[0], leng=1305)


def regressing(userDetails):
    lcs = int(userDetails['location'])
    area = float(userDetails['area'])
    bedroom = int(userDetails['bedroom'])
    bathroom = userDetails['bathroom']
    balcony = userDetails['balcony']
    avail = userDetails['availability']
    type = userDetails['type']

    if avail == "Need To Deliver":
        avail_1 = 1
        avail_2 = 0
    elif avail == "Ready To Move":
        avail_1 = 0
        avail_2 = 1
    else:
        avail_1 = 0
        avail_2 = 0

    if type == "Carpet Area":
        type_1 = 1
        type_2 = 0
        type_3 = 0
    elif type == "Plot Area":
        type_1 = 0
        type_2 = 1
        type_3 = 0
    elif type == "Super built-up Area":
        type_1 = 0
        type_2 = 0
        type_3 = 1
    else:
        type_1 = 0
        type_2 = 0
        type_3 = 0

    file = open('Model/Prediction.pkl', 'rb')
    regressor = pickle.load(file)
    file.close()

    value = regressor.predict([[lcs, bedroom, area, bathroom, balcony, avail_1, avail_2, type_1, type_2, type_3]])
    print(value[0][0])
    return value[0][0]


@app.route('/getinfo', methods=['GET', 'POST'])
def getinfo():
    if request.method == 'POST':
        userDetails = request.form
        val = regressing(userDetails)
        val = round(val, 2)
    return render_template('result.html', value=val)


if __name__ == '__main__':
    app.run(debug=True)
