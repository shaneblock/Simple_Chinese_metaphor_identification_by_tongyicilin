import pymysql,gensim

class Identify:

    def __init__(self):
        self.new_model = gensim.models.Word2Vec.load('word2vec/smp.w2v.300d')#初始化 加载w2v模型
        #数据库链接
        self.conn = pymysql.connect(host = 'localhost', user = 'root', passwd = '', db = 'tongyicilin',
                                    port = 3306, charset = 'utf8')
        self.cur = self.conn.cursor()

    def identify(self,word):
        cate = 'concrete'   #默认为具象 抽象的词一定是少的

        sql = "select ID from terms where term = %s"
        self.cur.execute(sql,word)
        wid = self.cur.fetchall()
#查得到结果 定类别
        if len(wid) > 0:
            # print("找到了")
            for i in wid:
                if i[0][0] == 'B' or i[0][0:2] == 'Cb':
                    cate = 'concrete'
                    break
                if i[0][0:2] == 'Ca' or ( i[0][0] == 'D' and i[0][0:2] != 'Dj'
                                          and i[0][0:2] != 'Dk' and i[0][0:2] != 'Dm'
                                          and i[0][0:4] != 'Dd15' and i[0][0:2] != 'Dg'
                                          and i[0][0:2] != 'Di' and i[0][0:2] != 'Dl')or i[0][0:2] == 'Eb' \
                        or i[0][0:4] == 'Dj01' or i[0][0:4] == 'Dk01' or i[0][0:4] == 'Dk02' or i[0][0:4] == 'Dk03' \
                        or i[0][0] == 'G' or i[0][0:4] == 'Di01' or i[0][0:4] == 'Di04' or i[0][0:4] == 'Di06' \
                        or i[0][0:4] == 'Di08' or i[0][0:5] == 'Di09B'or i[0][0:4] == 'Di14'or i[0][0:4] == 'Di15'\
                        or i[0][0:4] == 'Di18' or i[0][0:4] == 'Di21' or i[0][0:4] == 'Di22' or i[0][0:2] == 'Ee'\
                        or i[0][0] == 'H':
                    cate = 'abstract'
                    # print(i[0])
                    break

#查不到结果 根据相似度找最像的
        else:
            try:
                wv = self.new_model[word]
                sql = "select term from terms"
                self.cur.execute(sql)
                wlist = self.cur.fetchall()
                sw = wlist[0][0]
                sim = self.new_model.similarity(word,sw)
                for i in wlist:
                    try:
                        a = self.new_model.similarity(word,i[0])
                        if a > sim:
                            sim = a
                            sw = i[0]
                    except BaseException:
                        #print('数据库词'+i[0]+'不在词向量中')
                        continue
                # print("找不到 最像的是"+sw)
                sql = "select ID from terms where term = %s"
                self.cur.execute(sql,sw)
                swid = self.cur.fetchall()

                if len(swid) > 0:
                    for i in swid:
                        if i[0][0] == 'B' or i[0][0:2] == 'Cb':
                            cate = 'concrete'
                            break
                        if i[0][0:2] == 'Ca' or ( i[0][0] == 'D' and i[0][0:2] != 'Dj'
                                          and i[0][0:2] != 'Dk' and i[0][0:2] != 'Dm'
                                          and i[0][0:4] != 'Dd15' and i[0][0:2] != 'Dg'
                                          and i[0][0:2] != 'Di'and i[0][0:2] != 'Dl')or i[0][0:2] == 'Eb' \
                                or i[0][0:4] == 'Dj01' or i[0][0:4] == 'Dk01' or i[0][0:4] == 'Dk02' or i[0][0:4] == 'Dk03' \
                                or i[0][0] == 'G' or i[0][0:4] == 'Di01' or i[0][0:4] == 'Di04' or i[0][0:4] == 'Di06' \
                                or i[0][0:4] == 'Di08' or i[0][0:5] == 'Di09B'or i[0][0:4] == 'Di14'or i[0][0:4] == 'Di15'\
                                or i[0][0:4] == 'Di18' or i[0][0:4] == 'Di21' or i[0][0:4] == 'Di22'or i[0][0:2] == 'Ee'\
                                or i[0][0] == 'H':
                            cate = 'abstract'
                            break
            except BaseException:
                #print('被查词'+word+'不在词向量中')
                pass
        return cate

    def __del__(self):
        self.cur.close()
        self.conn.close()