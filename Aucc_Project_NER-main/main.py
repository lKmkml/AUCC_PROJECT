from flask import Flask, render_template, request , redirect, url_for
import spacy
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
#from sqlalchemy import null
from flaskext.markdown import Markdown
from spacy import displacy
import translators as ts



app = Flask(__name__, template_folder='template')
Markdown(app)
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
@app.route('/')
def Home():
    return render_template('index.html' ,go_article ="",rgo = 0,value = [])

@app.route('/ner_spacy', methods = ['GET', 'POST'])
def ner_spacy():
    if request.method == 'POST':
        article = request.form["article"]
        display = request.form['display']
        spacy_option = request.form.getlist('spacy_option')
        #print(spacy_option)
        if str(display) == "table" and article != "":
            totallists = spacy_that_article(article)
            return render_template('table_display.html', value = totallists , rgo = len(max(totallists)))
        elif str(display) == "terminology" and article != "":
            article = request.form["article"]
            test_list = list_word(article)
            test_list_ts = []
            for i in test_list:
                x = ts_to_thai(i)
                test_list_ts.append(x)
            total_list = []
            total_list.append(test_list)
            total_list.append(test_list_ts)
            return render_template('index.html',go_article = "",value = total_list , rgo = len(max(total_list)))
            #print(test_list_ts)
        else:
            nlp = spacy.load('en_core_web_sm')
            docx = nlp(article)
            options = {"ents": spacy_option}
            html = displacy.render(docx,style="ent",options=options)
            html = html.replace("\n\n","\n")
            result = HTML_WRAPPER.format(html)
            return render_template('index.html',go_article = result,rgo = 0,value = [])
def ts_to_thai(word):
  word_ts = ts.google(word, from_language='en', to_language='th')
  return word_ts
def list_word(text):
    article = text
    tokens = word_tokenize(article)
    lower_tokens = [t.lower() for t in tokens]
    alpha_only = [t for t in lower_tokens if t.isalpha()]
    no_stops = [t for t in alpha_only if t not in stopwords.words('english')]
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
    lemmatized_1 = []
    for i in lemmatized:
      if i not in lemmatized_1:
        lemmatized_1.append(i)
      else:
        pass
    lemmatized_1.sort()
    return lemmatized_1
def spacy_that_article(us_word):
    totallist = []
    person = []
    norp = []
    org = []
    gpe = []
    loc = []
    product = []
    event = []
    workart = []
    language = []
    date = []
    time = []
    percent = []
    money = []
    quantity = []
    ordinal = []
    cardinal = []
    nlp = spacy.load('en_core_web_sm')
    article = us_word
    doc = nlp(article)
    for ent in doc.ents:
        a = ent.label_,ent.text
        if a[0] == "CARDINAL":
            if a[1] not in cardinal:
                cardinal.append(a[1])
        elif a[0] == "PERSON":
            if a[1] not in person:
                person.append(a[1])
        elif a[0] == "NORP":
            if a[1] not in norp:
                norp.append(a[1])
        elif a[0] == "ORG":
            if a[1] not in org:
                org.append(a[1])
        elif a[0] == "GPE":
            if a[1] not in gpe:
                gpe.append(a[1])
        elif a[0] == "LOC":
            if a[1] not in loc:
                loc.append(a[1])
        elif a[0] == "PRODUCT":
            if a[1] not in product:
                product.append(a[1])
        elif a[0] == "EVENT":
            if a[1] not in event:
                event.append(a[1])
        elif a[0] == "WORK OF ART":
            if a[1] not in workart:
                workart.append(a[1])
        elif a[0] == "LANGUAGE":
            if a[1] not in language:
                language.append(a[1])
        elif a[0] == "DATE":
            if a[1] not in date:
                date.append(a[1])
        elif a[0] == "TIME":
            if a[1] not in time:
                time.append(a[1])
        elif a[0] == "PERCENT":
            if a[1] not in percent:
                percent.append(a[1])
        elif a[0] == "MONEY":
            if a[1] not in money:
                money.append(a[1])
        elif a[0] == "QUANTITY":
            if a[1] not in quantity:
                quantity.append(a[1])
        elif a[0] == "ORDINAL":
            if a[1] not in ordinal:
                ordinal.append(a[1])
    totallist.append(cardinal)
    totallist.append(person)
    totallist.append(norp)
    totallist.append(org)
    totallist.append(gpe)
    totallist.append(loc)
    totallist.append(product)
    totallist.append(event)
    totallist.append(workart)
    totallist.append(language)
    totallist.append(date)
    totallist.append(time)
    totallist.append(percent)
    totallist.append(money)
    totallist.append(quantity)
    totallist.append(ordinal)
    return totallist

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)