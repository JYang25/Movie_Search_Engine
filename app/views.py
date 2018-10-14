from flask import render_template, flash, redirect, url_for, request
from app import app, Movies, Index
from .forms import SearchForm
from Query_Evaluation import QueryEvaluation
import csv
import os

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search',methods=['GET','POST'])
def search():
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        query = request.form['text']
        ans = QueryEvaluation(query, Index, Movies)    
        return render_template('search_results.html', results=ans)
    else:
        return render_template('search.html', form=search_form)


