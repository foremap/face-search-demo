import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from lsh_index import LSHSearch 

app = Flask(__name__)
lsh_engine = LSHSearch('features/lfw_feature.txt', 150, 30, 8)
lsh_engine.build()
img_l_dir = os.path.join('static', 'img', 'lfw-large')
img_s_dir = os.path.join('static', 'img', 'lfw-small')
img_list = os.listdir(img_s_dir)
page = 0
per_page_num = 100
max_page = len(img_list) / per_page_num + 1

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('go_page'))

@app.route('/page', methods=['GET'])
def go_page():
    global page
    page += 1
    return render_template('index.html')

@app.route('/p_page', methods=['GET'])
def go_p_page():
    global page
    page -= 1
    if page < 0:
        page = 0
    return render_template('index.html')

@app.route('/all-images', methods=['GET'])
def get_images():
    global page
    lfw_face = []
    if page >= max_page:
        page = page % max_page
    begin = per_page_num * page
    last = (begin + per_page_num)
    print begin, last, page, max_page
    if last > len(img_list):
        page = -1
        last = len(img_list)
    for img in img_list[begin:last]:
        lfw_face.append(
            {'name': img, 'url': '/' + os.path.join(img_s_dir, img)}
        )
    return jsonify(photos=lfw_face)

@app.route('/s_page/<filelist>/<autotag>', methods=['GET'])
def s_index(filelist, autotag):
    p_file = filelist.split('+')
    p_file = filter(None, p_file)
    u_filelist = list(set(p_file))
    n_filelist = '+'.join(u_filelist)
    return render_template('search.html', name=p_file[0], url='/search/' + n_filelist, test=n_filelist, autotag=autotag)

@app.route('/search/<filelist>', methods=['GET'])
def search(filelist):
    p_file = filelist.split('+')
    result = lsh_engine.query(p_file)
    person_name = '_'.join(p_file[0].split('_')[:-1])
    lfw_face = []
    retreive = len(p_file)
    for item in result:
        img = item[0]
        score = "{:1.4f}".format(item[1])
        t_num = item[2]
        img_name = '_'.join(img.split('_')[:-1])
        # print img_name, person_name
        answer = 'True' if img_name == person_name else 'False'
        lfw_face.append(
            {'name': img, 'url': '/' + os.path.join(img_s_dir, img), 'score': score, 'answer': answer, 't_num': t_num, 'retreive': retreive}
        )
    # No result    
    if len(result) == 0:
         lfw_face.append(
            {'name': 'null', 'url': 'null', 'score': 'null', 'answer': 'null', 't_num': 'null', 'retreive': retreive}
        )       
    return jsonify(photos=lfw_face)

@app.route('/true_num/<filename>', methods=['GET'])
def true_num(filename):
    person_name = '_'.join(filename.split('_')[:-1])
    res = lsh_engine.true_num(person_name)
    return str(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
