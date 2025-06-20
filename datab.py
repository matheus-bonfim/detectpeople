import asyncio
import aiomysql
from videoChannel import VideoChannel
import ast

streams_lst = []
channels = {}
async def connectToDB():
    try:
        conn = await aiomysql.connect(
            host = 'localhost',
            user='root',
            password='17012023',
            db='monitoramentoLPR'
        )
        print("conectou")
    except aiomysql.MySQLError as err:
        print("erro de conexão: ", err)
        conn = None
    return conn

async def teste():
    a = await connectToDB()
    if a:
        print("fechando")
        a.close()

async def query_db(query, values, commit=False):
    conn = await connectToDB()
    if conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(query, values)
                if commit:
                    await conn.commit()
                res = await cur.fetchall()
                conn.close()
                return res
            except aiomysql.MySQLError as err:
                print("Erro na query: ", err)
    else:
        print("unable to connect to db")


#ok
async def get_ready_streams(firstTime=True):
    if firstTime:
        query = "SELECT ponto, p1, p2, ab, ba, ip, direction, TIPO FROM countTable WHERE state IN (0,1)"
    else:
        query = "SELECT ponto, p1, p2, ab, ba, ip, direction, TIPO FROM countTable WHERE state = 1"
    res_db = await query_db(query, None)
    ch_lst = []
    for item in res_db:
        ch_lst.append(item)
        print(ch_lst)
    pontos = [item[0] for item in ch_lst]
    if len(pontos) > 0:
        placeholders = ', '.join(['%s'] * len(pontos))
        query = f"UPDATE countTable SET state = 0 WHERE ponto IN ({placeholders})"
        await query_db(query, tuple(pontos), commit=True)

    return ch_lst

#asyncio.run(get_ready_streams())
async def change_channel_state(ponto, state):
    query = "UPDATE countTable SET state = %s WHERE ponto = %s"
    await query_db(query, (state, ponto), commit=True)
    print(f'estado do ponto {ponto} alterado para {state}')

async def update_channel_db(ponto, ab, ba):
    query = "UPDATE countTable SET ab = %s, ba = %s WHERE ponto = %s"
    await query_db(query, (ab, ba, ponto), True)
    print("adicionado: ", ponto, ab, ba)

async def set_channel_as_new(ponto, zerar=False):
    if zerar:
        query = "UPDATE countTable SET ab = 0, ba = 0, state = 1 WHERE ponto = %s"
    else:
        query = "UPDATE countTable SET state = 1 WHERE ponto = %s"
    
    await query_db(query, ponto, commit=True)





