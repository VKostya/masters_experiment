import redis
import time
import random
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE


def st_time(func):
    """
    st decorator to calculate the total time of a func
    """

    def st_func(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print("Function=%s, Time=%s" % (func.__name__, t2 - t1))
        return r

    return st_func


def generate_id_seq(i, koef):
    return [random.randint(1, 1000 * koef) for x in range((10 ** (i + 1)) * 3)]


@st_time
def select_no_cache(i, cur=None, seq=None):
    for iter in range((10 ** (i + 1)) * 3):
        id = seq[iter]
        cur.execute(
            "SELECT * FROM public.test_table WHERE ID = %s",
            (id,),
        )


@st_time
def select_cache(i, cur=None, redis=None, seq=None):
    for iter in range((10 ** (i + 1)) * 3):
        id = seq[iter]
        cache = redis.get(str(id))
        if cache:
            continue
        cur.execute(
            "SELECT * FROM public.test_table WHERE ID = %s",
            (id,),
        )
        res = cur.fetchone()
        r.set(str(res[0]), str(res[1]))


r = redis.Redis(port=9876)
print(r.ping())
con = psycopg2.connect(
    dbname="test_db", user="test", host="127.0.0.1", password="test", port="5432"
)
for k in range(3):
    koef = 10**k
    for i in range(2):
        cur = con.cursor()
        print("Iterations --", ((10 ** (i + 1)) * 3), f"selecting {koef}% values")
        seq = generate_id_seq(i=i, koef=koef)
        select_no_cache(i=i, cur=cur, seq=seq)
        select_cache(i=i, cur=cur, redis=r, seq=seq)

        #   r.flushall()s
        cur.close()

con.close()
