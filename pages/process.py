import os
from flask import jsonify
from ProcessImage import ProcessImage

def hitung(filename, perbesaran):
    process = ProcessImage(filename)
    if perbesaran == "40x":
        normal, mikrositik, urledit, filename = process.process()
        return jsonify(
            status="success",
            normal=normal,
            mikrositik=mikrositik,
            urledit=urledit,
            filename=filename)
    elif perbesaran == "100x":
        normal, mikrositik, urledit, filename = process.process2()
        return jsonify(
            status="success",
            normal=normal,
            mikrositik=mikrositik,
            urledit=urledit,
            filename=filename)

def hapus(filename):
    rootpath = os.getcwd()
    originalpath = rootpath + '/static/temp/' + filename
    editpath = rootpath + '/static/temp/edit-' + filename
    os.remove(originalpath)
    os.remove(editpath)

