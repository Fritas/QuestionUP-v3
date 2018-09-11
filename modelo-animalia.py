# classes modeladas, diagrama pg 28
class Animal:  
    def __init__(self, id=0, dono='', tipo='', raca=''):
        self.id = id
        self.dono = dono
        # Gato ou Cachorro, 1 caracter, pg 56
        self.tipo_animal = tipo 
        self.raca = raca
    def __str__(self):
        return '(%i) %s da raça %s pertencente a %s' % (self.id, 
            "Cachorro" if self.tipo_animal.upper()=="C" 
            else "Gato",
            self.raca, self.dono)
    def __eq__(self, outro):
        return self.id == outro.id and \
        self.dono == outro.dono and \
        self.tipo_animal == outro.tipo_animal and \
        self.raca == outro.raca

class Cliente:
    def __init__(self, id=0, nome='', email='', 
    tel='', login='', senha=''):
        self.id=id
        self.nome=nome
        self.email=email
        self.telefone=tel
        self.nome_login=login
        self.senha=senha
    def __str__(self):
        return '(%i) %s; contatos: %s, %s; acesso: %s, %s' % (
            self.id, self.nome, self.email, self.telefone, 
            self.nome_login, self.senha)
    def __eq__(self, outro):
        return self.id == outro.id and \
        self.nome == outro.nome and \
        self.email == outro.email and \
        self.telefone == outro.telefone and \
        self.nome_login == outro.nome_login and \
        self.senha == outro.senha

class Produto:
    def __init__(self, codigo=0, nomep='', q=0, descricao=''):
        self.codigo=codigo
        self.nomep=nomep
        self.quantidade=q
        self.descricao=descricao
    def __str__(self):
        return '(%i) %s: %s (em estoque: %i)' % (self.codigo,
            self.nomep, self.descricao, self.quantidade)

class Consulta:
    def __init__(self, data='', s='', h='', cli=None, animal=None, conf='', ID=''):
        self.data=data
        self.servico=s
        self.horario=h
        self.cliente=cli
        self.animal=animal
        self.confirma=conf # 'S' ou 'N', pg 39
        self.ID=ID #md5, pg 30
    def __str__(self):
        return '%s às %s:%s, cliente:%s, animal:%s, conf:%s, ID=%s' % (self.data,
        self.horario, self.servico, self.cliente, self.animal, 
        self.confirma, self.ID)
    def __eq__(self, outro):
        return self.data == outro.data and \
        self.servico == outro.servico and \
        self.horario == outro.horario and \
        self.cliente == outro.cliente and \
        self.animal == outro.animal and \
        self.confirma == outro.confirma and \
        self.ID == outro.ID

class Reserva:
    def __init__(self, data_reserva='', cli=None, prod=None, q=0, ID='', conf=''):
        self.data_reserva=data_reserva
        self.cliente=cli
        self.produto=prod
        self.quantidade=q
        self.ID=ID
        self.confirmacao=conf
    def __str__(self):
        return 'Em: %s, %s reservou: %i unidades de %s, confirmado: %s, ID=%s' %(
            self.data_reserva, self.cliente, self.quantidade, self.produto, 
            self.confirmacao, self.ID)

if __name__=="__main__":
    print("TESTE DO ANIMAL")
    a = Animal(1, "José", "C", "Chiuaua")
    print(a)
    b = Animal(1, "José", "C", "Chiuaua")
    c = Animal(1, "José", "G", "Chiuaua")
    print("a=b?",a==b)
    print("a=c?",a==c)

    print("TESTE DO CLIENTE")
    c = Cliente(1, "João da Silva", "joao@gmail.com", "99212-334", "josilva", "123")
    print(c)
    d = Cliente(1, "João da Silva", "joao@gmail.com", "99212-334", "josilva", "123")
    e = Cliente(1, "José da Silva", "joao@gmail.com", "99212-334", "josilva", "123")
    print('c=d?',c==d)
    print('c=e?',c==e)

    print("TESTE DO PRODUTO")
    p = Produto(1, "Caixa de bombom garoto 300gr", 30, "Caixa com bombons sortidos")
    print(p)

    print("TESTE DA CONSULTA")
    cons = Consulta("11/09/2018", 
        "Consulta de rotina", "14:00", c, a, "S", "1234ASDFG@#$%")
    print(cons)
    cons2 = Consulta("11/09/2018", 
        "Consulta de rotina", "14:00", c, a, "S", "1234ASDFG@#$%")
    cons3 = Consulta("11/09/2018", 
        "Consulta de rotina", "08:00", c, a, "S", "1234ASDFG@#$%")
    print("cons=cons2?",cons==cons2)
    print("cons=cons3?",cons==cons3)

    print("TESTE DA RESERVA")
    r = Reserva("11/09/2018", c, "Sabão natural em barra", 2, "!@#$%ÄSDFG@#$", "S")
    print(r)