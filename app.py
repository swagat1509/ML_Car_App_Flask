
from flask import Flask, render_template, request
import numpy as np
import joblib,os


def get_value(key,dicti):
    return dicti[key]

def load_model(model_path):
    loaded_model = joblib.load(open(os.path.join(model_path),"rb"))
    return loaded_model


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == "POST":
        bl_bk = request.form['buyinglevel']
        ml_bk = request.form['maintainancelevel']
        nd_bk = request.form['noofdoors']
        np_bk = request.form['noofpersons']
        lb_bk = request.form['luggboot']
        sf_bk = request.form['safety']
        model_bk = request.form['ml_model']

        buying_label = {"vhigh":0,"low":1,"medium":2,"high":3}
        main_label = {"vhigh":0,"low":1,"medium":2,"high":3}
        doors_label = {"2":0,"3":1,"4":2}
        persons_label = {"2":0,"4":1}
        lug_boot_label = {"sm":0,"md":1,"bg":2}
        safety_label = {"hg":0,"md":1,"lw":2}
        class_label = {0:"good",1:"acceptable",2:"very good",3:"unacceptable"}

        bl_ml=get_value(bl_bk,buying_label)
        mal_ml=get_value(ml_bk,main_label)
        nd_ml=get_value(nd_bk,doors_label)
        np_ml=get_value(np_bk,persons_label)
        lb_ml=get_value(lb_bk,lug_boot_label)
        sf_ml=get_value(sf_bk,safety_label)
        print(mal_ml)

        results = [bl_ml, mal_ml, nd_ml, np_ml, lb_ml,sf_ml]
        sample_data = np.array(results).reshape(1, -1)

    if model_bk == "lg":
        predictor = load_model('static/models/logit_car_model.pkl')
        prediction = int(predictor.predict(sample_data))
        final_result = get_value(prediction, class_label)
        return render_template('index.html',r = final_result)

    if model_bk == "nb":
        predictor = load_model('static/models/nb_car_model.pkl')
        prediction = int(predictor.predict(sample_data))
        final_result = get_value(prediction, class_label)
        return render_template('index.html',r = final_result)

    if model_bk == "mlp":
        predictor = load_model('static/models/nn_clf_car_model.pkl')
        prediction = int(predictor.predict(sample_data))
        final_result = get_value(prediction, class_label)
        return render_template('index.html',r = final_result)

        





        

    

    









if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)