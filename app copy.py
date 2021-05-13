from flask import Flask, request, json
from flask import render_template
import process_corpus as pc

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
@app.route('/index/<name>')
def hello_world(name=""):
    # return jsonify(pc.sentences_expert)
    data = pc.readCorpus(name)
    if name == "":
        return render_template('index.html', data=data, state=0)
    if name == "xk":
        return render_template('index.html', data=data, state=1)
    return render_template('index.html', data=data, state=2)


@app.route('/save_data', methods=['POST'])
def corpus_data():
    if request.method == 'POST':
        try:
            pc.updateCorpus(json.loads(request.form['data']))  # 等价于 request.form.get('data')
            return "Success"
        except Exception as e:
            return repr(e)
    else:
        return "Not POST Request"


@app.route('/write_data', methods=['GET'])
def write_data():
    try:
        pc.writeCorpus()
        return "保存文件成功！\n下载地址：https://process-quda.projects.zjvis.org/static/data/corpus_5_new.json"
    except Exception as e:
        return repr(e)


@app.route('/report', methods=['GET'])
@app.route('/report/expert', methods=['GET'])
def report_expert():
    pc.generateReport(True)
    return render_template('quda_expert_report.html')


@app.route('/report/all', methods=['GET'])
def report_all():
    pc.generateReport(False)
    return render_template('quda_all_report.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 80)
