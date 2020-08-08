from django.shortcuts import render
import pandas as pd 


def inicio(request):
    aux = csv_com_ordens_fechadas()
    data ={'tabela':aux.to_html()} 
    #print(" \n", data)

    return render(request,'analisador/teste.html',data)


def ler_csv_para_dataframe():
    caminho_base = 'web_analisador/tabelas/ELET3_deals_com_lucro_2019.csv'
    #caminho = 'BBDC4_deals_com_lucro_2019-versao4.csv'
    dados_read = pd.read_table(caminho_base, encoding = 'utf-16',sep=',') 
    dados=pd.DataFrame(dados_read)
    return dados

#order_ticket == ticket
def criar_tabela_vazia():
    nome_coluna = {'symbol':[] ,'ticket':[] ,'order_magic':[] ,'deal_type_open':[],'datetime_open':[],'price_open':[],'deal_type_closed':[],'datetime_closed':[],'price_closed':[],'profit':[],'volume':[]} 
    tabela = pd.DataFrame(data=nome_coluna)
    return tabela

def ordem_com_negociacao_fechada(position_ID,dados):
    #deal_type = 0  é compra
    aux = dados[dados['order_ticket']== position_ID]
    
    if aux.empty == False:
        aux = dados[(dados['position_ID'] == position_ID)]
        volume_compra = aux[(aux['deal_type']==0)]['volume'].sum()
        volume_venda = aux[(aux['deal_type']==1)]['volume'].sum()
        if volume_compra == volume_venda:
            #print("volume de compra : ",volume_compra, " volume venda",volume_venda,"\n")
            return True
        else:
            return False
    
    else:
        print('Não tem order_ticket como início. O número é ',position_ID,"\n")
        return False
    

def tabela_com_ordens_fechadas():
    dados = ler_csv_para_dataframe()
    position_ID_unique = dados['position_ID']
    position_ID_unique =  position_ID_unique.drop_duplicates()
    tabela =  criar_tabela_vazia()
 
    for i in position_ID_unique:
        if ordem_com_negociacao_fechada( i, dados) == True :
            ordem = criar_tabela_vazia()
            aux = dados[(dados['position_ID']== i)]
            volume_compra = aux[(aux['deal_type']==0)]['volume'].sum()

            ordem_abertura = dados[(dados['order_ticket']==i)]
            
            ordem_ultima = dados[(dados['position_ID']==i)]
            ordem_ultima = ordem_ultima.tail(1)
            ordem['symbol'] = ordem_abertura['symbol'] 
            ordem['ticket'] = ordem_abertura['order_ticket'].values
            ordem['order_magic'] = ordem_abertura['order_magic'].values
            ordem['deal_type_open'] = ordem_abertura['deal_type']
            ordem['datetime_open'] = ordem_abertura['transaction_time']
            ordem['price_open'] = ordem_abertura['price']
            ordem['profit'] = dados[(dados['position_ID']==i)]['profit'].sum()
            ordem['volume'] = (volume_compra*2)
            ordem['deal_type_closed'] = ordem_ultima['deal_type'].values
            ordem['datetime_closed'] = ordem_ultima['transaction_time'].values
            ordem['price_closed'] = ordem_ultima['price'].values
            #tabela = add_ordem_na_tabela(ordem,tabela)
            tabela = tabela.append(ordem,ignore_index=True)
    print(tabela)

def csv_com_ordens_fechadas():  
    dados = ler_csv_para_dataframe()
    position_ID_unique = dados['position_ID']
    position_ID_unique =  position_ID_unique.drop_duplicates()
    tabela = dados
    rejeitados = []
    aceitos = []
    for i in position_ID_unique:

        if ordem_com_negociacao_fechada( i, dados)== False:
            #print("FOI FALSO  ",i)
            ordem_rejeitada = dados[(dados['position_ID']==i)].index
            dados.drop(ordem_rejeitada,inplace=True)
            rejeitados.append(i) 
        aceitos.append(i)
    #print(tabela , "\n")
    #print("\n Rejeitados " , rejeitados,"\n")
    #print("\n Aceitos" , aceitos,"\n")
    #print("\n total de rejeitados: ", len(rejeitados), " total de aceitos: ", len(aceitos), "total: ",len(rejeitados)+len(aceitos))
    return tabela