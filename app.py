from flask import Flask, render_template, url_for
import matcher
import locale
import json
app = Flask(__name__)

with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
empreendedores = matcher.Empreendedor.load_from_csv('empreendedores.csv')
proprietarios = matcher.Proprietario.load_from_csv('proprietarios.csv')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/empreendedores')
def pag_empre():
  return render_template('empreendedores.html', empr=empreendedores)

@app.route('/empreendedor/<tcra>')
def matches_empre(tcra):
  empr = next((x for x in empreendedores if x.tcra == tcra), None)
  return render_template('matches.html', empr=empr, matches=empr.find_matches(proprietarios), cfg=cfg)

@app.route('/proprietarios')
def pag_propri():
  return render_template('proprietarios.html', propri=proprietarios)

  
@app.context_processor
def utility_processor():
  def bioma(bio):
    return u'{}'.format(matcher.bioma_textual(bio))

  def prioridade(pri):
    return u'{}'.format(matcher.prioridade_textual(pri))
    
  def preco(num):
    return locale.format(u'%.2f', num, True)
    
  def number(num):
    return locale.format(u'%.f' if num % 1 else u'%.0f', num, True)

  return dict(bioma=bioma, prioridade=prioridade, int=int, preco=preco, number=number)

if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True, host='0.0.0.0')
