import asyncio
import aiomysql

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
                print(res)
            except aiomysql.MySQLError as err:
                print("Erro na query: ", err)
            finally:

                conn.close()
                print("conexion closed")
    else:
        print("unable to connect to db")

async def insert_db(values):
    query = "INSERT INTO countTable (ponto, ab, ba) values(%s, %s, %s)"
    await query_db(query, values, True)

async def update_db2(values):
    query = "UPDATE countTable SET ab = %s, ba = %s where ponto = %s"
    await query_db(query, values, True)

async def update_db(ch, chName):
    queries = [
        "SELECT reset, ab, ba FROM countTable WHERE ponto = %s",
        "UPDATE countTable SET ab = %s, ba = %s WHERE ponto = %s",
        "UPDATE countTable SET ab = 0, ba = 0, reset = 0 WHERE ponto = %s"
        ]
    conn = await connectToDB()
    if conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(queries[0], chName)
                tup = await cur.fetchall()
                reset, ab, ba = tup[0]
                print(f"reset = {reset}, ab = {ab}, ba = {ba}")
                
                if reset:
                    ch.countAB = 0
                    ch.countBA = 0
                    await cur.execute(queries[2], (chName,))
                    await conn.commit()

                
                else:
                    if (ab > ch.countAB or ba > ch.countBA):
                        ch.countAB = ab
                        ch.countBA = ba
                    else:
                        await cur.execute(queries[1], (ch.countAB, ch.countBA, chName))
                        await conn.commit()
                
                
            except aiomysql.MySQLError as err:
                print("Erro na query: ", err)
            finally:

                conn.close()
                print("conexion closed")
    else:
        print("unable to connect to db")

#asyncio.run(update_db2('ch1'))


#asyncio.run(insert_db(('ch2', 0, 0)))



