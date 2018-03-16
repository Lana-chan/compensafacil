from unidecode import unidecode
import csv

class Empreendedor:
  def __init__(self, tcra, area, bioma, prioridade):
    self.tcra = tcra
    self.area = area
    self.bioma = bioma
    self.prioridade = prioridade
    
  def load_from_csv(filename):
    entradas = []
    with open(filename, 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        item = Empreendedor(row["nº TCRA/TAC"],
                            float(row["Área (m²)"]),
                            bioma_numerico(row["Bioma"]),
                            prioridade_numerica(row["Prioridade"]))
        item.municipio = row["Município"]
        entradas.append(item)
    return entradas
    
  """
    determina lista de proprietários que compensam a demanda do empreendedor
    proprietário precisa ter:
      área maior ou igual à demanda
      prioridade maior ou igual à demanda
      bioma igual à demanda
  """
  def find_matches(self, proprietarios):
    results = list(filter(lambda x: x.area >= self.area and
                                    x.prioridade >= self.prioridade and
                                    x.bioma == self.bioma,
                                    proprietarios))
    return results
    
  def custo(self, propriedade):
    if hasattr(propriedade, "preco"):
      return self.area * propriedade.preco
    return None
    
  def __str__(self):
    e = "TCRA/TAC: {} - {} m2 de {} com prioridade {}".format(self.tcra,
                                                              self.area,
                                                              bioma_textual(self.bioma),
                                                              prioridade_textual(self.prioridade).lower())
    if hasattr(self, 'municipio'):
      e = e + ", {}".format(self.municipio)
    return e
    
class Proprietario:
  def __init__(self, matricula, area, bioma, prioridade):
    self.matricula = matricula
    self.area = area
    self.bioma = bioma
    self.prioridade = prioridade
    
  def load_from_csv(filename):
    entradas = []
    with open(filename, 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        item = Proprietario(row["Nº Matrícula"],
                            float(row["Área disponível (m²)"]),
                            bioma_numerico(row["Bioma"]),
                            prioridade_numerica(row["Prioridade"]))
        item.municipio = row["Município"]
        item.proprietario = row["Proprietário"]
        item.preco = float(row["R$/m²"])
        item.latitude = float(row["Lat"][:-1])
        item.longitude = float(row["Long"][:-1])
        entradas.append(item)
    return entradas
    
  def __str__(self):
    e = "Matrícula: {} - {} m2 de {} com prioridade {}".format(self.matricula,
                                                               self.area,
                                                               bioma_textual(self.bioma),
                                                               self.prioridade)
    if hasattr(self, 'municipio'):
      e = e + ", {}".format(self.municipio)
    return e

# converte prioridade em texto para valor numérico    
def prioridade_numerica(string):
  # trata string, tirando acentos, transformando em minuscula e removendo espacos
  new_str = unidecode(string).lower().strip()
  
  pri = {"baixa":1,
          "media":2,
          "alta":3,
          "muito alta":4}
  
  return pri[new_str]
  
# converte prioridade em número para texto
def prioridade_textual(prioridade):
  pri = ["Baixa",
         "Média",
         "Alta",
         "Muito Alta"]
         
  return pri[prioridade-1]

# converte bioma em texto para valor numérico  
def bioma_numerico(string):
  # trata string, tirando acentos, transformando em minuscula e removendo espacos
  new_str = unidecode(string).lower().strip()
  
  bio = {"mata atlantica":1,
          "cerrado":2}
  
  return bio[new_str]
  
# converte bioma em código para nome
def bioma_textual(bioma):
  bio = ["Mata Atlântica",
          "Cerrado"]
        
  return bio[bioma-1]
