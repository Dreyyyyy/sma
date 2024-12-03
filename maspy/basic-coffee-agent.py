# Crença
crencas = ("graos", "maquina")

print("Crencas do agente: ")
print(crencas)

# Planos
def tem_cafe(crencas):
  if crencas[0] == 'poh_cafe' or crencas[0] == 'graos':
    return True
  else: return False

def fazer_cafe(crencas):
  if crencas[0] == 'poh_cafe' and crencas[1] == 'cafeteira':
    print("Fazer cafe filtrado")
  elif crencas[0] == 'graos' and crencas[1] == 'maquina':
    print("Fazer cafe expresso")
  else: print("Nao fazer cafe (crencas conflitantes)!")

#Execução
cafe = tem_cafe(crencas)

if (cafe == True):
  fazer_cafe(crencas)
else: print("Ir ao mercado comprar cafe")